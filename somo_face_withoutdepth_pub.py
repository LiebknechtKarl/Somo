#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
# sys.path.append(
#     "/home/ros/anaconda3/envs/somo_vision/lib/python3.10/site-packages")  # 服务器电脑
from sensor_msgs.msg import Image, CompressedImage
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
import random
import ctypes
sys.path.append('/home/robot/anaconda3/envs/point/lib/python3.6/site-packages') # ------------------------
import torch
import torch.backends.cudnn as cudnn

import torchvision
import time
# from time import time
import numpy as np
from PIL import ImageDraw, ImageFont
import PIL
import cv2
import os
from message_filters import ApproximateTimeSynchronizer,Subscriber
import message_filters
from cv_bridge import CvBridge
from somo_msgs.msg import FaceBoxes
from somo_msgs.msg import FaceBox
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
import rclpy
from std_msgs.msg import String,Float32,UInt16MultiArray


############# MMMMMMMMMMMMMMMMMMM
from somo_msgs.msg import FourPoint
from std_msgs.msg import Header

torch.set_grad_enabled(False)
cudnn.benchmark = True

odai_face = '/home/robot/somo/src/somo_face_recognition/somo_face_recognition/Retinaface_arcface'  # 人头电脑
sys.path.insert(0, odai_face)
# face detection tensorrt

# face detection pth
from utils.box_utils import decode, decode_landm
from utils.nms.py_cpu_nms import py_cpu_nms
from models.retinaface import RetinaFace
from layers.functions.prior_box import PriorBox
from data import cfg_mnet, cfg_re50

# face alignment
from utils.utils import Alignment_2_fivelandms, arcface_compare
# face recognition
from arcface_torch.backbones import get_model
np.set_printoptions(threshold=np.inf)

# ======================= Retinaface Pth ========================
class Retinaface_pth(object):
    def __init__(self, w,h,engine_file_path, conf_thres, iou_thres):

        # Create a Context on this device,
        self.cfx = cuda.Device(0).make_context()
        stream = cuda.Stream()
        TRT_LOGGER = trt.Logger(trt.Logger.INFO)
        runtime = trt.Runtime(TRT_LOGGER)

        # Deserialize the engine from file
        with open(engine_file_path, "rb") as f:
            engine = runtime.deserialize_cuda_engine(f.read())
        context = engine.create_execution_context()

        host_inputs = []
        cuda_inputs = []
        host_outputs = []
        cuda_outputs = []
        bindings = []

        for binding in engine:
            size = trt.volume(engine.get_binding_shape(
                binding)) * engine.max_batch_size
            dtype = trt.nptype(engine.get_binding_dtype(binding))
            # print("size",size)
            # Allocate host and device buffers
            host_mem = cuda.pagelocked_empty(size, dtype)
            cuda_mem = cuda.mem_alloc(host_mem.nbytes)
            # Append the device buffer to device bindings.
            bindings.append(int(cuda_mem))
            # Append to the appropriate list.
            if engine.binding_is_input(binding):
                host_inputs.append(host_mem)
                cuda_inputs.append(cuda_mem)
            else:
                host_outputs.append(host_mem)
                cuda_outputs.append(cuda_mem)

        # Store
        self.stream = stream
        self.context = context
        self.engine = engine
        self.host_inputs = host_inputs
        self.cuda_inputs = cuda_inputs
        self.host_outputs = host_outputs
        self.cuda_outputs = cuda_outputs
        self.bindings = bindings

        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.input_h = h
        self.input_w = w

    def check_keys(self, model, pretrained_state_dict):
        ckpt_keys = set(pretrained_state_dict.keys())
        model_keys = set(model.state_dict().keys())
        used_pretrained_keys = model_keys & ckpt_keys
        unused_pretrained_keys = ckpt_keys - model_keys
        missing_keys = model_keys - ckpt_keys
        # print('Missing keys:{}'.format(len(missing_keys)))
        # print('Unused checkpoint keys:{}'.format(len(unused_pretrained_keys)))
        # print('Used keys:{}'.format(len(used_pretrained_keys)))
        assert len(
            used_pretrained_keys) > 0, 'load NONE from pretrained checkpoint'
        return True

    def infer(self, img_raw, mulitperson=False, draw_res=False):
        # Make self the active context, pushing it on top of the context stack.
        self.cfx.push()
        # Restore
        stream = self.stream
        context = self.context
        engine = self.engine
        host_inputs = self.host_inputs
        cuda_inputs = self.cuda_inputs
        host_outputs = self.host_outputs
        cuda_outputs = self.cuda_outputs
        bindings = self.bindings

        img,frame,im_height,im_width=self.preprocess_image(img_raw)
        np.copyto(host_inputs[0], img.ravel())
        # Transfer input data  to the GPU.
        cuda.memcpy_htod_async(cuda_inputs[0], host_inputs[0], stream)
        # Run inference.
        context.execute_async(bindings=bindings, stream_handle=stream.handle)
        # Transfer predictions back from the GPU.
        cuda.memcpy_dtoh_async(host_outputs[0], cuda_outputs[0], stream)
        # Synchronize the stream
        stream.synchronize()
        # Remove any context from the top of the context stack, deactivating it.
        self.cfx.pop()
        # Here we use the first row of output in that batch_size = 1
        output = host_outputs[0]
        # t2 = time.time()
        # print("cost time:", t2-t1)

        result_boxes, result_scores, result_landmark = self.post_process(output,im_height,im_width)
        dets = np.hstack((result_boxes, result_scores[:, np.newaxis])).astype(np.float32, copy=False)
        dets = np.concatenate((dets, result_landmark), axis=1)
        dets = dets[dets[:, 4] > self.conf_thres]

        if not mulitperson and len(dets) > 0:
            List_width = dets[:, 2] - dets[:, 0]
            List_height = dets[:, 3] - dets[:, 1]
            det_area = np.multiply(List_width, List_height)
            max_area_id = det_area.argsort()[-1]
            dets = dets[max_area_id]
            dets = np.expand_dims(dets, axis=0)

        if draw_res:
            for b in dets:
                text = "{:.4f}".format(b[4])
                b = list(map(int, b))
                cv2.rectangle(frame, (b[0], b[1]), (b[2], b[3]), (0, 0, 255),
                              2)
                cv2.putText(frame, text, (b[0], b[1] + 12),
                            cv2.FONT_HERSHEY_DUPLEX, 0.5,
                            (255, 255, 255))  # 打印人脸检测的阈值

                # landms
                cv2.circle(frame, (b[5], b[6]), 1, (0, 0, 255), 4)
                cv2.circle(frame, (b[7], b[8]), 1, (0, 255, 255), 4)
                cv2.circle(frame, (b[9], b[10]), 1, (255, 0, 255), 4)
                cv2.circle(frame, (b[11], b[12]), 1, (0, 255, 0), 4)
                cv2.circle(frame, (b[13], b[14]), 1, (255, 0, 0), 4)

        return dets, frame

    def destroy(self):
        # Remove any context from the top of the context stack, deactivating it.
        self.cfx.pop()

    def xywh2xyxy(self, origin_h, origin_w, x, landmark):

        y = torch.zeros_like(x) if isinstance(
            x, torch.Tensor) else np.zeros_like(x)

        r_w = self.input_w / origin_w
        r_h = self.input_h / origin_h

        y[:, 0] = x[:, 0]/r_w
        y[:, 2] = x[:, 2] / r_w
        y[:, 1] = x[:, 1] / r_h
        y[:, 3] = x[:, 3] / r_h

        landmark[:, 0] = landmark[:, 0]/r_w
        landmark[:, 1] = landmark[:, 1] / r_h
        landmark[:, 2] = landmark[:, 2]/r_w
        landmark[:, 3] = landmark[:, 3] / r_h
        landmark[:, 4] = landmark[:, 4]/r_w
        landmark[:, 5] = landmark[:, 5] / r_h
        landmark[:, 6] = landmark[:, 6]/r_w
        landmark[:, 7] = landmark[:, 7] / r_h
        landmark[:, 8] = landmark[:, 8]/r_w
        landmark[:, 9] = landmark[:, 9] / r_h

        return y, landmark
    def preprocess_image(self, input_image):
        """
        description: Read an image from image path, resize and pad it to target size,
                        normalize to [0,1],transform to NCHW format.
        param:
            input_image_path: str, image path
        return:
            image:  the processed image
            image_raw: the original image
            h: original height
            w: original width
        """
        # image_raw = cv2.imread(input_image_path)
        image_raw = input_image.copy()
        h, w, c = image_raw.shape
        image = cv2.resize(image_raw, (self.input_w, self.input_h))

        image = image.astype(np.float32)

        # HWC to CHW format:
        image -= (104, 117, 123)
        image = np.transpose(image, [2, 0, 1])
        # CHW to NCHW format
        image = np.expand_dims(image, axis=0)
        # Convert the image to row-major order, also known as "C order":
        image = np.ascontiguousarray(image)
        return image, image_raw, h, w

    def post_process(self, output, origin_h, origin_w):
        """
        description: postprocess the prediction
        param:
            output:     A tensor likes [num_boxes,x1,y1,x2,y2,conf,landmark_x1,landmark_y1,
            landmark_x2,landmark_y2,...]
            origin_h:   height of original image
            origin_w:   width of original image
        return:
            result_boxes: finally boxes, a boxes tensor, each row is a box [x1, y1, x2, y2]
            result_scores: finally scores, a tensor, each element is the score correspoing to box
            result_classid: finally classid, a tensor, each element is the classid correspoing to box
        """
        # Get the num of boxes detected
        num = int(output[0])
        # Reshape to a two dimentional ndarray
        pred = np.reshape(output[1:], (-1, 15))[:num, :]
        # to  torch Tensor
        pred = torch.Tensor(pred).cuda()
        # Get the boxes
        boxes = pred[:, :4]
        # Get the scores
        scores = pred[:, 4]
        # Get the landmark
        landmark = pred[:, 5:15]
        # Choose those boxes that score > CONF_THRESH
        si = scores > self.conf_thres
        boxes = boxes[si, :]
        scores = scores[si]

        landmark = landmark[si, :]

        # Get boxes and landmark
        boxes, landmark = self.xywh2xyxy(origin_h, origin_w, boxes, landmark)

        # Do nms
        indices = torchvision.ops.nms(
            boxes, scores, iou_threshold=self.iou_thres).cpu()
        result_boxes = boxes[indices, :].cpu()
        result_scores = scores[indices].cpu()
        result_landmark = landmark[indices].cpu()
        return result_boxes, result_scores, result_landmark


# ========================= Arcface Pth ========================
class Arcface_pth(object):
    def __init__(self, rec_model, rec_weights, tolerance):
        self.model = get_model(rec_model, fp16=False)
        self.model.load_state_dict(torch.load(rec_weights))
        self.model.eval()
        self.model = self.model.to('cuda')
        self.tolerance = tolerance

    def infer(self, img_raw, dets):
        # 人脸对齐 + 人脸识别
        face_encodings = []
        crop_imgs = []

        for det in dets:
            feat, crop_img_112 = self.face_align_rec(img_raw, det)
            face_encodings.append(feat)
            crop_imgs.append(crop_img_112)

        face_names = []
        face_sims = []
        for face_encoding in face_encodings:
            # 取出一张脸并与数据库中所有的人脸进行对比，计算得分
            sims = []
            for known_face_encoding in self.known_face_encodings:
                sim = arcface_compare(known_face_encoding, face_encoding)
                sims.append(sim)
            name = "unrecognizable"
            best_match_index = np.argmax(sims)
            if sims[best_match_index] >= self.tolerance:
                name = self.known_face_names[best_match_index]
            face_names.append(name)
            face_sims.append(sims[best_match_index])
        return face_names, face_sims, crop_imgs

    def load_face_encodings(self, face_encodings):
        self.known_face_encodings = np.load(f"{face_encodings}_encoding.npy")
        self.known_face_names = np.load(f"{face_encodings}_names.npy")

    def face_align_rec(self, img_raw, det):
        # 获取 5个 landmark 点信息
        landmark_in = det[5:]
        # 人脸区域 对齐矫正，输出 112*112*3 大小人脸图crop_img
        crop_img = Alignment_2_fivelandms(img_raw, det, landmark_in)
        if crop_img.shape[0] != 112 or crop_img.shape[1] != 112:
            crop_img = cv2.resize(crop_img, (112, 112))
        crop_img_112 = crop_img.copy()
        crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
        crop_img = np.transpose(crop_img, (2, 0, 1))
        crop_img = torch.from_numpy(crop_img).unsqueeze(0).float()
        crop_img.div_(255).sub_(0.5).div_(0.5)
        # 人脸识别输出人脸特征
        feat = self.model(crop_img.cuda()).cpu().detach().numpy()
        return feat, crop_img_112


# ================= Face Det and Rec With Ros =====================
class Somo_Face_Recognition_Node(Node):
    def __init__(self, name):
        super().__init__(name)
        # 声明参数
        self.declare_parameter("det_trt_model",
                               "/home/robot/somo/src/somo_face_recognition/somo_face_recognition/Retinaface_arcface/od_face/weights/det/retina_r50.engine")
        self.declare_parameter("rec_weights",
                               "/home/robot/somo/src/somo_face_recognition/somo_face_recognition/Retinaface_arcface/od_face/weights/rec/gr50/backbone.pth")

        self.declare_parameter("rec_model", "r50")
        self.declare_parameter("det_model", "r50")
        self.declare_parameter("conf_thres", 0.8)
        self.declare_parameter("iou_thres", 0.4)
        self.declare_parameter("input_h", 480)#480
        self.declare_parameter("input_w", 640)#640
        self.declare_parameter("tolerance", 0.3)

        self.declare_parameter("face_database",
                               "/home/robot/somo/src/somo_face_recognition/somo_face_recognition/Retinaface_arcface/od_face/face_database")
        self.declare_parameter("face_encodings",
                               "/home/robot/somo/src/somo_face_recognition/somo_face_recognition/Retinaface_arcface/od_face/face_db")

        # self.declare_parameter("depth_sub_topic", "/camera_up/aligned_depth_to_color/image_raw/compressed")
        # 单独服务器测试----------------------
        # self.declare_parameter(
        #     "sub_topic", "/camera/color/image_raw/compressed")
        self.declare_parameter("sub_topic", "/camera_up/color/image_raw/compressed")
        self.declare_parameter("pub_topic", "/face_match")
        # self.declare_parameter("pub_topic","/face_match_result")
        self.declare_parameter("pub_image", "False")
        self.declare_parameter("mulitperson", "False")
        self.declare_parameter("draw_det", "True")
        self.declare_parameter("draw_rec", "True")
        self.declare_parameter("resultshow", "True")
        self.declare_parameter("lib_path", "/home/robot/somo/src/somo_face_recognition/somo_face_recognition/Retinaface_arcface/libdecodeplugin.so")
 
        self.center_x = 0
        self.center_y = 0

        # 设置参数
        # det_weights = self.get_parameter('det_weights').value
        rec_weights = self.get_parameter('rec_weights').value
        rec_model = self.get_parameter('rec_model').value
        det_trt_model = self.get_parameter('det_trt_model').value

        face_database = self.get_parameter('face_database').value
        face_encodings = self.get_parameter('face_encodings').value

        conf_thres = self.get_parameter('conf_thres').value
        iou_thres = self.get_parameter('iou_thres').value
        tolerance = self.get_parameter('tolerance').value
        self.input_h = self.get_parameter('input_h').value
        self.input_w = self.get_parameter('input_w').value

        self.pub_image = self.get_parameter('pub_image').value
        self.mulitperson = self.get_parameter('mulitperson').value
        self.draw_det = self.get_parameter('draw_det').value
        self.draw_rec = self.get_parameter('draw_rec').value
        self.resultshow = self.get_parameter('resultshow').value

        self.ros_sub_topic = self.get_parameter('sub_topic').value
        self.ros_pub_topic = self.get_parameter('pub_topic').value
        # self.depth_topic = self.get_parameter("depth_sub_topic").value
        lib_path=self.get_parameter("lib_path").value

        print("****** Init odface_det Model ******")
        ctypes.CDLL(lib_path)
        self.retinaface = Retinaface_pth(self.input_w,self.input_h,det_trt_model, conf_thres,
                                         iou_thres)

        print("****** Init Compressed2Image Module ******")
        # self.compressed2image = Compressed2Image(self.input_w,self.input_h) # -------------------------------------

        print("****** Init odface_rec Model ******")
        self.arcface = Arcface_pth(rec_model, rec_weights, tolerance)

        print("****** Update face encodeings ******")
        self.encode_face_database(face_database, face_encodings)

        print("****** Load face encodeings ******")
        self.arcface.load_face_encodings(face_encodings)

        self.get_logger().info("****** Init Publisher ******")
        self.res_pub = self.create_publisher(FaceBoxes, self.ros_pub_topic, 1)

        self.get_logger().info("****** Init Subscriber ******")
        self.image_sub = message_filters.Subscriber(
            self, CompressedImage, self.ros_sub_topic)
        
        self.tts = self.create_subscription(
            CompressedImage,
            '/camera_up/color/image_raw/compressed',
            self.union_callback,
            10  # 队列大小
        )
        # self.subscription 

        self.bridge = CvBridge()

        # if no image messages
        # self.getImageStatus = False
        # while (not self.getImageStatus) :
        #     self.get_logger().info("waiting for sub image.")
        #     rclpy.spin_once(self)
        #     time.sleep(2)
        self.pub_fourpoint = self.create_publisher(UInt16MultiArray, "four_point", 10)

    def union_callback(self, data):
            print('++++++++++++++++++++++++++++++++++++++++')

            # self.getImageStatus = True
            # try:
                # print('enter_try')

            image_data = self.bridge.compressed_imgmsg_to_cv2(
                data, desired_encoding="passthrough")
            # depth_data=self.compressed2image.forward(depth)
            depth_data=[]


            start = time.time()
            # 人脸检测
            dets, image_det_res = self.retinaface.infer(
                image_data, self.mulitperson, self.draw_det)
            # 人脸识别
            face_names, face_sims, crop_imgs = self.arcface.infer(image_data, dets)
            use_time = time.time() - start


            faceboxes = FaceBoxes()
            faceboxes.header = data.header
            # 发布结果 & 画图,
            # res_out, image_rec_res, four_pointxy = self.post_process(
            #     image_data, depth_data, dets, face_names, face_sims, crop_imgs)
            # four_pointxy=[0,0,0,0,0,0,0,0]
            res_out, image_rec_res, four_pointxy = self.post_process( image_data, depth_data, dets, face_names, face_sims, crop_imgs)



            faceboxes.result = res_out
            # if self.pub_image == True:
            #     faceboxes.image_data = self.bridge.cv2_to_imgmsg(
            #         image_rec_res, 'bgr8')
            #     print("pub the image in the faceboxes")
            # # ----------------------------- 当非空列表时，发布facebox
            if res_out != []:
                self.res_pub.publish(faceboxes)

            self.get_logger().info("Topic %s: Det_number: %s, Det_number: %s, Cost_Time: %.2f ms" %
                                (self.ros_pub_topic, len(dets), len(face_names), use_time * 1000))
            for i, j in zip(face_names, face_sims):
                self.get_logger().info("Face Recognition Result: %s, Face Recognition Sim: %.4f" % (i, j))

            # if self.resultshow == True:
            if len(crop_imgs) == 0:
                crop_img = np.zeros((112, 112, 3), dtype=np.uint8)
            else:
                crop_img = crop_imgs[0]
            # cv2.imshow('crop_img', crop_img)
            cv2.imshow('det_result', image_det_res)
            cv2.circle(image_rec_res, (self.center_x,
                    self.center_y), 3, (0, 255, 255), 0)
            # cv2.imshow('rec_result', image_rec_res)
            cv2.waitKey(1)
        # except:
        #      pass



    def post_process(self, image_data, depth_data, dets, face_names, face_sims, crop_imgs):
        ############### MMMMMMMMMMMMMMMM
        # depth_data = [[0]]
        a = []
        ############### WWWWWWWWWWWWWWWWW
        rec_img = image_data.copy()
        res_out = []
        for i, b in enumerate(dets):
            a = FaceBox()
            # Boxes
            a.xmin = float(b[0])
            a.ymin = float(b[1])
            a.xmax = float(b[2])
            a.ymax = float(b[3])
            # Score
            a.det_score = float(b[4])
            a.rec_score = float(face_sims[i])
            # classes
            name = face_names[i]
            a.classname = name

            a.x1 = int((a.xmin + a.xmax) / 2)  # 中心点
            a.y1 = int((a.ymin + a.ymax) / 2)
            self.center_x = a.x1
            self.center_y = a.y1
            # a.depth1 = float(depth_data[self.center_y][self.center_x] / 1000)

            # print("the_depth:",a.depth1)
            # a.depth1 = self.get_depth(a.x1, a.y1, depth_data)

            a.x2 = int((a.xmin + a.xmax) / 2) + 5  # 中心点 下方5像素点
            a.y2 = int((a.ymin + a.ymax) / 2)
            # a.depth2 = self.get_depth(a.x2, a.y2, depth_data)

            a.x3 = int((a.xmin + a.xmax) / 2) - 5  # 中心点 上方5像素点
            a.y3 = int((a.ymin + a.ymax) / 2)
            # a.depth3 = self.get_depth(a.x3, a.y3, depth_data)

            a.x4 = int((a.xmin + a.xmax) / 2)
            a.y4 = int((a.ymin + a.ymax) / 2) + 5  # 中心点 左方5像素点
            # a.depth4 = self.get_depth(a.x4, a.y4, depth_data)
            # print([x1,y1,depth1, x2,y2,depth2, x3,y3,depth3, x4,y4,depth4])

            # print('四点',a)

            if self.pub_image == True:
                a.crop_img = self.bridge.cv2_to_imgmsg(crop_imgs[i], 'bgr8')

            res_out.append(a)

            if self.draw_rec == True:
                b = list(map(int, b))
                cv2.rectangle(rec_img, (b[0], b[1]),
                              (b[2], b[3]), (0, 255, 0), 2)
                # 输出中文名
                rec_img = self.cv2ImgAddText(rec_img, name, b[0], b[3] - 20)
            four_point = a
            # print('four_point',a.x1)
        # return res_out, rec_img, a
        return res_out, rec_img, a
    

    def destroy(self):
        self.retinaface.destroy()

    def encode_face_database(self, face_database, face_encodings):
        known_face_encodings = []
        names = []
        # 获取人脸库 图像路径
        list_dir = os.listdir(face_database)
        for i, name in enumerate(list_dir):
            img_path = os.path.join(face_database, name)
            names.append(name.split(".")[0])
            img_raw = PIL.Image.open(img_path)
            img_raw = np.asarray(img_raw)
            dets, frame = self.retinaface.infer(img_raw)

            det_max = 0
            i_max = 0
            for i in range(dets.shape[0]):
                if det_max <= dets[i][4]:
                    det_max = dets[i][4]
                    i_max = i
            det = dets[i_max]

            feat, _ = self.arcface.face_align_rec(img_raw, det)

            known_face_encodings.append(feat)
        np.save(f'{face_encodings}_encoding.npy', known_face_encodings)
        np.save(f'{face_encodings}_names.npy', names)

    def cv2ImgAddText(self, img, label, left, top, textColor=(255, 255, 255)):
        img = PIL.Image.fromarray(np.uint8(img))
        # 设置字体
        font = ImageFont.truetype(font=f'{odai_face}/simhei.ttf', size=20)
        draw = ImageDraw.Draw(img)
        label = label.encode('utf-8')  # 中文名字编译
        draw.text((left, top), str(label, 'UTF-8'), fill=textColor, font=font)
        return np.asarray(img)


def main():
    rclpy.init()
    face_recog_node = Somo_Face_Recognition_Node("somo_face_node")
    rclpy.spin(face_recog_node)
    face_recog_node.destroy()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print(err)

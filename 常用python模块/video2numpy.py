# 输出视频信息,存储视频为一个数组返回  帧率、宽度、高度
import cv2
import numpy as np

def read_video_frames(video_path):
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 获取视频的帧数、宽度和高度
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 创建一个 NumPy 数组来存储所有帧
    frames = np.zeros((frame_count, height, width, 3), dtype=np.uint8)

    # 读取每一帧并存储到数组中
    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        frames[i] = frame

    # 释放视频资源
    cap.release()

    return frames

if __name__ == '__main__':
    # 使用示例
    video_path = 'train_src/eval_face/robot_ctrl/deep_to_light_matched.mp4'  # 替换为你的视频文件路径
    all_frames = read_video_frames(video_path)

    # 打印视频的基本信息
    print(f"视频总帧数: {all_frames.shape[0]}")
    print(f"视频宽度: {all_frames.shape[2]}")
    print(f"视频高度: {all_frames.shape[1]}")
    print(f"视频形状: {all_frames.shape}")


    # 释放资源
    del all_frames
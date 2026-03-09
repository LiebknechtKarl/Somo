
相关网站

```
https://github.com/THUDM/VisualGLM-6B
```

权重网站
```
https://huggingface.co/THUDM/visualglm-6b/tree/main
```

下载权重
```shell
git clone https://huggingface.co/THUDM/visualglm-6b
```

文字转语音播报节点

```shell
# /kaldi_vits_glm$ 
ros2 run vits vits_tts
ros2 topic pub /llm_response_result std_msgs/msg/String {"data: '你好'"} -1
```



2023/10/18 测试


#启动大模型
```shell
cd /media/ros/1T/yongtong/nlp/demo_ros_02_visualglm_vits
conda activate chatGLM
python api_hf_1018.py 
```



#启动语音播报
```shell
cd /home/ros/kaldi_vits_glm
source install/setup.bash
ros2 run vits vits_tts
ros2 topic echo /llm_response_result
```


#启动视频发布
```shell
cd /media/ros/1T/yongtong/nlp/demo_ros_03_photo_vits
source install/setup.bash
ros2 run video_pub video_pub1
```



#截图，请求文字回复并发布
```shell
cd /media/ros/1T/yongtong/nlp/demo_ros_03_photo_vits
source install/setup.bash
ros2 run video_pub photograph_pub
```
 

#发布嘴部动作
```shell
cd /home/ros/kaldi_vits_glm/src/head-control
source install/setup.bash
ros2 run ulaahead facial_mouth_audio
```


#发布舵机角度
```shell
cd /home/ros/kaldi_vits_glm/src/head-control
source install/setup.bash
ros2 run ulaahead facial_features
```










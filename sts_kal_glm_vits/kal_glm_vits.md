
## 配置
    文件路径     /media/ros/1T/yongtong/sts

在部署语音识别包时，即运行ros2 run VoiceOffline ros_kaldi
会出现  

```
File "/media/ros/1T/yongtong/sts/install/VoiceOffline/lib/python3.10/site-packages/VoiceOffline/ros_kaldi.py", line 10, in <module>
    from kaldi_python import SherpaNcnn
ModuleNotFoundError: No module named 'kaldi_python'
```

解决方案：我们把kaldi_python.py放入上述报错的文件夹中即可。无需colcon build，可直接运行



```
> 在演示时，需要在sts文件夹下打开终端。

> 开启五个终端

> 终端1：ros2 topic pub /speech2tts_kaldi_call std_msgs/msg/String {"data: ''"} -1           # 启动语音识别指令

> 终端2：ros2 run VoiceOffline ros_kaldi                                                     # 语音识别节点

> 终端3：ros2 run llm ros_llm                                                                # 调用chatGLM的use_api节点

> 终端4：ros2 run vits vits_tts                                                              # 语音合成节点

> 终端5：ros2 topic echo /llm_response_result                                                # 查看回复的对话 内容             
  
> 另外，需要在 /media/ros/1T/yongtong/sts/src/llm/llm 中，打开终端，运行python openai_api.py，启动chatGLM的节点。
```


/media/ros/1T/yongtong/sts



### 终端1：ros2 topic pub /speech2tts_kaldi_call std_msgs/msg/String {"data: ''"} -1           # 启动语音识别指令

### 终端2：ros2 run VoiceOffline ros_kaldi                                                     # 语音识别节点
```
    ros2 run VoiceOffline ros_kaldi   
    # "ros_kaldi = VoiceOffline.ros_kaldi:main"
```
主体

```
节点 ros_kaldi
    # 接收输入   speech2tts_kaldi_call
    subscription(String,"speech2tts_kaldi_call",self.kaldi_sub_callback,10)  # 调用同目录 kaldi_python.sherpaNcnn.SherpaNcnn_speechtotts 
                生成返回值
    publisher(String,"speech2tts_kaldi_result", 10)    # 将生成的返回值输出   应该是返回输入语音转的文字
```
    

### 终端3：ros2 run llm ros_llm         # 调用chatGLM的use_api节点     "ros_llm = llm.api_use:main"


```
节点    llm_node
        subscription(String,"speech2tts_kaldi_result",self.llm_callback,10)    # 返回语音转的文本，输入chat_glm 得到回答
        publisher(String,"llm_response_result",10)            # 发布回答   txt
```


### 终端4：ros2 run vits vits_tts         # 语音合成节点  "vits_tts=vits.tts:main"


```
节点    tts_node
        subscription(String,"llm_response_result",self.command_callback,10)    # 接收发布文本  数据清洗（去空格...）  its转文本

```

### 终端5：ros2 topic echo /llm_response_result   # 查看返回文本txt（转语音前）



## 关于vits

训练位置

![输入图片说明](Screenshot%20from%202023-08-12%2011-07-36.png)


网站



> https://www.bilibili.com/video/BV1Lo4y1B7JX/?spm_id_from=333.337.search-card.all.click&vd_source=fc610f34af4cf456f594ac833cd15c6f



















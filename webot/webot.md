
humanoid  humanoid_behavior_tree  humanoid_bringup  humanoid_moveit2_config  humanoid_msgs  humanoid_slam  humanoid_tf2  humanoid_voice  humanoid_voice_base  webots_ros2_2022a

还要改lib文件
主要 ：humanoid_voice

# humanoid
ros2 launch humanoid humanoid_launch.py             # 打开webot

# humanoid_bringup
ros2 launch humanoid_bringup  humanoid_launch.py  # 打开导航

直接测试  打开目录
/src/humanoid_bringup/test/nav.py
eg     /usr/bin/python3 /home/lilei/Desktop/reco/national_game/src/humanoid_bringup/test/nav.py


# humanoid_moveit2_config
ros2 launch humanoid_moveit2_config  move_group.launch.py
ros2 launch humanoid_moveit2_config  move_group_interface_controller.launch.py

# humanoid_slam

# humanoid_tf2
ros2 launch humanoid_tf2 humanoid_tf2_launch.py

# humanoid_voice
本功能包只运行以下即可
ros2 launch humanoid_voice humanoid_voice_control_launch.py

包含节点
humanoid_voice
    awaken_record
    awaken_node
    humanoid_voice
humanoid_voice_base
    iat_publish
    tts_subscribe
    
#############################################


```
ros2 launch humanoid_bringup  humanoid_launch.py   # 环境，导航
    test.py

ros2 launch humanoid_voice humanoid_voice_control_launch.py   # 语音
    ros2 topic echo /iat_raw   # 查看语音转文字结果

ros2 topic pub  /iat_raw  std_msgs/String "data: '马上前往书房'" -1
```



ros2 launch mm_bringup robot_launch.py 

















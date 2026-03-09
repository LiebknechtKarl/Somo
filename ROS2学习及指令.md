#### 新建ros

```
# linux新建普通用户
sudo adduser -r YongHuMing # 然后接下来按照提示输入密码等（注意密码不能包含任何本机用户名）
# 为此普通用户添加sudo权限
sudo vim /etc/sudoers
# 在 root    ALL=(ALL:ALL) ALL 下面添加代码如下即可
# YongHuMing ALL=(ALL:ALL) ALL
```

```
# 为新平台安装向日葵时，若出现缺少相关包 libgconf-2.4
# 统一解决平台方案：在如下网址下载缺少的包，下载安装即可
http://archive.ubuntu.com/ubuntu/pool/universe/g/gconf/
```


```shell
#新建工作空间 txt2audio并新建功能包txt_pub
mkdir -p txt2audio/src
cd txt2audio/src
ros2 pkg create --build-type ament_python txt_pub
cd txt_pub/txt_pub
```
```shell
# 只编译一个包
colcon build --packages-select <name-of-pkg>
```
```shell
ros2 topic pub /llm_response_result std_msgs/msg/String {"data: '你好'"} -1
```
```shell
source /opt/ros/humble/setup.bash
```

```
# 查看 服务 名 的消息类型
ros2 service type /Gripper_ctrl
```

```
# 查看服务的消息，不需要记忆具体消息类型命令，善用tab键可补齐 以及提示
ros2 service call /Gripper_ctrl std_srvs/srv/SetBool  data:\ false\
```





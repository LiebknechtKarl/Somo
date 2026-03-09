# Docker配置语音交互系统

## 1.安装docker

卸载旧docker

一般来说ubuntu自带docker的库但是版本太低了一般需要卸载后再安装新的。

```
sudo apt-get remove docker docker-engine docker.io containerd runc
```

安装docker依赖

更新软件包

```bash
sudo apt update
sudo apt upgrade
```

安装docker依赖

```bash
sudo apt-get install ca-certificates curl gnupg lsb-release
```

添加Docker官方密钥

```bash
curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
```

安装Docker

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

启动docker服务

```
sudo service docker start
```

添加nvidia-docker的源

```
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
```

安装nvidia-container-toolkit(不然用不了gpu)

```
sudo apt-get install -y nvidia-container-toolkit
```

重启docker

```
sudo systemctl restart docker
```

## 2.配置pulseaudio socket用于使docker使用外部音频设备

创建pulseaudio socket

```
cd /tmp
touch pulseaudio.socket
```

```
pactl load-module module-native-protocol-unix socket=/tmp/pulseaudio.socket
```

创建pulseaudio客户端的配置文件

```
touch pulseaudio.client.conf
```

将下面内容复制到配置文件里

```
default-server = unix:/tmp/pulseaudio.socket
# Prevent a server running in the container
autospawn = no
daemon-binary = /bin/true
# Prevent the use of shared memory
enable-shm = false
```

## 3.加载镜像并启动docker

```
cd /home/ros
```

加载语音交互镜像

```
docker load<imi-voice.tar
```

创建容器并启动

```
docker run -it --gpus all --env PULSE_SERVER=unix:/tmp/pulseaudio.socket --env PULSE_COOKIE=/tmp/pulseaudio.cookie --volume /tmp/pulseaudio.socket:/tmp/pulseaudio.socket --volume /tmp/pulseaudio.client.conf:/etc/pulse/client.conf --volume /dev/snd:/dev/snd --privileged --name llm imi-voice /bin/bash
```

启动后如果用exit退出程序要把容器设为运行状态

```
docker start llm
```

之后再启动容器时使用

```
docker exec -it llm /bin/bash
```

### 注：之后换电脑使用时要把容器内/home/imi/tts_llm/kaldi_vits_glm/install/llm/lib/site-packages/llm下的api_use.py和openai_api.py中的网络IP分别改为

```
openai.api_base = "http://localhost:8000/v1"
```

和

```
uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)
```

## 4.测试用例

测试大模型通信

```
ros2 topic pub /speech2tts_kaldi_result std_msgs/msg/String {"data: "你好""} -1
```


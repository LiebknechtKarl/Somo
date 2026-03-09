

#### docker


```shell
docker ps -a    # 显示所有容器，包括未运行的

docker run -it --gpus all imi-cuda-11.7.1 /bin/bash   # 
# docker run：启动一个新的容器。
# -it：以交互式模式运行容器，允许用户与容器进行交互。
# --gpus all：在容器中启用所有可用的GPU设备。
# imi-cuda-11.7.1：指定要运行的镜像名称或ID。在这种情况下，是一个名为"imi-cuda-11.7.1"的镜像。
# /bin/bash：在容器内部执行的命令，这将启动一个bash终端。

docker run -it --gpus all --device /dev/snd:/dev/snd  imi-cuda-11.7.1 /bin/bash     # 带声卡

```


#### docker 安装
参考网站    https://zhuanlan.zhihu.com/p/143156163

最好开梯子
更新软件包索引，并且安装必要的依赖软件，来添加一个新的 HTTPS 软件源：


```shell
sudo apt update
sudo apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
```

使用下面的 curl 导入源仓库的 GPG key：

```shell
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

将 Docker APT 软件源添加到系统：

```shell
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```
现在，Docker 软件源被启用了，你可以安装软件源中任何可用的 Docker 版本。

安装 Docker 最新版本

```shell
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

安装完成，Docker 服务将会自动启动。可以输入下面的命令，验证它：

```shell
sudo systemctl status docker
```

输出将会类似下面这样：

```shell
● docker.service - Docker Application Container Engine
     Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2020-05-21 14:47:34 UTC; 42s ago
...
```

#### 创建

```
docker run ubuntu:20.04 /bin/echo "Hello world"
#  Docker 以 ubuntu20.04 镜像创建一个新容器，然后在容器里执行 bin/echo "Hello world"，然后输出结果。
```

运行交互式的容器

通过 docker 的两个参数 -i -t，让 docker 运行的容器实现"对话"的能力：


```shell
sudo docker run -i -t ubuntu:20.04 /bin/bash   # 用ubuntu:20.04镜像创建新容器   
## root@2686d52ecfdf:/# ls
#各个参数解析：
#-t: 在新容器内指定一个伪终端或终端。
#-i: 允许你对容器内的标准输入 (STDIN) 进行交互。
```
在docker内部终端  通过运行 exit 命令或者使用 CTRL+D 来退出容器。


查看容器

```shell
docker ps -a
# 返回
##CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS                      PORTS     NAMES
##2686d52ecfdf   ubuntu:20.04   "/bin/bash"              17 minutes ago   Exited (0) 8 minutes ago              hungry_brahmagupta

#CONTAINER ID: 容器 ID。
#IMAGE: 使用的镜像。
#COMMAND: 启动容器时运行的命令。
#CREATED: 容器的创建时间。
#STATUS: 容器状态。

#docker start 启动一个已停止的容器：
docker start 2686d52ecfdf
#sudo docker ps -a  # 查看所有容器显示已启动
##CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS                      PORTS     NAMES
##2686d52ecfdf   ubuntu:20.04   "/bin/bash"              20 minutes ago   Up 9 seconds                          hungry_brahmagupta
```

删除容器

``` shell
docker rm -f <CONTAINER ID > # 比如    docker rm -f 2686d52ecfdf 
```

进入容器
在使用 -d 参数时，容器启动后会进入后台。此时想要进入容器，可以通过以下指令进入：

```shell
docker attach  <CONTAINER ID > # 比如    docker attach 2686d52ecfdf      # 进入容器
docker exec： #推荐大家使用 docker exec 命令，因为此命令会退出容器终端，但不会导致容器的停止。
```































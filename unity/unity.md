

视频网站
https://www.bilibili.com/video/BV1gQ4y1e7SS/?p=2&spm_id_from=pageDriver&vd_source=fc610f34af4cf456f594ac833cd15c6f

另一个    https://www.bilibili.com/video/BV17x411575F/?p=3&vd_source=fc610f34af4cf456f594ac833cd15c6f

公众号    GamerFeiYu

代码位置    https://pan.baidu.com/s/12rHhusN8BVUjEUG6IkqaJQ?pwd=s63g

官方手册    https://docs.unity.cn/cn/current/Manual/UnityManual.html    （好像要翻墙）

![输入图片说明](Screenshot%20from%202023-08-28%2010-54-30.png)

![输入图片说明](Screenshot%20from%202023-08-28%2010-57-23.png)

游戏引擎是指一些编写好的可重复利用的代码与开发游戏所用的各功能编辑器。

AR    现实增强技术
MR    混合现实技术
unityhub    unity版本管理
LTS    稳定版本


#### 新建项目

新建项目流程：

    新项目————>编辑其版本，3D核心版本，文件名，位置————>创建项目

![输入图片说明](Screenshot%20from%202023-08-28%2016-03-57.png)

![输入图片说明](Screenshot%20from%202023-08-28%2016-05-23.png)

要等一会儿

![输入图片说明](Screenshot%20from%202023-08-28%2016-11-01.png)

新建成功界面

![输入图片说明](Screenshot%20from%202023-08-28%2016-12-14.png)

选择右上角    layout————>2by3    转化为与作者相同界面

![输入图片说明](Screenshot%20from%202023-08-28%2016-15-53.png)

左下角可能会报错，忽略

![输入图片说明](Screenshot%20from%202023-08-28%2016-25-43.png)

Edit-->Project Setting    管理工程设置  （声音,物理，质量等） 
Edit-->Preferences    编辑器测试（C打开？  语言设置    ）

可以设为中文重启执行设置
![输入图片说明](Screenshot%20from%202023-08-28%2016-40-39.png)

游戏对象-->3d对象-->立方体

场景（上）和摄像机场景（下）

![输入图片说明](Screenshot%20from%202023-08-28%2016-59-01.png)

可以拖拽摄像机和立方体

管理摄像机camera，灯光，立方体属性（检查器）

![输入图片说明](Screenshot%20from%202023-08-28%2017-01-34.png)

右键换角度，滚轮平动

创建一些物体

![输入图片说明](Screenshot%20from%202023-08-28%2017-18-12.png)

创建两物体拖动设置父子关系

![输入图片说明](Screenshot%20from%202023-08-28%2017-23-36.png)

平移旋转缩放工具

![输入图片说明](Screenshot%20from%202023-08-28%2017-33-26.png)

按住ctrl选择多个文件，  右键-->导出包      命名为test将其导出到桌面    

![输入图片说明](Screenshot%20from%202023-08-29%2010-37-04.png)

![输入图片说明](Screenshot%20from%202023-08-29%2010-39-35.png)

删除其它，只留空包

![输入图片说明](Screenshot%20from%202023-08-29%2010-51-12.png)

右键--->导入包--->自定义包    选择之前导出的包   导入

![输入图片说明](Screenshot%20from%202023-08-29%2011-27-22.png)

打开scene里面的salsa文件加载模型

![输入图片说明](Screenshot%20from%202023-08-29%2011-29-13.png)

改变颜色材质

![输入图片说明](Screenshot%20from%202023-08-29%2011-35-39.png)

在scenes中   右键--->新建--->材质    建立材质球改变颜色

![输入图片说明](Screenshot%20from%202023-08-29%2011-38-02.png)

将材质球拖到要改变材质的目录下方 （eg:boxhead.v2_root）

![输入图片说明](Screenshot%20from%202023-08-29%2011-40-08.png)

![输入图片说明](Screenshot%20from%202023-08-29%2011-43-36.png)

unity        3d资源

#### 加载网络资源

`https://assetstore.unity.com/3d`

主页中  3d————>免费资源————>添加至我的资源
右上角 我的资源--->在unity打开   （eg:low poly simple nature）

找到免费资源，

![输入图片说明](Screenshot%20from%202023-08-29%2016-34-21.png)

打开unity    窗口-->包管理器-->包：我的资产-->下载 low poly simple nature--->右上角下载--->导入--->全部导入

![输入图片说明](Screenshot%20from%202023-08-29%2016-39-24.png)

![输入图片说明](Screenshot%20from%202023-08-29%2016-41-51.png)

导入之后，  项目-->asserts-->simplenaturepack--->scenes--->点击指定图标并且打开

![输入图片说明](Screenshot%20from%202023-08-29%2016-47-07.png)

![输入图片说明](Screenshot%20from%202023-08-29%2016-49-28.png)



#### 创建地形

需要资源  https://pan.baidu.com/s/12rHhusN8BVUjEUG6IkqaJQ?pwd=s63g

将该网站的包 standard asset 导入

![输入图片说明](Screenshot%20from%202023-08-29%2022-14-43.png)

创建3d地形

![输入图片说明](Screenshot%20from%202023-08-29%2022-12-20.png)

![输入图片说明](Screenshot%20from%202023-08-31%2023-54-18.png)























































### websocket通信

Websocket是一种协议设计用于提供低延迟、全双工和长期运行的连接
全双工:通信的两个参与方可以同时发送和接收数据,不需要等待对方的响应或传输完成
降低延迟链接一旦建立便会保持开放,数据可以在客户端和服务器之间以比HTTP更低的延迟进行传输更高效的资源利用可以减少重复请求和响应的开销,因为它的连接只需要建立一次

![输入图片说明](Screenshot%20from%202023-08-31%2023-53-21.png)































 





















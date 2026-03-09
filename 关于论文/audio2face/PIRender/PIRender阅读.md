## 摘要
控制人脸生成运动人脸  <br />
PIRender使用3DMM参数控制面部运动  <br />
扩展模型  从音频输入中提取序列动作。音频驱动的面部重演任务。模型可以仅从单个参考图像和驱动音频流中生成具有令人信服的运动的连贯视频。

模型作用
> 1. 原图片+指定动作（3dMM）---> 原图片动图
> 2. 原图片+别人动图 ---> 原图片动图
> 3. 原图片+语音 ---> 原图片动图

![输入图片说明](Screenshot%20from%202024-12-24%2016-31-01.png)

## Introduction
直观地控制给定人脸的姿势和表情来编辑人像图像   <br />
建模方法： 参数化人脸   3DMM   ----> 控制人脸渲染 <br />
模型分为三部分： <br />
> 1. 映射网络（Mapping Network）:从动作描述符中生成潜在向量
> 2. 扭曲网络（Warping Network）:估计源与期望目标之间的形变，并通过扭曲源图像以估计的形变生成粗略结果
> 3. 编辑网络（Editing Network）:从粗略图像生成最终图像

贡献：
> 实现直观的照片级面部表情、头部旋转和平移编辑。   <br />
> 表情模仿   <br />
> 够提取与主体无关的运动并生成逼真的视频   <br />
> 仅从一个肖像图像和一个驱动音频流中生成多样且生动视频   <br />

## 2. Related Work   相关工作
通过语义参数化进行人像编辑   <br />
通过动作模仿进行人像编辑。   <br />
通过音频进行人像编辑。   <br />
将输入的运动描述符p映射到潜在向量z。然后通过变形网络生成一个粗略图像。最后，编辑网络通过编辑粗略结果来生成最终的图像。   <br />

![输入图片说明](Screenshot%20from%202024-12-24%2016-45-56.png)

## 3. Our Approach  我们的方法
在目标运动描述符p的指导下，模型可以通过修改给定图像 I<sub>s</sub>  的面部表情、头部姿势和平移，生成逼真的肖像图像   $ \hat{I} $  
### 3.1. 目标运动描述符 Target Motion Descriptor 
3DMM，面部的三维形状 S 被参数化为
$S =\overline{S}+\alpha B_{id}+\beta B_{exp}$

$\overline{S}$ ：平均脸型，    <br />
B<sub>id</sub>和B<sub>exp</sub>是基于200个人脸扫描通过主成分分析（PCA）计算出的身份和表情的基础，    <br />
系数α∈R<sup>80</sup>   面部形状   <br />
β∈R<sup>64</sup>	表情    <br />
头部旋转  R∈SO(3)   <br />
头部平移  t∈R<sup>3</sup>    <br />
有了参数集p<sub>i</sub> ≡ {β<sub>i</sub>, R<sub>i</sub>, t<sub>i</sub>} {表情，头部旋转，头部平移}   ，脸i期望的运动可以被清楚地表达出来。


### 3.2. 语义控制的PIrender  PIRenderer for Semantic Control    
源图像 I<sub>s</sub>  +  目标运动描述符  p  ---Pirender---> 目标运动的人像图像  $ \hat{I} $  

 **映射网络 Mapping Network**   <br />
映射网络 fm ：P→Z        P{表情，头部旋转，头部平移}---->隐向量Z   <br />
z = f<sub>m</sub>(p)   <br />
z ---仿射变换---> y = (y<sub>s</sub>, y<sub>b</sub>)   <br />
y 用于控制自适应实例归一化（AdaIN）操作  <br />
AdaIN 操作负责将 z 描述的运动注入到变形网络和编辑网络  <br />
$AdaIN( x_{i},y ) = y_{s,i} \frac { x_{i}-\mu(x_{i}) } { \sigma(x_{i}) } + y_{b,i}$   <br>
 μ(·) 和 σ(·) 分别表示平均值和方差的运算。每一个特征图 xi 首先进行归一化，然后使用 y 对应的标量分量进行缩放和偏置。

 **The Warping Network 扭曲网络** 

扭曲网络g<sub>w</sub> 来对源图像 I<sub>s</sub> 的重要信息进行空间转换。<br>
源图像 I<sub>s</sub> + 潜在向量 z ---扭曲网络g<sub>w</sub>--->包含坐标偏移的流场 w      <br>
w = g<sub>w</sub>(I<sub>s</sub>,z)     <br>
扭曲网络g<sub>w</sub>  自编码器   每个卷积层之后使用AdaIN操作来注入由z描述的运动   <br>

$\hat{I}_{w} = w(I_{s})$   使用w对源图像Is进行变形。   <br>
warping loss的损失函数L<sub>w</sub>  :  扭曲后的图像$\hat{I}_{w}$与目标图像I<sub>t</sub>之间的重建误差    <br>
$L_{w}=\sum\limits_i^{}\parallel\phi_{i}(I_{t})-\phi_{i}(\hat{I}_{w})\parallel_{1}$     <br>
 $\phi_{i} $  是VGG-19网络第i层的激活图  <br>

 **The Editing Network编辑网络**    <br>

扭曲网络: 转换源图像效率高,扭曲操作引入的伪影会导致性能下降 <br>
编辑网络: g<sub>e</sub> ， 用于修改扭曲后的粗略结果 $\hat{I}_{w}$  。<br>
$\hat{I} = g_{e} (  \hat{I}_{w} , I_{s} , z )$   <br>
&nbsp;&nbsp;&nbsp;  $\hat{I}_{w}$  扭曲后的粗略结果<br>
&nbsp;&nbsp;&nbsp;   I<sub>s</sub> 源图像 <br>
&nbsp;&nbsp;&nbsp;   z 潜在向量    <br>
&nbsp;&nbsp;&nbsp;   $\hat{I}$  最终的预测   <br>

编辑网络采用与扭曲网络相似的架构设计,也使用了AdaIN操作来注入潜在向量 z 。   <br>

 _损失函数_ : 重建损失 L<sub>c</sub>  和风格损失 L<sub>s</sub>   <br>
$L_{c} =  \sum\limits_i^{} \parallel \phi_{i}(I_{t})-\phi_{i}(\hat{I})\parallel_{1}$   <br>
$L_{s} =\sum\limits_i^{} \parallel G_j^\phi(I_{t})- G_j^\phi (\hat{I})\parallel_{1}$   <br>
&nbsp;&nbsp;&nbsp;   $\hat{I}$  最终的预测   <br>
&nbsp;&nbsp;&nbsp;   I<sub>t</sub> 真实目标    <br>
&nbsp;&nbsp;&nbsp;   $\phi_{i}$  VGG-19网络第i层的激活图    <br>
&nbsp;&nbsp;&nbsp;   $G_j^\phi$ 是由激活图$\phi_{i}$构成的Gram格拉姆矩阵    <br>

$L = \lambda_{w}L_{w} + \lambda_{c}L_{c} + \lambda_{s}L_{s}$   <br>
在实验中，设定 λ<sub>w</sub> = 2.5， λ<sub>c</sub>  = 4， λ<sub>s</sub>  = 1000。   <br>

![音频驱动](Screenshot%20from%202024-12-25%2010-17-47.png)
> 音频驱动模型

###  _3.3. 声音驱动的面部重现扩展 Extension on Audio-driven Reenactment_      <br>
&nbsp;&nbsp;&nbsp; 连续音频 --f<sub>θ</sub>--> 3DMM   <br>
(p, c) ≡ (p<sub>1:t</sub>, c<sub>1:t</sub>) &nbsp;&nbsp;&nbsp; p:运动  条件信息:c  潜在变量 :n   <br>



之前生成的k个运动 p<sub>i-k:i-1</sub>  以及音频a<sub>i-k:i+τ</sub>被用作条件信息c<sub>i</sub>     <br>
$n =  f_\theta^{-1}(p,c)$     <br>
&nbsp;&nbsp;&nbsp; n 潜在变量



&nbsp;&nbsp;&nbsp; 在时间点i生成运动p<sub>i</sub>      <br>

## 4.实验  Experiment
### 4.1. 实施细节 Implementation Details
 **数据集** 
VoxCeleb数据集   22496个说话人头部视频      <br>
原始视频裁剪出脸部    裁剪后视频包含自然动作，脸部在固定的边界框内自由移动    视频大小为256×256     <br>
音频从视频中提取出来,用于音频驱动任务    总共获得17913训练视频和514测试视频，长度从64到1024帧不等 <br>

**评估指标**  <br>
&nbsp;&nbsp;&nbsp; LPIPS：估计重建误差。计算生成图像与参考图像之间的感知距离    <br>
&nbsp;&nbsp;&nbsp; FID： 计算假图像和真图像分布之间的Wasserstein-2距离（衡量两个分布相似程度）  <br>
&nbsp;&nbsp;&nbsp; 平均表情距离（AED）&平均姿态距离（APD）：计算生成图像与目标之间的3DMM表情和姿态距离  <br>
&nbsp;&nbsp;&nbsp; 评估主观质量：Just Noticeable Difference（JND） 人看统计  从真实和假样本的数据对中选择更逼真的 <br> 
**训练详情** 
 分阶段
1. 映射网络和变形网络预先训练200k次迭代。
2. 以端到端的方式再训练整个模型200k次迭代。ADAM优化器，学习率衰减

### 4.2. 直观的人像图像编辑 Intuitive Portrait Image Editing
对比试验： ours&StyleRig <br> 
StyleRig 通过控制 Style-GAN 来实现语义编辑 <br> 

 
### 4.3. 说话头部动作模仿 Talking-head Motion Imitation

**两个任务：** <br> 
&nbsp;&nbsp;&nbsp;（1）同身份重建任务，其中源图像和驱动图像为同一个人； <br> 
&nbsp;&nbsp;&nbsp;（2）跨身份动作模仿任务，其中通过模仿另一个个体的动作生成不存在的视频。 <br> 

### 4.4. 声音驱动的面部再现  Audio-driven Facial Reenactment

1. 首先通过fθ生成具有各种姿态和表情的连续动作。
2. 使用PIRenderer将这些动作转换成任意个体。
 <br> 
 <br> 
 <br> 
### A. PIRenderer的额外结果
1. 直观人像编辑任务
2. 动作模仿任务
3. 声音驱动的面部
4. 视频连贯研究
5. 动作平滑


### B. 目标运动描述符的分析

连续帧窗口的系数：即包含中心帧及其前后各13帧。他们将这个窗口中所有帧的3DMM系数平均起来，作为中心帧的运动描述符p。   <br> 
使用单个输入帧的3DMM系数作为目标运动描述符，训练了一个消融模型。     <br> 

### C. 隐空间插值Z

映射网络 f<sub>m</sub>: P → Z 将运动描述符 p 映射到支持面部运动插值任务的线性隐空间 z    <br> 
计算隐向量 z′     <br> 
$z' = \alpha f_{m}(p_{1}) + (1-\alpha)f_{m}(p_{2})$    <br> 
p<sub>1</sub> 和 p<sub>2</sub> 是两种不同的运动，f<sub>m</sub> 是映射函数    <br> 
α的增加，从运动p<sub>1</sub>线性变换到运动p<sub>2</sub>       <br> 
插值潜在向量z'控制生成具有相同表达式和平滑变化的姿势的图像        <br> 

### D 实施细节 
#### D.1. PIRenderer的实施细节 
  
学习率衰减   中心帧的运动描述符p        <br> 
λw=2.5，λc=4，λs=1000        <br> 

 **D.2. f<sub>θ</sub>实现细节** 

$\begin{equation}
\mathbf{n} \stackrel{f_1(*, \mathbf{c})}{\longleftrightarrow} \mathbf{h}_1 \stackrel{f_2(*, \mathbf{c})}{\longleftrightarrow} \mathbf{h}_2 \cdots \stackrel{f_K(*, \mathbf{c})}{\longleftrightarrow} \mathbf{p}
\end{equation}$



   <br>
   <br>
   <br>
   <br>
   <br>
   <br>
   <br>
   <br>
   <br>
   <br>
   <br>
   <br>   <br>
   <br>
   <br>
   <br>
   <br>   <br>
   <br>
   <br>
   <br>
   <br>


















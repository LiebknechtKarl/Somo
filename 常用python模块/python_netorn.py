import netron
import torch.onnx
from torch.autograd import Variable
from torchvision.models import resnet18  # 以 resnet18 为例
import hiddenlayer as h
myNet = resnet18()  # 实例化 resnet18
x = torch.randn(16, 3, 40, 40)  # 随机生成一个输入

### MMM 主要模块
modelData = "./demo.pth"  # 定义模型数据保存的路径
torch.onnx.export(myNet, x, modelData)  # 将 pytorch 模型以 onnx 格式导出并保存
netron.start(modelData)   # 输出网络结构
### WWW 主要模块

### MMM 直接加载保存好的
# modelData = "./demo.pth"  # 定义模型数据保存的路径
# netron.start(modelData)  # 输出网络结构
### WWW 直接加载保存好的



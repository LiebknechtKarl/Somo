
######################################################################## 2D
# t-SNE 分析
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.datasets import load_digits

# 1. 加载示例数据（这里用手写数字数据集，你可以换成自己的数据）
digits = load_digits()
X = digits.data      # 数据特征 (n_samples, n_features)
y = digits.target    # 标签 (n_samples,)
# X.shape     (1797, 64)
# y.shape     (1797,)
# y             array([0, 1, 2, ..., 8, 9, 8])

# 2. 创建 t-SNE 模型
tsne = TSNE(
    n_components=2,   # 降到2维方便可视化
    learning_rate='auto',
    init='random',
    perplexity=30,
    random_state=42
)

# 3. 拟合并转换数据
X_tsne = tsne.fit_transform(X)

# 4. 可视化
plt.figure(figsize=(8, 6))
scatter = plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y, cmap="tab10", s=15)
plt.colorbar(scatter)
plt.title("t-SNE Visualization")
plt.xlabel("Dimension 1")
plt.ylabel("Dimension 2")
plt.show()


######################################################################## 3D
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.datasets import load_digits

# 1. 加载示例数据（这里用手写数字数据集，你可以换成自己的数据）
digits = load_digits()
X = digits.data      # 数据特征 (n_samples, n_features)
y = digits.target    # 标签 (n_samples,)
# X.shape     (1797, 64)
# y.shape     (1797,)
# y             array([0, 1, 2, ..., 8, 9, 8])

# 2. 创建 t-SNE 模型
tsne = TSNE(n_components=3, perplexity=30, random_state=42)
X_tsne = tsne.fit_transform(X)

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(X_tsne[:, 0], X_tsne[:, 1], X_tsne[:, 2], c=y, cmap="tab10", s=15)
plt.colorbar(scatter)
plt.title("3D t-SNE Visualization")
plt.show()



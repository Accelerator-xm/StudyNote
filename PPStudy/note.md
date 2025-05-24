# paddle 深度学习框架学习

## 线性代数补充
- 向量一般指列向量

- 矩阵求导
![矩阵求导](img/img00/math1.png)

- 矩阵求导推广
![矩阵求导推广](img/img00/math2.png)

## 1 Machine Learning 机器学习
每个算法都有对应的假设函数、目标函数、优化方法

### 以房价预测为例
两个变量：大小、房间数
标签：房价
![题目](img/img01/q_instruction.png)

- 确立假设函数
![假设函数](img/img01/Hypothetical_function.png)

- 寻找目标函数
根据训练样本 (x1,y1)...(xn,yn) 确定出近似函数 appro_y
近似函数与实际函数中间存在误差，可以找到损失函数 loss
损失值越小，预测越好
这个损失函数就是目标函数
最小二乘法为例
我们的目标就是找到系数值使得目标函数最小
![损失函数](img/img01/loss_fun.png)

- 定位优化方法
使用梯度下降求**极值**（偏导等于），计算出系数
![梯度下降](img/img01/Gradient_descent.png)

### sklearn分类（以水果分类为例）
scikit算法库流程

- 加载数据集
```python 
import numpy as np      # 科学计算库
import matplotlib.pyplot as plt # 可视化函数
import pandas as pd     # 数据分析工具
import seaborn as sns   # 高级可视化工具
from sklearn.model_selection import train_test_split    # 分割数据集

fruit_df = pd.read_table("fruit_data_with_colors.txt")
print(fruit_df.head(3))
fruit_name_dict = dict(zip(fruit_df["fruit_label"], fruit_df["fruit_name"]))
print("-------------")
print(fruit_name_dict)
```
```
# 结果：
   fruit_label fruit_name fruit_subtype  mass  width  height  color_score
0            1      apple  granny_smith   192    8.4     7.3         0.55
1            1      apple  granny_smith   180    8.0     6.8         0.59
2            1      apple  granny_smith   176    7.4     7.2         0.60
-------------
{1: 'apple', 2: 'mandarin', 3: 'orange', 4: 'banana'}
```

- 分割数据集
```python
X = fruit_df[["mass", "width", "height", "color_score"]] # 建立特征矩阵
Y = fruit_df["fruit_label"] # 标签矩阵
# 分割数据集：random_state随机种子保证可复现
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=1/4, random_state=0)

print("数据集总共：{}, 训练集：{}, 测试集：{}".format(
    len(X), len(X_train), len(X_test)
))
# 数据集总共：56, 训练集：42, 测试集：14

# 可视化查看特征变量
sns.pairplot(data=fruit_df, hue="fruit_name", vars=["mass", "width", "height", "color_score"])
plt.show()
```

![](img/img01/fruitdemo1.png)

- 建立模型
```python
from sklearn.neighbors import KNeighborsClassifier  # KNN分类器算法库
knn = KNeighborsClassifier(n_neighbors=5)
```

- 训练模型
```python
knn.fit(X_train, Y_train)
```

- 预测模型
```python
Y_pred = knn.predict(X_test)
print(Y_pred)
# [4 1 1 3 1 1 1 4 4 3 2 1 3 3]

from sklearn.metrics import accuracy_score  # 准确率
acc = accuracy_score(Y_test, Y_pred)
print(acc)
# 准确率0.7142857142857143
```

```python
# 比较k对准确率的影响
k_range = range(1, 20)
acc_score = []

for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, Y_train)
    acc_score.append(knn.score(X_test, Y_test))

plt.figure()
plt.xlabel("k")
plt.ylabel("accuracy")
plt.scatter(k_range, acc_score)
plt.xticks([0,5,10,15,20])
plt.show()
# k = 1,2,3时准确率最大
```
![](img/img01/fruitdemo2.png)


### sklearn 回归（以销售额数据为例）
- 加载数据集
```python 
import csv
import numpy as np      # 科学计算库
import matplotlib.pyplot as plt # 可视化函数
import matplotlib as mpl
import pandas as pd     # 数据分析工具
import seaborn as sns   # 高级可视化工具
from sklearn.model_selection import train_test_split    # 分割数据集
from sklearn.linear_model import LinearRegression

data = pd.read_csv("data.csv")
x = data[["TV", "Radio", "Newspaper"]]
y = data["Sales"]
print(x.head(5))
```
```
# 结果：
      TV  Radio  Newspaper
0  230.1   37.8       69.2
1   44.5   39.3       45.1
2   17.2   45.9       69.3
3  151.5   41.3       58.5
4  180.8   10.8       58.4
```

```python
# 分析数据
mpl.rcParams["font.sans-serif"] = ["simHei"]    # 防止乱码
mpl.rcParams["axes.unicode_minus"] = False
# plot(横轴向量， 纵轴向量)
plt.plot(data["TV"], y, "ro", label="TV")
plt.plot(data["Radio"], y, "g^", label="Radio")
plt.plot(data["Newspaper"], y, "mv", label="Newspaper")
plt.title("线性回归对于多媒体与广告的销售数据", fontsize=16)
plt.legend(loc = "lower right")   # 标签位置
plt.grid()
plt.show()
```
![](img/img01/salesdemo1.png)


- 分割数据集
```python
x_train, x_test, y_train, y_test = train_test_split(x,y,random_state=1)
```

- 建立模型
```python
linreg = LinearRegression()
```

- 训练模型
```python
model = linreg.fit(x_train, y_train)
print("Linereg0 = ", linreg.coef_)
# Linereg0 =  [0.05904274 0.1046685  0.05113963]
print("Linereg截距项 = ", linreg.intercept_)
# Linereg截距项 =  1.005635540428223
# y_pred = 0.06*x1 + 0.105*x2 + 0.05*x3 + 1.01
```

- 预测模型
```python
y_pred = linreg.predict(np.array(x_test))
mse = np.average((y_pred - np.array(y_test))**2) # 平方和损失
rmse = np.sqrt(mse)

print("RMSE = ", rmse)
# RMSE =  1.2930884632246415

t=np.arange(len(x_test))
mpl.rcParams["font.sans-serif"] = ["simHei"]    # 防止乱码
mpl.rcParams["axes.unicode_minus"] = False
plt.plot(t, y_test, "r-", linewidth=2, label="test")
plt.plot(t, y_pred, "g-", linewidth=2, label="predict")
plt.title("线性回归对多媒体与广告额销售数据", fontsize=16)
plt.legend(loc = "upper right")   # 标签位置
plt.grid()
plt.show()
```

![](img/img01/saledemo2.png)



paddlepaddle流程
- 加载库文件
- 预处理数据
- 搭建神经网络
- 配置训练
- 训练模型
- 保存测试文件
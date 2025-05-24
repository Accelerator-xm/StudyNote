"""
水果分类分析
"""

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



X = fruit_df[["mass", "width", "height", "color_score"]] # 建立特征矩阵
Y = fruit_df["fruit_label"] # 标签矩阵
# 分割数据集：random_state随机种子保证可复现
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=1/4, random_state=0)

print("数据集总共：{}, 训练集：{}, 测试集：{}".format(
    len(X), len(X_train), len(X_test)
))

# 可视化查看特征变量
# sns.pairplot(data=fruit_df, hue="fruit_name", vars=["mass", "width", "height", "color_score"])
# plt.show()


from sklearn.neighbors import KNeighborsClassifier  # KNN分类器算法库
knn = KNeighborsClassifier(n_neighbors=5)


knn.fit(X_train, Y_train)

Y_pred = knn.predict(X_test)
print(Y_pred)

from sklearn.metrics import accuracy_score  # 准确率
acc = accuracy_score(Y_test, Y_pred)
print(acc)


# 比较准确率
k_range = range(1, 20)
acc_score = []

for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, Y_train)
    acc_score.append(knn.score(X_test, Y_test))

plt.figure()
plt.xlabel("k")
plt.ylabel("accuracy")
# scatter(横轴向量, 纵轴向量)
plt.scatter(k_range, acc_score)
plt.xticks([0,5,10,15,20])
plt.show()





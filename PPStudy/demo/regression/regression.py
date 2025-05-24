"""
销售额回归
"""

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

# 分析数据
# mpl.rcParams["font.sans-serif"] = ["simHei"]    # 防止乱码
# mpl.rcParams["axes.unicode_minus"] = False
# # plot(横轴向量， 纵轴向量)
# plt.plot(data["TV"], y, "ro", label="TV")
# plt.plot(data["Radio"], y, "g^", label="Radio")
# plt.plot(data["Newspaper"], y, "mv", label="Newspaper")
# plt.title("线性回归对于多媒体与广告的销售数据", fontsize=16)
# plt.legend(loc = "lower right")   # 标签位置
# plt.grid()
# plt.show()


# 分割数据集
x_train, x_test, y_train, y_test = train_test_split(x,y,random_state=1)

linreg = LinearRegression()

linreg.fit(x_train, y_train)
print("Linereg0 = ", linreg.coef_)
print("Linereg截距项 = ", linreg.intercept_)

y_pred = linreg.predict(np.array(x_test))
mse = np.average((y_pred - np.array(y_test))**2) # 平方和损失
rmse = np.sqrt(mse)

print("RMSE = ", rmse)

t=np.arange(len(x_test))
mpl.rcParams["font.sans-serif"] = ["simHei"]    # 防止乱码
mpl.rcParams["axes.unicode_minus"] = False
plt.plot(t, y_test, "r-", linewidth=2, label="test")
plt.plot(t, y_pred, "g-", linewidth=2, label="predict")
plt.title("线性回归对多媒体与广告额销售数据", fontsize=16)
plt.legend(loc = "upper right")   # 标签位置
plt.grid()
plt.show()





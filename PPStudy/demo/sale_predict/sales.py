import os
import paddle
import paddle.nn as nn
from paddle.nn import Linear
import numpy as np
import pandas as pd
import random

# 数据预处理
def load_data():
    ## 加载数据集
    df =  pd.read_csv("PPStudy/demo/sale_predict/BostonHousing.csv")
    print(df[:2])
    features = list(df.columns)
    # print(features)
    datas = df.values
    # print(datas[:2])

    ## 数据形状变化
    ### 已经是矩阵形式了

    ## 数据集划分
    radio = 0.8
    offset = int(datas.shape[0] * radio)
    train_data = datas[:offset]
   
    ### 计算train数据集的最大值，最小值，平均值
    ### axis=0列处理
    maximuns = train_data.max(axis=0)
    minimus = train_data.min(axis=0)
    avgs = train_data.sum(axis=0)/train_data.shape[0]
    # print(maximuns)
    # print(minimus)
    # print(avgs)
    
    global max_values, min_values, avg_values
    max_values = maximuns
    min_values = minimus
    avg_values = avgs

    ## 数据归一化处理  min-max 归一化
    for i in range(len(features)):
        datas[:, i] = (datas[:, i] - minimus[i]) / (maximuns[i] - minimus[i])

    # 训练集和测试及划分  
    train_data = datas[:offset]
    test_data = datas[offset:]

    return train_data, test_data

# train_data, test_data = load_data()
# train_x = train_data[:, :-1]
# train_y = train_data[:, -1]
# print(train_x[0])
# print(train_y[0])


# 搭建神经网络
class Regressor(nn.Layer):
    ## 定义网络层
    def __init__(self):
        super(Regressor, self).__init__()
        ## 定义一层全连接层，输出维度为1，不适用激活函数
        self.fc = Linear(in_features=13, out_features=1)

    ## 前向计算forward
    def forward(self, inputs):
        x  = self.fc(inputs)
        return x
        
# 配置训练
## 声明模型实例
model = Regressor() 
### 开启训练模式
model.train()   
## 加载训练和测试数据
train_data, test_data = load_data()
## 设置优化算法和学习率
### 优化器
opt = paddle.optimizer.SGD(learning_rate=0.01, parameters=model.parameters())


# 模型训练
epoch_num = 10
batch_size = 10

for epoch_id in range(epoch_num):
    ## 数据准备
    ### 打乱训练集
    np.random.shuffle(train_data)
    ### 数据拆分：0-10一组，10-20一组...
    mini_batches = [train_data[k:k+batch_size] for k in range(0, len(train_data), batch_size)]

    for iter_id, mini_batche in enumerate(mini_batches):
        ### 划分特征和标签
        x = np.array(mini_batche[:, :-1]).astype("float32")
        y = np.array(mini_batche[:, -1]).astype("float32")
        ### 转换成动态图
        house_feature = paddle.to_tensor(x)
        prices = paddle.to_tensor(y)

        ## 前向计算
        predict = model(house_feature)

        ## 计算损失
        loss = paddle.nn.functional.mse_loss(predict, label=prices)
        avg_loss= paddle.mean(loss)

        if iter_id%20 == 0:
            print(f"epoch:{epoch_id}, iter:{iter_id}, loss:{avg_loss.numpy()}")

        ## 反向传播: 梯度下降
        avg_loss.backward()
        opt.minimize(avg_loss)  # 最小化loss，更新参数
        model.clear_gradients() # 消除梯度

print("训练完毕-----------------")

# 保存测试模型
## 保存模型
paddle.save(model.state_dict(), "PPStudy/demo/sale_predict/LR_model.pdparams")
print("模型保存成功")

## 推理测试
def load_one_example(data_file):
    df = pd.read_csv(data_file)
    datas = df.values

    ### 选择倒数第10行数据用于测试
    one_data = datas[-10]

    ### 归一化
    for i in range(len(one_data)-1):
        one_data[i] = (one_data[i] - min_values[i]) / (max_values[i] - min_values[i])

    data = np.reshape(np.array(one_data[:-1]), [1,-1]).astype(np.float32)
    label = one_data[-1]
    return data, label

### 加载模型
model_dict = paddle.load("PPStudy/demo/sale_predict/LR_model.pdparams")
model.load_dict(model_dict)
model.eval()    # 预测状态

### 加载测试集
test_data, label = load_one_example("PPStudy/demo/sale_predict/BostonHousing.csv")
test_data = paddle.to_tensor(test_data)
results = model(test_data)

### 反归一化处理
results = results * (max_values[-1] - min_values[-1]) + min_values[-1]
print(f"infer: {results.numpy()}, label:{label}")



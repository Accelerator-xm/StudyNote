# 英语专有名词

## 软件工程与架构
- Software Development Lifecycle (SDLC)：软件开发生命周期，涵盖需求到退役  
- Continuous Integration (CI)：持续集成，高频合并与自动构建  
- Continuous Delivery (CD)：持续交付，随时可发布  
- Continuous Deployment (CD)：持续部署，自动上线生产  
- Infrastructure as Code (IaC)：基础设施即代码，用代码管理环境  
- Application Programming Interface (API)：应用程序接口，系统交互契约  
- Remote Procedure Call (RPC)：远程过程调用，像本地函数调用远端  
- Representational State Transfer (REST)：表现层状态转移，资源导向接口风格  
- GraphQL：GraphQL，声明式查询接口规范  
- gRPC：gRPC，基于 HTTP/2 + Protobuf 的高性能 RPC 框架  
- Event-Driven Architecture (EDA)：事件驱动架构，事件流触发解耦  
- Microservices Architecture (MSA)：微服务架构，按业务边界拆分服务  
- Object-Relational Mapping (ORM)：对象关系映射，面向对象与关系数据桥接  
- CRUD：增删改查，基本数据操作集合  
- ACID：事务四特性，原子性一致性隔离性持久性  
- BASE：基本可用软状态最终一致，分布式弱一致策略  
- CAP Theorem：CAP 定理，一致性可用性分区容错三选二  
- OLTP：联机事务处理，高频小事务场景  
- OLAP：联机分析处理，复杂聚合分析  
- ETL：抽取转换加载，传统数据管道模式  
- ELT：抽取加载转换，先加载后转换模式  
- Serializable：可序列化，将状态转为可存储传输并可恢复格式  
- Non-Serializable：非可序列化，状态无法安全记录复现  
- Finite State Machine (FSM)：有限状态机，状态迁移逻辑模型  
- State Serialization：状态序列化，快照/持久化状态  
- Vector Database：向量数据库，支持相似度检索的存储  
- Vector Similarity：向量相似度，衡量语义接近程度  

## 机器学习与训练范式
- Supervised Learning (SL)：监督学习，有标注训练  
- Unsupervised Learning (UL)：无监督学习，无标签结构发现  
- Semi-Supervised Learning：半监督学习，少量标注结合未标注  
- Self-Supervised Learning：自监督学习，构造预文本任务  
- Contrastive Learning：对比学习，拉近正样本推远负样本  
- Transfer Learning：迁移学习，源任务知识复用  
- Domain Adaptation：领域自适应，跨分布泛化  
- Fine-Tuning：微调，特定任务继续训练  
- Instruction Tuning：指令微调，使模型遵循指令  
- Alignment：对齐，使模型行为符合人类意图价值  
- Reinforcement Learning (RL)：强化学习，试错回报机制  
- Markov Decision Process (MDP)：马尔可夫决策过程，RL 数学框架  
- Backpropagation：反向传播，梯度计算机制  
- Gradient Vanishing / Exploding：梯度消失/爆炸，深层训练难题  
- Optimizer (SGD / Adam)：优化器，参数更新算法  
- Learning Rate Scheduler：学习率调度，动态调整步长  
- Regularization：正则化，抑制过拟合  
- Dropout：随机失活，降低共适应  
- Batch Normalization (BatchNorm)：批归一化，稳定梯度  
- Layer Normalization：层归一化，层内分布稳定  
- Early Stopping：提前停止，防止过拟合  
- Overfitting：过拟合，训练好泛化差  
- Knowledge Distillation：知识蒸馏，大模型向小模型迁移  
- Reinforcement Learning from Human Feedback (RLHF)：人类反馈强化学习，用偏好信号对齐  
- Direct Preference Optimization (DPO)：直接偏好优化，无需 RL 的对齐方法  

## 评估与指标
- Loss Function：损失函数，优化目标度量  
- Cross Entropy：交叉熵，分类常用损失  
- Mean Squared Error (MSE)：均方误差，回归常用损失  
- Precision：准确率，预测为正中正确比例  
- Recall：召回率，正样本被找回比例  
- F1 Score：F1 分数，精确率与召回调和  
- Confusion Matrix：混淆矩阵，分类预测分布  
- ROC Curve：ROC 曲线，TPR 对 FPR 曲线  
- AUC：曲线下面积，分类综合性能  
- Perplexity：困惑度，语言模型平均不确定性  
- Fine-Grained Evaluation：细粒度评估，多维度衡量性能  

## 深度学习结构与表示
- Multilayer Perceptron (MLP)：多层感知机，基础前馈网络  
- Embedding：嵌入，将离散符号向量化  
- Tokenization：分词/切分，将输入拆分为子单位  
- Byte Pair Encoding (BPE)：字节对编码，子词级统计分词  
- SentencePiece：语言无关子词建模工具  
- Latent Space：潜在空间，高维抽象表示  
- Transformer：Transformer，自注意力序列架构  
- Attention Mechanism：注意力机制，计算相关性权重  
- Multi-Head Attention：多头注意力，多个子空间并行关注  
- Positional Encoding：位置编码，注入序列位置信息  
- Residual Connection：残差连接，缓解梯度退化  

## 大模型与推理策略
- Large Language Model (LLM)：大语言模型，大规模参数语言模型  
- Retrieval-Augmented Generation (RAG)：检索增强生成，外部知识结合生成  
- Few-Shot Learning：小样本学习，少量示例条件推理  
- Zero-Shot：零样本，无示例直接推理  
- Prompt Engineering：提示工程，设计输入引导输出  
- Chain of Thought (CoT)：思维链，显式多步推理  
- Tree of Thoughts (ToT)：思维树，分支探索推理  
- Graph of Thoughts (GoT)：思维图，图结构组织推理  
- Self-Consistency：自一致性，多样采样取最一致答案  
- Beam Search：集束搜索，保留前 k 候选  
- Top-k Sampling：Top-k 采样，在最高 k 概率中抽样  
- Top-p (Nucleus) Sampling：核心采样，累积概率阈值内采样  
- Temperature：温度，控制概率分布平滑度  
- Model Context Protocol (MCP)：模型上下文协议，统一上下文交互标准  
- Open Agent Network (OAN)：开放智能体网络，多智能体生态协作  
- Direct Preference Optimization (DPO)：直接偏好优化，无需 RL 的对齐方法

## 图与结构化学习
- Knowledge Graph (KG)：知识图谱，实体与关系网络  
- Graph Neural Networks (GNN)：图神经网络，图结构表示学习  
- Graph Convolutional Network (GCN)：图卷积网络，邻域聚合  
- Graph Auto-Encoder (GAE)：图自编码器，无监督图表示  
- Graph Foundation Model (GFM)：图基础模型，预训练通用图模型  
- Task Dependency Graph (TDG)：任务依赖图，任务拓扑顺序  
- Directed Acyclic Graph (DAG)：有向无环图，无循环依赖结构  

## 问答与检索
- Question Answering (QA)：问答，根据上下文输出答案  
- Retrieval：检索，从库中找到相关信息  
- Embedding Search：向量检索，基于向量相似度搜索 


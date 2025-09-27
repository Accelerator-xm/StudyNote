# 综述阅读

## 基于LLM的代码生成智能体

### 简介

**代码生成**：
  - **定义**: 将用户需求转化为计算机程序
  - **要求**: 语法合法、语义一致、正确运行
  - **意义**: 降低人工编码成本, 提高开发效率, 减少人为错误, 最终达到软件开发自动化
  - **技术局限性**: 上下文理解不足、生成能力有限、通用性和灵活性差
  - **突破**: LLM的出现

**发展**:
  - **程序合成**: 通过形式化**规范**推导出可验证的正确程序
    - 规范化困难
  - **基于深度学习的数据驱动范式**: 将代码生成视为概率序列学习问题
    - 生成的代码功能有限, 包含语法语义错误
  - **LLM**: github庞大的训练数据集, 使模型能够掌握编程语言的语法和语义以及编程算法和范式
    - 缺乏自主分解任务、环境交互、验证纠错能力
  - **基于LLM的代码生成智能体**: 能够自主规划、行动、观察和迭代优化, 模拟人类进行需求分析、代码编写、运行测试、错误诊断和应用修复

**代码生成智能体优势**:
  - **自主性**: 自主管理整个工作流程, 从任务分解到编码调试
  - **扩展任务范围**: 包含完整的软件开发生命周期(SDLC)
  - **实用性**: 工程级代码生成, 系统可靠性、过程管理、工具集成等


### 基础知识

#### LLM 核心特性

**架构**: 以Transformer为核心，通过海量文本预训练学习语言模式

**代码生成领域**: 大量开源代码作为训练数据, 可掌握多语言语法、编程范式, 展示了强大的代码生成和理解能力
  - 代表模型CodeX、CodeLlama、DeepSeek-Coder、Qwen2.5-Coder等
  - 应用于代码补全、测试代码生成、bug修复等全软件开发生命周期

**关键emergent能力**: 规划能力、工具使用能力、环境交互能力. 

#### LLM-based 智能体

<div align="center">
<img src="img/A_Survey_on_Code_Generation_with_LLM-based_Agents/1.png" alt="基于LLM的代码生成智能体演变" width="400">
</div>

以LLM为核心推理引擎，集成了感知、记忆、决策和动作模块

**核心组件**:
   - **规划**: 分解复杂任务
   - **记忆**: 短期记忆(LLM上下文窗口)、长期窗口(RAG + 向量数据库)
   - **工具使用**: 调用外部工具(编译器、搜索引擎等)
   - **反思**: 检查评估并修正自身输出



**LLM 与 LLM-based 智能体的核心差异**:
| 对比维度 | LLM | LLM-based 代码生成智能体 |
|----------------|------------------------------|-----------------------------------------|
| 工作模式 | 单轮被动响应（输入→输出） | 动态自主 workflow（规划→执行→观察→调整）|
| 核心能力 | 上下文生成能力 | 任务分解、工具调用、反思自修正能力 |
| 适用场景 | 简单代码片段生成（函数补全） | 复杂 SDLC 任务（多文件开发、动态调试） |
| 与环境交互 | 无交互 | 可与开发环境（终端、编辑器）持续交互 |

### 关键技术

#### 单智能体代码生成

<div align="center">
<img src="img/A_Survey_on_Code_Generation_with_LLM-based_Agents/2_1.png" alt="单智能体代码生成" width="300">
</div>

**规划与推理技术**:
<div align="center">
<img src="img/A_Survey_on_Code_Generation_with_LLM-based_Agents/2_2.png" alt="规划与推理技术" width="500">
</div>

单路径规划 -> 多路径并行推理
线性规划 -> 结构化规划

  - **单路径规划**: 
    - Self-Planning: 首个引入**规划阶段**，先出步骤再生成代码
    - CodeChain: 在规划阶段引入**聚类**和**自修订**, 构建可重用的模块化代码
    - CodeAct: 引入**统一动作空间**, 将动作转化为python代码, 集成Python解释器, 可以立即执行代码, 实时反馈挑调整
    - KareCoder: 融入**专业知识库**（如编程库、学科文献库等）, 注入外部知识
    - WebAgent: 规划机制应用到web自动化场景, 指令分解、HTML内容总结、程序生成
    - CodePlan: 引入**多阶段控制流**和**自定义控制指令**, 推理时动态选择生成或者修改

  - **多路径探索**: 
    - GIF-MCTS: 引入**蒙特卡洛树搜索**, 多路径评分筛选
    - PlanSearch: 首次将规划过程形式化为搜索任务, 并行评估候选计划

  - **结构化规划**: 
    - CodeTree/Tree-of-Code: 将线性规划转为**树结构**, 结合执行反馈剪枝
    - DARS: 采用**多阶段控制**, 引入**分层目标**和**中间奖励信号**, 缓解端到端生成的**目标偏移**问题. 自适应树结构, 关键节点分支新的规划路径, 动态调整规划路径
    - VerilogCoder: 硬件任务中引入基于**抽象语法树**的图结构规划机制和波形跟踪工具, 展示了规划范式在**跨模态**和特定任务中的自适应潜力
    - Guided Search: 提出**一步前瞻one-step lookahead**和**轨迹选择trajectory selection**策略, 解决传统搜索方法难以在**非序列化环境**中应用的挑战
      - 一步前瞻: 提前预测下一步动作
      - 轨迹选择: 根据过去成功过的路径选更有效的

**工具集成与检索增强**:
<div align="center">
<img src="img/A_Survey_on_Code_Generation_with_LLM-based_Agents/2_3.png" alt="工具集成与检索增强" width="500">
</div>

  - **工具集成**:
    - ToolCoder: 集成**API搜索工具**, 缓解模型**幻觉**导致API调用错误
    - ToolGen: 集成**自动补全工具**, 解决代码生成中的**依赖问题**, 例如变量未定义、成员错误等
    - CodeAgent: 进一步增强**复杂需求**和**复杂依赖关系**, 集成5类编程工具(**网站搜索**、**文档阅读**、**代码符号导航**、**格式检擦器**、**代码解释器**), 支持信息检索、代码生成与测试
    - ROCODE: 工具**反馈机制**方面, 引入**闭环机制**(生成 -> 错误检测 -> 自适应回溯), 结合静态分析定位修改范围
    - CodeTool：增强对工具调用的**逐步控制**, 引入**过程级监督机制**, 监督工具调用步骤, 提高工具调用的准确性和鲁棒性

  - **检索增强(RAG)**
    - RepoHyper: **仓库级向量检索**, 定位可复用代码片段, 提升对**长距离依赖**的把控能力
    - CodeNav: 根据需求检索**真实存储库**, 导入相关函数和代码块, 解决依赖需**预注册**工具问题
    - AUTOPATCH: 应用于**运行时性能优化**问题, 将历史代码示例与控制流图(CFG)分析相结合, 进行上下文感知学习, 通过上下文提示模型优化代码
    - Knowledge Graph Based Repository-Level Code
Generation: 将代码库表示为**知识图谱**, 提高检索上下文的结构化表达能力, 项目级生成任务准确率提升**10%+**
    - cAST: 基于抽象语法树(AST)的**结构化分块**, 提升代码检索的Recall与Pass@1等指标

  
**反思与自改进**: 模仿开发过程的生成、评估、修改过程
<div align="center">
<img src="img/A_Survey_on_Code_Generation_with_LLM-based_Agents/2_4.png" alt="反思与自改进" width="500">
</div>

自然语言层面的自我反馈 -> 结合执行结果的自动修复 -> 基于程序结构和多解评估的模块级优化

  - **文本级反思**: 
    - Self-Refine: 自然语言自评 -> 迭代修订, 无需额外训练
    - Self-Iteration: 角色分工+结构化迭代框架, 解决**误差累积问题**
    - Self-Debug: 逐行解释定位错误

  - **执行反馈驱动**: 
    - Self-Edit: 结合执行反馈二次编辑代码
    - Self-Repair: 代码模型+反馈模型, 基于测试失败生成修复解释

  - **模块化优化**: 
    - CodeChain: 引入模块化的**自修订框架**, 聚类代表性子模块, 复用经过验证的组件
    - LeDeX: 增强**闭环自调试框架**, 分步标注错误代码, 生成修复方案并收集数据集微调

#### 多智能体代码生成

<div align="center">
<img src="img/A_Survey_on_Code_Generation_with_LLM-based_Agents/3_1.png" alt="多智能体代码生成" width="300">
</div>

**多智能体工作流**
<div align="center">
<img src="img/A_Survey_on_Code_Generation_with_LLM-based_Agents/3_2.png" alt="多智能体工作流" width="500">
</div>

  - **Pipeline分工**: 按照SDLC阶段拆分任务, 结构清晰但**串行**依赖
    - Self-Collaboration: **基于瀑布模型**, 需求分析→编码→测试
    - AgentCoder: 程序员→测试设计者→测试执行者
    - CodePori: 引入一组智能体, 包括管理者、开发人员、优化人员、测试人员
      - 管理员: 需求分析、分解任务
      - 开发人员: 多个智能体并行协作, 编写不同模块的代码
      - 优化人员: 多个智能体细化代码
      - 测试人员: 执行集成测试
    - MAGIS: 聚焦**仓库维护**类任务, 包含项目经理、维护人员、开发人员和质量保障人员, 完成github Issue跟踪、分配与修复
    - HyperAgent: 专注于**跨语言**、**跨任务**的代码生成, 包含规划者、导航者、代码编辑器、执行器, 同时引入自动工具链检索机制

  - **分层规划-执行**: 高智能体规划、低智能体执行
    - PairCoder: Navigator 规划 + Driver 实现
    - FlowGen: 模拟瀑布/TDD等软件工程模型，阶段性规划和目标验证
    - SoA: 引入**动态智能体调度**机制, 动态扩展或收缩智能体数量
    - MAGE: 高级目标分解为微操作并将其分配给不同的智能体

  - **自协商循环优化**：多轮交互改进
    - MapCoder: 四智能体循环, 回忆→规划→生成→调试
    - AutoSafeCoder: 编码器、静态安全检测器(静态安全检测)、模糊测试器(动态安全检测)
    - QualityFlow: 生成单元测试 → 检查单元测试合理性 → 执行测试
    - CodeCoR: 引入**自我反思**评分机制, 反思智能体评分定位问题，反馈优化
    - MARCO: 代码生成智能体+性能评估智能体, 不断优化生成的代码性能

  - **自进化结构**：自发、动态调整系统结构
    - SEW: 基于协作效果重组通信路径和职责划分
    - EvoMAC: **文本反向传播**机制, 调整协作策略

  - **角色分工**：通过 Prompt 设定角色
    - ChatDev: 程序员、评审员、测试员
    - MetaGPT: 模拟软件公司组织架构

**上下文管理与记忆技术**
<div align="center">
<img src="img/A_Survey_on_Code_Generation_with_LLM-based_Agents/3_3.png" alt="上下文管理与记忆技术" width="500">
</div>

  - Self-Collaboration：首次引入**黑板模型**，基于**共享视图得到协作流**，建立共享内存空间存储任务描述、中间结果等，所有智能体可读写
  - L2MAC：基于**类冯・诺依曼架构**，设计指令寄存器与文件存储模块，突破 LLM 上下文窗口限制，支持多文件生成
  - Cogito：基于**类脑机制**，分为短期记忆（任务状态）、长期知识库（通用知识）、进化增长单元（抽象能力提升），具备自学习能力
  - SoA：引入**自组织内存**，根据任务复杂度动态扩展智能体池，中央控制器保持各智能体上下文对齐，支持大规模代码库生成
  - GameGPT: 采用**双协同**机制，减少冗余的语句重传
  - CleanAgent: 基于 Dataprep.Clean 库构建了一个**声明式 API 记忆模块**，从历史调用轨迹中提取并重用领域知识

**协同优化**
<div align="center">
<img src="img/A_Survey_on_Code_Generation_with_LLM-based_Agents/3_4.png" alt="协同优化" width="500">
</div>

  - Lingma SWEGPT：分三阶段（代码库理解→故障定位→补丁生成），收集多智能体行为数据，通过监督微调优化协同
  - CodeCoR：四智能体（prompt / 代码 / 测试 / 修复）互评估，剪枝低质量输出，迭代提升协同质量
  - SyncMind：解决**状态偏移**问题，通过多维度评估实现失步恢复
  - CANDOR：采用**小组讨论策略**，要求多个审稿人智能体达成共识，再生成

### 应用

- 自动化代码生成与实现
  - 函数级代码生成：Self-Planning、LATS、Lemur、CodeChain、MapCoder、FlowGen、PairCoder、CodeTree、CodeCoR、QualityFlow、CodeSim、DARS、SEW
  - 代码库级代码生成：Self-Collaboration、ChatDev、Webagent、MetaGPT、CodePlan、CoAgents、GamePoW、GameGPT、SoA、ToolGen、AgileCoder、AgileAgent
- 自动化调试与程序修复：Self-Refine、Self-Debug、Self-Edit、Self-Repair、RepairAgent、AutoCodeRover、SWEx-Agent、OrcaLog、PatchPlot、Thinking-Longer、HyperAgent、FixIt、MetaS、AutoSafeCoder、SOLverlntentAgent、Nemorron-CORTEXA
- 自动化测试代码生成
  - 自动化测试用例生成：TestPilot、CANDOR、XUAT-Copilot、LogiAgent、SeedMind、ACH
  - 自动化执行与分析：AUTestAgent、HEPH
- 自动化代码重构与优化
  - 结构化代码重构：DataClump-Pipeline、iSMELL、EM-assist、HaskellAgent
  - 代码性能优化：AIDE、MARCO、LASSI-EE、SysLLMatic
- 自动化需求澄清：MARE、ClarifyGPT、TiCoder、SpecFix、interAgent、HLDe


### 挑战
- 核心能力局限：
  - 缺乏结构化领域知识
  - 意图理解和上下文感知能力不足
  - 跨文件关联理解不足
  - 多模态理解能力不足，无法理解 UI 草图 / 架构图
- 系统鲁棒性：
  - 多智能体**错误级联**：上游错误放大
  - 智能体协调复杂度：交互**指数增长**
  - 知识更新：无法持续学习项目特定标准，**易过时**
- 人机交互与成本：
  - 模型**幻觉**导致可靠性不足
  - 灵活性和安全性问题
  - 高运营成本：多轮交互导致计算 / 时间**开销大**
- 评估与范式：
  - 评估体系不完整
  - 软件开发范式转型：需支持 “软件即服务”，用户仅提供意图



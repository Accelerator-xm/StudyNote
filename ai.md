# 大模型学习

## 私有大模型部署和调参
- 基本概念
    - 提示工程prompt：提问方式
    - RAG：补充知识库
    - 微调：调参数
    - token：一个词，例如“人”、“工”
    - 向量数据库：存每个token对应的向量，管理向量的关系 faiss
    - embeddings：词向量化
    - langchain：用于开发由语言模型驱动的应用程序的框架

- RAG：让模型更聪明
    
    个人、企业知识库（文本）--> split成片段（段落） --> embeddings成向量存入向量数据库
    
    用户提问 --> 向量数据库匹配出TopN个结果（段落） --> 段落+问题 组合成prompt --> 大模型进行推理

- 大模型微调
    - 全参微调：模型遗忘问题，约等于训练一个新模型
    - 低参微调：节约内存、减少训练时间


## AI框架
### langchain

类似于数据库领域的jdbc：作为连接和集成不同系统的桥梁

- 组成
    - 组件components：为LLMs提供接口封装，模板提示和信息检索索引
    - 链chain：组合不同的组件解决特定问题，如在大量文本中查找信息
    - 代理agents：使LLMs能与外部进行交互，如通过API请求执行操作

- 核心
    - models：提供包装器连接大语言模型，可以自由切换模型
    - prompt templates：避免硬编码文本输入，动态的将用户输入插入模板，并发送给语言模型
    - chains：组个各个组件解决特定任务
    - agent：与外部api交互
    - embeddings：嵌入与向量存储 VectorStore 是数据表示和检索的手段，为模型提供必要的语言理解基础
    - indexes：从语言模型中提取相关信息

- 优点：
    - 数据连接：允许将大模型连接到你自己的数据源，比如数据库、pdf文件或其他文档
    - 行动执行：不仅可以提取信息，还可以根据信息执行特定操作，如发邮件

- LangSmith：

    提供调试、测试、评估和监控基于任何LLM框架构建的链和智能代理的功能，与langchain无缝集成

- 使用流程

    创建模型 --> 准备prompt --> 创建返回数据的解析器 --> 得到链 --> 使用chain调用

```python
# 创建模型
model = ChatDashScope(model='qwen-turbo', dashscope_api_key=my_dashscope_api_key)

# 创建返回数据的解析器
parser = StrOutputParser()

# 定义提示模板
prompt_template = ChatPromptTemplate.from_messages([
    ('system', '请将下面内容翻译成{language}'),
    ('user', '{text}')
])

# 得到链
chain = prompt_template | model | parser

# 使用chain调用
# 准备prompt
# msg = [
#     SystemMessage(content = '请将下列内容翻译成English'),
#     HumanMessage(content = '你好')
# ]
# result = model.invoke(msg)  +  res_str = parser.invoke(result)
print(chain.invoke({'language':'English',
                    'text':'你好,请问要去哪里'
                    }))
```

    历史+流式输出

```python
# 定义提示模板
prompt_template = ChatPromptTemplate.from_messages([
    ('system', '你是一个乐于助人的助手，用{language}尽你所你回答所有问题'),
    MessagesPlaceholder(variable_name='my_msg')
])

# 得到链
chain = prompt_template | model

# 保存历史聊天记录
store = {}      # key: sessionId  vakue: 历史聊天记录

def get_session_history(session_id: str):
    if session_id not in store:
        # ChatMessageHistory记录历史数据
        store[session_id] = ChatMessageHistory()

    return store[session_id]


do_message = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="my_msg" #每次聊天发送消息的key
)

config = {'configurable': {'session_id': 'zs123'}}

# 流式输出，一个token一个token输出
for res in do_message.stream(
    {
        'my_msg': [HumanMessage(content="请给我讲一个笑话")],
        'language': '中文'
    },
    config = config
):
    print(res.content, end='-')
```


- langserve：

    部署应用程序，封装成api

```python
# 创建 fastapi
app = FastAPI(title="我的服务", version='v1.0', description="翻译工具")

add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

    # post请求：http://127.0.0.1:8000/chain/invoke
    # 请求体json：
    # {
    #     "input":{
    #         "language":"English",
    #         "text":"你好请问要去哪里"
    #     }
    # }
```

```python
# 客户端部分
if __name__ == "__main__":
    client = RemoteRunnable("http://127.0.0.1:8000/chain/")
    print(client.invoke({
        "language":"日语",
        "text":"你好"
    }))
```


- 构建向量数据库和检索器

    支持从向量数据库和其他来源检索数据

```python
# 准备测试数据集
documents = [
    Document(
        page_content="肺炎患病概率为0.06%，无特发人群，无传染性",
        metadata={"source": "肺炎内容文档"}
    )
    # ......
]

# 加载embedding模型
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 实例化向量数空间
vector_store = Chroma.from_documents(documents, embedding=embedding_model)
# 相似度查询: 分数越低相似度越高
# print(vector_store.similarity_search_with_score('治疗'))

# 检索器
# bind(k=1)选取相似度最高的一个
retriever = RunnableLambda(vector_store.similarity_search).bind(k=1)
# 相似度查询
# print(retriever.batch(['治疗', '症状']))

# 提示模板
message = """
使用提供的上下文仅回答这个问题。
{question}
上下文：
{context}
"""

prompt_temp = ChatPromptTemplate.from_messages([
    ('human', message)
])

# 创建模型
model = ChatDashScope(model='qwen-turbo', dashscope_api_key=my_dashscope_api_key)

# RunnablePassthrough()允许将用户的问题之后再传递给prompt和model
chain = {'question': RunnablePassthrough(), 'context': retriever} | prompt_temp | model

res = chain.invoke('请谈谈肺炎怎么治疗')

print(res)
```

- 构建代理Agent

    使用大语言模型作为推理引擎来确定要执行的操作以及这些操作的输入应该是什么

    大模型绑定工具，推理时如果单靠大模型不能完成，则大模型会使用工具
```python
# 单靠大模型不能完成
res = model.invoke([HumanMessage(content="武汉今天天气怎么样")])
print(res)  # content='抱歉，我无法提供实时的天气信息。

# Tavily搜索工具
search = TavilySearchResults(max_results = 2)   # max_results返回结果数
# print( search.invoke("武汉的天气怎么样") )    # 搜索

tools = [search]
# 模型绑定工具
# model_with_tool = model.bind_tools(tools)

# model_with_tool可以智能选择是否需要工具
# res = model_with_tool.invoke([HumanMessage(content="武汉今天天气怎么样")])
# print(f'model: {res.content}')    # 空
# print(f'tools: {res.tool_calls}') # 搜索结果

# 创建代理
agent_executor = chat_agent_executor.create_tool_calling_executor(model, tools)

# res包含三个对象
# HumanMessage：用户提示
# AIMessage：ai推理结果，如果为空则使用工具
# ToolMessage：使用工具获取的结果
res = agent_executor.invoke({
    'messages': [HumanMessage(content="武汉今天天气怎么样")]
})
print(res['messages'][2].content)
```

### RAG对话应用
- 基本概念

    增强型的大语言模型知识方法，通过引入额外数据来实现

- 实现思路：
    - 加载：爬虫，通过DocumentLoaders
    - 分割：Text splitters将大型文档分割成更小的块，便于处理
    - 存储：使用VectorStore和Embedding完成
    - 检索：通过检索器从存储中检索相关分割
    - 生成：CharModel/LLM使用“问题+检索的数据生成答案”

- 注意
    - 历史记录：需要包括 问答记录 和 查询检索器的上下文
    - 实现：添加子链，采用最新用户问题和聊天历史，并在引用历史信息中的任何信息时重新表述问题。简单认为是新的“历史感知”检索器，将检索过程融入了对话上下文

```python
# 加载数据：本地数据库、本地word文档等
# 一篇博客为例
loader = WebBaseLoader(
    web_path=['https://lilianweng.github.io/posts/2023-06-23-agent/'],
    bs_kwargs=dict(
        parse_only = bs4.SoupStrainer(class_=('post-header', 'post-title', 'post-content'))
    )
)

docs = loader.load()

# 分割
# 分割器：chunk_size分割大小，chunk_overlap重叠大小
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

splits = splitter.split_documents(docs)

# 存储
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 实例化向量数空间
vector_store = Chroma.from_documents(documents=splits, embedding=embedding_model)

# 检索器
retriever = vector_store.as_retriever()

# 整合
# 提示模板
system_prompt = """
你是一个专门做问答任务的助手。
使用下面检索器检索出的内容去回答问题。
如果你不知道答案，你说“我不知道”。
如果你知道答案就用不超过三句话回答，保证回答简洁。\n
{context}
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),  # 历史记录
        ("human", "{input}")
    ]
)

# 创建链
chain1 = create_stuff_documents_chain(model, prompt)

# 创建子链
# 子链的提示模板
contextualize_q_system_prompt = """
给一个聊天记录和可能引用聊天历史中上下文的最近的用户的问题，
生成在没有聊天历史的情况下可以理解的独立问题，不要回答这个问题，
只是在需要的时候重新表述它，否则就按原样返回
"""

retriever_history_temp = ChatPromptTemplate.from_messages(
    [
        ('system', contextualize_q_system_prompt),
        MessagesPlaceholder('chat_history'),
        ("human", "{input}")
    ]
)

# 子链
history_chain = create_history_aware_retriever(model, retriever, retriever_history_temp)

# 保存历史聊天记录
store = {}      # key: sessionId  vakue: 历史聊天记录

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()

    return store[session_id]

# 创建一个父链
chain = create_retrieval_chain(history_chain, chain1)

result_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key='input',
    history_messages_key='chat_history',
    output_messages_key='answer'
)

# 第一轮对话
res1 = result_chain.invoke(
    {'input':'什么是任务拆解'},
    config={'configurable': {'session_id': 'zs123456'}}
)
print(res1['answer'])

# 第二轮对话
res1 = result_chain.invoke(
    {'input':'它有哪些常用的方法'},
    config={'configurable': {'session_id': 'zs123456'}}
)
print(res1['answer'])
```

### langchain读取数据库

基于数据库数据的问答

使用chain和agents实现：通过查询数据库中的数据并得到自然语言答案。代理可以根据需要多次查询数据库

- 实现：
    - 将问题转换成DSL查询：模型将用户输入转换成SQL查询
    - 执行SQL查询：执行查询
    - 回答问题：模型使用查询结果响应用户输入

使用链完成数据库查询
```python
# 连接数据库 sqlalchemy
# 初始化mysql数据库连接
MYSQL_URI = 'mysql+pymysql://root:'+ my_api_key.Mysql_Password + '@localhost:3306/web?charset=utf8mb4'
db = SQLDatabase.from_uri(MYSQL_URI)

# 定义模板
answer_prompt = PromptTemplate.from_template(
    """
    给定以下用户问题、可能的SQL语句和SQL执行后的结果，回答用户问题。
    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    回答:
    """
)

# 初始化生成SQL语句的链
create_sql_chain = create_sql_query_chain(model, db)
# 创建执行sql语句的工具
execute_sql_tool = QuerySQLDatabaseTool(db=db)

# 1、生成sql  2、执行sql 
# 3、提示模板  
chain = (
    RunnablePassthrough
    .assign(query=create_sql_chain)
    .assign(result=itemgetter("query") | execute_sql_tool) # 执行sql语句
    | answer_prompt
    | model
    | StrOutputParser()
)

res = chain.invoke({"question": "请问用户表有多少数据"})
print(res)  # 返回结果
```

使用代理完成数据库查询
```python
# 初始化mysql数据库连接
MYSQL_URI = 'mysql+pymysql://root:'+ my_api_key.Mysql_Password + '@localhost:3306/web?charset=utf8mb4'
db = SQLDatabase.from_uri(MYSQL_URI)

# 创建工具
toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()

prompt = ChatPromptTemplate.from_messages([
    ("system", """
        你是一个被设计用来与SQL数据库交互的代理。
        给定一个输入问题，创建一个正确的SQL语句并执行，然后查看结果并返回答案。
        除非用户指定了他们想要获取的示例的具体数量，否则始终将SQL查询限制为10个结果。
        你可以按相关列对结果进行排序，以返回MySQL数据库中最匹配的数据。
        你可以使用与数据库交互的工具。在执行查询之前，你必须仔细检查。
        
        不要对数据库做任何修改（不要做DML语句）。
        首先，你应该查看数据库中的表，不要凭空猜表名，务必调用工具获取，不要跳过这一步。
        然后查询最相关的表的模式。
        当你已经获得了正确结果，并生成了自然语言回答，就可以结束对话，不要继续调用工具。
     """
     ),
    ("human", "{messages}")
])

# 创建代理
agent_executor = chat_agent_executor.create_tool_calling_executor(model=model, tools=tools, prompt=prompt)

res = agent_executor.invoke({"messages": "请问联系人里哪个省份人最多"})

print(res['messages'][-1])
```





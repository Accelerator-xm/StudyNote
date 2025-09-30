# 大模型应用学习

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

### langchain检索YouTube视频字幕

- youtube-transcript-api pytube
    - 获取视频字幕的接口
    - 数据抓取：利用公开接口，能够搜索到视频的元数据
    - 字幕提取：如果视频有内置字幕，该API可以下载

- yt_dlp
    - 用 yt_dlp 替代 pytube 来抓取 YouTube 视频信息（比如标题、发布日期、字幕等），是个更稳定的方案。
    - 但这就需要自定义 Loader。

- HTTP Error 429: Too Many Requests
    - 向 YouTube 发了太多请求（可能是批量下载、频繁调用等），所以 YouTube 认为你是爬虫，临时拒绝你的访问。
    - 使用 --cookies-from-browser 或 --cookies

- 用浏览器 cookies（推荐）
    - 安装 Get cookies.txt
    - 打开你已登录 YouTube 的浏览器页面，导出 cookies.txt。

使用yt_dlp爬取YouTube字幕

```python
COOKIE_FILE = "your_cookies.txt"

def get_video_id(url: str) -> str | None:
    m = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11})", url)
    return m.group(1) if m else None

def load_youtube_video(url: str):
    video_id = get_video_id(url)
    if not video_id:
        raise ValueError("URL 无法解析到视频 ID")

    # ① 先取元数据
    ydl_opts = {
        "quiet": True,
        "cookiefile": COOKIE_FILE,
        "sleep_interval": 1,
        "max_sleep_interval": 3,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # ② 取字幕 —— 把 cookie 也传进去，并做退避
    for _ in range(4):                       # 最多 4 次指数退避
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=['zh-Hans', 'zh-Hant', 'en'],
                cookies=COOKIE_FILE          # ← 关键：同一份 cookie
            )
            break
        except TranscriptsDisabled:
            print(f"该视频无字幕: {url}")
            return []
        except Exception as e:               # 429、IP 被封等
            wait = random.uniform(2, 6)
            print(f"取字幕失败：{e}，{wait:.1f}s 后重试…")
            time.sleep(wait)
    else:
        raise RuntimeError("重试后仍无法获取字幕")

    full_text = "\n".join(seg['text'] for seg in transcript)

    publish_date = info.get('upload_date')   # '20240312'
    publish_date = (datetime.datetime.strptime(publish_date, '%Y%m%d')
                    .isoformat() if publish_date else 'Unknown')
    metadata = {
        "title": info.get('title', 'Unknown'),
        "channel": info.get('channel', 'Unknown'),
        "publish_date": publish_date,
        "video_id": video_id,
        "url": url,
    }
    return [Document(page_content=full_text, metadata=metadata)]
```

持久化存储向量数据库

```python
persist_dir = 'LangchainDemo/demo8/chroma_data_dir' # 存放向量数据库的目录

# 初始化一些youtube视频
urls = [
    "https://www.youtube.com/watch?v=HAn9vnJy6S4",
    "https://www.youtube.com/watch?v=dA1cHGACXCo",
    "https://www.youtube.com/watch?v=ZcEMLz27sL4",
    "https://www.youtube.com/watch?v=hvAPnpSfSGo",
    "https://www.youtube.com/watch?v=EhlPDL4QrWY",
    "https://www.youtube.com/watch?v=mmBo8nlu2j0",
]

# socument数组
docs = []
for url in urls:
    try:
        # 一个视频一个document
        print(f"正在加载：{url}")
        docs.extend(load_youtube_video(url))
    except Exception as e:
        print(f"加载失败：{url}")
        print(e)

print(len(docs))

# 给doc添加额外的元数据：视频发布的年份
for doc in docs:
    doc.metadata['publish_year'] = datetime.datetime.strptime(
        doc.metadata['publish_date'],
        '%Y-%m-%dT%H:%M:%S'
    ).year

print(docs[0].metadata)

# 根据多个doc构建向量数据库
# 分割器：chunk_size分割大小，chunk_overlap重叠大小
splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=30)
split_docs = splitter.split_documents(docs)

# 存储
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 向量数数据库持久化
# 持久化 persist_directory=persist_dir
vector_store = Chroma.from_documents(documents=split_docs, embedding=embedding_model, persist_directory=persist_dir)
```

加载数据库并进行智能化检索
```python
persist_dir = 'LangchainDemo/demo8/chroma_data_dir' # 存放向量数据库的目录

# 存储模型
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 加载向量数据库
vector_store = Chroma(persist_directory=persist_dir, embedding_function=embedding_model)

# 定义提示词模板
# 防止模型自动脑补无关信息：If no year is mentioned, leave `publish_year` as null.
system_message = """"
    You are an expert at translating user questions into database queries.
    You have access to a database of tutorial videos on software libraries for building LLM-driven applications.
    Given a question, generate a list of database queries to optimize to retrieve the most relevant results.
    If there are abbreviations or words you are not familiar with, don't try to change them.
    If no year is mentioned, leave `publish_year` as null.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ('system', system_message),
        ('human','{question}')
    ]
)

# pydantic 数据管理的库
class Search(BaseModel):
    """
    定义了数据模型
    """
    # 内容的相似性 发布年份
    query: str = Field(None, description="Similarity search query applied to video transcripts")
    publish_year: Optional[int] = Field(None, description="year video was published")

chain = {'question': RunnablePassthrough()} | prompt | model.with_structured_output(Search)

def retrieval(search: Search) -> List[Document]:
    """
    检索函数
    """

    _filter = None
    if search.publish_year:
        # 如果年份不为空，则进行检索
        # $eq是Chroma的查询语法
        _filter = {'publish_year': {'$eq': search.publish_year}}
    
    return vector_store.similarity_search(search.query, filter=_filter)

new_chain = chain | retrieval

# 根据问题进行检索
# res3 = new_chain.invoke("videos on RAG published in 2024")
res3 = new_chain.invoke("RAG tutorial")
print([(doc.metadata['title'], doc.metadata['publish_year']) for doc in res3])
```

### 提取结构化的数据

    从非结构化的文本中提取结构化信息。
    在自然语言处理(NLP)中，表格数据抽取是一个重要的任务，涉及从文本中提取结构化数据

```python
# 定义数据模型
class Person(BaseModel):
    """
    关于一个人的数据模型
    """
    name: Optional[str] = Field(default=None, description="表示人的名字")

    hair_color: Optional[str] = Field(
        default=None, description="如果知道的话，这个人的头发颜色"
    )

    height_in_meters: Optional[str] = Field(
        default=None, description="这个人的身高（米）"
    )


# 用于获取多个数据
class ManyPerson(BaseModel):
    """
    关于多个人的数据模型
    """
    people: List[Person] = Field(
        default=[], description="一个人列表"
    )


# 提示模板
prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            "你是一个专业的提取算法"
            "只从未结构化文本中提取相关信息"
            "如果你不知道要提取的属性值"
            "返回该属性的值未null",
        ),
        # 如果需要参考对话上下文，则加上
        # MessagesPlaceholder(variable_name="history")
        ('human', "{text}"),
    ]
)

chain = {'text': RunnablePassthrough()} | prompt | model.with_structured_output(schema=ManyPerson)

text = """
    马路上走来一个女生，长长的黑头发披在肩上，大概1米7左右.
    走在她旁边的是她的男朋友，叫张三，比他高10厘米。
"""
res = chain.invoke(text)
print(res)
```

### AI自动生成数据

    合成数据是人工生成的数据，用于模拟真实数据，不会泄露隐私或遇到现实世界的限制
    pip install langchain_experimental

- 优势
    - 隐私安全：非真是个人数据
    - 数据增强：扩展机器学习的数据集
    - 灵活性：创建特定或罕见的场景
    - 成本效益：通常比现实世界数据收集更便宜
    - 监管合规：
    - 模型鲁棒性：可以带来更好的泛化AI模型
    - 快速原型设计：无需真实数据即可快速测试
    - 控制实验：模拟特定条件
    - 数据访问：当数据不可用时的替代方案


langchain_experimental 初试：

```python
# 创建链
chain = create_data_generation_chain(model)

res = chain.invoke(
    {
        'fields':['蓝色', '红色', '绿色'],    #关键词
        'preferences': {'style': '像诗歌一样'} # 偏好，话题
    }
)
print(res)
# """
# 在蓝色的梦之海与红色的烈焰山之间，  
# 绿色的希望之树静静生长，  
# 色彩交织成诗，绘出世界的秘密。
# """
```

生成结构化数据
```python
# 1 定义数据模型
class MedicalBilling(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    patient_id: str = Field(description="患者ID")
    patient_name: str = Field(description="患者姓名")
    diagnosis_code: str = Field(description="诊断代码")
    procedure_code: str = Field(description="手术代码")
    total_cost: float = Field(description="总费用")
    insurance_claim_amount: float = Field(description="保险索赔金额")


# 2 提供样例数据
examples = [
    {
        "example": """
        {{
            "patient_id": "P001",
            "patient_name": "张三",
            "diagnosis_code": "D001",
            "procedure_code": "PR001",
            "total_cost": 1500.0,
            "insurance_claim_amount": 1200.0
        }}
        """
    },
    {
        "example": """
        {{
            "patient_id": "P002",
            "patient_name": "王五",
            "diagnosis_code": "D002",
            "procedure_code": "PR002",
            "total_cost": 2000.0,
            "insurance_claim_amount": 1800.0
        }}
        """
    }
]

# 3 创建提示模板
example_template = PromptTemplate(
    input_variables=["example"],template='{example}'
)


PREFIX = """你是一个医疗数据生成器，请生成符合以下格式的结构化账单数据。
字段包括：patient_id、patient_name、diagnosis_code、procedure_code、total_cost、insurance_claim_amount。
以下是几个示例数据："""

SUFFIX = """
请根据以下指令生成类似结构的 JSON 数据（一次只生成**1**条）：
主题: {subject}
补充要求: {extra}

严格要求：
1. 必须输出单个 JSON 对象（不是数组）。
2. JSON 放在 ```json ... ``` 代码块中。
3. 代码块前后不得有任何额外文字。
"""

prompt_template = FewShotPromptTemplate(
    prefix=PREFIX,
    suffix=SUFFIX,
    examples=examples,
    example_prompt=example_template,
    input_variables=["subject", "extra"],
)

raw_parser = PydanticOutputParser(pydantic_object=MedicalBilling)
parser = OutputFixingParser.from_llm(parser=raw_parser, llm=model)

# 4 创建结构化数据生成器
generator = create_openai_data_generator(
    output_schema=MedicalBilling,
    llm=model,
    prompt=prompt_template,
    output_parser=parser
)

# 5 调用生成器
res = generator.generate(
    subject="生成医疗账单数据",
    extra="人的名字更符合日常人名；总费用呈现正态分布，均值为 2000，标准差为 500；保险索赔金额呈现正态分布，均值为 1500，标准差为 300；诊断代码和手术代码可以是随机的，但要符合医疗行业的标准。",
    runs=10     # 生成10条数据
)
print(res)

```

### 实现文本分类

    将文本数据自动归类到预定义的类别中

- 场景
    - 情感分析
    - 话题标记
    - 新闻分类
    - 对话行为分类
    - 自然语言推理
    - 关系分类
    - 事件预测

```python
class Classification(BaseModel):
    """
    用于情感分类的模型
    """
    sentiment: str = Field(..., enum=['happy', 'sad', 'neutral'], description="文本的情感")
    aggressiveness: int = Field(..., enum=[1, 2, 3, 4, 5], description="文本的攻击性,数字越大越攻击性")
    language: str = Field(description="文本使用的语言")

# 提示模板
tagging_prompt = ChatPromptTemplate.from_template(
"""
从以下段落中提取所需的信息
只提取'Classification'类的内容
段落: {text}
"""
)
    
chain = tagging_prompt | model.with_structured_output(Classification)

text = "我非常生气"
# text = "更高兴认识你"
res = chain.invoke(
    {
        "text": text
    }
)
print(res)
```

### 文本自动摘要

    总结文档里的内容
    pip install tiktoken chromadb

- 总结或组合文档的三种方式
    - 填充 stuff，简单的将文档连接成一个提示
    - 映射-规约 Map-reduce，将文档分成批次，总结这些批次，然后总结
    - 细化 refine：通过顺序迭代文档来更新滚动摘要


stuff方式进行摘要:
直接把整个文档输入，文档可能超出输出token上限，所以可能不是对完整的文档进行总结
```python
# 加载文档
loader = WebBaseLoader('https://lilianweng.github.io/posts/2023-06-23-agent/')
docs = loader.load()  # 得到整篇文章

# 写法一
# chain = load_summarize_chain(model, chain_type="stuff")
# res = chain.invoke(docs)
# print(res)

# 写法二
# 定义提示
prompt_template = """
针对下面的内容，写一个简介的总结摘要：
{text}
简洁的总结摘要, 中文回答
"""
prompt = PromptTemplate.from_template(prompt_template)

chain = LLMChain(llm=model, prompt=prompt)

stuff_chain = StuffDocumentsChain(llm_chain=chain, document_variable_name='text')

res = stuff_chain.invoke(docs)
print(res)
```

map_reduce方式进行摘要:
分而治之，把的分成多组，分别进行摘要；
再把多组摘要分组总结，得到更少组的摘要；
递归获得最终摘要
```python
# 1 切割阶段
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000,  # 每段1000个token
    chunk_overlap=0,  # 不重叠
)
split_docs = text_splitter.split_documents(docs) 

# 2 map阶段
map_template = """
以下是一组文档(document):
{docs}
根据这个文档列表，请给出总结摘要
"""
map_prompt = PromptTemplate.from_template(map_template)
map_llm_chain = LLMChain(llm=model, prompt=map_prompt)

# 3 reduce阶段
reduce_template = """
以下是一组总结摘要：
{docs}
将这些内容提炼成一个最终的、同一的总结摘要
"""
reduce_prompt = PromptTemplate.from_template(reduce_template)
reduce_llm_chain = LLMChain(llm=model, prompt=reduce_prompt)


# 定义combine链
combine_chain = StuffDocumentsChain(
    llm_chain=reduce_llm_chain,
    document_variable_name="docs"
)

reduce_chain = ReduceDocumentsChain(
    # 最终调用的链
    combine_documents_chain=combine_chain,
    # 中间汇总的链
    collapse_documents_chain=combine_chain,
    # 汇总token数
    token_max=4000,
)

# 合并链
map_reduce_chain = MapReduceDocumentsChain(
    llm_chain=map_llm_chain,
    reduce_documents_chain=reduce_chain,
    document_variable_name="docs",
    # 不返回中间结果
    return_intermediate_steps=False
)

res = map_reduce_chain.invoke(split_docs)
print(res['output_text'])
```

refine方式进行摘要（了解）：
文档链通过循环遍历输入文档并逐步更新答案，
对于每个文档，将当前文档和最新的中间答案传递给模型，获得最新答案
```python
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000,  # 每段1000个token
    chunk_overlap=0,  # 不重叠
)
split_docs = text_splitter.split_documents(docs) 

chain = load_summarize_chain(model, chain_type="refine")
res = chain.invoke(split_docs)
print(res['output_text'])
```

## 国产大模型

### 智普GLM大模型
    国产大模型，可以不用翻墙

```python
model = ChatOpenAI(
    model="glm-4-air",
    api_key=my_api_key.GLM_API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/",
)
```

### 自定义tool
    可以自定义tool扩展功能。

- 以查询天气为例：
    - 百度天气接口：https://lbsyun.baidu.com/faq/api?title=webapi/weather/base
    - 自定义Schema：
    - 自定义Tool类：

```python
class WeatherInputArgs(BaseModel):
    """
    Input的Schema类
    """
    location: str = Field(..., description="用于查询天气的位置信息")

class WeatherTool(BaseTool):
    """
    查询实时天气的工具
    """
    name: str = "weather_tool"
    description: str = "查询任意位置的当前天气情况"
    args_schema: Type[WeatherInputArgs] = WeatherInputArgs

    def _run(
            self,
            location: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """
        调用工具时执行的函数
        """
        district_code = find_code('GLMDemo\demo2\weather_district_id.csv', location)

        print(f"{location}: {district_code}")

        url = f'https://api.map.baidu.com/weather/v1/?district_id={district_code}&data_type=now&ak={baidu_api_key}'

        # 发送请求
        res = requests.get(url)
        data = res.json()

        text = data['result']['now']['text']
        temp = data['result']['now']['temp']
        feels_like = data['result']['now']['feels_like']
        rh = data['result']['now']['rh']
        wind_dir = data['result']['now']['wind_dir']
        wind_class = data['result']['now']['wind_class']

        return f"当前{location}的天气情况为：{text}，温度为{temp}°C，体感温度为{feels_like}°C，相对湿度为{rh}%，风向为{wind_dir}，风力等级为{wind_class}"

# 创建工具列表
tools = [WeatherTool()]
```


### 整合数据库操作

    prompt -> LLM -> SQL -> Function -> DB执行 -> Prompt -> LLM -> Result

### RAG

- 文件加载
    - text
    - csv: CSVLoader
    - json: JSONLoader
    - html: WebBaseLoader
    - markdown: UnstructuredMarkdownLoader
    - pdf: PyPDFLoader

- 文件切割
    - 通用递归切割器：按回车换行符、句号等切割
    - 根据标题切割：根据标头（一、 1、 a、 等）
    - 根据语义切割：类似语义的为一组
        - 百分位数：计算所有句子间差异的百分位数，超过阈值分割
        - 标准差：数据的波动程度
        - 四分位距：语义嵌入空间显著不同的句子

- 向量数据库
    - Chroma
    - FAISS
    - Qdrant
    - Pinecone
    - Milvus
    - LanceDB

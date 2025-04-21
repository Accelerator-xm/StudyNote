import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_chroma import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
import bs4
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
import my_api_key

# 设置代理
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

# LangSmith
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = "LangchainDemo"
os.environ['LANGCHAIN_API_KEY'] = my_api_key.LangSmith_API_KEY
os.environ['TAVILY_API_KEY'] = my_api_key.tavily_API_KEY
my_dashscope_api_key = my_api_key.DashScope_API_KEY

# RAG对话应用

# 创建模型
# model = ChatOpenAI(
#     model="openai/gpt-3.5-turbo-1106", 
#     temperature=0,
#     openai_api_key="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",
#     openai_api_base="https://openrouter.ai/api/v1"
# )
model = ChatTongyi(
    api_key=my_dashscope_api_key,
    model="qwen-turbo"
)

# 加载数据：本地数据库、本地word文档等
# 一篇博客为例
loader = WebBaseLoader(
    web_path=['https://lilianweng.github.io/posts/2023-06-23-agent/'],
    bs_kwargs=dict(
        parse_only = bs4.SoupStrainer(class_=('post-header', 'post-title', 'post-content'))
    )
)

docs = loader.load()
# print(len(docs))    # 1个文档
# print(docs)     # 文档内容

# 分割
# 分割器：chunk_size分割大小，chunk_overlap重叠大小
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# 测试
# text = """本次测试全面涵盖了工业物联网智慧生产安全管理系统的核心功能和非功能需求，通过精心设计的测试用例，对系统的功能性、易用性、性能、稳定性以及兼容性进行了深入评估。
# 在功能测试方面，系统主界面跳转、用户管理、设备管理、库存管理、水产管理、水质管理、盈收管理、物联网大屏展示、大模型问答及水下机器人模块全部达到预期目标，功能表现稳定可靠，未发现明显缺陷。尤其是水下机器人模块及大模型问答模块表现突出，自动巡航、水质清理与数据采集精准高效，大模型问答准确性高，能够有效支持渔业管理决策。
# """
# res = splitter.split_text(text)
# for s in res:
#     print(s, end="***\n")

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
# chain2 = create_retrieval_chain(retriever, chain1)

# res = chain2.invoke({
#     "input": "什么是任务拆解"
# })

# print(res['answer'])

# 历史记录
# 问答记录 和 查询检索器的上下文
# 添加子链，采用最新用户问题和聊天历史，并在引用历史信息中的任何信息时重新表述问题
# 简单认为是新的“历史感知”检索器，将检索过程融入了对话上下文

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

# 创建子链
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
res2 = result_chain.invoke(
    {'input':'它有哪些常用的方法'},
    config={'configurable': {'session_id': 'zs123456'}}
)
print(res2['answer'])







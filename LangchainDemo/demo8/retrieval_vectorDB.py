import os
import sys
# 添加 LangchainDemo 目录到模块路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from pydantic.v1 import BaseModel, Field
from typing import Optional, List
import my_api_key

os.environ["USER_AGENT"] = "MyLangchainApp/0.1"

# 设置代理
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

# LangSmith
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = "LangchainDemo"
os.environ['LANGCHAIN_API_KEY'] = my_api_key.LangSmith_API_KEY
os.environ['TAVILY_API_KEY'] = my_api_key.tavily_API_KEY
my_dashscope_api_key = my_api_key.DashScope_API_KEY



# 创建模型
model = ChatTongyi(
    api_key=my_dashscope_api_key,
    model="qwen-turbo"
)


"""
## 加载存储的向量数据库
"""
persist_dir = 'LangchainDemo/demo8/chroma_data_dir' # 存放向量数据库的目录

# 存储模型
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 加载向量数据库
vector_store = Chroma(persist_directory=persist_dir, embedding_function=embedding_model)

# 测试向量数据库的相似检索
# res = vector_store.similarity_search_with_score('how do I build a RAG agent')
# print(res[0])
# print(res[0][0].metadata['publish_year'])


"""
## 整合大模型和向量数据库
## 定义数据模型得到检索指令
"""
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

# 获取查询条件
# res1 = chain.invoke("how do I build a RAG agent")
# print(res1)
# res2 = chain.invoke("videos on RAG published in 2024")
# print(res2)


"""
## 根据检索条件进行检索
"""
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



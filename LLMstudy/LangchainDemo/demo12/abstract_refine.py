import os
import sys
# 添加 LangchainDemo 目录到模块路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
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

# 使用refine总结文章
# https://lilianweng.github.io/posts/2023-06-23-agent/

"""
refine介绍: 类似于map_reduce
文档链通过循环遍历输入文档并逐步更新答案，
对于每个文档，将当前文档和最新的中间答案传递给模型，获得最新答案
"""

# 加载文档
loader = WebBaseLoader('https://lilianweng.github.io/posts/2023-06-23-agent/')
docs = loader.load()  # 得到整篇文章

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000,  # 每段1000个token
    chunk_overlap=0,  # 不重叠
)
split_docs = text_splitter.split_documents(docs) 

chain = load_summarize_chain(model, chain_type="refine")
res = chain.invoke(split_docs)
print(res['output_text'])


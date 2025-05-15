import os
import sys
# 添加 LangchainDemo 目录到模块路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.combine_documents.reduce import ReduceDocumentsChain
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain
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

# 使用map_reduce总结文章
# https://lilianweng.github.io/posts/2023-06-23-agent/

"""
map_reduce介绍: 
假设有50万字的文章
map: 把50万字的文章分成5000段，每段500字给模型生成一个摘要
combine: 5000个摘要，1000个一组, 每组1000个摘要给模型生成一个摘要
reduce: 5个摘要，给模型生成一个摘要
"""

# 加载文档
loader = WebBaseLoader('https://lilianweng.github.io/posts/2023-06-23-agent/')
docs = loader.load()  # 得到整篇文章

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

"""
reduces思路：
如果map之后的文档累计token数超过4000个，
则递归将文档以<=4000的批次传给StuffDocumentsChain进行总结；
一旦这些批量摘要的累积token数小于4000，
则将它们全部传递给StuffDocumentsChain进行最终的总结。
"""

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

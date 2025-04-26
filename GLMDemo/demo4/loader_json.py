import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import chat_agent_executor
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.document_loaders import JSONLoader
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.tools import QuerySQLDatabaseTool
from langchain.schema.runnable import RunnableLambda
from operator import itemgetter
import re
import bs4
import my_api_key

# 读取CSV文件
# loader = JSONLoader(
#     file_path='GLMDemo\demo4\medical.json', 
#     jq_schema=".[]",   # 重点：告诉它遍历数组
#     content_key='desc', # 哪个字段作为文档内容
#     text_content=False
# )

# loader = JSONLoader(
#     file_path='GLMDemo\demo4\medical.json', 
#     jq_schema=".[] | {name, prevent}",    # 提取哪些字段
#     text_content=False
# )


# 提取元数据
def create_metadata(record: dict, metadata: dict) -> dict:
    metadata['name'] = record.get('name')
    return metadata

loader = JSONLoader(
    file_path='GLMDemo\demo4\medical.json', 
    jq_schema=".[]",
    metadata_func=create_metadata,
    content_key='desc',
    text_content=False
)

# 加载整个文件
docs = loader.load()
print(docs)
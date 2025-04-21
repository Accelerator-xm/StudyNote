import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.tools import QuerySQLDatabaseTool
from langchain_community.utilities import SQLDatabase
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain.schema.runnable import RunnableLambda
from operator import itemgetter
import re
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

# 使用链完成数据库查询

# 创建模型
# 免费额度到期换个模型
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

# 连接数据库 sqlalchemy
# 初始化mysql数据库连接
MYSQL_URI = 'mysql+pymysql://root:'+ my_api_key.Mysql_Password + '@localhost:3306/web?charset=utf8mb4'
db = SQLDatabase.from_uri(MYSQL_URI)

# 测试数据库是否连接成功
# print(db.get_usable_table_names())  # 查询数据库表明
# print(db.run("SELECT * FROM users limit 5;"))   # 查询数据表前5行数据

# 初始化生成SQL语句的链
# test_chain = create_sql_query_chain(model, db)
# 根据问题生成数据库查询语句
# res = test_chain.invoke({"question": "请问用户表有多少数据"})
# print(res)

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

"""
不同模型生成的sql语句格式不一样，需要提取出sql语句
例如："qwen-turbo"生成的sql语句是这样的：SQLQuery: SELECT COUNT(*) AS total_users FROM users;
有'SQLQuery:'前缀
"""
# 提取 SQL 语句的函数
def extract_sql(text: str) -> str:
    """返回第一条以 SELECT / INSERT / UPDATE / DELETE 开头、以 ; 结束的 SQL"""
    m = re.search(r"(?is)(select|insert|update|delete)[\s\S]+?;", text)
    if m:
        return m.group(0).strip()
    raise ValueError("No SQL found in LLM output")

# 添加提取 SQL 的中间步骤
extract_sql_runnable = RunnableLambda(extract_sql)


# 1、生成sql  2、执行sql 
# 3、提示模板  
chain = (
    RunnablePassthrough
    .assign(query=create_sql_chain)
    .assign(query=itemgetter("query") | extract_sql_runnable)   # sql: 纯 SQL
    .assign(result=itemgetter("query") | execute_sql_tool)  # 执行
    | answer_prompt
    | model
    | StrOutputParser()
)

res = chain.invoke({"question": "请问用户表有多少数据"})
print(res)  # 返回结果
















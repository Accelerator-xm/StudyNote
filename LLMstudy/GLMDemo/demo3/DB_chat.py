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
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.tools import QuerySQLDatabaseTool
from langchain.schema.runnable import RunnableLambda
from operator import itemgetter
import re
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

# 使用代理完成数据库查询

# 创建模型
model = ChatOpenAI(
    model="glm-4-air",
    api_key=my_api_key.GLM_API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/",
    temperature=0
)


# 连接数据库 sqlalchemy
# 初始化mysql数据库连接
MYSQL_URI = 'mysql+pymysql://root:'+ my_api_key.Mysql_Password + '@localhost:3306/web?charset=utf8mb4'
db = SQLDatabase.from_uri(MYSQL_URI)

create_sql_chain = create_sql_query_chain(model, db)
# res = create_sql_chain.invoke({"question": "请问用户表有多少数据"})
# print(res)
# # ```sql
# # SELECT COUNT(*) AS user_count FROM users;
# # ```
# #
# # SQLResult:
# sql = res.replace('```sql', '').replace('```', '').replace('SQLResult:', '')
# print(sql)
# # SELECT COUNT(*) AS user_count FROM users;
# print(db.run(sql))  
# # [(9,)]

execute_sql_tool = QuerySQLDatabaseTool(db=db)

# # 添加中间处理的函数
# # prompt -> LLM -> SQL -> Function -> DB执行
# chain = create_sql_chain | (lambda x: x.replace('```sql', '').replace('```', '').replace('SQLResult:', '')) | execute_sql_tool

# res = chain.invoke({"question": "请问用户表有多少数据"})
# print(res)

# 创建aql的链
create_sql_chain = create_sql_chain | (lambda x: x.replace('```sql', '').replace('```', '').replace('SQLResult:', ''))

# 创建提示词
answer_prompt = PromptTemplate.from_template(
    """
    给定以下用户问题、可能的SQL语句和SQL执行后的结果，回答用户问题。
    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    回答:
    """
)

# 最终回答的链
# Prompt -> LLM -> Result
answer_chain = answer_prompt | model | StrOutputParser()

chain = (
    RunnablePassthrough
    .assign(query = create_sql_chain)
    .assign(result = itemgetter("query") | execute_sql_tool)
    | answer_chain
)

res = chain.invoke({"question": "请问用户表有多少数据"})
print(res)











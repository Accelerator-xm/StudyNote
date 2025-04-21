import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import chat_agent_executor
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.chat_models.tongyi import ChatTongyi
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
model = ChatTongyi(
    api_key=my_dashscope_api_key,
    model="qwen-turbo"
)


# 连接数据库 sqlalchemy
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
















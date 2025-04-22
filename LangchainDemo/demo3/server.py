import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI
from langserve import add_routes
import my_api_key

# 设置代理
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

# LangSmith
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_API_KEY'] = my_api_key.LangSmith_API_KEY
my_dashscope_api_key = my_api_key.DashScope_API_KEY


# 调用大语言模型
# 创建模型
model = ChatTongyi(
    api_key=my_dashscope_api_key,
    model="qwen-turbo"
)

# 创建返回数据的解析器
parser = StrOutputParser()

# 定义提示模板
prompt_template = ChatPromptTemplate.from_messages([
    ('system', '请将下面内容翻译成{language}'),
    ('user', '{text}')
])

# 得到链
chain = prompt_template | model | parser


# 把我们的程序部署成服务
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
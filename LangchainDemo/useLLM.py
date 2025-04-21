import os
from langchain_openai import ChatOpenAI
from chat_dashscope import ChatDashScope
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


# # 把我们的程序部署成服务
# # 创建 fastapi
# app = FastAPI(title="我的服务", version='v1.0', description="翻译工具")

# add_routes(
#     app,
#     chain,
#     path="/chain"
# )

# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="localhost", port=8000)
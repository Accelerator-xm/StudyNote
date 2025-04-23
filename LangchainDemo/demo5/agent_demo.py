import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import chat_agent_executor
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



# 构建代理

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

# res = model.invoke([HumanMessage(content="武汉今天天气怎么样")])
# print(res)  # content='抱歉，我无法提供实时的天气信息。

# Tavily搜索工具
search = TavilySearchResults(max_results = 2)   # max_results返回结果数
# print( search.invoke("武汉的天气怎么样") )    # 搜索

tools = [search]
# 模型绑定工具
# model_with_tool = model.bind_tools(tools)

# model_with_tool可以智能选择是否需要工具
# res = model_with_tool.invoke([HumanMessage(content="武汉今天天气怎么样")])
# print(f'model: {res.content}')
# print(f'tools: {res.tool_calls}')

# 创建代理
agent_executor = chat_agent_executor.create_tool_calling_executor(model, tools)

# res包含三个对象
# HumanMessage：用户提示
# AIMessage：ai推理结果，如果为空则使用工具
# ToolMessage：使用工具获取的结果
res = agent_executor.invoke({
    'messages': [HumanMessage(content="武汉今天天气怎么样")]
})
print(res['messages'][2].content)





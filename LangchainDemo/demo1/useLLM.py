import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from chat_dashscope import ChatDashScope
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
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

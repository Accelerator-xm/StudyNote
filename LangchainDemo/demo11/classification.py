import os
import sys
# 添加 LangchainDemo 目录到模块路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
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
    model="qwen-plus",
    temperature=0,
)

class Classification(BaseModel):
    """
    用于情感分类的模型
    """
    sentiment: str = Field(..., enum=['happy', 'sad', 'neutral'], description="文本的情感")
    aggressiveness: int = Field(..., enum=[1, 2, 3, 4, 5], description="文本的攻击性,数字越大越攻击性")
    language: str = Field(description="文本使用的语言")

# 提示模板
tagging_prompt = ChatPromptTemplate.from_template(
"""
从以下段落中提取所需的信息
只提取'Classification'类的内容
段落: {text}
"""
)
    
chain = tagging_prompt | model.with_structured_output(Classification)

text = "我非常生气"
# text = "更高兴认识你"
res = chain.invoke(
    {
        "text": text
    }
)
print(res)
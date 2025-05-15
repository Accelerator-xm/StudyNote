import os
import sys
# 添加 LangchainDemo 目录到模块路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic.v1 import BaseModel, Field
from typing import Optional, List
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

# pydantic: 处理数据，验证数据，定义数据格式，虚拟化和反虚拟化，类型转换
# 定义数据模型
class Person(BaseModel):
    """
    关于一个人的数据模型
    """
    name: Optional[str] = Field(default=None, description="表示人的名字")

    hair_color: Optional[str] = Field(
        default=None, description="如果知道的话，这个人的头发颜色"
    )

    height_in_meters: Optional[str] = Field(
        default=None, description="这个人的身高（米）"
    )


# 用于获取多个数据
class ManyPerson(BaseModel):
    """
    关于多个人的数据模型
    """
    people: List[Person] = Field(
        default=[], description="一个人列表"
    )


# 提示模板
prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            "你是一个专业的提取算法"
            "只从未结构化文本中提取相关信息"
            "如果你不知道要提取的属性值"
            "返回该属性的值未null",
        ),
        # 如果需要参考对话上下文，则加上
        # MessagesPlaceholder(variable_name="history")
        ('human', "{text}"),
    ]
)

# 只能提取一个数据
# chain = {'text': RunnablePassthrough()} | prompt | model.with_structured_output(schema=Person)
# 提取多个数据
chain = {'text': RunnablePassthrough()} | prompt | model.with_structured_output(schema=ManyPerson)

text = """
    马路上走来一个女生，长长的黑头发披在肩上，大概1米7左右.
    走在她旁边的是她的男朋友，叫张三，比他高10厘米。
"""
res = chain.invoke(text)
print(res)






import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import my_api_key

# 设置代理
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

# LangSmith
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = "LangchainDemo"
os.environ['LANGCHAIN_API_KEY'] = my_api_key.LangSmith_API_KEY
my_dashscope_api_key = my_api_key.DashScope_API_KEY

# 聊天机器人: 结合历史回答

# 创建模型
model = ChatTongyi(
    api_key=my_dashscope_api_key,
    model="qwen-turbo"
)

# 定义提示模板
prompt_template = ChatPromptTemplate.from_messages([
    ('system', '你是一个乐于助人的助手，用{language}尽你所你回答所有问题'),
    MessagesPlaceholder(variable_name='my_msg')
])

# 得到链
chain = prompt_template | model

# 保存历史聊天记录
store = {}      # key: sessionId  vakue: 历史聊天记录

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()

    return store[session_id]


do_message = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="my_msg" #每次聊天发送消息的key
)

config = {'configurable': {'session_id': 'zs123'}}

# 第一轮
res1 = do_message.invoke(
    {
        'my_msg': [HumanMessage(content="你好啊，我是小明")],
        'language': '中文'
    },
    config = config
)

print(res1.content)

# 第二轮
res2 = do_message.invoke(
    {
        'my_msg': [HumanMessage(content="请问我的名字是什么")],
        'language': '中文'
    },
    config = config
)

print(res2.content)


# 第三轮
# 流式输出，一个token一个token输出
for res3 in do_message.stream(
    {
        'my_msg': [HumanMessage(content="请给我讲一个笑话")],
        'language': '中文'
    },
    config = config
):
    print(res3.content, end='-')

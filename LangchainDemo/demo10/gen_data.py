import os
import sys
# 添加 LangchainDemo 目录到模块路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_experimental.synthetic_data import create_data_generation_chain
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

# 创建链
chain = create_data_generation_chain(model)

# 生成数据
# 给一些关键词生成一些话
# res = chain.invoke(
#     {
#         'fields':['蓝色', '红色', '绿色'],    #关键词
#         'preferences': {}     # 偏好，话题
#     }
# )
# print(res)
# """
# 在一片宁静的湖 面上，清晨的薄雾如同一层轻纱，将周围的景色点缀得如梦似幻。
# 远处，一面旗帜迎风飘扬，蓝色、红色和绿色的条纹交织在一起，
# 在阳光的照耀下闪烁着迷人的光芒，仿佛诉说着一个关于勇气、热情与希望的故事。
# """

res = chain.invoke(
    {
        'fields':['蓝色', '红色', '绿色'],
        'preferences': {'style': '像诗歌一样'}
    }
)
print(res)
# """
# 在蓝色的梦之海与红色的烈焰山之间，  
# 绿色的希望之树静静生长，  
# 色彩交织成诗，绘出世界的秘密。
# """






import csv
import os
import sys
from typing import Optional, Type

import requests
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import my_api_key
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from langgraph.prebuilt import chat_agent_executor


glm_api_key = my_api_key.GLM_API_KEY
baidu_api_key = my_api_key.BaiDuMap_api_key

# 天气问答机器人

# 创建模型
model = ChatOpenAI(
    model="glm-4-air",
    api_key=my_api_key.GLM_API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/",
)


def find_code(csv_file_path, district_name) -> str:
    """
    根据区域或者城市的名字，返回该区域的编码
    :param csv_file_path: csv文件路径
    :param district_name: 区域或者城市的名字
    :return: 区域或者城市的编码
    """

    district_map = {}
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            district_code = row['district_id'].strip()
            district = row['district'].strip()
            if district not in district_map:
                district_map[district] = district_code

    return district_map.get(district_name, None)


class WeatherInputArgs(BaseModel):
    """
    Input的Schema类
    """
    location: str = Field(..., description="用于查询天气的位置信息")

class WeatherTool(BaseTool):
    """
    查询实时天气的工具
    """
    name: str = "weather_tool"
    description: str = "查询任意位置的当前天气情况"
    args_schema: Type[WeatherInputArgs] = WeatherInputArgs

    def _run(
            self,
            location: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """
        调用工具时执行的函数
        """
        district_code = find_code('GLMDemo\demo2\weather_district_id.csv', location)

        print(f"{location}: {district_code}")

        url = f'https://api.map.baidu.com/weather/v1/?district_id={district_code}&data_type=now&ak={baidu_api_key}'

        # 发送请求
        res = requests.get(url)
        data = res.json()

        text = data['result']['now']['text']
        temp = data['result']['now']['temp']
        feels_like = data['result']['now']['feels_like']
        rh = data['result']['now']['rh']
        wind_dir = data['result']['now']['wind_dir']
        wind_class = data['result']['now']['wind_class']

        return f"当前{location}的天气情况为：{text}，温度为{temp}°C，体感温度为{feels_like}°C，相对湿度为{rh}%，风向为{wind_dir}，风力等级为{wind_class}"

tools = [WeatherTool()]

# 创建代理
agent_executor = chat_agent_executor.create_tool_calling_executor(model, tools)

res1 = agent_executor.invoke({
    'messages': [HumanMessage(content="中国首都在哪里")]
})
print(res1['messages'])
# AIMessage(content='中国的首都是北京。北京是中国的政治、文化和国际交流中心，同时也是中国的历史古都之一。',

res2 = agent_executor.invoke({
    'messages': [HumanMessage(content="武汉今天天气怎么样")]
})
print(res2['messages'])
# ToolMessage(content='当前武汉的天气情况为：阴，温度为20°C，体感温度为21°C，相对湿度为83%，风向为西南风，风力等级为1级',
# AIMessage(content='今天武汉的天气情 况如下：阴天，气温约为20°C，相对湿度为83%，风向为西南风，风力较小，为1级。请注意天气变化，合理安排您的外出计划。',
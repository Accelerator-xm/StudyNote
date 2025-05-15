import os
import sys
# 添加 LangchainDemo 目录到模块路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

from zhipuai import ZhipuAI
import my_api_key

glm_api_key = my_api_key.GLM_API_KEY
model = ZhipuAI(api_key=glm_api_key)

# res = model.chat.completions.create(
#     model="glm-4-air",
#     messages=[
#         {
#             "role": "user",
#             "content": "请介绍以下你自己"
#         }
#     ],
# )
# print(res.choices[0].message.content)

# 流式输出
res = model.chat.completions.create(
    model="glm-4-air",
    messages=[
        {
            "role": "user",
            "content": "请介绍以下你自己"
        }
    ],
    stream=True
)
for s in res:
    print(s.choices[0].delta.content)
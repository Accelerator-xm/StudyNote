import os
import sys
# 添加 LangchainDemo 目录到模块路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from pydantic import BaseModel, Field, ConfigDict
from langchain_experimental.tabular_synthetic_data.openai import create_openai_data_generator
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
    model="qwen-plus"
)

# 生成结构化的数据
# 1 定义数据模型
class MedicalBilling(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    patient_id: str = Field(description="患者ID")
    patient_name: str = Field(description="患者姓名")
    diagnosis_code: str = Field(description="诊断代码")
    procedure_code: str = Field(description="手术代码")
    total_cost: float = Field(description="总费用")
    insurance_claim_amount: float = Field(description="保险索赔金额")


# 2 提供样例数据
examples = [
    {
        "example": """
        {{
            "patient_id": "P001",
            "patient_name": "张三",
            "diagnosis_code": "D001",
            "procedure_code": "PR001",
            "total_cost": 1500.0,
            "insurance_claim_amount": 1200.0
        }}
        """
    },
    {
        "example": """
        {{
            "patient_id": "P002",
            "patient_name": "王五",
            "diagnosis_code": "D002",
            "procedure_code": "PR002",
            "total_cost": 2000.0,
            "insurance_claim_amount": 1800.0
        }}
        """
    }
]

# 3 创建提示模板
example_template = PromptTemplate(
    input_variables=["example"],template='{example}'
)



PREFIX = """你是一个医疗数据生成器，请生成符合以下格式的结构化账单数据。
字段包括：patient_id、patient_name、diagnosis_code、procedure_code、total_cost、insurance_claim_amount。
以下是几个示例数据："""

SUFFIX = """
请根据以下指令生成类似结构的 JSON 数据（一次只生成**1**条）：
主题: {subject}
补充要求: {extra}

严格要求：
1. 必须输出单个 JSON 对象（不是数组）。
2. JSON 放在 ```json ... ``` 代码块中。
3. 代码块前后不得有任何额外文字。
"""

prompt_template = FewShotPromptTemplate(
    prefix=PREFIX,
    suffix=SUFFIX,
    examples=examples,
    example_prompt=example_template,
    input_variables=["subject", "extra"],
)

# LangChain 在使用 OpenAI Functions 的输出解析器时，
# 期待模型输出包含 function_call 字段，
# 但（qwen-plus 通过 ChatTongyi）并没有返回这个字段，会报错。
# 不要使用 OpenAI Functions 模式，而是直接输出 JSON，然后用 Pydantic 来解析。
raw_parser = PydanticOutputParser(pydantic_object=MedicalBilling)
# 让模型 只输出干净 JSON 往往很难 100% 保证
# 用 OutputFixingParser 自动纠偏, 让另一次 LLM 调用把“脏”JSON 转成干净 JSON。
parser = OutputFixingParser.from_llm(parser=raw_parser, llm=model)



# 4 创建结构化数据生成器
generator = create_openai_data_generator(
    output_schema=MedicalBilling,
    llm=model,
    prompt=prompt_template,
    output_parser=parser
)

# 5 调用生成器
res = generator.generate(
    subject="生成医疗账单数据",
    extra="人的名字更符合日常人名；总费用呈现正态分布，均值为 2000，标准差为 500；保险索赔金额呈现正态分布，均值为 1500，标准差为 300；诊断代码和手术代码可以是随机的，但要符合医疗行业的标准。",
    runs=10     # 生成10条数据
)
print(res)

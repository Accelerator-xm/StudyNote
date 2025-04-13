import os
from chat_dashscope import ChatDashScope
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory, RunnableLambda, RunnablePassthrough
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
import my_api_key

# 设置代理
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

# LangSmith
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = "LangchainDemo"
os.environ['LANGCHAIN_API_KEY'] = my_api_key.LangSmith_API_KEY
my_dashscope_api_key = my_api_key.DashScope_API_KEY

# 构建向量数据库和检索器

# 准备测试数据集
documents = [
    Document(
        page_content="肺炎患病概率为0.06%，无特发人群，无传染性",
        metadata={"source": "肺炎内容文档"}
    ),
    Document(
        page_content="肺炎治疗部门为内科、呼吸内科，通过药物治疗、支持性治疗，治疗时间持续7-10天，治愈率95%，常用药物为阿奇霉素片、头孢克洛颗粒，一般需要做痰液病原体检查、尿常规、痰液常规检查、痰液细菌培养、胸部平片、胸部MRI、纤维支气管镜检查、胸部CT检查、嗜中性杆状粒细胞数、血常规",
        metadata={"source": "肺炎内容文档"}
    ),
    Document(
        page_content="肺炎是指终末气道，肺泡和肺间质的炎症，可由疾病微生物、理化因素，免疫损伤、过敏及药物所致。细菌性肺炎是最常见的肺炎，也是最常见的感染性疾病之一。日常所讲的肺炎主要是指细菌性感染引起的肺炎，此肺炎也是最常见的一种，在抗生素应用以前，细菌性肺炎对儿童及老年人健康威胁极大，抗生素的出现及发展曾一度使肺炎病死率明显下降，但近年来，尽管应用强有力的抗生素和有效的疫苗，肺炎总的病死率不再降低，甚至有所上升。",
        metadata={"source": "肺炎内容文档"}
    ),
    Document(
        page_content="肺炎所属类别：疾病百科、内科、呼吸内科",
        metadata={"source": "肺炎内容文档"}
    ),
    Document(
        page_content="肺炎预防措施：1、平时注防寒保暖，遇有气候变化，随时更换衣着，体虚易感者，可常服玉屏风散之类药物，预防发生外感。\n2、避免吸入粉尘和一切有毒或刺激性气体。\n3、加强体育锻炼，增强体质。\n4、进食或喂食时，注意力要集中，要求患者细嚼慢咽，避免边吃边说，食物呛吸入肺。\n健康教育：\n1、饮食指导\n进高蛋白，高热量，高维生素易消化的半流质食物。对伴有发热的肺炎患者应注意多饮水这样不仅可使机体水分的丢失得到补充，还有利于细菌毒素的排泄及降低体温。多食用水果，不要大量食用辛辣油腻食物。对于原有慢性肺病的肺炎病人，要注意食用高蛋白食物\n2、休息与活动指导\n发热者要卧床休息，注意保暖，保持室内空气清新，鼓励患者每隔1h进行深呼吸和有效咳嗽。卧床患者应注意翻身，每4h为患者叩背排痰一次。恢复期适当活动，应增加休息时间，坚持深呼吸锻炼至少要持续4-6周，这样可以减少肺不张的发生;还要避免呼吸道的刺激，如灰尘，化学飞沫等;尽可能避免去人群拥挤的地方或接触已有呼吸道感染的患者。",
        metadata={"source": "肺炎内容文档"}
    ),
    Document(
        page_content="肺炎发病原因：肺炎球菌一般寄居在正常人的鼻咽部，一般不会发病，当人体免疫力下降时，如感冒、劳累、慢性支气管炎，慢性心脏病、长期吸烟等，肺炎球菌即可乘机侵入人体，引起肺炎、中耳炎、鼻窦炎、脑膜炎、心内膜炎、败血症等。\n肺炎球菌、甲型溶血性链球菌、金黄色葡萄球菌、肺炎克雷白杆菌、流感嗜血杆菌、铜绿假单胞菌、埃希大肠杆菌、绿脓杆菌等细菌都会引发肺炎。\n冠状病毒、腺病毒、流感病毒、巨细胞病毒、单纯疱疹病毒等病毒都会引发肺炎。\n白念珠菌、曲霉、放射菌等真菌都会引发肺炎。\n如军团菌、支原体、衣原体、立克次体、弓形虫、原虫等非典型病原体都会引发肺炎。\n放射性、胃酸吸入、药物等理化因素都会引发肺炎。",
        metadata={"source": "肺炎内容文档"}
    ),
    Document(
        page_content="肺炎症状有：呼气时两颊鼓起和缩唇、 咳泡沫黏液痰、呼吸困难、咳嗽伴胸痛、咳痰、咳嗽、持续性发热、咳铁锈色痰、发热伴寒战、恶性胸水 ",
        metadata={"source": "肺炎内容文档"}
    )
]


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 实例化向量数空间
vector_store = Chroma.from_documents(documents, embedding=embedding_model)
# 相似度查询: 分数越低相似度越高
# print(vector_store.similarity_search_with_score('治疗'))

# 检索器
# bind(k=1)选取相似度最高的一个
retriever = RunnableLambda(vector_store.similarity_search).bind(k=1)
# 相似度查询
# print(retriever.batch(['治疗', '症状']))

# 提示模板
message = """
使用提供的上下文仅回答这个问题。
{question}
上下文：
{context}
"""

prompt_temp = ChatPromptTemplate.from_messages([
    ('human', message)
])

# 创建模型
model = ChatDashScope(model='qwen-turbo', dashscope_api_key=my_dashscope_api_key)

# RunnablePassthrough()允许将用户的问题之后再传递给prompt和model
chain = {'question': RunnablePassthrough(), 'context': retriever} | prompt_temp | model

res = chain.invoke('请谈谈肺炎怎么治疗')

print(res)
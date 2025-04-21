import os
from langchain_chroma import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.chat_models.tongyi import ChatTongyi
from getVideoText import load_youtube_video
import datetime
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

# 爬取youtube数据构建向量数据库, 持久化存储

# 创建模型
model = ChatTongyi(
    api_key=my_dashscope_api_key,
    model="qwen-turbo"
)

persist_dir = 'chroma_data_dir' # 存放向量数据库的目录

# 初始化一些youtube视频
urls = [
    "https://www.youtube.com/watch?v=HAn9vnJy6S4",
    "https://www.youtube.com/watch?v=dA1cHGACXCo",
    "https://www.youtube.com/watch?v=ZcEMLz27sL4",
    "https://www.youtube.com/watch?v=hvAPnpSfSGo",
    "https://www.youtube.com/watch?v=EhlPDL4QrWY",
    "https://www.youtube.com/watch?v=mmBo8nlu2j0",
]

# socument数组
docs = []
for url in urls:
    try:
        # 一个视频一个document
        print(f"正在加载：{url}")
        docs.extend(load_youtube_video(url))
    except Exception as e:
        print(f"加载失败：{url}")
        print(e)

print(len(docs))

# 给doc添加额外的元数据：视频发布的年份
for doc in docs:
    doc.metadata['publish_year'] = datetime.datetime.strptime(
        doc.metadata['publish_date'],
        '%Y-%m-%dT%H:%M:%S'
    ).year

print(docs[0].metadata)

# 根据多个doc构建向量数据库
# 分割器：chunk_size分割大小，chunk_overlap重叠大小
splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=30)
split_docs = splitter.split_documents(docs)

# 存储
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 向量数数据库持久化
# 持久化 persist_directory=persist_dir
vector_store = Chroma.from_documents(documents=split_docs, embedding=embedding_model, persist_directory=persist_dir)









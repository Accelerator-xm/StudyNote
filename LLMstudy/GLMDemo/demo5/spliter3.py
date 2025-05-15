import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

from langchain_experimental.text_splitter import SemanticChunker
from langchain.embeddings import HuggingFaceEmbeddings

# 设置代理
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

with open('GLMDemo/demo5/text.txt', 'r', encoding='utf-8') as f:
    file_content = f.read()

# 百分位数
text_spliter = SemanticChunker(
    embeddings=embedding_model,
    breakpoint_threshold_type='percentile',
    breakpoint_threshold_amount=60
)

docs_list = text_spliter.create_documents([file_content])

print(len(docs_list))
print(docs_list[0].page_content)
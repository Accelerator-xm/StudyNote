import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

from langchain_community.document_loaders import WebBaseLoader
import bs4

# 读取CSV文件
loader = WebBaseLoader(
    web_paths=('https://fastapi.tiangolo.com/zh/features/',),
    encoding='utf-8',
    bs_kwargs=dict(parse_only=bs4.SoupStrainer(class_=('md-content',)))
)

# 加载整个文件
docs = loader.load()
print(docs)
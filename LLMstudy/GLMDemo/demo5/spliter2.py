import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

from langchain_text_splitters import MarkdownHeaderTextSplitter

with open('GLMDemo/demo5/text.md', 'r', encoding='utf-8') as f:
    file_content = f.read()

# 定义结构
label_split = [
    ('##', 'Header 1'),
    ('###', 'Header 2')
]

md_spliter = MarkdownHeaderTextSplitter(headers_to_split_on=label_split)

docs_list = md_spliter.split_text(file_content)

print(docs_list)
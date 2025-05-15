import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

from langchain_text_splitters import RecursiveCharacterTextSplitter

with open('GLMDemo/demo5/text.txt',encoding='utf-8') as f:
    text_data = f.read()

# 递归切割器

# 默认分隔符："\n\n", "\n", " ", ""
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100, # 块的大小
    chunk_overlap=20, # 重叠的数量
    length_function=len, # 统计每个块的长度
    is_separator_regex=False, # 是否支持正则表达式
    separators=[
        "\n\n", "\n", "。", "？", "！", ",", "，"
    ]
)

chunks_list = text_splitter.create_documents([text_data])

print(len(chunks_list))
print(chunks_list[0])
print(chunks_list[1])
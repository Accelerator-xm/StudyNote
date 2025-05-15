import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

from langchain_community.document_loaders import UnstructuredMarkdownLoader



# # 整个文档一个document
# loader = UnstructuredMarkdownLoader(
#     file_path='GLMDemo/demo4/text.md'
# )

# 根据元素分割
loader = UnstructuredMarkdownLoader(
    file_path='GLMDemo/demo4/text.md',
    mode='elements'
)

# 加载整个文件
docs = loader.load()
print(docs)
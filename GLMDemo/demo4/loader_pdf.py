import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

from langchain_community.document_loaders import PyPDFLoader


# # 每页一个document，不包含图片
# loader = PyPDFLoader(
#     file_path='GLMDemo/demo4/text.pdf'
# )

# 每页一个document，提取图片文字
loader = PyPDFLoader(
    file_path='GLMDemo/demo4/text.pdf',
    extract_images=True
)


docs = loader.load()
print(docs)
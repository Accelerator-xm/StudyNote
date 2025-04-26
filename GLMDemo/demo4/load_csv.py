import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

from langchain_community.document_loaders import CSVLoader

# 读取CSV文件
loader = CSVLoader(file_path='GLMDemo\demo4\weather_district_id.csv', encoding='utf-8')\

# 加载整个文件
data = loader.load()

for re in data[:2]:
    print(re)
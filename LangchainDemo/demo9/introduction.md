# 提取结构化的数据

    从非结构化的文本中提取结构化信息。

- demo介绍
    - retract_data.py: 从文本中提取关于人的信息
        - pydantic: 用于定义数据模型，让大模型去提取数据
        - model.with_structured_output(schema=数据模型)

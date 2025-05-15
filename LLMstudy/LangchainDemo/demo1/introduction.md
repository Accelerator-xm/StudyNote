# langchain调用模型

    创建模型 --> 准备prompt --> 创建返回数据的解析器 --> 得到链 --> 使用chain调用

- demo介绍
    - useLLM.py: 调用大语言模型完成翻译任务
    - chat_dashscope.py: 自定义 LangChain 聊天模型，用于接入通义千问
        - 开始以为同义不能用langchain，要自定义才让gpt写的
        - 局限性很大不能流式输出，不能实用工具，因为没实现
        - 之后换成 from langchain_community.chat_models.tongyi import ChatTongyi
   
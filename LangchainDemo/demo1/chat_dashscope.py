# chat_dashscope.py
from typing import List, Optional
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain.schema.messages import AIMessageChunk
from langchain.schema.output import ChatGenerationChunk
import dashscope
import os
from typing import Generator



class ChatDashScope(BaseChatModel):
    """自定义 LangChain 聊天模型，用于接入通义千问"""

    model: str = "qwen-turbo"
    dashscope_api_key: Optional[str] = None

    def __init__(self, model: str = "qwen-turbo", dashscope_api_key: Optional[str] = None):
        super().__init__(model=model, dashscope_api_key=dashscope_api_key)
        self.model = model
        self.dashscope_api_key = dashscope_api_key or os.getenv("DASHSCOPE_API_KEY")
        dashscope.api_key = self.dashscope_api_key

    def _format_messages(self, messages: List[BaseMessage]):
        """LangChain message 转换为 DashScope message 格式"""
        role_map = {
            SystemMessage: "system",
            HumanMessage: "user",
            AIMessage: "assistant"
        }
        formatted = []
        for msg in messages:
            role = role_map.get(type(msg), "user")
            formatted.append({"role": role, "content": msg.content})
        return formatted

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs
    ) -> ChatResult:
        formatted_messages = self._format_messages(messages)

        response = dashscope.Generation.call(
            model=self.model,
            messages=formatted_messages,
            result_format="message"
        )

        content = response.output.choices[0].message["content"]

        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content=content))]
        )
    
    @property
    def _llm_type(self) -> str:
        return "dashscope-chat"
    
    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs
    ) -> Generator[ChatGenerationChunk, None, None]:
        formatted_messages = self._format_messages(messages)

        response = dashscope.Generation.call(
            model=self.model,
            messages=formatted_messages,
            result_format="message",
            stream=True
        )

        prev_content = ""
        for chunk in response:
            try:
                full_content = chunk.output.choices[0].message["content"]
                # 获取“新增”部分
                delta = full_content[len(prev_content):]
                prev_content = full_content

                if delta:
                    yield ChatGenerationChunk(message=AIMessageChunk(content=delta))
                    if run_manager:
                        run_manager.on_llm_new_token(delta)

            except Exception as e:
                print(f"处理流式 chunk 出错: {e}")
                continue

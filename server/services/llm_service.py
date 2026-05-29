import json
from typing import List, Optional, Dict, Any
from openai import AsyncOpenAI
import httpx

from config import settings


class LLMService:
    """大模型服务"""
    
    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.base_url = settings.LLM_BASE_URL
        self.model = settings.LLM_MODEL_NAME
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.1,
    ) -> str:
        """
        调用大模型进行对话
        """
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"}
            )
        result = response.choices[0].message.content
        return result
    

# 全局LLM服务实例
llm_service = LLMService()

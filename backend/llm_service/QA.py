import litellm
import logging
from typing import List, Dict, AsyncGenerator

# 配置简单的日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_lawyer_chat(
    history: List[Dict[str, str]], 
    model: str = "ollama/qwen3:1.7b", #在这里替换模型
    api_base: str = "http://localhost:11434",
    temperature: float = 0.6
) -> AsyncGenerator[str, None]:
    """
    支持多轮对话的流式生成
    :param history: 完整的对话历史 [{"role": "user", "content": "..."}, ...]
    """
    
    # 确保系统提示词始终在第一位
    system_prompt = {
        "role": "system", 
        "content": "你是一名中国法律顾问。请根据案情，引用法条（如《劳动合同法》）进行严谨分析。"
    }
    
    # 如果历史记录里没有系统提示词，手动加上
    if not history or history[0].get("role") != "system":
        messages = [system_prompt] + history
    else:
        messages = history

    logger.info(f"🚀 发送请求给模型: {model}, 消息数: {len(messages)}")

    try:
        response = await litellm.acompletion(
            model=model,
            messages=messages,
            api_base=api_base,
            stream=True,
            temperature=temperature,
            api_key="ollama",
            timeout=600  # 设置 600秒 超时，防止生成过长卡死
        )

        async for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                # DeepSeek R1 会输出 <think> 标签。
                # 如果你想在后端处理掉思考过程，可以在这里加正则过滤。
                # 但通常建议保留，让前端决定是否折叠显示。
                yield content

    except litellm.Timeout:
        logger.error("模型响应超时")
        yield "⚠️ 回答超时，请简化问题或稍后再试。"
    except Exception as e:
        logger.error(f"调用异常: {e}")
        yield "⚠️ 系统内部错误，请联系管理员。"
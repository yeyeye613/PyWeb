from os import getenv
from openai import OpenAI
from django.http import StreamingHttpResponse
# from .models import Conversation
# from markdown import markdown
from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)

# 1.把返回改成json，并在前端加渲染
# 2.前端引入marked.js
# 3.编写测试用例


def stream_chat(request):
    logger.info('Stream chat view called')
    user_input = request.GET.get('user_input')

    def generator():
        try:
            api_key = getenv('DASHSCOPE_API_KEY')
            client = OpenAI(api_key=api_key,
                            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                            )
            chunks = client.chat.completions.create(
                model="deepseek-r1",
                stream=True,
                messages=[{"role": "user", "content": user_input}]
                # message是个包含消息字典的列表，用于描述对话的上下文
                # 每个消息字典包含 "role" 和 "content" 两个键。
                # "role" 可以是 "system"（系统消息，用于设置对话的初始指令或背景信息）、"user"（用户输入的消息）或 "assistant"（模型之前生成的回复）。
            )
            # stream = True，该方法会返回一个生成器对象（generator）在异步函数调用会返回异步生成器
            # 返回的是一个ChatCompletion对象。包含了模型生成的回复以及其他相关信息，你可以通过访问该对象的属性来获取具体内容。
            for chunk in chunks:
                delta = chunk.choices[0].delta if chunk.choices else None
                if delta:
                    ai_reasoning = getattr(delta, "reasoning_content", "") or ""
                    ai_answer = getattr(delta, "content", "") or ""
                    if ai_reasoning:
                        logger.info('Received ai_reasoning: %s', ai_reasoning)
                        yield f"data: {ai_reasoning}\n\n"
                    elif ai_answer:
                        logger.info('Received ai_answer: %s', ai_answer)
                        yield f"data: {ai_answer}\n\n"
                else:
                    ai_usage = getattr(chunk, "usage", "使用情况读取出错")
                    logger.info('Received ai_usage: %s', ai_usage)
                    yield f"data: {ai_usage}\n\n"  # → 前端触发 onmessage
            yield "event:done\ndata:\n\n"
        except Exception as e:
            logger.error(f"Error in streaming chat: {e}")
            yield f"event:error\ndata: {str(e)}\n\n"
    if user_input == "close()":
        return StreamingHttpResponse("event:close\ndata:\n\n", content_type='text/event-stream')
    else:
        return StreamingHttpResponse(generator(), content_type='text/event-stream')


def test(request):
    return render(request, "AI_model/test.html")

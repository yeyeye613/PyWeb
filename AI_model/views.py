from django.shortcuts import render
from .models import Conversation
from openai import OpenAI
from os import getenv
from markdown import markdown


class ChatBot:
    def __init__(self):
        """初始化"""
        self.api_key = getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY 环境变量未设置")

        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        self.messages = []  # 维护对话历史

    def get_response(self, content):
        """从接口获取回答"""
        stream = self.client.chat.completions.create(
            model="deepseek-r1",
            messages=[{"role": "user", "content": content}],
            stream=True,
            stream_options={"include_usage": True}
        )
        full_answer = self.print_response(stream)
        return full_answer

    def print_response(self, stream):
        """实时输出回答"""
        full_answer = ""
        try:
            for chunk in stream:
                delta = chunk.choices[0].delta if chunk.choices else None
                if not delta:
                    continue  # 跳过空 chunk
                answer = getattr(delta, 'content', '') or ''
                full_answer += answer
                print(answer, end="", flush=True)  # 实时输出
        except Exception as e:
            print(f"\n发生错误: {str(e)}")
            full_answer += f"\n（处理中断：{str(e)}）"
        finally:
            return full_answer


def chat_view(request):
    if request.method == "POST":
        user_input = request.POST.get('message')
        if user_input:
            try:
                chatbot = ChatBot()
                ai_response = chatbot.get_response(user_input)
                if ai_response is None:
                    ai_response = "无有效响应"
                Conversation.objects.create(
                    user_input=user_input,
                    ai_response=ai_response
                )
            except Exception as e:
                ai_response = f"出现错误: {str(e)}"
                Conversation.objects.create(
                    user_input=user_input,
                    ai_response=ai_response
                )
    conversations = Conversation.objects.all()

    formatted_responses = []
    for conv in conversations:
        # 确保 ai_response 是字符串
        md_content = conv.ai_response if isinstance(conv.ai_response, str) else "不存在"
        html_content = markdown(md_content, extensions=['fenced_code', 'codehilite'])
        formatted_responses.append(html_content)

    return render(request, 'AI_model/chat.html', {
        'formatted_responses': formatted_responses
    })

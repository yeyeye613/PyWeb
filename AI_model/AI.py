from openai import OpenAI
from os import getenv
from json import dump
from datetime import datetime
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
        self.messages = ""  # 维护对话历史

    def ask(self):
        content = ""
        print("Enter your message (按 Ctrl+D 结束输入)(按一次回车保存一次，记得回车后再结束输入): ")
        while True:
            try:
                line = input()
                content += line + "\n"
            except EOFError:
                break
        self.get_response(content)

    def get_response(self, content):
        """从接口获取回答"""
        stream = self.client.chat.completions.create(
            model="deepseek-r1",
            messages=[{"role": "user", "content": content}],
            stream=True,
            stream_options={"include_usage": True}
        )
        self.print_response(stream, content)

    def print_response(self, stream, content):
        """实时输出回答"""
        full_answer = ""
        full_reasoning = ""
        chunk = None
        try:
            for chunk in stream:
                delta = chunk.choices[0].delta if chunk.choices else None
                if not delta:
                    continue  # 跳过空 chunk
                reasoning = getattr(delta, 'reasoning_content', '') or ''
                answer = getattr(delta, 'content', '') or ''

                # 实时输出（单行更新）
                if reasoning:
                    print(f"{reasoning}", end="")
                elif answer:
                    print(f"{answer}", end="")

                # 累积内容
                full_reasoning += reasoning
                full_answer += answer

        except Exception as e:
            print(f"\n发生错误: {str(e)}")

        finally:

            # 最终换行并显示 token 使用
            print("\n" + "-" * 30)
            if chunk and chunk.usage:
                print(f"Token 使用: {chunk.usage}")
            print(markdown(full_answer))
            # print(f"\r思考过程: {full_reasoning}")
            # print(f"\r回答过程: {full_answer}")
            self.save_history(content, full_reasoning, full_answer)

    def save_history(self, content, full_reasoning, full_answer):
        """保存对话历史"""
        current_time = datetime.now()
        current_time = current_time.strftime("%Y_%m_%d-%H:%M")  # 加上时间戳
        self.messages = {
            "content": content,
            "reasoning": full_reasoning,
            "answer": full_answer,
            "time": current_time
        }
        with open("history.json", "a", encoding="utf-8") as f:
            dump(self.messages, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    bot = ChatBot()
    bot.ask()

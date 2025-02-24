import sys
from openai import OpenAI
from os import getenv


class ChatBot:
    def __init__(self):
        """初始化并验证环境变量"""
        self.api_key = getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY 环境变量未设置")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.messages = []
        self.last_output_length = 0  # 用于跟踪上次输出长度

    def get_user_input(self):
        """获取多行用户输入"""
        print("\n请输入消息（按 Ctrl+D 提交）: ")
        try:
            return sys.stdin.read().strip()
        except EOFError:
            return ""
        except KeyboardInterrupt:
            print("\n操作已取消")
            sys.exit(0)

    def _clear_line(self):
        """使用 ANSI 转义码清除当前行"""
        sys.stdout.write('\x1b[2K\r')  # 清除整行
        sys.stdout.flush()

    def _update_display(self, content, prefix):
        """更新显示内容并处理换行"""
        lines = content.split('\n')
        display_content = f"{prefix}: " + lines[-1]  # 只显示最后一行用于刷新

        # 清除上次输出
        if self.last_output_length > 0:
            self._clear_line()

        # 输出新内容
        sys.stdout.write(display_content)
        sys.stdout.flush()

        # 如果有多行内容，先输出前面的行
        if len(lines) > 1:
            self._clear_line()
            for line in lines[:-1]:
                print(f"{prefix}: {line}")
            sys.stdout.write(display_content)
            sys.stdout.flush()

        self.last_output_length = len(display_content)

    def process_stream(self, stream):
        """处理流式响应"""
        full_content = {"reasoning": "", "answer": ""}
        current_type = None

        try:
            for chunk in stream:
                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta
                reasoning = getattr(delta, 'reasoning_content', '')
                answer = getattr(delta, 'content', '')

                if reasoning:
                    full_content["reasoning"] += reasoning
                    self._update_display(full_content["reasoning"], "思考")
                    current_type = "reasoning"
                elif answer:
                    full_content["answer"] += answer
                    self._update_display(full_content["answer"], "回答")
                    current_type = "answer"

            # 最终换行处理
            print("\n" + "-" * 30)
            if chunk.usage:
                print(f"Token 使用: {chunk.usage}")
            print(f"完整思考过程:\n{full_content['reasoning']}")
            print(f"\n最终回答:\n{full_content['answer']}")

        except Exception as e:
            print(f"\n处理过程中发生错误: {str(e)}")
        finally:
            self.last_output_length = 0  # 重置输出长度计数器

    def run(self):
        """主运行循环"""
        try:
            while True:
                user_input = self.get_user_input()
                if not user_input:
                    print("输入不能为空！")
                    continue

                self.messages.append({"role": "user", "content": user_input})
                stream = self.client.chat.completions.create(
                    model="deepseek-r1",
                    messages=self.messages,
                    stream=True,
                    stream_options={"include_usage": True}
                )
                self.process_stream(stream)

                # 添加历史记录
                self.messages.append({
                    "role": "assistant",
                    "content": full_content["answer"]
                })

                # 退出机制
                print("\n输入 'exit' 退出，其他内容继续对话...")
                if input().strip().lower() == 'exit':
                    break

        except KeyboardInterrupt:
            print("\n再见！")
            sys.exit(0)


if __name__ == '__main__':
    try:
        bot = ChatBot()
        bot.run()
    except ValueError as e:
        print(f"初始化失败: {e}")
        sys.exit(1)
from django.test import TestCase

# Create your tests here.

# tests/test_views.py
from django.test import TestCase
from unittest.mock import patch

# 单元测试（后端）：
class ChatTests(TestCase):
    @patch('openai.ChatCompletion.create')
    def test_stream_response(self, mock_openai):
        # 模拟OpenAI流式响应
        mock_openai.return_value = iter([
            {'choices': [{'delta': {'content': 'Hello'}}]},
            {'choices': [{'delta': {'content': ' World'}}]}
        ])

        response = self.client.post('/chat', {'message': 'test'})

        # 验证流式响应格式
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            b''.join(response.streaming_content),
            b'data: {"content": "Hello"}\n\ndata: {"content": " World"}\n\n'
        )
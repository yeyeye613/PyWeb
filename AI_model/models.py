# models.py
# from django.conf import settings
# from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
# 作为ai对话网站，我需要对话的时间，双方，内容
# 时间用时间戳，ask和response都用textfield，会话要专门生成个id便于查找，还要有对话备注
# 用户模型


class Conversation(models.Model):
    """对话，包括关联用户，对话数据"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 关联用户
    user_input = models.TextField(max_length=1000)  # 用户输入
    ai_response = models.TextField()  # AI回复
    timestamp = models.DateTimeField(auto_now_add=True)  # 时间戳
    # language = models.CharField(max_length=10, default='zh')  # 语言选项
    session_id = models.CharField(max_length=40)  # 会话标识

    class Meta:
        """模型的元数据，比如表名，排序方式，权限，详细名称和复数名称"""
        ordering = ['-timestamp']  # 按时间倒序排列
        indexes = [models.Index(fields=['user', 'session_id'])]

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"

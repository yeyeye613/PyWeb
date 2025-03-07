# models.py
from django.db import models
from django.conf import settings
from django.utils import timezone


class Conversation(models.Model):
    """
    对话会话模型 - 代表一次完整的对话
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 关联用户模型
        on_delete=models.CASCADE,  # 用户删除时级联删除对话
        related_name='conversations'  # 反向关系名称
    )
    title = models.CharField(
        max_length=200, 
        blank=True,  # 允许初始为空
        help_text="自动生成的对话标题"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,  # 自动记录创建时间
        db_index=True  # 添加数据库索引
    )
    updated_at = models.DateTimeField(
        auto_now=True  # 自动更新最后修改时间
    )

    class Meta:
        ordering = ['-updated_at']  # 默认按更新时间倒序排列
        verbose_name = '对话会话'
        verbose_name_plural = '对话会话'

    def __str__(self):
        return f"{self.user.username}的对话 - {self.title}"


class Message(models.Model):
    """
    消息模型 - 存储对话中的每条消息
    """
    ROLE_CHOICES = (
        ('user', '用户'),
        ('assistant', '助理'),
        ('system', '系统'),
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,  # 对话删除时级联删除消息
        related_name='messages'  # 反向关系名称
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,  # 角色选项
        default='user'
    )
    content = models.TextField(
        verbose_name='消息内容'
    )
    timestamp = models.DateTimeField(
        default=timezone.now,  # 自动记录时间
        db_index=True
    )
    # 可选字段：存储API调用的元数据
    metadata = models.JSONField(
        null=True,
        blank=True,
        help_text="API响应元数据（如token消耗）"
    )

    class Meta:
        ordering = ['timestamp']  # 按时间顺序排列
        verbose_name = '消息记录'
        verbose_name_plural = '消息记录'

    def __str__(self):
        return f"{self.conversation.id}-{self.role}-{self.timestamp}"

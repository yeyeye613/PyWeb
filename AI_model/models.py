from django.db import models


class Conversation(models.Model):
    user_input = models.TextField()
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

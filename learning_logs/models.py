from django.db import models


class Topic(models.Model):
    text = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text  # 定义 __str__ 的默认行为


class Entry(models.Model):
    text = models.TextField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    # class Meta:
    #     verbose_name_plural = 'entries'  # 定义复数形式的名称
    # #     覆盖默认复数名称：当默认生成的复数形式不符合语法或语义时，手动指定一个更合理的名称。不然他默认加's'

    class Meta:
        verbose_name = "日志条目"  # 单数形式（如中文场景）
        verbose_name_plural = "日志条目"  # 复数形式（中文中复数通常不变）

    def __str__(self):
        if len(self.text) > 10:
            return self.text[:10] + "..."
        return f"{self.text}"

from django import forms
from .models import Topic
# model,fields,labels,widgets


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',  # 添加 Bootstrap 类
                'rows': 3
            })
        }

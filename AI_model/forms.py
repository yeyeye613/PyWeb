from django import forms


class ChatForm(forms.Form):
    # CharField属性：max_length,required是否必填,widget渲染表单部件，label
    message = forms.CharField(
        max_length=50000,
        required=True,
        label='输入消息',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': '请输入您的问题...'
        }),
    )
    # 作为i18n看看吧，没用
    # language = forms.ChoiceField(
    #     label='语言选择',
    #     choices=[('zh', '中文'), ('en', 'English')],
    #     widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    # )

    def clean_message(self):
        message = self.cleaned_data['message'].strip()
        if len(message) < 2:
            raise forms.ValidationError("消息太短，请至少输入2个字符")
        return message

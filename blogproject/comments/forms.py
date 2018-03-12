from django import forms
from .models import Comment

#通过调用这个CommentForm类，django自动为我们创建表单的代码
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','url','text']
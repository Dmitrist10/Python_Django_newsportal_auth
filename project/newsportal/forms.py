from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from typing import Any
from django import forms
from .models import News, Article, Author
from django.core.exceptions import ValidationError

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'title',
            'content'
        ]

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        title = cleaned_data.get("title")
        if title is None or len(title) < 10:
            raise ValueError("Min lenght of title is 10!")
        
        content = cleaned_data.get("content")
        if content is None or len(content) < 25:
            raise ValidationError("Min lenght of content is 25!")

        return cleaned_data
    
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'category'
        ]

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        title = cleaned_data.get("title")
        if title is None or len(title) < 10:
            raise ValueError("Min lenght of title is 10!")
        
        content = cleaned_data.get("content")
        if content is None or len(content) < 25:
            raise ValueError("Min lenght of content is 25!")
        
        content = cleaned_data.get("category")
        if content is None:
            raise ValueError("no Category!")
        
        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user

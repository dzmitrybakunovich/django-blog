from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser,  Article, Comment


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'avatar',
        )


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = (
            'title',
            'text',
            'short_description',
            'image',
        )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = (
            'text',
        )

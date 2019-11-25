from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import mark_safe
from ckeditor.fields import RichTextField


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='images/for_profile', null=True, blank=True)
    last_online = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.email

    def image_in_admin(self):
        return mark_safe(f'<img src="/media/{self.avatar}" width="110" height="110" style="object-fit: cover;" />')

    image_in_admin.short_description = 'profile image'


class Article(models.Model):
    class Meta:
        db_table = 'article'
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='images/for_article', null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    short_description = models.CharField(max_length=120, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey('main_app.CustomUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    class Meta:
        db_table = 'comment'
    text = RichTextField()
    date = models.DateTimeField(blank=True, null=True)
    article = models.ForeignKey('main_app.Article', on_delete=models.CASCADE)
    author = models.ForeignKey('main_app.CustomUser', on_delete=models.CASCADE, null=True, blank=True)


class Like(models.Model):
    user = models.ForeignKey('main_app.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey('main_app.Article', on_delete=models.CASCADE, null=True, blank=True)
    is_liked = models.BooleanField()


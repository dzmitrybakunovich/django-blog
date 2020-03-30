from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import mark_safe
from django.utils import timezone
from django.utils.text import slugify


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='images/for_profile', null=True, blank=True)
    last_online = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.email

    def is_online(self):
        if self.last_online:
            return (timezone.now() - self.last_online) < timezone.timedelta(minutes=10)
        return False

    def image_in_admin(self):
        return mark_safe(f'<img src="/media/{self.avatar}" width="110" height="110" style="object-fit: cover;" />')

    image_in_admin.short_description = 'profile image'


class Article(models.Model):
    class Meta:
        db_table = 'article'

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=40)
    image = models.ImageField(upload_to='images/for_article', null=True, blank=True)
    text = RichTextField()
    short_description = models.CharField(max_length=120, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('main_app.CustomUser', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Article, self).save(*args, **kwargs)


class Comment(models.Model):
    class Meta:
        db_table = 'comment'
    text = RichTextField()
    date = models.DateTimeField(auto_now=True)
    article = models.ForeignKey('main_app.Article', on_delete=models.CASCADE)
    author = models.ForeignKey('main_app.CustomUser', on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey('main_app.CustomUser', on_delete=models.CASCADE)
    article = models.ForeignKey('main_app.Article', on_delete=models.CASCADE)
    is_liked = models.BooleanField()

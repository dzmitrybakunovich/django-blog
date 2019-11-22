from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
 path('articles/', views.ArticleView.as_view()),
 path('articles/<pk>', views.SingleArticleView.as_view())
]


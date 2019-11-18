from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
 path('articles/', views.ArticleList.as_view(), name='subject_list'),
 path('article/<pk>/', views.ArticleDetail.as_view(), name='subject_detail'),
 path('article/<pk>/add_auhtor/', views.AddAuthorInArticle.as_view(), name='add_author'),
]

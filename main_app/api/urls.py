from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
 path('article/', views.ArticleView.as_view()),
 #path('article/<int:id>', views.SingleArticleView.as_view())
]


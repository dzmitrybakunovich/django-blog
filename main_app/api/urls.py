from django.urls import path

from . import views

app_name = 'articles'

urlpatterns = [
 path('article/', views.ArticleView.as_view()),
 path('article/<int:pk>', views.SingleArticleView.as_view()),
 path('user/', views.UserView.as_view()),
 path('user/<int:pk>', views.UserDetail.as_view())
]

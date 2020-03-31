from django.conf import settings
from django.urls import path
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='index'),
    path('article/new', views.ArticleView.as_view(request_type='CREATE'), name='new_post'),
    path('article/<slug:article_slug>', views.ArticlePage.as_view(), name='article_detail'),
    path('article/<int:article_id>/delete', views.ArticleView.delete, name='delete_article'),
    path('article/<slug:article_slug>/edit', views.ArticleView.as_view(request_type='UPDATE'), name='edit_article'),
    path('article/<int:article_id>/add_like', views.LikeDislike.as_view(vote_type=True), name='add_like'),
    path('article/<int:article_id>/add_dislike', views.LikeDislike.as_view(vote_type=False), name='add_dislike'),
    path('articles/user/<str:username>', views.UserArticle.as_view(), name='user_articles'),
    path('registration', views.RegisterFormView.as_view(), name='register'),
    path('user/<str:username>', views.UserView.as_view(template_name='main_app/user_profile.html'),
         name='user_profile'),
    path('user/<str:username>/edit/', views.UserView.as_view(template_name='main_app/edit_user_profile.html'),
         name='edit_profile'),
    path('get_online/', views.get_online, name='get_online'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

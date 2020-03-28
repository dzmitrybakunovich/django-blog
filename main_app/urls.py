from django.conf import settings
from django.urls import include, path
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from main_app import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='index'),
    path('article/add', views.new_article, name='new_post'),
    path('article/<slug:article_slug>', views.page_article, name='article_detail'),
    path('delete_article/<int:article_id>', views.delete_article, name='delete_article'),
    path('edit_article/<int:article_id>', views.edit_article, name='edit_article'),
    path('article/<int:article_id>/add_like', views.add_like, name='add_like'),
    path('article/<int:article_id>/add_dislike', views.add_dislike, name='add_dislike'),
    path('articles/user/<int:user_id>', views.article_created_by_user, name='article_created_by_user'),
    path('registration', views.RegisterFormView.as_view(), name='register'),
    path('profile/<slug:user_slug>', views.user_profile, name='user_profile'),
    path('edit_profile', views.edit_user, name='edit_profile'),
    path('get_online/', views.get_online, name='get_online'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

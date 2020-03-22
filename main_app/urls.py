from django.conf import settings
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from main_app import views

urlpatterns = [
    url('^$', views.main_page, name='index'),
    url(r'^articles/(?P<article_id>\d+)$', views.page_article, name='article_detail'),
    url(r'^profile/(?P<user_id>\d+)$', views.user_profile, name='user_profile'),
    url('post/new', views.new_article, name='new_post'),
    url('edit/profile', views.edit_user, name='edit_profile'),
    url(r'^articles/(?P<article_id>\d+)/add_like/$', views.add_like, name='add_like'),
    url(r'^articles/(?P<article_id>\d+)/add_dislike/$', views.add_dislike, name='add_dislike'),
    url(r'articles/user/(?P<user_id>\d+)$', views.article_created_by_user, name='article_created_by_user'),
    url(r'delete/(?P<article_id>\d+)$', views.delete_article, name='delete_article'),
    url(r'edit/(?P<article_id>\d+)$', views.edit_article, name='edit_article'),
    url('get_online', views.get_online, name='get_online'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

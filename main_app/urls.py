from django.conf import settings
from django.conf.urls import url
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from main_app import views

urlpatterns = [
    url('^$', views.main_page, name='index'),
    url(r'^articles/(?P<article_id>\d+)$', views.page_article, name='article_detail'),
    url(r'^profile/(?P<user_id>\d+)$', views.user_profile, name='user_profile'),
    url('post/new', views.new_article, name='new_post'),
    url('edit/profile', views.edit, name='edit_profile'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url('', include('main_app.urls')),
    url('^admin/', admin.site.urls),
    url('accounts/', include('django.contrib.auth.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url('', include('social_django.urls', namespace='social')),
    url('api/', include('main_app.api.urls', namespace='api')),
]

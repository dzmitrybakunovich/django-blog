from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url('', include('main_app.urls')),
    url('^admin/', admin.site.urls),
    url('accounts/', include('django.contrib.auth.urls')),
    url('', include('social_django.urls', namespace='social'))
]

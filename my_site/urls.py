from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main_app.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('api/v1/', include('main_app.api.urls', namespace='api')),
]

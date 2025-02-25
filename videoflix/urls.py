from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('content_app.api.urls')),
    path('api/auth/', include('user_auth_app.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # path('__debug__/', include('debug_toolbar.urls')),
    # path('django-rq/', include('django_rq.urls'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


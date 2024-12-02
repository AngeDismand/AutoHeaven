from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from AutoHeavenWebsite import views
from dashboard import views
urlpatterns = [
    path('',include('AutoHeavenWebsite.urls')),
    path('',include('dashboard.urls')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
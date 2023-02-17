from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('', include('main.urls', namespace='main')),
    path('auth/', include('siteauth.urls', namespace='siteauth')),
    path('patient/', include('patients.urls', namespace='patients')),
    path('doctors/', include('doctors.urls', namespace='doctors')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

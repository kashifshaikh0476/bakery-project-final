from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views # Ye add karein

urlpatterns = [
    path('admin/', admin.site.urls),
    # Ye line default logout ko force-allow karegi
    path('accounts/logout/', auth_views.LogoutView.as_view(http_method_names=['get', 'post', 'options']), name='logout'),
    path('', include('main_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

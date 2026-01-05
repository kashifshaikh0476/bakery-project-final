from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views # Ye line add karni hai

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # === LOGOUT REDIRECT FIX ===
    # Ye line aapko seedha Home page par bhejegi aur Logout 405 error bhi theek karegi
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home', http_method_names=['get', 'post']), name='logout'),
    
    path('', include('main_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

# Media settings for images
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

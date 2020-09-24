from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from social_network.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('travel-blog/', include('social_network.urls')),
    path('auth/', include('django.contrib.auth.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

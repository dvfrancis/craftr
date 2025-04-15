from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path('details/', include('details.urls')),
    path('account/', include('account.urls')),
    path('contact/', include('contact.urls')),
    path('diary/', include('diary.urls')),
    path('faq/', include('faq.urls')),
    path('', include('home.urls')),
    path('login/', include('login.urls')),
    path('register/', include('register.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path('', include('details.urls')),
    path('', include('account.urls')),
    path('', include('contact.urls')),
    path('', include('diary.urls')),
    path('', include('faq.urls')),
    path('', include('home.urls')),
    path('', include('login.urls')),
    path('', include('register.urls')),
    path('admin/', admin.site.urls),
]

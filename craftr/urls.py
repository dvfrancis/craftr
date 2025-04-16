"""
URL configuration for the craftr project.

This module defines the URL patterns for the entire project, including
routes for various apps and custom error handlers for 404 and 500 errors.

Attributes:
    handler404 (str): Path to the custom 404 error handler view.
    handler500 (str): Path to the custom 500 error handler view.
    urlpatterns (list): List of URL patterns for the project.
"""

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

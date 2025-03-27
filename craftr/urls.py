"""
URL configuration for craftr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from craftr import views as home
from diary import views as diary
from faq import views as faq
from contact import views as contact
from login import views as login

handler404 = 'craftr.views.custom_404'

urlpatterns = [
    path('', home.home_page, name='home'),
    path('diary/', diary.diary_page, name='diary'),
    path('faq/', faq.faq_page, name='faq'),
    path('contact/', contact.contact_page, name='contact'),
    path('login/', login.login_page, name='login'),
    path('admin/', admin.site.urls),
]

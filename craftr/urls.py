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
from home import views as home_page
from diary import views as diary_page
from faq import views as faq_page
from contact import views as contact_page
from login import views as login_page
from . import views

urlpatterns = [
    path('', home_page.home, name='home'),
    path('diary/', diary_page.diary, name='diary'),
    path('faq/', faq_page.faq, name='faq'),
    path('contact/', contact_page.contact, name='contact'),
    path('login/', login_page.login, name='login'),
    path('admin/', admin.site.urls),
    path('test/', views.test_404, name='test'),
]

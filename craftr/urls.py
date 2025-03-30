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
from details import views as details
from faq import views as faq
from contact import views as contact
from login import views as login
from account import views as account
from register import views as registration

handler404 = 'craftr.views.custom_404'

urlpatterns = [
    path('', home.home_page, name='home'),
    path('diary/', diary.diary_details, name='diary'),
    path('details/', details.details_page, name='details'),
    path('faq/', faq.faq_page, name='faq'),
    path('contact/', contact.contact_page, name='contact'),
    path('login/', login.login_page, name='login'),
    path('register/', registration.registration_page, name='register'),
    path('account/', account.account_page, name='account'),
    path('admin/', admin.site.urls),
]

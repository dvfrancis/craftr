from django.contrib import admin
from django.urls import path, include
from diary import views as diary
from details import views as details
from faq import views as faq
from contact import views as contact
from register import views as registration
from django.contrib.auth.views import LoginView
from account import views as account
from home import views as home

handler404 = 'craftr.views.custom_404'

urlpatterns = [
    path('', home.home_page, name='home'),
    path('diary/', diary.diary_details, name='diary'),
    path('details/<int:class_id>/', details.enrol, name='details'),
    path(
        "remove_enrolment/<int:class_id>/",
        details.remove_enrolment,
        name="remove_enrolment",
    ),
    path('faq/', faq.faq_page, name='faq'),
    path('contact/', contact.contact_page, name='contact'),
    path(
        "login/",
        LoginView.as_view(template_name="login/login.html"),
        name="login",
    ),
    path('register/', registration.register_user, name='register'),
    path('account/', account.user_details, name='account'),
    path(
        'update_profile/',
        registration.update_profile,
        name="update_profile",
    ),
    path('account/', include('account.urls')),
    path("delete_account/", account.delete_account, name="delete_account"),
    path('admin/', admin.site.urls),
]

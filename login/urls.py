from django.urls import path
from django.contrib.auth.views import LoginView

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="login/login.html"),
        name="login",
    ),
]

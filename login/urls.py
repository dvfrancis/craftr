from django.urls import path
from .views import CustomLoginView

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path(
        "",
        CustomLoginView.as_view(template_name="login/login.html"),
        name="login",
    ),
]

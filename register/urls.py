from django.urls import path
from register import views as registration

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path('', registration.register_user, name='register'),
    path(
        'update_profile/',
        registration.update_profile,
        name="update_profile",
    ),
]

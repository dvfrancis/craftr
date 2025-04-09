from django.urls import path
from account import views as account
from .views import custom_logout

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path("logout/", custom_logout, name="logout"),
    path('account/', account.user_details, name='account'),
    path("delete_account/", account.delete_account, name="delete_account"),
]

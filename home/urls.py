from django.urls import path
from home import views as home

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path('', home.home_page, name='home'),
]

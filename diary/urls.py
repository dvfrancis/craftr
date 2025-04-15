from django.urls import path
from diary import views as diary

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path('', diary.diary_details, name='diary'),
]

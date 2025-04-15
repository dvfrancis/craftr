from django.urls import path
from faq import views as faq

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path('', faq.faq_page, name='faq'),
]

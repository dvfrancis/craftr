from django.urls import path
from contact import views as contact

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path('', contact.contact_page, name='contact'),
]

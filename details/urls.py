from django.urls import path
from details import views as details

handler404 = 'craftr.views.custom_404'
handler500 = 'craftr.views.custom_500'

urlpatterns = [
    path('<int:class_id>/', details.enrol, name='details'),
    path(
        "remove_enrolment/<int:class_id>/",
        details.remove_enrolment,
        name="remove_enrolment",
    ),
]

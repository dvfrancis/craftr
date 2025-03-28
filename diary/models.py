from django.db import models
from django.contrib.auth.models import User

DIFFICULTY_CHOICES = (
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),)

# Create your models here.


class EventDay(models.Model):
    event_day_id = models.AutoField(primary_key=True)
    class_date = models.DateField()
    event_title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} enrolled in {self.class_title}"


class EventClass(models.Model):
    event_class_id = models.AutoField(primary_key=True)
    class_date = models.ForeignKey(
        EventDay,
        on_delete=models.CASCADE,
        related_name="event_classes"
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    class_title = models.CharField(max_length=100)
    class_description = models.TextField()
    difficulty = models.CharField(
        max_length=12,
        choices=DIFFICULTY_CHOICES,
        default='Beginner'
    )


class Enrolment(models.Model):
    enrolment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="enrol_status"
    )
    class_title = models.ForeignKey(
        EventClass,
        on_delete=models.CASCADE,
        related_name="enrolments"
    )

    def __str__(self):
        return self.event

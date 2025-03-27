from django.db import models
from django.contrib.auth.models import User

DIFFICULTY_CHOICES = (
    ('B', 'Beginner'),
    ('I', 'Intermediate'),
    ('A', 'Advanced'),)

# Create your models here.


class EventDay(models.Model):
    event_day_id = models.AutoField(primary_key=True)
    class_date = models.DateField()
    event_title = models.CharField(max_length=100)

    def __str__(self):
        return self.event


class EventClass(models.Model):
    event_class_id = models.AutoField(primary_key=True)
    class_date = models.ForeignKey(
        EventDay,
        on_delete=models.CASCADE,
        related_name="event_day"
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    class_title = models.CharField(max_length=100)
    class_description = models.TextField()
    difficulty = models.CharField(
        max_length=1,
        choices=DIFFICULTY_CHOICES,
        default='B'
    )


class enrolment(models.Model):
    enrolment_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="username"
    )
    class_title = models.ForeignKey(
        EventClass,
        on_delete=models.CASCADE,
        related_name="event_class"
    )

    def __str__(self):
        return self.event

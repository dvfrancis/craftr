from django.db import models


class EventDay(models.Model):
    event_day_id = models.AutoField(primary_key=True)
    class_date = models.DateField()
    event_title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} enrolled in {self.class_title}"
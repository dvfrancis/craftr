from django.db import models
from django.core.exceptions import ValidationError


class EventDay(models.Model):
    id = models.AutoField(primary_key=True)
    class_date = models.DateField()
    event_title = models.CharField(max_length=100, unique=True)

    # Enforce unique event titles regardless of case
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['event_title'],
                name='unique_event_title_case_insensitive',
                condition=models.Q(event_title__iexact=models.F('event_title'))
            )
        ]

    def clean(self):
        # Require all fields to be completed
        if not self.class_date or not self.event_title:
            raise ValidationError("All fields must be completed")

    def __str__(self):
        return (
            f"{self.class_date}")

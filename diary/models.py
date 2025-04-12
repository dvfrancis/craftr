from django.db import models
from django.core.exceptions import ValidationError


class EventDay(models.Model):
    id = models.AutoField(primary_key=True)
    day_date = models.DateField()
    day_title = models.CharField(max_length=100, unique=True)
    day_description = models.TextField()

    # Enforce unique event titles regardless of case
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['day_title'],
                name='unique_event_title_case_insensitive',
                condition=models.Q(day_title__iexact=models.F('day_title'))
            )
        ]

    def clean(self):
        # Require all fields to be completed
        if not self.day_date or not self.day_title:
            raise ValidationError("All fields must be completed")

    def __str__(self):
        return (
            f"{self.day_date}")

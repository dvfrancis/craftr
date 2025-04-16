from django.db import models
from django.core.exceptions import ValidationError


class EventDay(models.Model):
    """
    Represents a day with scheduled events.

    This model stores information about a specific day, including its date,
    title, and description. It enforces unique titles regardless of case.

    Attributes:
        id (AutoField): The primary key for the EventDay instance.
        day_date (DateField): The date of the event day.
        day_title (CharField): The title of the event day, must be unique.
        day_description (TextField): A description of the event day.
    """
    id = models.AutoField(primary_key=True)
    day_date = models.DateField()
    day_title = models.CharField(max_length=100, unique=True)
    day_description = models.TextField()

    # Enforce unique event titles regardless of case
    class Meta:
        """
        Meta options for the EventDay model.

        Enforces a unique constraint on the day_title field, ensuring
        uniqueness regardless of case sensitivity.
        """
        constraints = [
            models.UniqueConstraint(
                fields=['day_title'],
                name='unique_event_title_case_insensitive',
                condition=models.Q(day_title__iexact=models.F('day_title'))
            )
        ]

    def clean(self):
        """
        Validate the EventDay instance.

        Ensures that all required fields are completed.

        Raises:
            ValidationError: If any required field is missing.
        """
        # Require all fields to be completed
        if not self.day_date or not self.day_title:
            raise ValidationError("All fields must be completed")

    def __str__(self):
        """
        Return a string representation of the EventDay instance.

        Returns:
            str: The date of the event day.
        """
        return (
            f"{self.day_date}")

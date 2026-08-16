from django.db import models
from django.db.models.functions import Lower
from django.core.exceptions import ValidationError


class EventDay(models.Model):
    """
    Represents a day with scheduled events.

    This model stores information about a specific day, including its date,
    title, and description. It enforces unique titles regardless of case.

    Attributes:
        id (AutoField): The primary key for the EventDay instance.
        day_date (DateField): The date of the event day.
        day_title (CharField): The title of the event day. Unique when
            compared without regard to case; see the Meta constraint.
        day_description (TextField): A description of the event day.
    """
    id = models.AutoField(primary_key=True)
    day_date = models.DateField()
    # No unique=True here. The constraint below compares lowercased titles,
    # which is strictly stronger: anything it allows is already unique
    # exactly. Keeping both would mean two indexes enforcing overlapping
    # rules, which is how the previous version came to be misleading.
    day_title = models.CharField(max_length=100)
    day_description = models.TextField()

    class Meta:
        """
        Meta options for the EventDay model.

        Enforces unique day titles, compared without regard to case, so
        "Opening Day" and "OPENING DAY" cannot both exist.
        """
        constraints = [
            # Issue #127. This previously passed fields=['day_title'] with
            # condition=Q(day_title__iexact=F('day_title')), which folded no
            # case at all: a condition decides which rows an index covers,
            # not how their values are compared, and comparing a column to
            # itself is true for every row. The result was a plain unique
            # index wearing a name that promised otherwise.
            #
            # Passing Lower() as a positional expression is what actually
            # compares case-insensitively. Expressions and fields cannot be
            # mixed in one UniqueConstraint, hence no fields= argument.
            models.UniqueConstraint(
                Lower('day_title'),
                name='unique_event_title_case_insensitive',
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

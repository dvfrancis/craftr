from django.db import models
from diary.models import EventDay
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Define the choices for difficulty levels
BEGINNER = 'Beginner'
INTERMEDIATE = 'Intermediate'
ADVANCED = 'Advanced'

DIFFICULTY_CHOICES = [
    (BEGINNER, 'Beginner'),
    (INTERMEDIATE, 'Intermediate'),
    (ADVANCED, 'Advanced'),
]


class EventClass(models.Model):
    """
    Represents a class scheduled on a specific event day.

    This model stores information about a class, including its start and end
    times, title, description, difficulty level, instructor details, and
    images.

    Attributes:
        event_day (ForeignKey): The event day associated with the class.
        start_time (TimeField): The start time of the class.
        end_time (TimeField): The end time of the class.
        class_title (CharField): The title of the class.
        class_description (TextField): A description of the class.
        difficulty (CharField): The difficulty level of the class.
        class_image (CloudinaryField): An optional image for the class.
        instructor (CharField): The name of the instructor.
        instructor_image (CloudinaryField): An optional image of the
        instructor.
        instructor_bio (TextField): A biography of the instructor.
    """
    event_day = models.ForeignKey(
        EventDay,
        on_delete=models.CASCADE,
        related_name="event_day"
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    class_title = models.CharField(max_length=100)
    class_description = models.TextField()
    difficulty = models.CharField(
        max_length=12,
        choices=DIFFICULTY_CHOICES,
        default=BEGINNER)
    class_image = CloudinaryField(
        'image',
        default='class_placeholder',
        blank=True,
        null=True
    )
    instructor = models.CharField(max_length=100)
    instructor_image = CloudinaryField(
        'image',
        default='instructor_placeholder',
        blank=True,
        null=True
    )
    instructor_bio = models.TextField()

    class Meta:
        """
        Meta options for the EventClass model.

        Enforces a unique constraint on the combination of event day and start
        time to ensure no duplicate classes are scheduled at the same time.
        """
        constraints = [
            models.UniqueConstraint(
                fields=['event_day', 'start_time'],
                name='unique_class_title_case_insensitive'
            )
        ]

    def clean(self):
        """
        Validate the EventClass instance.

        Ensures that the end time is later than the start time.

        Raises:
            ValidationError: If the end time is not later than the start time.
        """
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be later than start time.")

    def __str__(self):
        """
        Return a string representation of the EventClass instance.

        Returns:
            str: A formatted string containing the class title, start and end
            times, and the event day.
        """
        class_date = self.event_day.day_date.strftime('%d %B %Y')
        class_start = (
            f"{self.start_time.hour % 12 or 12}:"
            f"{self.start_time.minute:02d} "
            f"{'AM' if self.start_time.hour < 12 else 'PM'}"
        )
        class_end = (
            f"{self.end_time.hour % 12 or 12}:"
            f"{self.end_time.minute:02d} "
            f"{'AM' if self.end_time.hour < 12 else 'PM'}"
        )

        return (
            f"{self.class_title} (from {class_start} to {class_end} "
            f"on {class_date})"
        )


class Enrolment(models.Model):
    """
    Represents a user's enrolment in a specific class.

    This model links a user to a class they are enrolled in.

    Attributes:
        user (ForeignKey): The user enrolled in the class.
        enrolled_class (ForeignKey): The class the user is enrolled in.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="enrol_status"
    )
    enrolled_class = models.ForeignKey(
        EventClass,
        on_delete=models.CASCADE,
        related_name="enrolments"
    )

    class Meta:
        """
        Meta options for the Enrolment model.

        Enforces a unique constraint to ensure a user cannot enrol in the same
        class multiple times.
        """
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'enrolled_class'],
                name='unique_user_enrolment'
            )
        ]

    def __str__(self):
        """
        Return a string representation of the Enrolment instance.

        Returns:
            str: A formatted string indicating the user's enrolment in a class.
        """
        return (
            f"{self.user.username} is enrolled on "
            f"{self.enrolled_class.class_title}"
        )

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
        default='default_class_image',
        blank=True,
        null=True
    )
    instructor = models.CharField(max_length=100)
    instructor_photo = CloudinaryField(
        'image',
        default='default_instructor_image',
        blank=True,
        null=True
    )
    instructor_bio = models.TextField()

    # Enforce unique class titles regardless of case
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['event_day', 'start_time'],
                name='unique_class_title_case_insensitive'
            )
        ]

    def clean(self):
        # End time must be later than start time
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be later than start time.")

    def __str__(self):
        # Formats the date as "dd-mm-yyyy"
        class_date = self.event_day.class_date.strftime('%d %B %Y')
        # Formats as "12:00pm"
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

    # Enforce unique enrolments for each user and class
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'enrolled_class'],
                name='unique_user_enrolment'
            )
        ]

    def __str__(self):
        return (
            f"{self.user.username} is enrolled on "
            f"{self.enrolled_class.class_title}"
        )

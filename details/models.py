from django.db import models
from django.contrib.auth.models import User
from diary.models import EventDay
from django.core.exceptions import ValidationError
from django.contrib import admin

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
        default=BEGINNER
    )

    # Enforce unique class titles regardless of case
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['class_title'],
                name='unique_class_title_case_insensitive',
                condition=models.Q(event_title__iexact=models.F('class_title'))
            )
        ]

    def clean(self):
        # Require all fields to be completed
        if (
            not self.event_day or not self.start_time or not self.end_time or
            not self.class_title or
            not self.class_description or not self.difficulty
        ):
            raise ValidationError("All fields must be completed")

        # End time must be later than start time
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be later than start time.")

    def __str__(self):
        return (
            f"{self.class_title} ({self.start_time} - {self.end_time} on "
            f"{self.event_day}"
        )


@admin.register(EventClass)
class EventClassAdmin(admin.ModelAdmin):
    list_display = (
        'event_day', 'class_title', 'start_time', 'end_time',
        'class_description', 'difficulty'
    )
    list_filter = ('difficulty', 'class_date')
    search_fields = (
        'event_day', 'class_title', 'start_time', 'end_time',
        'class_description', 'difficulty'
    )
    ordering = ('event_day', 'class_title', 'start_time', 'end_time',
                'difficulty')


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

    def clean(self):
        # Require all fields to be completed
        if (
            not self.user or not self.enrolled_class
        ):
            raise ValidationError("All fields must be completed")

    def __str__(self):
        return (
            f"{self.user.username} is enrolled in "
            f"{self.enrolled_class.class_title}"
        )


@admin.register(Enrolment)
class EnrolmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrolled_class')
    list_filter = ('enrolled_class')
    search_fields = ('user', 'enrolled_class')
    ordering = ('user', 'enrolled_class')

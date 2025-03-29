from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

# Define the choices for experience levels
BEGINNER = 'Beginner'
INTERMEDIATE = 'Intermediate'
ADVANCED = 'Advanced'

EXPERIENCE_CHOICES = [
    (BEGINNER, 'Beginner'),
    (INTERMEDIATE, 'Intermediate'),
    (ADVANCED, 'Advanced'),
]


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    location = models.CharField(max_length=100)
    experience = models.CharField(
        choices=EXPERIENCE_CHOICES,
        default=BEGINNER,
        max_length=12)
    photograph = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    def clean(self):
        # Require fields to be completed
        if (not self.location or not self.experience):
            raise ValidationError(
                "Please complete user, location, and experience fields"
            )

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()

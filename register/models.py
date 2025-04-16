from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
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
    """
    Represents a user's profile

    This model extends the default Django User model by adding additional
    fields such as location, experience level, and a photograph.

    Attributes:
        user (User): A one-to-one relationship with the Django User model.
        location (str): The user's location.
        experience (str): The user's experience level, chosen from predefined
        options.
        photograph (CloudinaryField): An optional profile photograph
        stored in Cloudinary.
    """
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
    photograph = CloudinaryField(
        'image',
        default='placeholder',
        blank=True,
        null=True
    )

    def clean(self):
        """
        Validates the UserProfile instance.

        Ensures that the location and experience fields are not empty.
        Raises:
            ValidationError: If required fields are missing.
        """
        # Require fields to be completed
        if (not self.location or not self.experience):
            raise ValidationError(
                "Please complete the location and experience fields"
            )

    def __str__(self):
        """
        Returns a string representation of the UserProfile instance.

        Returns:
            str: The username associated with the profile, or a default message
            if no user is associated.
        """
        return (
            f"{self.user.username}'s profile"
            if self.user
            else "Profile without user"
        )


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create or update a UserProfile.

    This function is triggered whenever a User instance is saved. If the
    User is newly created, a corresponding UserProfile is created. If the
    User already exists, the associated UserProfile is updated.

    Args:
        sender: The model class that sent the signal.
        instance: The instance of the model that was saved.
        created (bool): A boolean indicating whether the instance was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()

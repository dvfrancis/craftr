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
    """
    Represents a user's profile

    This model extends the default Django User model by adding additional
    fields such as location, experience level, and a photograph.

    Attributes:
        user (User): A one-to-one relationship with the Django User model.
        location (str): The user's location.
        experience (str): The user's experience level, chosen from predefined
        options.
        photograph (ImageField): An optional profile photograph stored in
        the S3 media bucket.
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
    # See the note in details/models.py: this prefix is also named in
    # infra/media-permissions.yaml and the two have to agree.
    photograph = models.ImageField(
        upload_to='profiles/',
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
def create_user_profile(sender, instance, created, raw=False, **kwargs):
    """
    Ensure every User has a UserProfile.

    Triggered whenever a User is saved. Creates the profile when one is
    missing and does nothing when it already exists, so a User can always
    be saved regardless of what state its profile is in.

    This used to call instance.profile.save() on every non-creating save,
    which raised RelatedObjectDoesNotExist for a User with no profile. That
    was reachable through the admin, where UserProfile can be deleted on its
    own: editing that user afterwards then failed (issue #105). Nothing on
    UserProfile derives from User, so the re-save it performed achieved
    nothing anyway.

    Args:
        sender: The model class that sent the signal.
        instance: The instance of the model that was saved.
        created (bool): Whether the instance was newly created.
        raw (bool): True while loaddata is replaying a fixture.
        **kwargs: Additional keyword arguments.

    Returns:
        None.
    """
    # loaddata sends post_save with raw=True while the fixture is still
    # loading, before related rows necessarily exist. Creating related
    # objects at that point can fail or write rows the fixture then
    # duplicates, so the documented behaviour is to return early.
    if raw:
        return
    UserProfile.objects.get_or_create(user=instance)

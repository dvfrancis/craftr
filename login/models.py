from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from django import forms

EXPERIENCE_CHOICES = (
    ('B', 'Beginner'),
    ('I', 'Intermediate'),
    ('A', 'Advanced'),)

# Create your models here.


class UserProfile(models.Model):
    user_profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    location = models.CharField(max_length=100)
    experience = models.CharField(
        choices=EXPERIENCE_CHOICES,
        default='B',
        max_length=1)
    photograph = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username}'s profile"


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'experience', 'photograph')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        profile = UserProfile.objects.get(user=instance)
        profile.save()
    except UserProfile.DoesNotExist:
        pass  # Handle cases where the UserProfile doesn't exist


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'password',
            'first_name', 'last_name', 'email'
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['location', 'experience', 'photograph']

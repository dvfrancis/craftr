"""Tests for the UserProfile model and the signal that maintains it."""

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from register.models import UserProfile, create_user_profile


class UserProfileSignalTests(TestCase):
    """
    Cover the post_save handler that guarantees every User has a profile.

    The regression in issue #105 is easy to write a test for that passes
    against the broken code, so read test_saving_a_user_whose_profile_was
    _deleted before changing any of this.
    """

    def test_creating_a_user_creates_a_profile(self):
        """A new User gets exactly one profile."""
        user = User.objects.create_user("newcomer", password="pw")
        self.assertEqual(UserProfile.objects.filter(user=user).count(), 1)

    def test_saving_an_existing_user_does_not_duplicate(self):
        """Re-saving a User leaves the single profile alone."""
        user = User.objects.create_user("repeat", password="pw")
        user.first_name = "Changed"
        user.save()
        self.assertEqual(UserProfile.objects.filter(user=user).count(), 1)

    def test_saving_a_user_whose_profile_was_deleted(self):
        """
        A User with no profile can still be saved (issue #105).

        The instance must be reloaded from the database first. A User caches
        its profile, so calling save() on the same in-memory object that
        created it passes even against the broken handler, and the re-save
        puts the row back and hides the fault from anything asserted later.
        The admin loads the user fresh, which is why it saw the failure.
        """
        user = User.objects.create_user("orphaned", password="pw")
        UserProfile.objects.filter(user=user).delete()

        reloaded = User.objects.get(pk=user.pk)
        self.assertFalse(UserProfile.objects.filter(user=reloaded).exists())

        reloaded.last_name = "Edited"
        reloaded.save()

        self.assertEqual(
            UserProfile.objects.filter(user=reloaded).count(), 1
        )

    def test_raw_saves_are_skipped(self):
        """
        loaddata sends post_save with raw=True and must be ignored.

        Creating related rows while a fixture is still loading can fail, or
        write a row the fixture then tries to create itself.
        """
        user = User.objects.create_user("fixture", password="pw")
        UserProfile.objects.filter(user=user).delete()

        create_user_profile(User, instance=user, created=False, raw=True)

        self.assertFalse(UserProfile.objects.filter(user=user).exists())


class UserProfileModelTests(TestCase):
    """Cover the model's own validation and representation."""

    def setUp(self):
        """Create a user whose profile the tests can work with."""
        self.user = User.objects.create_user("crafter", password="pw")
        self.profile = UserProfile.objects.get(user=self.user)

    def test_clean_rejects_a_missing_location(self):
        """location is required, and clean() says so."""
        self.profile.location = ""
        with self.assertRaises(ValidationError):
            self.profile.clean()

    def test_clean_accepts_a_complete_profile(self):
        """A profile with both fields filled in validates."""
        self.profile.location = "Bristol"
        self.profile.experience = "Beginner"
        self.profile.clean()  # must not raise

    def test_str_names_the_user(self):
        """__str__ is used in the admin, so it should identify the owner."""
        self.assertEqual(str(self.profile), "crafter's profile")

    def test_a_profile_starts_with_no_photograph(self):
        """
        photograph is optional, and empty is the normal state.

        Five of the six production profiles were emptied by register/0004
        when the Cloudinary placeholders were dropped, so templates must
        cope with this rather than treat it as exceptional.
        """
        self.assertFalse(self.profile.photograph)

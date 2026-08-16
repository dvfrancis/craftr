"""Tests for logging in."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from django.conf import settings


class LoginTests(TestCase):
    """Cover the login page and the authentication round trip."""

    def setUp(self):
        """Create a user to log in as."""
        self.user = User.objects.create_user("crafter", password="s3cret-pw")

    def test_page_renders(self):
        """The login page is public and returns 200."""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/login.html")

    def test_valid_credentials_log_the_user_in(self):
        """Correct details authenticate and redirect away from the form."""
        response = self.client.post(
            reverse("login"),
            {"username": "crafter", "password": "s3cret-pw"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("_auth_user_id", self.client.session)

    def test_a_successful_login_lands_on_the_account_page(self):
        """LOGIN_REDIRECT_URL sends a user to their own details."""
        response = self.client.post(
            reverse("login"),
            {"username": "crafter", "password": "s3cret-pw"},
            follow=True,
        )
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)

    def test_a_wrong_password_does_not_log_anyone_in(self):
        """Bad credentials re-render the form rather than authenticating."""
        response = self.client.post(
            reverse("login"),
            {"username": "crafter", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_an_unknown_user_does_not_log_in(self):
        """A username that does not exist is refused the same way."""
        response = self.client.post(
            reverse("login"),
            {"username": "nobody", "password": "s3cret-pw"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

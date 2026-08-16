"""Tests for the landing page."""

from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    """Cover home.home_page, which holds no models and renders one template."""

    def test_page_renders(self):
        """The landing page is public and returns 200."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")

    def test_images_are_served_from_the_repository(self):
        """
        The landing page images are static files, not uploaded media.

        All fifteen decorative images moved into the repository in issue
        #112 so that S3 holds only genuinely uploaded content. A Cloudinary
        URL reappearing here would mean that had been undone.
        """
        content = self.client.get(reverse("home")).content.decode()
        self.assertIn("/static/craftr/images/", content)
        self.assertNotIn("res.cloudinary.com", content)

    def test_links_to_the_diary(self):
        """The page's main call to action points at the class list."""
        response = self.client.get(reverse("home"))
        self.assertContains(response, reverse("diary"))

"""Tests for the FAQ page."""

from django.test import TestCase
from django.urls import reverse


class FaqPageTests(TestCase):
    """Cover faq.faq_page, which holds no models and renders one template."""

    def test_page_renders(self):
        """The FAQ page is public and returns 200."""
        response = self.client.get(reverse("faq"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "faq/faq.html")

    def test_uses_the_shared_base_template(self):
        """
        The page extends base.html, so it gets the nav and the toast area.

        Worth asserting, because a template that stops extending the base
        still renders and still returns 200, but loses the navigation
        without any error to notice.
        """
        response = self.client.get(reverse("faq"))
        self.assertTemplateUsed(response, "base.html")

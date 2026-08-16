"""Tests for the contact form and the notification it sends."""

from unittest.mock import patch

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from contact.models import Contact


VALID = {
    "first_name": "Ada",
    "last_name": "Lovelace",
    "email": "ada@example.com",
    "message": "Do you run beginner sessions?",
}


class ContactFormTests(TestCase):
    """
    Cover contact.contact_page.

    The important behaviour is the order: the submission is saved before the
    email is attempted, and a failure to send is swallowed. An enquiry is
    never lost because a mail server was unreachable, and the visitor is not
    shown an error that would only prompt them to submit again.
    """

    def setUp(self):
        """Remember the contact URL."""
        self.url = reverse("contact")

    def test_page_renders(self):
        """The form is reachable without logging in."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_a_valid_submission_is_stored(self):
        """The enquiry is written to the database."""
        self.client.post(self.url, VALID)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.first().email, "ada@example.com")

    def test_a_valid_submission_sends_a_notification(self):
        """One email goes out per accepted enquiry."""
        self.client.post(self.url, VALID)
        self.assertEqual(len(mail.outbox), 1)

    def test_the_notification_replies_to_the_visitor(self):
        """
        The email is sent from and to the site's own address.

        The visitor's address is not one SES may send as, so it goes in
        reply_to instead. Getting this wrong meant nothing was delivered at
        all before the fix in the SES migration.
        """
        self.client.post(self.url, VALID)
        sent = mail.outbox[0]
        self.assertEqual(sent.from_email, "craftr@dominicfrancis.co.uk")
        self.assertEqual(sent.to, ["craftr@dominicfrancis.co.uk"])
        self.assertEqual(sent.reply_to, ["ada@example.com"])

    def test_the_enquiry_survives_a_failed_send(self):
        """
        A send failure must not lose the enquiry or alarm the visitor.

        The submission is saved first, so it is already safe. The visitor is
        redirected exactly as on success, because from their point of view
        the message was received.
        """
        with patch(
            "contact.views.EmailMessage.send",
            side_effect=Exception("SMTP unavailable"),
        ):
            # assertLogs both proves the failure is recorded rather than
            # silently discarded, and keeps the traceback out of the test
            # output where it reads like a real error.
            with self.assertLogs("contact.views", level="ERROR") as logged:
                response = self.client.post(self.url, VALID)

        self.assertEqual(Contact.objects.count(), 1)
        self.assertRedirects(response, reverse("home"))
        self.assertIn("SMTP unavailable", "\n".join(logged.output))

    def test_an_invalid_submission_is_not_stored(self):
        """A bad email address means nothing is written."""
        response = self.client.post(self.url, {**VALID, "email": "not-valid"})
        self.assertEqual(Contact.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_missing_fields_are_rejected(self):
        """Every field on the form is required."""
        response = self.client.post(self.url, {"first_name": "Ada"})
        self.assertEqual(Contact.objects.count(), 0)
        self.assertEqual(response.status_code, 200)

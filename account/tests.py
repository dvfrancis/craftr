"""Tests for the account page and its enrolment listing."""

import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from details.models import Enrolment, EventClass
from diary.models import EventDay


class UserDetailsViewTests(TestCase):
    """
    Cover account.user_details, which lists a user's enrolments.

    The ordering is the interesting part: enrolments are shown by event day
    and then by start time, so a visitor reads their timetable in the order
    it happens rather than the order they signed up.
    """

    def setUp(self):
        """Create two days, three classes and a logged-in user."""
        self.day_one = EventDay.objects.create(
            day_date=datetime.date(2026, 9, 1),
            day_title="Day One",
            day_description="First",
        )
        self.day_two = EventDay.objects.create(
            day_date=datetime.date(2026, 9, 2),
            day_title="Day Two",
            day_description="Second",
        )
        self.user = User.objects.create_user("crafter", password="pw")
        self.client.force_login(self.user)

    def _make_class(self, day, start, title):
        """Create a class on a day at a given start time."""
        return EventClass.objects.create(
            event_day=day,
            start_time=start,
            end_time="23:00",
            class_title=title,
            class_description="d",
            difficulty="Beginner",
            instructor="Ada",
            instructor_bio="b",
        )

    def test_requires_login(self):
        """The account page is not public."""
        self.client.logout()
        response = self.client.get(reverse("account"))
        self.assertEqual(response.status_code, 302)

    def test_enrolments_are_ordered_by_day_then_start_time(self):
        """
        Enrolments come back in timetable order, not creation order.

        They are deliberately created in the wrong order so that a view
        which forgot to sort would fail this.
        """
        late_day_one = self._make_class(self.day_one, "16:00", "Late")
        day_two_class = self._make_class(self.day_two, "09:00", "Next day")
        early_day_one = self._make_class(self.day_one, "09:00", "Early")

        for event_class in (day_two_class, late_day_one, early_day_one):
            Enrolment.objects.create(
                user=self.user, enrolled_class=event_class
            )

        response = self.client.get(reverse("account"))
        titles = [
            e.enrolled_class.class_title
            for e in response.context["enrolments"]
        ]
        self.assertEqual(titles, ["Early", "Late", "Next day"])

    def test_a_user_sees_only_their_own_enrolments(self):
        """Another user's enrolments must not appear."""
        mine = self._make_class(self.day_one, "09:00", "Mine")
        theirs = self._make_class(self.day_one, "11:00", "Theirs")
        other = User.objects.create_user("someone", password="pw")
        Enrolment.objects.create(user=self.user, enrolled_class=mine)
        Enrolment.objects.create(user=other, enrolled_class=theirs)

        response = self.client.get(reverse("account"))
        titles = [
            e.enrolled_class.class_title
            for e in response.context["enrolments"]
        ]
        self.assertEqual(titles, ["Mine"])

    def test_page_renders_with_no_enrolments(self):
        """A user who has enrolled on nothing still gets a page."""
        response = self.client.get(reverse("account"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["enrolments"]), [])

    def test_default_profile_image_is_a_static_file(self):
        """
        The fallback comes from settings, not from Cloudinary.

        This was built from the Cloudinary cloud name at request time until
        issue #112, so it broke the moment that setting went away.
        """
        response = self.client.get(reverse("account"))
        self.assertIn(
            "profile-placeholder", response.context["default_profile_url"]
        )

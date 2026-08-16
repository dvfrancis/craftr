"""Tests for the enrol view and the class and enrolment models."""

import datetime

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from details.models import Enrolment, EventClass
from diary.models import EventDay


def make_class(day, start="09:00", title="Vinyl Cutting"):
    """
    Build an EventClass for a given day.

    Args:
        day (EventDay): The day the class belongs to.
        start (str): Start time as HH:MM.
        title (str): Class title.

    Returns:
        EventClass: The saved instance.
    """
    return EventClass.objects.create(
        event_day=day,
        start_time=start,
        end_time="10:00",
        class_title=title,
        class_description="Description",
        difficulty="Beginner",
        instructor="Ada",
        instructor_bio="Bio",
    )


class EnrolViewTests(TestCase):
    """
    Cover details.enrol, which serves the page and handles both POSTs.

    Enrol and withdraw arrive at the same URL and are told apart by an
    "action" field, so the wrong value must not quietly do the other one.
    """

    def setUp(self):
        """Create a day, a class and a logged-out user."""
        self.day = EventDay.objects.create(
            day_date=datetime.date(2026, 9, 1),
            day_title="Day One",
            day_description="First day",
        )
        self.event_class = make_class(self.day)
        self.user = User.objects.create_user("crafter", password="pw")
        self.url = reverse("details", args=[self.event_class.id])

    def test_page_renders_for_an_anonymous_visitor(self):
        """The class page is public, and shows nobody as enrolled."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["is_enrolled"])

    def test_enrolling_creates_one_enrolment(self):
        """A logged-in user posting action=enrol is enrolled."""
        self.client.force_login(self.user)
        response = self.client.post(self.url, {"action": "enrol"})
        self.assertRedirects(response, self.url)
        self.assertEqual(
            Enrolment.objects.filter(
                user=self.user, enrolled_class=self.event_class
            ).count(),
            1,
        )

    def test_enrolling_twice_does_not_duplicate(self):
        """
        A second enrol is ignored rather than raising.

        The view checks is_enrolled first, so the unique constraint is a
        backstop rather than the mechanism.
        """
        self.client.force_login(self.user)
        self.client.post(self.url, {"action": "enrol"})
        self.client.post(self.url, {"action": "enrol"})
        self.assertEqual(Enrolment.objects.count(), 1)

    def test_withdrawing_removes_the_enrolment(self):
        """action=remove deletes an existing enrolment."""
        self.client.force_login(self.user)
        Enrolment.objects.create(
            user=self.user, enrolled_class=self.event_class
        )
        self.client.post(self.url, {"action": "remove"})
        self.assertEqual(Enrolment.objects.count(), 0)

    def test_withdrawing_when_not_enrolled_changes_nothing(self):
        """action=remove without an enrolment is a no-op, not an error."""
        self.client.force_login(self.user)
        response = self.client.post(self.url, {"action": "remove"})
        self.assertRedirects(response, self.url)
        self.assertEqual(Enrolment.objects.count(), 0)

    def test_an_unrecognised_action_does_nothing(self):
        """
        An unknown action must not fall through to enrol or withdraw.

        Both branches are guarded by an explicit action value, so anything
        else lands in the warning branch.
        """
        self.client.force_login(self.user)
        self.client.post(self.url, {"action": "something-else"})
        self.assertEqual(Enrolment.objects.count(), 0)

    def test_a_missing_class_is_a_404(self):
        """An id with no class behind it returns 404, not a 500."""
        response = self.client.get(reverse("details", args=[999999]))
        self.assertEqual(response.status_code, 404)

    def test_placeholder_is_used_when_a_class_has_no_image(self):
        """
        A class with no image renders the static fallback.

        ImageField.url raises ValueError when empty, so this is guarded in
        the template with {% if %} rather than a |default: filter, which
        cannot catch it.
        """
        response = self.client.get(self.url)
        self.assertContains(response, "class-placeholder")


class EventClassModelTests(TestCase):
    """Cover the EventClass constraints and validation."""

    def setUp(self):
        """Create a day for the classes to hang off."""
        self.day = EventDay.objects.create(
            day_date=datetime.date(2026, 9, 1),
            day_title="Day One",
            day_description="First day",
        )

    def test_two_classes_cannot_share_a_start_time_on_one_day(self):
        """
        The unique constraint is on (event_day, start_time).

        Its name says unique_class_title_case_insensitive, which describes
        neither the fields nor the behaviour. The constraint is what counts.
        """
        make_class(self.day, start="09:00", title="First")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                make_class(self.day, start="09:00", title="Second")

    def test_the_same_start_time_on_a_different_day_is_allowed(self):
        """The constraint is per day, not global."""
        other = EventDay.objects.create(
            day_date=datetime.date(2026, 9, 2),
            day_title="Day Two",
            day_description="Second day",
        )
        make_class(self.day, start="09:00")
        make_class(other, start="09:00")
        self.assertEqual(EventClass.objects.count(), 2)

    def test_reverse_accessor_is_named_event_day(self):
        """
        Classes are reached from a day as day.event_day.all().

        related_name is "event_day", so the accessor reads like the forward
        field rather than a collection. diary.html depends on this.
        """
        made = make_class(self.day)
        self.assertIn(made, self.day.event_day.all())


class EnrolmentModelTests(TestCase):
    """Cover the enrolment uniqueness rule."""

    def setUp(self):
        """Create a user and a class to enrol on."""
        self.day = EventDay.objects.create(
            day_date=datetime.date(2026, 9, 1),
            day_title="Day One",
            day_description="First day",
        )
        self.event_class = make_class(self.day)
        self.user = User.objects.create_user("crafter", password="pw")

    def test_a_user_cannot_enrol_twice_on_one_class(self):
        """The unique constraint on (user, enrolled_class) holds."""
        Enrolment.objects.create(
            user=self.user, enrolled_class=self.event_class
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Enrolment.objects.create(
                    user=self.user, enrolled_class=self.event_class
                )

    def test_two_users_can_enrol_on_the_same_class(self):
        """Uniqueness is per user, not per class."""
        other = User.objects.create_user("second", password="pw")
        Enrolment.objects.create(
            user=self.user, enrolled_class=self.event_class
        )
        Enrolment.objects.create(user=other, enrolled_class=self.event_class)
        self.assertEqual(Enrolment.objects.count(), 2)

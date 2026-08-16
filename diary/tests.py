"""Tests for the diary page and the EventDay model."""

import datetime

from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from details.models import EventClass
from diary.models import EventDay


class DiaryViewTests(TestCase):
    """Cover diary.diary_details, which lists days and their classes."""

    def setUp(self):
        """Create two days out of order, to prove the view sorts them."""
        self.later = EventDay.objects.create(
            day_date=datetime.date(2026, 9, 3),
            day_title="Day Three",
            day_description="Third",
        )
        self.earlier = EventDay.objects.create(
            day_date=datetime.date(2026, 9, 1),
            day_title="Day One",
            day_description="First",
        )

    def test_days_are_listed_in_date_order(self):
        """Created out of order, shown in order."""
        response = self.client.get(reverse("diary"))
        titles = [day.day_title for day in response.context["days"]]
        self.assertEqual(titles, ["Day One", "Day Three"])

    def test_page_renders_with_no_days(self):
        """An empty diary is a page, not an error."""
        EventDay.objects.all().delete()
        response = self.client.get(reverse("diary"))
        self.assertEqual(response.status_code, 200)

    def test_a_class_with_no_image_does_not_break_the_page(self):
        """
        The diary template was unguarded until issue #112.

        ImageField.url raises ValueError when the field is empty, so an
        imageless class would have produced a 500 here. It never did only
        because every class in production happened to have an image.
        """
        EventClass.objects.create(
            event_day=self.earlier,
            start_time="09:00",
            end_time="10:00",
            class_title="No picture",
            class_description="d",
            difficulty="Beginner",
            instructor="Ada",
            instructor_bio="b",
        )
        response = self.client.get(reverse("diary"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "class-placeholder")


class EventDayModelTests(TestCase):
    """Cover the EventDay title constraint."""

    def setUp(self):
        """Create a day for the duplicate tests to collide with."""
        self.day = EventDay.objects.create(
            day_date=datetime.date(2026, 9, 1),
            day_title="Opening Day",
            day_description="First",
        )

    def test_an_identical_title_is_rejected(self):
        """The unique constraint on day_title holds for an exact match."""
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                EventDay.objects.create(
                    day_date=datetime.date(2026, 9, 2),
                    day_title="Opening Day",
                    day_description="Second",
                )

    def test_the_constraint_is_not_actually_case_insensitive(self):
        """
        A title differing only in case IS accepted, despite the name.

        The constraint is called unique_event_title_case_insensitive and its
        docstring claims uniqueness "regardless of case sensitivity", but it
        is a plain unique index on day_title carrying the always-true
        condition Q(day_title__iexact=F('day_title')). That condition makes
        it a partial index over every row; it does not fold case.

        This test records what the code does rather than what it says. If
        case-insensitive uniqueness is wanted, the constraint needs
        Lower('day_title') as an expression, and this test should then be
        inverted.
        """
        EventDay.objects.create(
            day_date=datetime.date(2026, 9, 2),
            day_title="OPENING DAY",
            day_description="Second",
        )
        self.assertEqual(EventDay.objects.count(), 2)

    def test_str_is_the_date_not_the_title(self):
        """
        __str__ returns the date, which is what the admin dropdowns show.

        Worth pinning down, because "Opening Day" would be the more useful
        label and it is easy to assume that is what appears. Changing it is
        a deliberate decision, not a tidy-up, so this test should fail if
        anyone makes it.
        """
        self.assertEqual(str(self.day), "2026-09-01")

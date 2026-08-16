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

    def test_a_title_differing_only_by_case_is_rejected(self):
        """
        Uniqueness folds case, which is what the constraint name promises.

        Until issue #127 this passed the wrong way round: the constraint
        carried the always-true condition Q(day_title__iexact=F(day_title)),
        which decides which rows an index covers rather than how their
        values are compared, so it folded no case whatsoever.
        """
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                EventDay.objects.create(
                    day_date=datetime.date(2026, 9, 2),
                    day_title="OPENING DAY",
                    day_description="Second",
                )

    def test_mixed_case_variants_are_all_rejected(self):
        """Any casing of an existing title collides, not just upper case."""
        for variant in ("opening day", "OpEnInG dAy", "Opening DAY"):
            with self.subTest(variant=variant):
                with self.assertRaises(IntegrityError):
                    with transaction.atomic():
                        EventDay.objects.create(
                            day_date=datetime.date(2026, 9, 3),
                            day_title=variant,
                            day_description="Another",
                        )

    def test_a_genuinely_different_title_is_accepted(self):
        """The constraint must not reject titles that merely look similar."""
        EventDay.objects.create(
            day_date=datetime.date(2026, 9, 2),
            day_title="Closing Day",
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

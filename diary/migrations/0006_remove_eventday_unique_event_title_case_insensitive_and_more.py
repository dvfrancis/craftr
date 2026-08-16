"""
Make the EventDay title constraint genuinely case insensitive (issue #127).

The old constraint carried condition=Q(day_title__iexact=F('day_title')),
which is true for every row and therefore folded no case. day_title also had
unique=True, and that field flag is what actually rejected exact duplicates.
Both are replaced here by one constraint on Lower('day_title'), which is
strictly stronger than either.

The check below runs first because this migration can legitimately fail. If
two rows already differ only by case, the new index cannot be built, and the
error PostgreSQL raises names the index rather than the rows. Failing early
with the offending titles is the difference between a two-minute fix and a
puzzle.
"""

import django.db.models.functions.text
from django.db import migrations, models


def reject_existing_case_collisions(apps, schema_editor):
    """
    Refuse to migrate if two titles already differ only by case.

    Args:
        apps: Historical model registry supplied by Django.
        schema_editor: Unused; this inspects data only.

    Returns:
        None.

    Raises:
        RuntimeError: If any two rows share a lowercased title, listing them
            so they can be corrected before the migration is retried.
    """
    EventDay = apps.get_model("diary", "EventDay")
    seen = {}
    clashes = []
    for pk, title in EventDay.objects.values_list("id", "day_title"):
        key = (title or "").lower()
        if key in seen:
            clashes.append(f"{seen[key]!r} and {title!r}")
        else:
            seen[key] = title
    if clashes:
        raise RuntimeError(
            "Cannot apply a case-insensitive unique constraint: these event "
            "day titles differ only by case, so one of each pair must be "
            "renamed first - " + "; ".join(clashes)
        )


def noop(apps, schema_editor):
    """
    Do nothing when reversing.

    The check guards the forward direction only; removing a constraint
    cannot fail on data.

    Args:
        apps: Unused.
        schema_editor: Unused.

    Returns:
        None.
    """


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0005_rename_class_date_eventday_day_date'),
    ]

    operations = [
        migrations.RunPython(reject_existing_case_collisions, noop),
        migrations.RemoveConstraint(
            model_name='eventday',
            name='unique_event_title_case_insensitive',
        ),
        migrations.AlterField(
            model_name='eventday',
            name='day_title',
            field=models.CharField(max_length=100),
        ),
        migrations.AddConstraint(
            model_name='eventday',
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower('day_title'),
                name='unique_event_title_case_insensitive',
            ),
        ),
    ]

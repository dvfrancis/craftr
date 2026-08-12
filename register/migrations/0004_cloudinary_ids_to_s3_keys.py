"""
Rewrite profile photographs from Cloudinary IDs to S3 keys.

Part of issue #112, and the counterpart to details/0012. Runs after 0003 has
changed the field type, so the historical model hands back plain strings.

Of the six profiles in production on 12 August 2026, five held the bare
default "image/upload/placeholder" and only one held a real photograph. The
five are emptied; account.html already falls through to the default image
when photograph is falsy, so nothing on the page changes.
"""

import re

from django.db import migrations


# See details/0012 for the shape this matches and why the version and format
# groups are both optional.
CLOUDINARY_VALUE = re.compile(
    r"^(?P<resource_type>[^/]+)/(?P<type>[^/]+)/"
    r"(?:v(?P<version>\d+)/)?"
    r"(?P<public_id>[^/]+?)"
    r"(?:\.(?P<format>[^.]+))?$"
)

PREFIX = "profiles"


def to_s3_keys(apps, schema_editor):
    """
    Convert each stored Cloudinary value into its S3 key.

    Args:
        apps: Historical model registry supplied by Django.
        schema_editor: Unused; the change is data only.

    Returns:
        None.
    """
    UserProfile = apps.get_model("register", "UserProfile")
    for row in UserProfile.objects.all():
        stored = str(getattr(row, "photograph") or "")
        parsed = CLOUDINARY_VALUE.match(stored)
        if parsed is None:
            continue
        if parsed.group("format"):
            new = (
                f"{PREFIX}/{parsed.group('public_id')}"
                f".{parsed.group('format')}"
            )
        else:
            new = ""
        if new != stored:
            row.photograph = new
            row.save(update_fields=["photograph"])


def to_cloudinary_ids(apps, schema_editor):
    """
    Rebuild Cloudinary values from the S3 keys, for a rollback.

    The version segment is not recoverable but is not needed: Cloudinary
    serves the same object without it. An emptied row returns to the
    placeholder default it held before.

    Args:
        apps: Historical model registry supplied by Django.
        schema_editor: Unused; the change is data only.

    Returns:
        None.
    """
    UserProfile = apps.get_model("register", "UserProfile")
    for row in UserProfile.objects.all():
        stored = str(row.photograph or "")
        if not stored:
            row.photograph = "image/upload/placeholder"
        elif stored.startswith(f"{PREFIX}/"):
            row.photograph = f"image/upload/{stored[len(PREFIX) + 1:]}"
        row.save(update_fields=["photograph"])


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_alter_userprofile_photograph'),
    ]

    operations = [
        migrations.RunPython(to_s3_keys, to_cloudinary_ids),
    ]

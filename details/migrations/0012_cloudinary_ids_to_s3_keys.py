"""
Rewrite class and instructor images from Cloudinary IDs to S3 keys.

Part of issue #112. Runs after 0011 has changed the field type, so the
historical model hands back plain strings rather than CloudinaryResource
objects.

The objects must already be in the bucket before this is applied. See the
copy_media_to_s3 management command, which had to be run first: this
migration rewrites the rows to point at S3, and if the files are not there
yet every class image on the site 404s until they are.

The reverse below no longer leads anywhere. It still runs, but the cloudinary
package was removed once this had proved itself in production, so 0011 cannot
be unapplied and the values it rebuilds have no backend to serve them.
Recovering from here means restoring a database snapshot, not migrating
backwards.
"""

import re

from django.db import migrations


# What CloudinaryField stored, as built by CloudinaryResource.get_prep_value:
# "<resource_type>/<type>/[v<version>/]<public_id>[.<format>]". Both the
# version and the format are optional, which is how the placeholder rows are
# stored - bare "image/upload/class_placeholder" with neither.
CLOUDINARY_VALUE = re.compile(
    r"^(?P<resource_type>[^/]+)/(?P<type>[^/]+)/"
    r"(?:v(?P<version>\d+)/)?"
    r"(?P<public_id>[^/]+?)"
    r"(?:\.(?P<format>[^.]+))?$"
)

FIELDS = (("class_image", "classes"), ("instructor_image", "instructors"))


def to_s3_keys(apps, schema_editor):
    """
    Convert every stored Cloudinary value into its S3 key.

    Rows holding a placeholder are emptied rather than translated. Those
    three images are decorative and now live in the repository, reached
    through the DEFAULT_*_IMAGE_URL settings, so there is no object in the
    bucket for them to point at.

    Args:
        apps: Historical model registry supplied by Django.
        schema_editor: Unused; the change is data only.

    Returns:
        None.
    """
    EventClass = apps.get_model("details", "EventClass")
    for row in EventClass.objects.all():
        changed = False
        for field, prefix in FIELDS:
            stored = getattr(row, field) or ""
            parsed = CLOUDINARY_VALUE.match(str(stored))
            if parsed is None:
                continue
            if parsed.group("format"):
                new = (
                    f"{prefix}/{parsed.group('public_id')}"
                    f".{parsed.group('format')}"
                )
            else:
                new = ""
            if new != str(stored):
                setattr(row, field, new)
                changed = True
        if changed:
            row.save(update_fields=[f for f, _ in FIELDS])


def to_cloudinary_ids(apps, schema_editor):
    """
    Rebuild Cloudinary values from the S3 keys, for a rollback.

    The original version segment is not recoverable, but Cloudinary serves
    the same object without it - verified against the live account - so the
    rebuilt value resolves to the same image.

    An emptied row becomes the placeholder it started as, which is the only
    sensible reverse: the row carried no real image in either direction.

    Args:
        apps: Historical model registry supplied by Django.
        schema_editor: Unused; the change is data only.

    Returns:
        None.
    """
    EventClass = apps.get_model("details", "EventClass")
    defaults = {
        "class_image": "image/upload/class_placeholder",
        "instructor_image": "image/upload/instructor_placeholder",
    }
    for row in EventClass.objects.all():
        for field, prefix in FIELDS:
            stored = str(getattr(row, field) or "")
            if not stored:
                setattr(row, field, defaults[field])
            elif stored.startswith(f"{prefix}/"):
                name = stored[len(prefix) + 1:]
                setattr(row, field, f"image/upload/{name}")
        row.save(update_fields=[f for f, _ in FIELDS])


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0011_alter_eventclass_class_image_and_more'),
    ]

    operations = [
        migrations.RunPython(to_s3_keys, to_cloudinary_ids),
    ]

"""
Copy every uploaded image from Cloudinary into the S3 media bucket.

This is a one-off migration step for issue #112, kept as a management command
rather than a loose script so it runs with the application's own settings and
database connection.

It must run BEFORE the model fields are swapped from CloudinaryField to
ImageField, because the cutover rewrites each database row to an S3 key. If
the rows are rewritten while the objects are still only in Cloudinary, every
image on the site breaks until the copy finishes.

Run it with --dry-run first. It prints exactly what it would copy and touches
nothing.
"""

import re

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connection

import urllib.request
import urllib.error


# Matches what CloudinaryField writes to the column, which is
# "<resource_type>/<type>/[v<version>/]<public_id>[.<format>]" as built by
# CloudinaryResource.get_prep_value. The version segment is optional and the
# format is too: the placeholder rows are stored as bare
# "image/upload/placeholder" with neither.
CLOUDINARY_VALUE = re.compile(
    r"^(?P<resource_type>[^/]+)/(?P<type>[^/]+)/"
    r"(?:v(?P<version>\d+)/)?"
    r"(?P<public_id>[^/]+?)"
    r"(?:\.(?P<format>[^.]+))?$"
)

# Which table and column maps to which destination prefix. The prefixes have
# to match both the upload_to values on the models and the IAM policy in
# infra/media-permissions.yaml, or uploads are denied after the cutover.
SOURCES = (
    ("details_eventclass", "class_image", "classes"),
    ("details_eventclass", "instructor_image", "instructors"),
    ("register_userprofile", "photograph", "profiles"),
)


class Command(BaseCommand):
    help = "Copy uploaded images from Cloudinary into the S3 media bucket."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List what would be copied without writing anything.",
        )
        parser.add_argument(
            "--bucket",
            default="craftr-dominicfrancis",
            help="Destination bucket. Defaults to the production one.",
        )

    def handle(self, *args, **options):
        """
        Copy each stored image from Cloudinary to S3 under its new key.

        Args:
            *args: Unused.
            **options: Parsed command-line options, including dry_run
                and bucket.

        Returns:
            None. Progress and a summary are written to stdout.

        Raises:
            CommandError: If the Cloudinary cloud name is not configured, or
                if boto3 is missing while running for real.
        """
        dry_run = options["dry_run"]
        bucket = options["bucket"]

        cloud = (settings.CLOUDINARY_STORAGE or {}).get("CLOUD_NAME")
        if not cloud:
            raise CommandError(
                "CLOUDINARY_CLOUD_NAME is not set, so there is nothing to "
                "copy from."
            )

        client = None
        if not dry_run:
            try:
                import boto3
            except ImportError as exc:
                raise CommandError(
                    "boto3 is not installed. Add it to requirements.txt and "
                    "redeploy before running this for real."
                ) from exc
            # No credentials here on purpose. On the apps box boto3 picks up
            # the instance role, which infra/media-permissions.yaml grants
            # PutObject on exactly the three prefixes below.
            client = boto3.client(
                "s3", region_name=getattr(
                    settings, "AWS_S3_REGION_NAME", "eu-west-2"
                )
            )

        copied = skipped = present = failed = 0

        for table, column, prefix in SOURCES:
            for stored in self._stored_values(table, column):
                parsed = CLOUDINARY_VALUE.match(stored)
                if parsed is None:
                    self.stderr.write(f"  UNPARSED  {stored}")
                    failed += 1
                    continue

                # A value with no format is a placeholder, not an upload.
                # Those three images are decorative and are served from the
                # repository by WhiteNoise, exactly like the backgrounds and
                # the logo, so they deliberately never reach the bucket.
                if not parsed.group("format"):
                    self.stdout.write(
                        f"  placeholder, not copied: {stored}"
                    )
                    skipped += 1
                    continue

                name = f"{parsed.group('public_id')}.{parsed.group('format')}"
                key = f"{prefix}/{name}"
                url = f"https://res.cloudinary.com/{cloud}/{stored}"

                if dry_run:
                    self.stdout.write(f"  would copy  {url}")
                    self.stdout.write(f"           -> {key}")
                    copied += 1
                    continue

                if self._exists(client, bucket, key):
                    self.stdout.write(f"  already there  {key}")
                    present += 1
                    continue

                try:
                    body, content_type = self._fetch(url)
                except (urllib.error.URLError, urllib.error.HTTPError) as exc:
                    self.stderr.write(f"  FETCH FAILED  {url}: {exc}")
                    failed += 1
                    continue

                client.put_object(
                    Bucket=bucket,
                    Key=key,
                    Body=body,
                    ContentType=content_type,
                )
                self.stdout.write(f"  copied  {key}  ({len(body)} bytes)")
                copied += 1

        self.stdout.write("")
        verb = "would copy" if dry_run else "copied"
        self.stdout.write(
            f"{verb}: {copied}   already present: {present}   "
            f"placeholders skipped: {skipped}   failed: {failed}"
        )
        if failed:
            raise CommandError(
                f"{failed} image(s) could not be copied. The cutover must not "
                f"be deployed until this reports zero failures."
            )

    def _stored_values(self, table, column):
        """
        Read the raw column values, bypassing the model field.

        Reading through the ORM would hand back a CloudinaryResource whose
        __str__ is only the public_id, losing the version and format that the
        source URL needs. Raw SQL also means this command keeps working
        whichever field type is currently on the model.

        Args:
            table (str): Database table name.
            column (str): Column holding the Cloudinary value.

        Returns:
            list[str]: Every non-empty value in that column.
        """
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT {column} FROM {table} "
                f"WHERE {column} IS NOT NULL AND {column} <> ''"
            )
            return [row[0] for row in cursor.fetchall()]

    def _exists(self, client, bucket, key):
        """
        Report whether an object is already in the bucket.

        Args:
            client: A boto3 S3 client.
            bucket (str): Destination bucket name.
            key (str): Object key to test.

        Returns:
            bool: True if the object is present.
        """
        from botocore.exceptions import ClientError

        try:
            client.head_object(Bucket=bucket, Key=key)
            return True
        except ClientError:
            # Any error here means "carry on and try the upload". A genuine
            # permissions problem will surface on put_object with a clearer
            # message than it would here, where 403 and 404 are hard to tell
            # apart without s3:ListBucket.
            return False

    def _fetch(self, url):
        """
        Download one image from Cloudinary.

        Args:
            url (str): Fully qualified Cloudinary delivery URL.

        Returns:
            tuple[bytes, str]: The image bytes and its content type.

        Raises:
            urllib.error.URLError: If the download fails.
        """
        with urllib.request.urlopen(url, timeout=30) as response:
            return (
                response.read(),
                response.headers.get_content_type(),
            )

"""
Settings for running the test suite.

Use with:

    python3 manage.py test --settings=craftr.test_settings

This exists so the suite runs on a clean checkout with no environment set up
and no PostgreSQL server, which is what kept the apps' tests.py files empty
stubs until issue #106.

It changes three things and nothing else. Everything not listed here is
inherited from craftr.settings, so the tests exercise the real configuration.
"""

import os

# Both have no default in craftr.settings, deliberately, so that a
# misconfigured deployment fails loudly instead of running on a placeholder
# key. Tests need neither to be real, and setdefault means a value already in
# the environment still wins.
os.environ.setdefault("SECRET_KEY", "test-only-key-not-used-in-any-deployment")
os.environ.setdefault("DATABASE_URL", "sqlite://")

from craftr.settings import *  # noqa: E402,F401,F403

# Tests never run collectstatic, so there is no staticfiles.json for the
# manifest backend to read, and the first {% static %} tag in any rendered
# template raises "Missing staticfiles manifest entry". The plain backend
# resolves the same paths without hashing them, which is all a test needs.
#
# Production keeps the manifest backend from issue #111; this override applies
# only while the suite is running.
STORAGES = {
    **STORAGES,  # noqa: F405
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Uploads would otherwise try to reach the real S3 bucket. Nothing in the
# suite uploads a file, but pointing this at local temporary storage means a
# test that starts to would fail loudly rather than write to production.
STORAGES["default"] = {
    "BACKEND": "django.core.files.storage.InMemoryStorage",
}

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Craftr is a Django 5.2 site for a fictional three-day digital-crafting event. Visitors browse a diary of event days, drill into individual classes, and register an account to enrol on them. Deployed on an AWS EC2 box behind Gunicorn; uploaded images live in a private S3 bucket served through CloudFront at `media.craftr.dominicfrancis.co.uk`, and transactional email goes through Amazon SES.

## Commands

```bash
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver          # admin at /admin
python3 manage.py makemigrations     # after any models.py change
```

There is **no virtualenv, no `.env`, and no local database** checked in. Both `manage.py` and `runserver` need `DATABASE_URL` and `SECRET_KEY` set before they will start (see Configuration).

### Tests

`python3 manage.py test` runs, but every app's `tests.py` is an untouched three-line stub — there is no automated test suite. Verification for this project is manual and recorded in `TESTING.md` (per-template walkthroughs, user-story checks, browser matrix, fixed-bug log). Extend that document when changing behaviour.

Running `manage.py test` still needs a reachable PostgreSQL server, because Django builds the test database from `DATABASES`. `settings.py` keeps a commented-out SQLite block "for future automated testing"; switching to it is the intended route if a no-Postgres test path is ever wanted.

### Linting

Python is held to PEP 8 at a 79-character limit — every module in the repo already wraps to it, including long setting names split across parenthesised strings. `README.md`/`TESTING.md` cite the Code Institute Python Linter (`https://pep8ci.herokuapp.com/`) and the Flake8 VS Code extension. There is no `setup.cfg`, `.flake8`, or `pyproject.toml`, so `flake8` runs on defaults.

## Architecture

`craftr/` is the project package (settings, root URLconf, WSGI/ASGI, shared `base.html`, site-wide CSS/JS). Eight apps sit at the repo root, each mounted at its own prefix in `craftr/urls.py`.

Only four apps own models; the rest are view-and-template only:

- **diary** — `EventDay` (date, unique title, description).
- **details** — `EventClass` (FK to `EventDay`, start/end times, difficulty, instructor, two `ImageField`s under `classes/` and `instructors/`) and `Enrolment` (unique user × class).
- **register** — `UserProfile`, one-to-one with `auth.User`, carrying location, experience level and an `ImageField` photograph under `profiles/`.
- **contact** — `Contact`, a stored copy of every contact-form submission.

`home`, `faq`, `login`, `account` render pages and hold no models.

The data flow is `EventDay → EventClass → Enrolment`. `details.enrol` is the hub: it serves the class detail page and handles both enrol and withdraw as POSTs on the same URL, keyed on an `action` field. `account.user_details` reads the other direction, listing a user's enrolments ordered by event date then start time.

`UserProfile` is created by a `post_save` signal on `User` in `register/models.py`, so a profile always exists for `request.user.profile` — but the signal calls `instance.profile.save()` on every non-creating `User` save, which means a `User` saved before its profile exists will raise.

Error pages are wired project-wide via `handler404`/`handler500` in `craftr/urls.py`, pointing at `craftr/views.py`. Each app's `urls.py` re-declares the same two handlers; those per-app copies have no effect (Django only reads them from the root URLconf) and are harmless duplication.

### Reverse-accessor naming

`EventClass.event_day` uses `related_name="event_day"`, so from an `EventDay` instance the classes are reached as `day.event_day.all()` — the accessor reads like the forward field, not like a collection. `diary/diary.html` relies on this. `Enrolment` uses `related_name="enrolments"` (from a class) and `related_name="enrol_status"` (from a user).

## Configuration

Everything comes from the environment. `settings.py` calls `load_dotenv()` only when a `.env` file exists in the working directory.

| Variable | Notes |
| --- | --- |
| `SECRET_KEY` | No default. |
| `DATABASE_URL` | Parsed by `dj_database_url` with `ssl_require=True`, so a plain local Postgres without TLS will be rejected. |
| `DEBUG` | String comparison against `'True'`; anything else is false. |
| `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` | Comma-separated. Defaults preserve the old hardcoded Railway/Vercel values so unset behaves as before. |
| `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_REGION_NAME`, `AWS_S3_CUSTOM_DOMAIN` | All default to the production values, so unset works. No AWS credentials are read: boto3 uses the EC2 instance role. |

`DEBUG` also selects the email backend: console when true, `django_ses.SESBackend` (region `eu-west-2`) when false. SES needs no credentials in the app — django-ses uses boto3, which picks up the EC2 instance role. `AWS_SES_AUTO_THROTTLE` is deliberately `None` because django-ses's throttling calls `ses:GetSendQuota`, which cannot be scoped to a resource.

`DEFAULT_FROM_EMAIL` is `craftr@dominicfrancis.co.uk`; the whole domain is DKIM-verified in SES. The contact form sends *from* and *to* that address and sets `reply_to` to the visitor, because the visitor's address is not one SES may send as. It saves the submission first and swallows send failures, so a bounced notification never shows the visitor an error.

## Deployment

`.github/workflows/deploy.yml` fires on push to `main` (or manual dispatch) and holds a `deploy-craftr` concurrency group so two merges cannot overlap. It stores no AWS keys: it exchanges a GitHub OIDC token for temporary credentials via `aws-actions/configure-aws-credentials@v6`, assuming `arn:aws:iam::115019371912:role/github-actions-deploy-craftr` in `eu-west-2`. Both the role and the SSM document are per-repository, so nothing here is shared with the other apps on the box.

The workflow then runs `aws ssm send-command --document-name DeployCraftr --instance-ids i-07bca300c5bb852d9` and polls with `get-command-invocation` rather than `aws ssm wait`, so the remote script's stdout and stderr land in the workflow log whether the deploy passes or fails. **The deploy script itself lives on the EC2 box, not in this repo** — it pulls the commit, installs, migrates (snapshotting the database first if the schema changed), restarts, smoke-tests, and rolls back on failure. Changing deploy behaviour usually means changing that script, not this workflow.

**The IAM role is defined in `apps-box-config/infra/github-actions-deploy-role.yaml`, a different repository.** Change it there and apply the stack; do not edit it by hand in the console. Its trust policy matches the OIDC subject claim as an exact string and pins the repository *name* as well as its immutable ID, so renaming or moving this repo can break deploys. The failure is opaque — `Not authorized to perform sts:AssumeRoleWithWebIdentity` names neither the repository nor the condition that did not match. This has already happened once, to `kanban`.

`Procfile` (`web: gunicorn craftr.wsgi`) is a leftover from Heroku/Railway hosting and is not used by the current AWS deploy.

## Traps

**`staticfiles/` holds 12 files that `collectstatic` cannot regenerate.** The per-app `styles.css` files and three images under `images/` have no source anywhere in the repo; their directories were deleted long ago. Nine of the CSS files are zero bytes. No template references any of them, so they are dead weight rather than a hazard, but `collectstatic --clear` would delete them for good.

The rest of `STATIC_ROOT` is reproducible. `STATICFILES_DIRS` now points at `craftr/static`, and the deploy runs `collectstatic`, so **editing `craftr/static/craftr/base.css` or `base.js` is enough**; the copy under `staticfiles/` is regenerated on deploy and does not need editing by hand. (Before August 2026 it did, because `STATICFILES_DIRS` pointed at a `BASE_DIR/'static'` that has never existed and the project package `craftr` is not in `INSTALLED_APPS`, so `AppDirectoriesFinder` never reached it either.)

**Static storage deliberately uses WhiteNoise's non-manifest backend.** `STORAGES` in `settings.py` sets `CompressedStaticFilesStorage`, not `CompressedManifestStaticFilesStorage`. Manifest storage resolves every `{% static %}` tag through `staticfiles.json` and raises `ValueError` on a miss, so a deploy that skipped `collectstatic` would take the whole site down rather than one page. That risk has since been ruled out (production serves per-file gzip, which only `collectstatic` produces, and the codebase contains just three `{% static %}` references, all with live sources), so switching is now viable if the compression and cache-busting are wanted.

**`requirements.txt` is much wider than the code.** `django-allauth`, `django-ckeditor`, `crispy-forms`, `django-star-ratings`, `stripe` and `django-countries` are pinned but appear in no `INSTALLED_APPS` entry, import, or template. Bootstrap 5.3.5 is loaded from a CDN in `base.html`, not from any Python package.

## Conventions

Every module, class, view and non-trivial method carries a Google-style docstring with `Args:`/`Returns:`/`Raises:` sections; match that when adding code. Comments in `settings.py` and the contact view explain *why* a non-obvious choice was made rather than what the line does — preserve that style. User-facing strings are British English (`enrolment`, `Enrol`), matching `LANGUAGE_CODE = 'en-gb'`. Feedback to users goes through `django.contrib.messages` and surfaces as Bootstrap toasts from `base.html`.

Work happens on branches named `feat/`, `fix/`, `chore/`, `ci/` or `docs/` and lands on `main` by pull request; commits use Conventional Commit prefixes. Merging to `main` deploys to production immediately.

## Media

Uploaded images are `ImageField`s stored in the private `craftr-dominicfrancis`
S3 bucket and served through CloudFront at `media.craftr.dominicfrancis.co.uk`.
The three `upload_to` prefixes (`classes/`, `instructors/`, `profiles/`) are
also named in `infra/media-permissions.yaml`, which scopes the instance role's
write access to exactly those paths — change one without the other and every
upload is denied with an error that names no permission.

The bucket holds only genuinely uploaded content. Decorative images (page
backgrounds, the six landing-page photographs, the logo, and the three
placeholder images) live in `craftr/static/craftr/images/` and are served by
WhiteNoise. Fallbacks for records with no image come from the
`DEFAULT_CLASS_IMAGE_URL`, `DEFAULT_INSTRUCTOR_IMAGE_URL` and
`DEFAULT_PROFILE_IMAGE_URL` settings.

**`ImageField.url` raises `ValueError` when the field is empty, and a
`|default:` filter cannot catch it** — the exception happens during variable
resolution, before any filter runs. Templates must guard with `{% if %}`.

Cloudinary was removed in issue #112. Historical migrations that referenced
`CloudinaryField` now use `CharField(max_length=255)`, which produces an
identical column; do not reintroduce the import, or `migrate` breaks on a
fresh database. The reverse of `details/0012` and `register/0004` still runs
but leads nowhere, since the package is gone: recovery means restoring a
snapshot, not migrating backwards.

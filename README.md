# TAL Chess Academy

A Django website for a chess academy: a public marketing site (home, programs,
coaches, achievements, events, contact) backed by a real database — trial
registrations and contact enquiries are saved to the database, staff manage
them through Django admin, and email notifications go out automatically.

This README assumes little to no prior Django experience and spells out each
step. If a command looks unfamiliar, read the sentence above it before running
it — it explains what the command does and why.

## How the project is organized

```
tal_academy/        Project-wide settings and URL routing
academy/             The app: models, admin, views, API, emails, tests
templates/           HTML pages
static/              CSS and JavaScript
requirements.txt     Python packages this project needs
.env.example          Template listing which environment variables to set
.env                    Your real, private settings (never committed to git)
```

The site has two kinds of URLs:
- **Page routes** (`/`, `/about/`, `/contact/`, etc.) — render the HTML pages.
- **API routes** (`/api/programs/`, `/api/registrations/`, `/api/contact/`) — accept form submissions as JSON. The "Book a Trial" and "Contact" forms on the site submit to these behind the scenes using JavaScript, without reloading the page.

---

## 1. Install dependencies

You need Python 3.12+ installed. Everything else is a Python package.

**Create a virtual environment** — this is a private, isolated copy of Python
just for this project, so its packages don't clash with anything else on your
machine:

```bash
python -m venv venv
```

**Activate it** (you'll need to do this every time you open a new terminal to
work on this project):

- Windows (PowerShell): `venv\Scripts\Activate.ps1`
- Windows (cmd.exe): `venv\Scripts\activate.bat`
- Mac/Linux: `source venv/bin/activate`

Your terminal prompt should now start with `(venv)`. **Install the project's
packages into it:**

```bash
pip install -r requirements.txt
```

This installs Django itself, Django REST Framework (used for the `/api/...`
endpoints), and a handful of small support packages — nothing exotic.

---

## 2. Configure your `.env` file

Real secrets (database passwords, email credentials, etc.) never go directly
in the code — they live in a file called `.env` that stays on your machine
and is never uploaded to GitHub (it's listed in `.gitignore`).

**Copy the template:**

```bash
cp .env.example .env
```

(On Windows without `cp`, just duplicate `.env.example` in File Explorer and
rename the copy to `.env`.)

Open `.env` in a text editor. At minimum, set `SECRET_KEY` to a random string
— you can generate one with:

```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Paste the output after `SECRET_KEY=`. Leave `DATABASE_URL` and the `EMAIL_*`
variables blank for now — sensible local defaults kick in automatically (see
sections 3 and 8 below).

**`SECRET_KEY` is required whenever `DEBUG=False`.** The app will refuse to
start (raising an error instead of running insecurely) if it's missing in
that case — this is deliberate, so a forgotten env var fails loudly instead
of silently running production with a weak, publicly-known key.

---

## 3. Create the database

For local development, this project uses **SQLite** — a database that's just
a single file (`db.sqlite3`) with no separate server to install or run. As
long as `DATABASE_URL` is blank in your `.env`, Django uses it automatically.
There's nothing to "create" — the next step (migrations) creates the file and
its tables for you.

(In production, you'd set `DATABASE_URL` to a real Postgres connection string
instead — see section 9.)

---

## 4. Run migrations

Migrations are Django's way of building (and updating) your database's
tables to match the models defined in `academy/models.py`. Run:

```bash
python manage.py migrate
```

You'll see a list of migrations being applied, including one called
`0002_seed_initial_programs` — that one pre-populates the database with the
five programs (Junior, Beginner, Intermediate, Advanced, Private Coaching)
shown on the site, so you don't start with an empty Programs list.

Run this command again any time you pull code that adds new migrations.

---

## 5. Create an admin account

This account lets you log in to the admin panel to view and manage trial
registrations, contact enquiries, and programs.

```bash
python manage.py createsuperuser
```

It'll ask for a username, email, and password (the password won't be shown
as you type — that's normal). **Choose a genuinely strong, unique password**
— repeated failed logins get locked out for an hour after 5 attempts (via
`django-axes`), but that's a backstop, not a substitute for a strong password.

Once created, you can log in at `http://127.0.0.1:8000/staff-portal/` after
starting the server (next step). The admin path is intentionally not the
well-known `/admin/` — it's controlled by the `ADMIN_URL` env var (defaults
to `staff-portal/`; set your own in `.env` if you'd like a different one).

---

## 6. Start the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser — that's the site. Visit
`http://127.0.0.1:8000/staff-portal/` (or your own `ADMIN_URL`, see step 5)
and log in with the account from step 5 to see the admin panel: registrations
and enquiries under **Academy**, where you can filter by status, search, and
update each one's status (New → Contacted → Trial Scheduled → Enrolled, etc.).

Leave this command running in its terminal while you work; press `Ctrl+C` to
stop it.

---

## 7. Test the API

There are two ways to try the API:

**A) In your browser (easiest).** With the server running, visit
`http://127.0.0.1:8000/api/programs/` — Django REST Framework renders a
readable page showing the JSON response, and even lets you submit test POST
requests to `/api/registrations/` and `/api/contact/` using an HTML form at
the bottom of the page, without writing any code.

**B) With `curl`,** to see the raw JSON:

```bash
curl http://127.0.0.1:8000/api/programs/

curl -X POST http://127.0.0.1:8000/api/contact/ \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Test\",\"email\":\"test@example.com\",\"subject\":\"Hi\",\"message\":\"Hello there\"}"
```

A successful submission returns `{"success": true, "message": "..."}` with
status `201`. An invalid one returns `{"success": false, "errors": {...}}`
with status `400`, listing exactly what was wrong with each field.

**Automated tests.** The project also has a full test suite covering
successful/invalid submissions, spam protection, email sending, and access
control. Run it with:

```bash
python manage.py test academy
```

You should see `OK` at the end with no failures.

---

## 8. Configure email

By default (when `EMAIL_HOST` is blank in `.env`), emails aren't actually
sent anywhere — they're printed to the terminal running `runserver` instead.
This is intentional: it lets you see exactly what an email would say, without
needing a real mail account while developing.

**To send real email**, fill in the `EMAIL_*` variables in `.env`. For
example, using Gmail:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=youracademyemail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=youracademyemail@gmail.com
ACADEMY_NOTIFICATION_EMAIL=info@talchessacademy.example
```

`EMAIL_HOST_PASSWORD` for Gmail must be an **App Password**, not your regular
login password — generate one at
[myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
(requires 2-factor authentication to be enabled on the account). Any other
SMTP provider (SendGrid, Mailgun, your web host's email, etc.) works the same
way — just use the host/port/credentials they give you.

`ACADEMY_NOTIFICATION_EMAIL` is where new registration/enquiry alerts get
sent — it can be different from `DEFAULT_FROM_EMAIL`.

Restart `runserver` after changing `.env` for the change to take effect.

**A submission is never lost if email fails.** The database record is always
saved first; sending the notification/confirmation emails happens afterward
and is "best effort" — if your SMTP settings are wrong or the mail server is
briefly down, the submission still shows up in `/admin/`, and the failure is
written to the server log so you can diagnose it. A 10-second `EMAIL_TIMEOUT`
also means a slow/unreachable mail server fails fast instead of leaving the
visitor's browser hanging on a stuck "submitting…" state.

**You'll also get emailed automatically if the site ever crashes.** Once
`DEBUG=False`, Django emails `ACADEMY_NOTIFICATION_EMAIL` on any unhandled
server error, with the full traceback — no extra setup needed beyond the
email config above.

---

## 9. Deploy the backend

This project is set up to deploy on [Render](https://render.com) using the
`render.yaml` file already in the repo (see `build.sh` for the exact build
steps: install dependencies, collect static files, run migrations).

`render.yaml` already declares the email variables below — Render will show
them in the dashboard as needing a value ("sync: false") rather than
deploying with anything guessed or hardcoded. **The site works without them
filled in** (it falls back to logging emails to the console instead of
sending them — see section 8), but real registrations/enquiries won't
actually reach anyone by email until you set them:

- `SECRET_KEY` — Render auto-generates this for you (already configured in `render.yaml`). **Required** — the app won't start without it once `DEBUG` is off (which it is by default in production).
- `DATABASE_URL` — if you add a Render Postgres database, Render can inject this automatically; otherwise the site falls back to SQLite (fine for low-traffic use, but **data doesn't persist across redeploys on Render's free tier** — don't collect real submissions until this is set).
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`, `ACADEMY_NOTIFICATION_EMAIL` — same values as section 8, set as env vars instead of `.env` entries.
- `ADMIN_URL` — optional, only if you want a different admin login path than the default `staff-portal/`.
- `ALLOWED_HOSTS` — only needed if deploying somewhere other than Render (Render's hostname is detected automatically via `RENDER_EXTERNAL_HOSTNAME`).

Deploying anywhere other than Render works the same way — set the same
environment variables through whatever mechanism that host provides.

After deploying, run the admin-account step (5) against the live service —
Render's dashboard has a "Shell" tab where you can run
`python manage.py createsuperuser` directly on the deployed app.

No background task system (Celery/Redis) is used or needed — see the
docstring at the top of `academy/emails.py` for why that's a deliberate
choice at this project's scale, not an oversight.

**Two other production details, already handled:**
- The web server (`gunicorn`) runs with 2 workers so one slow request (e.g. a form submission waiting on a slow mail server) doesn't block every other visitor — see the `startCommand` in `render.yaml`.
- Branded `404`/`500` error pages, a favicon, and `robots.txt`/`sitemap.xml` are already in place — nothing to configure.
- [Dependabot](https://github.com/dependabot) is enabled (`.github/dependabot.yml`) and will open a PR automatically if a dependency in `requirements.txt` gets a known vulnerability fix.

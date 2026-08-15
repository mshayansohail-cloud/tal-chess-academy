# TAL Chess Academy

A Django website for a chess academy: a public marketing site (home, about,
programs, coaches, events, FAQ, contact) backed by a real database —
trial registrations and contact enquiries are saved to the database, staff
manage them through Django admin, and email notifications go out
automatically. No frontend framework or build step: vanilla CSS and vanilla
JavaScript, on purpose (see "Design conventions" below).

**If you're a Claude session picking this up with no memory of prior work**,
read this whole file before touching code — it captures the architecture,
the deliberate design decisions (and why), and what's genuinely still
outstanding, so you don't have to rediscover any of it by reading every file.

---

## Current status

The app is fully built and functionally complete: real models, admin, API,
email notifications, tests, security hardening, and passes accessibility
(WCAG 2.2 AA) and SEO audits performed earlier in this project's history.
**It is not currently deployed anywhere** — it previously had a Render
config in the repo, which has been deliberately removed (see "Deployment"
below) so the project isn't tied to one host. There is no live URL right now.

What's still placeholder, deliberately, rather than invented to look real:

- **Email address** in `templates/partials/footer.html` and
  `templates/academy/contact.html` — `contact@yourdomain.com` is still an
  obvious placeholder. Replace it with the real business inbox before going
  live. **The phone number (+92 348 3186131) is real** — don't strip it; it
  also feeds the `LocalBusiness` structured data in `base.html` (see below).
- **The street address placeholder has been resolved, differently than
  originally planned.** Rather than eventually swapping "Academy Hall,
  Downtown Centre" for a real street address, every on-site mention of the
  location — the Contact page's own Location field
  (`templates/academy/contact.html`), the footer
  (`templates/partials/footer.html`), and the FAQ page
  (`templates/academy/faq.html`) — now links "TAL Chess Academy" straight to
  the academy's real Google Maps listing
  (`https://maps.app.goo.gl/GR9WaFxk5Cx3HJqL9`, new tab,
  `rel="noopener noreferrer"`) instead of displaying any street address text.
  This is arguably the better long-term answer, not just a workaround — it
  points at the real location instead of a placeholder, and is more useful to
  a visitor than plain address text. See `.location-link` (contact page) and
  `.footer-location` (footer) in `static/css/components.css`, and the
  `icon-pin` symbol added to `templates/partials/icon_sprite.html`. The
  `LocalBusiness` JSON-LD in `base.html` still deliberately omits
  `streetAddress` (see "SEO" below) — that's unrelated and still correct as-is.
- **The fabricated coaches have been removed entirely.** `data.COACHES` is now
  an empty list. It previously held four invented people with invented FIDE
  titles, invented ratings (2612, 2340, …), invented championships and
  federation representation. The whole entry was removed rather than partly
  cleaned, because the *names* were fabricated too — stripping a title off a
  made-up person still leaves a made-up person on the page. Every coach
  template now treats each field as optional and omits whatever is absent, so
  real data can be dropped into `data.COACHES` (see the field reference in
  that file) without touching any template. **Add only what can actually be
  substantiated** — the `credential` badge is for verified, checkable facts
  only. While the list is empty, the Coaches section and `/coaches/` page show
  an honest "profiles coming shortly" message plus the trial CTA, rather than
  an empty grid. All coach-credential claims elsewhere (hero, footer, About,
  `base.html` meta + JSON-LD, `llms.txt`, page metas) were rewritten to
  describe the teaching approach instead of unverifiable credentials.
- **Still invented: the event calendar** (`data.EVENTS`) — three made-up
  events with made-up dates and venues. Same problem class as the coaches,
  not yet addressed. (The homepage's Achievements section and its invented
  stats — 128 tournament victories, 940 students trained, etc. — were removed
  outright, since the academy has no real track record yet to report; the
  Testimonials section — three fabricated student quotes — was removed the
  same way and for the same reason. Add either back once there's something
  real to show.) The `/faq/` page was deliberately written using *only*
  claims already established elsewhere on the site, so it inherits no new
  fabrications — but it will need revisiting once the real coach/programme
  facts land.
- **SMTP credentials** — `EMAIL_HOST` etc. are unset, so emails currently
  print to the console instead of sending. Needs real credentials before
  registration/contact notifications actually reach anyone (see "Email"
  below).
- **No `og:image`** — Open Graph/Twitter Card tags exist (`templates/base.html`)
  but there's no image asset, so social shares fall back to a plain text
  card. Add an image and an `og:image`/`twitter:image` tag if that matters.
- **`SECRET_KEY`** in `.env` is a local dev-only value — generate a fresh one
  for any real deployment (see "Configure your `.env` file" below).
- **`/privacy/`'s content hasn't had legal review** — it's an accurate plain-
  language description of what the code actually does today, and says so
  explicitly, but it isn't a substitute for review by a qualified legal/
  privacy professional, and its retention-period wording needs an actual
  number once one's decided (see "Data retention & privacy" below).

---

## Tech stack

- **Django 6.1** — the whole app: pages, admin, models, ORM.
- **Django REST Framework** — the `/api/...` endpoints the frontend JS talks to.
- **django-axes** — brute-force lockout protection on admin login.
- **WhiteNoise** — serves and compresses static files directly from Django
  (no separate static file server/CDN needed).
- **gunicorn** — production WSGI server.
- **dj-database-url** — parses a `DATABASE_URL` connection string into
  Django's `DATABASES` setting.
- **python-dotenv** — loads `.env` into environment variables locally.
- **SQLite** in development, **Postgres** (or anything `dj-database-url`
  understands) in production via `DATABASE_URL`.
- **No frontend build step.** Plain CSS (with custom-property design tokens
  in `static/css/tokens.css`) and plain JS, loaded directly as static files.
  No npm, no bundler, no framework — this was a deliberate brief, not an
  oversight; don't introduce a build pipeline unless explicitly asked.
- **No CORS** — frontend and API are same-origin, so `django-cors-headers`
  is neither installed nor needed.
- **No Celery/Redis** — emails send synchronously; see the docstring at the
  top of `academy/emails.py` for the explicit reasoning and the note on how
  to swap to async later if volume ever justifies it.

---

## Project structure

```
tal_academy/            Project-wide settings and URL routing
  settings.py              All configuration (env-driven, see below)
  urls.py                  Top-level URL routes

academy/                 The one Django app — all real logic lives here
  models.py                 Program, TrialRegistration, ContactSubmission
  admin.py                   Django admin configuration for those models
  views.py                   Page views (render templates)
  api_views.py                DRF API views (registrations, contact, programs)
  api_urls.py                  /api/... routing
  serializers.py                 DRF serializers + validation
  emails.py                       Best-effort email sending, sync, no queue
  middleware.py                    Adds X-Robots-Tag: noindex to admin/API
  throttling.py                     Per-endpoint DRF throttle classes
  sitemaps.py                        django.contrib.sitemaps classes
  data.py                             Static content NOT in the database (see below)
  tests.py                             Full test suite (models, API, email, security)
  migrations/                          Including one that seeds the 5 initial programs

templates/               HTML (Django template language)
  base.html                 Shared shell: nav, footer, meta tags, skip link
  academy/                    One template per page, plus emails/ (plaintext email bodies)
  partials/                    Reusable includes (navbar, footer, cards, icon sprite)
  404.html, 500.html            Custom branded error pages

static/
  css/                       tokens.css (design tokens), base.css, components.css, animations.css
  js/                        main.js (nav/reveal/interactions), forms.js (AJAX form submission)
  favicon.svg

requirements.txt         Python dependencies
.env.example              Template listing every environment variable
.env                        Your real, private settings — gitignored, never committed
db.sqlite3                   Local dev database (gitignored in real usage; present here for convenience)
```

The site has two kinds of URLs:
- **Page routes** (`/`, `/about/`, `/contact/`, etc.) — `academy/views.py`
  renders server-side HTML templates.
- **API routes** (`/api/programs/`, `/api/registrations/`, `/api/contact/`)
  — accept/return JSON. The "Book a Trial" and "General Enquiry" forms on
  the contact page submit to these via `fetch()` in `static/js/forms.js`,
  without a page reload. `/api/programs/` is also used to hydrate the
  program dropdown.

---

## Data model

Three real database models, all in `academy/models.py`:

- **`Program`** — a course the academy offers (Junior, Beginner,
  Intermediate, Advanced, Private Coaching). Editable in admin. Has
  `is_active` (hide without deleting) and `display_order`. This used to be
  a hardcoded Python list; it was promoted to a real model so staff can
  edit programs without a code deploy. The original five are seeded by
  migration `0002_seed_initial_programs.py`. `highlights` is a `JSONField`
  list of short "what you'll learn" bullets, shown as a collapsed
  `<details>` on the programme row (`partials/program_row.html`) — kept
  short deliberately, this is not a place for a full syllabus.
- **`TrialRegistration`** — a "Book a Trial" submission. Write-only from the
  public API (no GET/list endpoint) — staff only ever read these through
  Django admin. Has a `status` workflow: New → Contacted → Trial Scheduled
  → Enrolled (or Closed).
- **`ContactSubmission`** — a general enquiry. Same write-only pattern, its
  own simpler status workflow (New → In Progress → Resolved/Closed).

**`academy/data.py` deliberately still holds plain Python data** — coaches
(currently an empty list awaiting real details — see "Current status" above),
"Why Us" points, and events. These have no submission workflow and no current
admin-editing requirement, so they were left as code rather than promoted to
models. If a future request needs these editable through admin too, follow the
same pattern used for `Program`: add a model, a migration to seed existing
content, update `admin.py` and the relevant view in `views.py`. Don't do this
preemptively.

---

## Design conventions worth knowing before you edit

- **Security is intentionally strict.** `DEBUG` defaults to `False` (fails
  closed, not open). `SECRET_KEY` raises `ImproperlyConfigured` at startup
  if unset while `DEBUG=False`, rather than silently falling back to an
  insecure key. DRF's `DEFAULT_PERMISSION_CLASSES` defaults to
  `IsAuthenticated` — any new API view is private unless it explicitly opts
  into `AllowAny`, so a forgotten `permission_classes` fails safe. The admin
  login path is `staff-portal/` by default (not `/admin/`), configurable via
  `ADMIN_URL`. `django-axes` locks out an IP+username pair after 5 failed
  admin login attempts for 1 hour. All of this came out of an explicit
  security audit earlier in the project — see git history for the full
  original findings if you need the reasoning behind any specific setting.
- **`CACHES` uses `DatabaseCache`, not Django's `LocMemCache` default —
  deliberately.** The throttles above are only as real as the counter
  backing them: `LocMemCache` is per-*process*, so with more than one
  gunicorn worker each worker keeps its own separate count and the real
  limit silently becomes `workers x configured rate`, resetting on every
  restart. `DatabaseCache` is shared across every worker since they all hit
  the same database — no new infrastructure (no Redis) needed at this
  scale. The table itself is created by migration
  `0004_cache_table.py` (via `call_command('createcachetable', ...)` inside
  `RunPython`, so it generates correct DDL for whatever database backend is
  actually configured rather than hardcoded SQL) — `python manage.py
  migrate` is still the only deploy step needed, nothing extra to remember.
- **The two public API views (`RegistrationCreateAPIView`,
  `ContactCreateAPIView`) explicitly set `authentication_classes = []`.**
  This is load-bearing, not incidental: `SessionAuthentication` enforces
  CSRF whenever it resolves a logged-in session, which would 403 any
  visitor who happens to be logged into `/staff-portal/` in the same
  browser, since `forms.js` never sends a CSRF token (these endpoints don't
  need one — they're `AllowAny` and don't act on behalf of a session).
  Don't remove this without understanding why it's there — it was a real
  bug once (forms silently 403ing for logged-in staff testing their own
  site) before this fix.
- **ALLOWED_HOSTS / CSRF_TRUSTED_ORIGINS are entirely env-driven and
  host-agnostic.** Set `ALLOWED_HOSTS` (comma-separated) in `.env` /
  platform env vars; `CSRF_TRUSTED_ORIGINS` is derived from it
  automatically (`https://` + each host). In `DEBUG` mode, localhost/
  127.0.0.1 and common ngrok domains are added automatically so local dev
  and ngrok tunnel previews work with zero config. This project previously
  had Render-specific auto-detection (`RENDER_EXTERNAL_HOSTNAME`); that's
  been removed entirely — the project is not tied to any one PaaS.
- **Emails are synchronous and best-effort** (see `academy/emails.py`
  docstring). A submission is always saved to the database first; email
  sending happens after and never rolls back or blocks the response if it
  fails — failures are logged, not raised. A 10s `EMAIL_TIMEOUT` prevents a
  slow/dead mail server from hanging a visitor's form submission.
  `ADMINS`/`SERVER_EMAIL` are also configured so Django emails the academy
  automatically on any unhandled server crash in production.
- **The mobile nav's full interaction contract** (see `static/js/main.js`):
  `inert` on the closed menu so its links aren't tab-reachable, closes on
  link click, on click-outside, and on Escape (which also returns focus to
  the toggle button), and `overflow-y: auto` on the menu panel itself so it
  scrolls rather than clipping its own content — this last one is easy to
  lose if the panel's markup changes, and only shows up in landscape
  orientation on a phone (short viewport height), not in normal portrait
  testing, so it's easy to reintroduce without noticing.
- **Accessibility (WCAG 2.2 AA) has already had a full audit-and-fix pass.**
  Notable patterns already in place, worth preserving in any future edits:
  a skip-to-content link; `aria-invalid` +
  `aria-describedby` wired per-field on both forms; full ARIA tabs keyboard
  pattern (arrow keys) on the Book a Trial / General Enquiry toggle;
  `--color-gold-contrast` used instead of the base gold wherever gold text
  sits on the ivory `surface-inverse` background (base gold is ~2.5:1
  contrast there, under the 4.5:1 AA minimum).
- **SEO has already had a full audit-and-fix pass.** Canonical tags, Open
  Graph + Twitter Card meta tags (via `{% block og_title %}` /
  `{% block og_description %}` in `base.html` — note Django templates
  cannot reuse the same block name twice in one template, which is why
  these are separate blocks from `title`/`meta_description` with duplicated
  text, not a shared block), `robots.txt` (see `academy/views.py:robots_txt`)
  disallowing `/staff-portal/` and `/api/`, an `X-Robots-Tag: noindex`
  header on those same paths via `academy/middleware.py`, and
  `django.contrib.sitemaps` wired up in `tal_academy/urls.py` /
  `academy/sitemaps.py`. There's also an `/llms.txt` (see
  `academy/views.py:llms_txt`) — a Markdown summary for AI agents/LLMs
  following the [llms.txt](https://llmstxt.org/) convention, listing the
  same public page set as the sitemap. Both `robots.txt` and `llms.txt`
  build their links with `request.build_absolute_uri()`, so they always
  reflect whatever host actually served the request — no hardcoded domain
  to keep in sync with `ALLOWED_HOSTS`. `base.html` also carries a
  `LocalBusiness`/`EducationalOrganization` JSON-LD block — deliberately
  includes only fields with real values (name, description, phone, city);
  `streetAddress`/`email` are left out entirely rather than filled with the
  placeholders those fields still hold elsewhere on the site, since
  structured data is a machine-readable factual claim, not display copy.
- **`/faq/` uses native `<details>`/`<summary>`**, not a JS accordion —
  keyboard support, focus handling and screen-reader semantics come free, and
  it adds no JavaScript to the page. If you restyle it, keep both
  `list-style: none` and the `::-webkit-details-marker` rule: they suppress
  the default disclosure triangle in different browsers.
- **Inline links need explicit styling.** `base.css` resets `a { color:
  inherit; text-decoration: none }` site-wide, which is right for nav/cards
  but makes inline links inside prose *invisible* — indistinguishable from
  body text. `.prose a`, `.page-header__desc a`, `.faq-item__answer a` and
  `.contact-expect__more a` each opt back in to gold + a hairline underline.
  Any new prose region needs the same treatment.
- **Django template gotchas** hit and worked around in this codebase:
  `{# #}` comments don't support multi-line content (they leak into
  rendered HTML if you try) — use `{% comment %}...{% endcomment %}`
  instead. `{{ block.super }}` only pulls the *parent template's* same-named
  block, not a sibling block in the current template.

---

## Setup (local development)

This section assumes little to no prior Django experience. If a command
looks unfamiliar, read the sentence above it — it explains what and why.

### 1. Install dependencies

You need Python 3.12+.

```bash
python -m venv venv
```

Activate it (every new terminal session):
- Windows (PowerShell): `venv\Scripts\Activate.ps1`
- Windows (cmd.exe): `venv\Scripts\activate.bat`
- Mac/Linux: `source venv/bin/activate`

Your prompt should now start with `(venv)`. Install packages:

```bash
pip install -r requirements.txt
```

### 2. Configure your `.env` file

Real secrets never go directly in code — they live in `.env`, which is
gitignored and never committed.

```bash
cp .env.example .env
```

(No `cp` on Windows? Duplicate `.env.example` in File Explorer and rename
the copy to `.env`.)

At minimum, set `SECRET_KEY` to a random string:

```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Paste the output after `SECRET_KEY=`. Leave `DATABASE_URL` and `EMAIL_*`
blank for now — sensible local defaults kick in (see sections 3 and 8
below). **`SECRET_KEY` is required whenever `DEBUG=False`** — the app
refuses to start without it in that case, on purpose, rather than silently
falling back to an insecure default.

### 3. The database

Local dev uses **SQLite** — a single file (`db.sqlite3`), no server needed.
Leaving `DATABASE_URL` blank in `.env` selects it automatically. Nothing to
manually "create" — the next step does that.

### 4. Run migrations

```bash
python manage.py migrate
```

Includes `0002_seed_initial_programs`, which pre-populates the five
programs shown on the site. Re-run this any time you pull code with new
migrations.

### 5. Create an admin account

```bash
python manage.py createsuperuser
```

Choose a genuinely strong password — `django-axes` locks out repeated
failed attempts (a backstop, not a substitute). Log in at
`http://127.0.0.1:8000/staff-portal/` (or your own `ADMIN_URL` if you set
one) once the server is running.

### 6. Start the dev server

```bash
python manage.py runserver
```

Site: `http://127.0.0.1:8000/`. Admin: `http://127.0.0.1:8000/staff-portal/`
— registrations and enquiries live under **Academy**, filterable/searchable,
with a status field you can update per entry.

### 7. Try the API

**Browser:** with the server running, visit
`http://127.0.0.1:8000/api/programs/` — DRF's browsable API renders the
JSON readably and even lets you POST test submissions via an HTML form
(only shown when `DEBUG=True`; production serves JSON only, deliberately —
see `REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES']` in `settings.py`).

**curl:**

```bash
curl http://127.0.0.1:8000/api/programs/

curl -X POST http://127.0.0.1:8000/api/contact/ \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Test\",\"email\":\"test@example.com\",\"subject\":\"Hi\",\"message\":\"Hello there\"}"
```

A success returns `{"success": true, "message": "..."}` (201). An invalid
submission returns `{"success": false, "errors": {...}}` (400) listing
exactly what was wrong per field.

### 8. Configure email

By default (`EMAIL_HOST` blank), email prints to the console running
`runserver` instead of actually sending — lets you see the content without
a real mail account. To send real email, fill in `EMAIL_*` in `.env`, e.g.
Gmail:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=youracademyemail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=youracademyemail@gmail.com
ACADEMY_NOTIFICATION_EMAIL=info@talchessacademy.example
```

Gmail requires an **App Password** (not your login password) — generate one
at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
(needs 2FA enabled). Any other SMTP provider works the same way with its
own host/port/credentials. `ACADEMY_NOTIFICATION_EMAIL` is where new
submission alerts go — can differ from `DEFAULT_FROM_EMAIL`. Restart
`runserver` after editing `.env`.

A submission is never lost if email fails — the database write always
happens first; email is best-effort afterward (see "Design conventions").
You'll also get emailed automatically if the site crashes in production
(`DEBUG=False`), no extra setup beyond the config above.

---

## Testing

```bash
python manage.py test academy
```

Full suite covering model behavior, successful/invalid API submissions,
spam protection (honeypot field + throttling), email sending (mocked
SMTP failure included), and access control (write-only endpoints, admin
auth). Should finish with `OK`, 20 tests, no failures.

```bash
python manage.py check
```

Django's system check framework — run this after any settings.py change.

---

## Data retention & privacy

A full privacy/data-handling audit was done on this codebase — see git history
for the complete findings. What it led to, concretely:

- **`/privacy/`** — a plain-language privacy policy page (linked from the
  footer, included in the sitemap) describing what the two public forms
  collect, why, who it's shared with, and how to request a copy/correction/
  deletion. It's explicitly labeled as *not* legal advice — review it with
  a qualified professional before using this site to collect data from real
  visitors, and fill in the real retention period once you've decided one
  (see below).
- **`SUBMISSION_RETENTION_DAYS`** (env var, see `.env.example`) — optional,
  no default. When set, `python manage.py purge_old_submissions` deletes
  `TrialRegistration`/`ContactSubmission` rows that are *both* older than
  this many days *and* already in a terminal status (Enrolled/Closed/
  Resolved) — open leads are never touched regardless of age. Use
  `--dry-run` to preview counts first. This isn't scheduled automatically;
  run it manually or wire it into a cron/scheduled task on your host once
  you've decided on an actual retention period — this command deliberately
  doesn't guess one for you.
- **`django-axes`'s own failed-login records** (IP + username, on admin
  login attempts) aren't covered by the command above — axes ships its own
  `python manage.py axes_reset_logs --age <days>` for that; also worth
  scheduling periodically if you want those pruned too.
- **Email failure logs don't include submitter PII** — `academy/emails.py`
  logs the template name on a send failure, not the subject (which could
  contain a student's name) or the recipient address.
- **Fonts are self-hosted** (`static/fonts/`, `static/css/fonts.css`) rather
  than loaded from Google Fonts — no third-party font request means no
  visitor IP/User-Agent goes to Google on page load. Only the Latin subset
  is included, which covers everything this site's content actually uses;
  if you add content requiring other scripts, you'll need to source
  additional subsets.

---

## Deployment

This project is **host-agnostic on purpose** — no PaaS-specific config file
is checked in (a previous Render Blueprint config was deliberately removed
so the project isn't tied to one platform). To deploy anywhere (a VPS,
Railway, Fly.io, PythonAnywhere, Render, etc.), the pattern is the same:

1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables on the host (same names as `.env.example`):
   - `SECRET_KEY` — **required**. Generate with the command in step 2 above.
   - `DEBUG` — leave unset or `False` in production.
   - `ALLOWED_HOSTS` — **required**. Comma-separated real domain(s), e.g.
     `example.com,www.example.com`. `CSRF_TRUSTED_ORIGINS` derives from
     this automatically.
   - `DATABASE_URL` — a Postgres connection string is strongly recommended
     for anything beyond a demo; SQLite has no persistence guarantee across
     redeploys on most platforms.
   - `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`,
     `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`, `ACADEMY_NOTIFICATION_EMAIL` —
     see "Configure email" above. Site works without these set (falls back
     to console logging) but real submissions won't reach anyone by email.
   - `ADMIN_URL` — optional, only if you want something other than the
     default `staff-portal/`.
3. Collect static files: `python manage.py collectstatic --no-input`
   (WhiteNoise serves these directly from Django — no separate static host
   needed).
4. Run migrations: `python manage.py migrate`
5. Start the app with gunicorn, e.g.:
   `gunicorn tal_academy.wsgi:application --workers 2 --timeout 30`
   (2 workers so one slow request — e.g. waiting on a slow mail server —
   doesn't block every other visitor.)
6. Create the admin account on the live service:
   `python manage.py createsuperuser` (via SSH/shell access, however your
   host provides it).

No background task system (Celery/Redis) is needed — see "Tech stack"
above. Branded 404/500 pages, a favicon, and `robots.txt`/`sitemap.xml`/
`llms.txt` are already wired up, nothing to configure. [Dependabot](https://github.com/dependabot)
is enabled (`.github/dependabot.yml`) and opens a PR automatically if a
`requirements.txt` dependency gets a known-vulnerability fix.

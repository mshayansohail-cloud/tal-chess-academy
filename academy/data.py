"""
Static content for the academy site.

Programs used to live here but are now a real model (academy.models.Program)
managed through Django admin — see academy/migrations/0002_seed_initial_programs.py
for the original seed data. The content below has no submission/status workflow
and no admin-editing need yet, so it stays as plain Python data. If that
changes, promote it to a model the same way Program was.
"""

WHY_US = [
    {
        "title": "Experienced Coaches",
        "description": "Coaches who work through the reasoning behind every move, not just the move itself, "
        "and hold each student to a standard they can actually reach.",
    },
    {
        "title": "Structured Curriculum",
        "description": "A progression built on decades of pedagogical practice, not a loose collection of tactics puzzles.",
    },
    {
        "title": "Tournament Preparation",
        "description": "Students train against the clock, under classical time controls, before they ever sit a rated game.",
    },
    {
        "title": "Individual Attention",
        "description": "Small group sizes and detailed game reviews mean every student's weaknesses are actually addressed.",
    },
    {
        "title": "Competitive Environment",
        "description": "Regular internal tournaments keep the stakes real between external competitions.",
    },
]

# Deliberately empty until real, verified coach details are supplied.
#
# This previously held four entirely fictional coaches — invented names,
# invented FIDE titles ("Grandmaster", "Woman FIDE Master", ...), invented
# ratings (2612, 2340, ...), invented championships and federation
# representation. All of it was placeholder content from the original build,
# and none of it was true. FIDE titles and ratings are a public, searchable
# database, so publishing fabricated ones is both checkable and damaging.
# The whole list was removed rather than partly cleaned, because the names
# themselves were fabricated: stripping the titles off a made-up person still
# leaves a made-up person on the page.
#
# Every template that renders a coach treats each field below as optional and
# simply omits anything absent, so partial real data is fine — add only what
# can actually be substantiated, and leave the rest out. Do not reintroduce a
# field just to fill the layout.
#
#   slug     (required) URL fragment, e.g. "asif-khan"
#   name     (required) Full name as it should appear
#   initials (required) Monogram shown in the photo area, e.g. "AK"
#   role      Coaching role, e.g. "Junior Programme Coach"
#   summary   One or two lines shown on the card
#   bio       Longer profile text, shown on the coach's own page
#   focus     List of specialisation areas, e.g. ["Endgames", "Calculation"]
#   credential  A verified, checkable credential only (a real FIDE title or
#               rating, an actual qualification). Omit entirely if there is
#               nothing verified to show — never a placeholder.
COACHES = []

# Deliberately empty until real, scheduled events exist.
#
# This previously held three invented events — made-up names ("Autumn Open
# Classical", "Junior Rapid Championship", "Winter Invitational"), made-up
# dates, and a made-up venue ("Riverside Conference Centre"). Publishing a
# tournament calendar nobody can actually turn up to is the same problem as
# publishing fabricated coach credentials, so it was removed rather than
# left in place.
#
# The Events section and /events/ page both stay live and show an honest
# "calendar being finalised" message while this is empty, so adding a real
# event here is all that's needed to bring the listings back.
#
#   name         (required) Event title
#   date         (required) ISO date, e.g. "2026-09-12" — used for ordering
#   date_label   (required) Human-readable date, e.g. "12 September 2026"
#   location     (required) Where it actually takes place
#   description  (required) What it is and who can enter
EVENTS = []

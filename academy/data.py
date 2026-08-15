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

EVENTS = [
    {
        "name": "Autumn Open Classical",
        "date": "2026-09-12",
        "date_label": "12 September 2026",
        "location": "Academy Hall, Downtown Centre, Karachi",
        "description": "Our flagship rated classical tournament, open to all Academy students rated 1000 and above.",
    },
    {
        "name": "Junior Rapid Championship",
        "date": "2026-10-03",
        "date_label": "3 October 2026",
        "location": "Academy Hall, Downtown Centre, Karachi",
        "description": "A rapid-format event for students in the Junior and Beginner programmes, run under FIDE rapid rules.",
    },
    {
        "name": "Winter Invitational",
        "date": "2026-12-06",
        "date_label": "6 December 2026",
        "location": "Riverside Conference Centre, Karachi",
        "description": "An invitation-only classical event for Advanced and Private Coaching students preparing for national play.",
    },
]

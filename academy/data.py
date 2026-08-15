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
#               rating, an actual qualification, or an online platform
#               rating). An online rating must be labelled as such (e.g.
#               "Online Rating: 2300") rather than left as a bare number,
#               so it's never mistaken for a FIDE rating. Omit entirely if
#               there is nothing verified to show — never a placeholder.
#   photo     Path to a real photo of the coach, e.g. "images/coaches/asif-khan.jpg"
#             (served via {% static %}). Omit to fall back to the initials
#             monogram — never use a stock or generated photo.
COACHES = [
    {
        "slug": "rouhan-ahmed-khatri",
        "name": "Rouhan Ahmed Khatri",
        "initials": "RK",
        "photo": "images/coaches/rouhan-ahmed-khatri.jpg",
        "role": "Beginner Programme Coach",
        "summary": "Focused on taking complete beginners through the fundamentals with a clear, steady progression.",
        "bio": "Rouhan works with students from their very first lesson, making sure every fundamental idea "
        "is properly understood before moving on to the next one. He takes a patient, methodical approach "
        "that builds real board awareness rather than rushing through material, giving each student the "
        "time they need to form good habits early and grow genuinely confident in their play. That "
        "grounding has already produced results: one of his students went on to win gold at the Under 8 "
        "level, competing out of Hyderabad, India.",
        "focus": ["Beginner Fundamentals", "Opening Principles", "Board Awareness"],
        "credential": "Online Rating: 2000",
    },
    {
        "slug": "syed-komail-abbas-rizvi",
        "name": "Syed Komail Abbas Rizvi",
        "initials": "SR",
        "photo": "images/coaches/syed-komail-abbas-rizvi.jpg",
        "role": "Beginner to Advanced Coach",
        "summary": "Works with players across the full range, from absolute fundamentals to advanced "
        "tournament preparation, with a focus on eliminating blunders and building genuine board vision.",
        "bio": "Komail coaches players from complete fundamentals through advanced tournament preparation, "
        "covering approximately 0 to 1800+ Rapid across online and FIDE rated play. His coaching is built "
        "around tactical vision, structured calculation routines, positional planning, and endgame "
        "conversion, with a particular emphasis on eliminating blunders, building genuine board vision, and "
        "developing the strategic understanding that helps students break through rating plateaus.",
        "focus": ["Tactical Vision", "Calculation", "Positional Planning", "Endgame Conversion"],
        "credential": "Online Rating: 2300",
    },
    {
        "slug": "raif-jafri",
        "name": "Raif Jafri",
        "initials": "RJ",
        "photo": "images/coaches/raif-jafri.jpg",
        "role": "Competitive Coach",
        "summary": "Goal oriented coaching built on a track record of national level competitive wins and "
        "producing national level talent.",
        "bio": "Raif is a goal oriented coach with a proven track record of national level competitive wins "
        "and of developing players who go on to compete at the national level themselves. He begins with "
        "fundamentals and building a solid, robust repertoire, bringing tactics in from the start rather "
        "than treating them as a separate stage later on. The middlegames and key endings that follow are "
        "explained with complete clarity, so students understand not just what to play but why. He expects "
        "full commitment from every student he takes on.",
        "focus": ["Repertoire Building", "Tactics", "Middlegame Planning", "Endgame Technique"],
        "credential": "Online Rating: 2300",
    },
    {
        "slug": "shayan-sohail",
        "name": "Shayan Sohail",
        "initials": "SS",
        "photo": "images/coaches/shayan-sohail.jpg",
        "role": "Openings and Tactics Coach",
        "summary": "Focuses on building a solid, robust opening repertoire for both colours alongside sharp "
        "tactical and positional understanding.",
        "bio": "Shayan is a dedicated player with experience competing against some of the strongest talent "
        "in the country. One of his students went from 1200 to 2000 in just six months under his coaching. "
        "His training centres on building a solid, robust opening repertoire for both colours, while "
        "polishing tactical patterns and positional understanding so students can apply what they learn "
        "under real pressure.",
        "focus": ["Opening Repertoire", "Tactical Patterns", "Positional Understanding"],
        "credential": "Online Rating: 2300",
    },
    {
        "slug": "tayyab-ali",
        "name": "Tayyab Ali",
        "initials": "TA",
        "photo": "images/coaches/tayyab-ali.jpg",
        "role": "Junior and Beginner Coach",
        "summary": "Brings enthusiasm and dedication to coaching kids and beginners, with a focus on "
        "interactive sessions that build solid intuition.",
        "bio": "Tayyab has close to 2000 training hours of experience, with a particular mastery in teaching "
        "kids and beginners. He prioritises interactive coaching sessions filled with enthusiasm, helping "
        "students develop solid intuition for the game from their very first lessons, all with the utmost "
        "dedication to every student he works with.",
        "focus": ["Junior Coaching", "Beginner Fundamentals", "Interactive Sessions", "Board Intuition"],
        "credential": "Online Rating: 2300",
    },
]

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

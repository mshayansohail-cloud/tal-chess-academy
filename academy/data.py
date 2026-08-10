"""
Static content for the academy site.

The academy has no dynamic/user-generated content yet, so page copy lives
here as plain Python data rather than in the database. If coach or event
management ever needs an admin UI, promote these to real models.
"""

PROGRAMS = [
    {
        "slug": "junior",
        "piece": "pawn",
        "name": "Junior Program",
        "age": "Ages 6–11",
        "summary": "A playful, structured introduction to the board — rules, tactics, and the discipline of sitting with a problem until it yields.",
        "cta": "View curriculum",
    },
    {
        "slug": "beginner",
        "piece": "knight",
        "name": "Beginner",
        "age": "New to competitive play",
        "summary": "Openings, tactical vision, and the habits that separate players who improve from players who plateau.",
        "cta": "View curriculum",
    },
    {
        "slug": "intermediate",
        "piece": "bishop",
        "name": "Intermediate",
        "age": "1200–1800 rated",
        "summary": "Positional understanding, endgame technique, and the calculation depth needed to hold your own in a rated tournament.",
        "cta": "View curriculum",
    },
    {
        "slug": "advanced",
        "piece": "rook",
        "name": "Advanced",
        "age": "1800+ rated",
        "summary": "Deep opening preparation, tournament strategy, and game analysis with coaches who have sat across the board from titled players.",
        "cta": "View curriculum",
    },
    {
        "slug": "private",
        "piece": "queen",
        "name": "Private Coaching",
        "age": "One-to-one",
        "summary": "A programme built entirely around your games, your openings, and your weaknesses — paced to your rating goals.",
        "cta": "Enquire now",
    },
]

WHY_US = [
    {
        "title": "Titled Coaches",
        "description": "Every coach on our roster holds a FIDE title and has represented their federation in competitive play.",
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

COACHES = [
    {
        "slug": "mikhail-orlov",
        "name": "Mikhail Orlov",
        "title": "FIDE Grandmaster",
        "rating": "2612",
        "initials": "MO",
        "summary": "Former national champion specialising in classical opening theory and endgame technique.",
        "bio": "Mikhail earned his Grandmaster title in 2009 after a decade on the international circuit, "
        "including three national championship titles. He has coached over 40 students to master-level "
        "ratings and leads the Academy's Advanced and Private Coaching programmes.",
        "focus": ["Opening theory", "Endgame technique", "Tournament preparation"],
    },
    {
        "slug": "elena-vasquez",
        "name": "Elena Vasquez",
        "title": "Woman FIDE Master",
        "rating": "2340",
        "initials": "EV",
        "summary": "Junior development specialist with a decade of experience building tournament-ready young players.",
        "bio": "Elena has spent ten years developing junior players from their first lesson through their first "
        "rated tournament. Her structured, patient approach makes her the Academy's lead coach for the "
        "Junior and Beginner programmes.",
        "focus": ["Junior development", "Tactical foundations", "Classroom pedagogy"],
    },
    {
        "slug": "daniel-kessler",
        "name": "Daniel Kessler",
        "title": "FIDE International Master",
        "rating": "2455",
        "initials": "DK",
        "summary": "Positional specialist known for deep, patient game analysis and structured middlegame planning.",
        "bio": "Daniel's methodical approach to the middlegame has shaped the Academy's Intermediate curriculum. "
        "A regular tournament competitor, he brings current competitive experience directly into the "
        "classroom every week.",
        "focus": ["Positional play", "Middlegame planning", "Game analysis"],
    },
    {
        "slug": "sofia-marchetti",
        "name": "Sofia Marchetti",
        "title": "FIDE Master",
        "rating": "2280",
        "initials": "SM",
        "summary": "Rapid and blitz specialist focused on calculation speed and practical decision-making under time pressure.",
        "bio": "Sofia represented her federation in three Olympiad cycles before joining the Academy. She now "
        "focuses on the calculation and time-management skills that separate strong players from "
        "tournament-ready ones.",
        "focus": ["Calculation speed", "Time management", "Practical decision-making"],
    },
]

STATS = [
    {"value": 128, "suffix": "+", "label": "Tournament Victories"},
    {"value": 940, "suffix": "+", "label": "Students Trained"},
    {"value": 76, "suffix": "", "label": "Rated Players Produced"},
    {"value": 12, "suffix": "", "label": "National Titles"},
]

EVENTS = [
    {
        "name": "Autumn Open Classical",
        "date": "2026-09-12",
        "date_label": "12 September 2026",
        "location": "Academy Hall, Downtown Centre",
        "description": "Our flagship rated classical tournament, open to all Academy students rated 1000 and above.",
    },
    {
        "name": "Junior Rapid Championship",
        "date": "2026-10-03",
        "date_label": "3 October 2026",
        "location": "Academy Hall, Downtown Centre",
        "description": "A rapid-format event for students in the Junior and Beginner programmes, run under FIDE rapid rules.",
    },
    {
        "name": "Winter Invitational",
        "date": "2026-12-06",
        "date_label": "6 December 2026",
        "location": "Riverside Conference Centre",
        "description": "An invitation-only classical event for Advanced and Private Coaching students preparing for national play.",
    },
]

TESTIMONIALS = [
    {
        "quote": "My son went from knowing how the pieces move to winning his club's under-12 championship in "
        "eighteen months. The coaches noticed things about his game I never would have.",
        "name": "Priya Nathan",
        "role": "Parent, Junior Programme",
    },
    {
        "quote": "I plateaued at 1500 for two years before joining. Daniel rebuilt my middlegame understanding "
        "from scratch. I crossed 1800 this spring.",
        "name": "Marcus Webb",
        "role": "Intermediate Programme",
    },
    {
        "quote": "The private coaching is genuinely built around your own games. No generic curriculum — "
        "every session started with something I'd actually played.",
        "name": "Aisha Rahman",
        "role": "Private Coaching",
    },
]

from django.db import migrations, models

# Descriptions and highlights derived from the approved 6-level TAL curriculum
# (Complete beginner -> Beginner -> Developing Player -> Intermediate -> Advanced
# -> Competitive Player). Programme count and rating bands are unchanged — only
# the copy is tightened to describe what each programme actually covers.
PROGRAM_UPDATES = {
    "junior": {
        "description": (
            "A structured path from first moves through early strategic thinking, paced and grouped "
            "for ages 6–11 — the same fundamentals every student builds on, just introduced at a "
            "child's pace."
        ),
        "highlights": [
            "Legal play, checkmate basics, and the discipline of sitting with a position",
            "First tactics — forks, pins, and skewers — through repetition, not memorisation",
            "Opening principles that transfer to any opening, not a list of moves to learn by heart",
            "A first real tournament game, with the rules of competition explained beforehand",
        ],
    },
    "beginner": {
        "description": (
            "For anyone starting from zero or just past it — the rules, first tactics, and the opening "
            "principles that hold up regardless of what your opponent plays. No prior experience assumed."
        ),
        "highlights": [
            "Every piece's legal moves, check, checkmate, and stalemate",
            "One-move tactics — forks, pins, skewers, hanging pieces — spotted reliably",
            "Opening principles over opening memorisation: centre, development, king safety",
            "Basic king-and-pawn endgames and the idea of opposition",
        ],
    },
    "intermediate": {
        "description": (
            "Positional understanding, real calculation habits, and a small, properly understood opening "
            "repertoire — for players building toward consistent tournament results. Rated 1200–1800 "
            "as a guide; your trial lesson confirms exact placement."
        ),
        "highlights": [
            "A capped, principle-first repertoire — two or three systems per colour, never a list to memorise",
            "Explicit calculation training: naming candidate moves and verifying before you play",
            "Rook and minor-piece endgame technique, including Lucena and Philidor positions",
            "Independent game analysis, reviewed together with your coach",
        ],
    },
    "advanced": {
        "description": (
            "Deep calculation under pressure, opening preparation built from your own results, and full "
            "tournament-cycle coaching — for players actively competing at a serious level."
        ),
        "highlights": [
            "Judging when a position demands deep calculation versus when principle is enough",
            "Opening preparation built around your own games and opponents, not a longer list of systems",
            "Complex rook and queen endgames, drilled under a clock",
            "A fixed prepare, play, and review cycle for every tournament",
        ],
    },
    "private": {
        "description": (
            "A programme built entirely around your own games, openings, and weaknesses — no fixed "
            "syllabus, paced to whatever goal you're actually training for."
        ),
        "highlights": [
            "Session content drawn directly from your recent games, not a preset curriculum",
            "Engine-assisted, session-by-session game review",
            "Opponent-specific preparation ahead of real events",
            "One-to-one, with the coach of your choosing",
        ],
    },
}


def populate_highlights(apps, schema_editor):
    Program = apps.get_model('academy', 'Program')
    for slug, fields in PROGRAM_UPDATES.items():
        Program.objects.filter(slug=slug).update(**fields)


def clear_highlights(apps, schema_editor):
    Program = apps.get_model('academy', 'Program')
    Program.objects.filter(slug__in=PROGRAM_UPDATES.keys()).update(highlights=[])


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0004_cache_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='highlights',
            field=models.JSONField(
                blank=True, default=list,
                help_text='Short "what you\'ll learn" bullet points, shown collapsed on the programme row.',
            ),
        ),
        migrations.RunPython(populate_highlights, clear_highlights),
    ]

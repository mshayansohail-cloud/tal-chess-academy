from django.db import migrations

PROGRAMS = [
    {
        "slug": "junior",
        "name": "Junior Program",
        "skill_level": "junior",
        "age_group": "Ages 6–11",
        "duration": "12-week terms",
        "icon": "pawn",
        "description": (
            "A playful, structured introduction to the board — rules, tactics, and the discipline of "
            "sitting with a problem until it yields."
        ),
        "cta_label": "View curriculum",
        "display_order": 0,
    },
    {
        "slug": "beginner",
        "name": "Beginner",
        "skill_level": "beginner",
        "age_group": "New to competitive play",
        "duration": "12-week terms",
        "icon": "knight",
        "description": (
            "Openings, tactical vision, and the habits that separate players who improve from players "
            "who plateau."
        ),
        "cta_label": "View curriculum",
        "display_order": 1,
    },
    {
        "slug": "intermediate",
        "name": "Intermediate",
        "skill_level": "intermediate",
        "age_group": "1200–1800 rated",
        "duration": "12-week terms",
        "icon": "bishop",
        "description": (
            "Positional understanding, endgame technique, and the calculation depth needed to hold your "
            "own in a rated tournament."
        ),
        "cta_label": "View curriculum",
        "display_order": 2,
    },
    {
        "slug": "advanced",
        "name": "Advanced",
        "skill_level": "advanced",
        "age_group": "1800+ rated",
        "duration": "12-week terms, ongoing",
        "icon": "rook",
        "description": (
            "Deep opening preparation, tournament strategy, and game analysis with coaches who have sat "
            "across the board from titled players."
        ),
        "cta_label": "View curriculum",
        "display_order": 3,
    },
    {
        "slug": "private",
        "name": "Private Coaching",
        "skill_level": "private",
        "age_group": "One-to-one",
        "duration": "Flexible, per session",
        "icon": "queen",
        "description": (
            "A programme built entirely around your games, your openings, and your weaknesses — paced "
            "to your rating goals."
        ),
        "cta_label": "Enquire now",
        "display_order": 4,
    },
]


def seed_programs(apps, schema_editor):
    Program = apps.get_model('academy', 'Program')
    for entry in PROGRAMS:
        Program.objects.update_or_create(slug=entry['slug'], defaults={**entry, 'is_active': True})


def remove_seeded_programs(apps, schema_editor):
    Program = apps.get_model('academy', 'Program')
    Program.objects.filter(slug__in=[entry['slug'] for entry in PROGRAMS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_programs, remove_seeded_programs),
    ]

"""
Sets the academy's published per-session rates.

Every figure here is PKR for ONE 60-minute session — not a month, not a term.

Junior and Private Coaching are deliberately left without a price. No rate was
published for them, and inventing one (or quietly reusing a neighbouring
programme's) would put a number on the site the academy never agreed to. They
keep their enquiry CTA instead, which is what a blank price renders as.

Written as an explicit map rather than makemigrations' auto default so the
rates are reviewable in one place, and re-runnable if the seed is ever needed
on a fresh database.
"""

from django.db import migrations

# slug -> (online PKR, face-to-face PKR)
RATES = {
    'beginner': (1500, 2500),
    'intermediate': (3000, 4000),
    'advanced': (3000, 4000),
}


def apply_rates(apps, schema_editor):
    Program = apps.get_model('academy', 'Program')
    for slug, (online, in_person) in RATES.items():
        Program.objects.filter(slug=slug).update(
            price_online=online,
            price_in_person=in_person,
            session_minutes=60,
        )


def clear_rates(apps, schema_editor):
    Program = apps.get_model('academy', 'Program')
    Program.objects.filter(slug__in=RATES).update(price_online=None, price_in_person=None)


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0006_program_price_in_person_program_price_online_and_more'),
    ]

    operations = [
        migrations.RunPython(apply_rates, clear_rates),
    ]

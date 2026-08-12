from django.db import migrations

# "View curriculum" implied a syllabus page that doesn't exist — the button
# actually opens the trial-booking form pre-filled for that program, same as
# every other primary CTA on the site, so it should say what it does.
OLD_LABEL = 'View curriculum'
NEW_LABEL = 'Book a Trial'
AFFECTED_SLUGS = ['junior', 'beginner', 'intermediate', 'advanced']


def rename_cta(apps, schema_editor):
    Program = apps.get_model('academy', 'Program')
    Program.objects.filter(slug__in=AFFECTED_SLUGS, cta_label=OLD_LABEL).update(cta_label=NEW_LABEL)


def revert_cta(apps, schema_editor):
    Program = apps.get_model('academy', 'Program')
    Program.objects.filter(slug__in=AFFECTED_SLUGS, cta_label=NEW_LABEL).update(cta_label=OLD_LABEL)


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0002_seed_initial_programs'),
    ]

    operations = [
        migrations.RunPython(rename_cta, revert_cta),
    ]

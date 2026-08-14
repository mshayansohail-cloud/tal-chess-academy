from django.core.management import call_command
from django.db import migrations


def create_cache_table(apps, schema_editor):
    # Delegates to createcachetable rather than hand-written SQL so this
    # produces correct DDL on whatever backend is actually configured
    # (SQLite locally, Postgres in production) instead of only working on
    # the one we happened to test with.
    call_command('createcachetable', 'django_cache')


def drop_cache_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS django_cache')


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0003_rename_view_curriculum_cta'),
    ]

    operations = [
        migrations.RunPython(create_cache_table, drop_cache_table),
    ]

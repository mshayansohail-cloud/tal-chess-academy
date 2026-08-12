from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from academy.models import ContactSubmission, TrialRegistration

# Only terminal statuses are eligible — an open lead (New / Contacted /
# Trial Scheduled / In Progress) never gets purged automatically no matter
# how old it is, since staff may still need it.
REGISTRATION_TERMINAL_STATUSES = [TrialRegistration.Status.ENROLLED, TrialRegistration.Status.CLOSED]
CONTACT_TERMINAL_STATUSES = [ContactSubmission.Status.RESOLVED, ContactSubmission.Status.CLOSED]


class Command(BaseCommand):
    help = (
        "Deletes trial registrations and contact submissions that are both "
        "in a terminal status (Enrolled/Closed/Resolved) and older than "
        "SUBMISSION_RETENTION_DAYS. No-ops if that setting isn't configured "
        "— this command never guesses a retention period on your behalf."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run', action='store_true',
            help="Show what would be deleted without actually deleting anything.",
        )

    def handle(self, *args, **options):
        retention_days = settings.SUBMISSION_RETENTION_DAYS
        if not retention_days:
            self.stdout.write(self.style.WARNING(
                'SUBMISSION_RETENTION_DAYS is not set — nothing to do. '
                'Set it in your environment to enable purging.'
            ))
            return

        cutoff = timezone.now() - timezone.timedelta(days=retention_days)

        registrations = TrialRegistration.objects.filter(
            status__in=REGISTRATION_TERMINAL_STATUSES, submitted_at__lt=cutoff,
        )
        submissions = ContactSubmission.objects.filter(
            status__in=CONTACT_TERMINAL_STATUSES, submitted_at__lt=cutoff,
        )

        reg_count = registrations.count()
        sub_count = submissions.count()

        if options['dry_run']:
            self.stdout.write(
                f'Would delete {reg_count} trial registration(s) and {sub_count} '
                f'contact submission(s) submitted before {cutoff.date()} (dry run, nothing deleted).'
            )
            return

        registrations.delete()
        submissions.delete()
        self.stdout.write(self.style.SUCCESS(
            f'Deleted {reg_count} trial registration(s) and {sub_count} '
            f'contact submission(s) submitted before {cutoff.date()}.'
        ))

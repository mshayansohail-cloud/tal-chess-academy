"""
Best-effort email notifications for new submissions.

Every function here catches its own exceptions and logs them rather than
raising — a failed send must never roll back or block a database write that
already succeeded. Callers can ignore the return value; it's only there for
tests to assert on delivery.

Sent synchronously, deliberately — no Celery/Redis. At this project's volume
an SMTP send finishes in well under a second, so a task queue would add real
infrastructure (a broker, a worker process) for no practical benefit, and it
would make the delivery tests below racy. If volume ever grows enough for
that trade-off to flip, every call site already goes through this module, so
swapping to `.delay()` is a small change, not a rewrite.
"""

import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _send(subject, template_name, context, to):
    try:
        body = render_to_string(template_name, context)
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to],
            fail_silently=False,
        )
        return True
    except Exception:
        # Deliberately excludes subject/recipient — both can contain
        # submitter-supplied PII (e.g. a student's name), and server logs
        # typically have weaker access controls than the DB itself. The
        # template name is enough to identify which send failed; the actual
        # record is already saved and visible in admin.
        logger.exception('Failed to send email (template: %s)', template_name)
        return False


def send_registration_notification(registration):
    return _send(
        subject=f'New Trial Request — {registration.student_name}',
        template_name='academy/emails/registration_notification.txt',
        context={'registration': registration},
        to=settings.ACADEMY_NOTIFICATION_EMAIL,
    )


def send_registration_confirmation(registration):
    return _send(
        subject='Your trial request — TAL Chess Academy',
        template_name='academy/emails/registration_confirmation.txt',
        context={'registration': registration},
        to=registration.email,
    )


def send_contact_notification(submission):
    return _send(
        subject=f'New Contact Enquiry — {submission.subject}',
        template_name='academy/emails/contact_notification.txt',
        context={'submission': submission},
        to=settings.ACADEMY_NOTIFICATION_EMAIL,
    )


def send_contact_confirmation(submission):
    return _send(
        subject='We received your message — TAL Chess Academy',
        template_name='academy/emails/contact_confirmation.txt',
        context={'submission': submission},
        to=submission.email,
    )

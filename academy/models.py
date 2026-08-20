from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

phone_validator = RegexValidator(
    regex=r'^[0-9+\-()\s]{7,20}$',
    message="Enter a valid phone number (digits, spaces, +, -, and parentheses only).",
)


class Program(models.Model):
    """A course the academy offers. Replaces the old hardcoded program list."""

    class SkillLevel(models.TextChoices):
        JUNIOR = 'junior', 'Junior'
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'
        PRIVATE = 'private', 'Private Coaching'

    class Icon(models.TextChoices):
        PAWN = 'pawn', 'Pawn'
        KNIGHT = 'knight', 'Knight'
        BISHOP = 'bishop', 'Bishop'
        ROOK = 'rook', 'Rook'
        QUEEN = 'queen', 'Queen'
        KING = 'king', 'King'

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True)
    description = models.TextField()
    highlights = models.JSONField(
        default=list, blank=True,
        help_text='Short "what you\'ll learn" bullet points, shown collapsed on the programme row.',
    )
    skill_level = models.CharField(max_length=20, choices=SkillLevel.choices)
    age_group = models.CharField(max_length=60, help_text='e.g. "Ages 6–11" or "1200+ rated"')
    duration = models.CharField(max_length=60, blank=True, help_text='e.g. "12-week term"')
    icon = models.CharField(max_length=20, choices=Icon.choices, default=Icon.PAWN)
    cta_label = models.CharField(max_length=40, default='View curriculum')

    # Rates live here rather than in a template so staff can change them in
    # admin without a deploy, and so every surface that quotes a price reads
    # the same number. Both are per single session of `session_minutes`, NOT
    # per month or per term.
    #
    # Null means "no published rate" — not "free". A programme without one
    # simply shows no price and keeps its enquiry CTA, which is how Junior
    # and Private Coaching behave: their rates vary, so quoting a single
    # figure would be inventing one.
    price_online = models.PositiveIntegerField(
        null=True, blank=True,
        help_text='PKR for one online session. Leave blank if there is no single published rate.',
    )
    price_in_person = models.PositiveIntegerField(
        null=True, blank=True,
        help_text='PKR for one face-to-face session. Leave blank if there is no single published rate.',
    )
    session_minutes = models.PositiveSmallIntegerField(
        default=60,
        help_text='Length of one session, in minutes — the unit both prices above refer to.',
    )

    is_active = models.BooleanField(default=True, help_text='Inactive programs are hidden from the site and API.')
    display_order = models.PositiveIntegerField(default=0, help_text='Lower numbers are shown first.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class TrialRegistration(models.Model):
    """A "Book a Trial" submission from a prospective student or parent."""

    class ChessLevel(models.TextChoices):
        NONE = 'none', 'Never played'
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'

    class Status(models.TextChoices):
        NEW = 'new', 'New'
        CONTACTED = 'contacted', 'Contacted'
        TRIAL_SCHEDULED = 'trial_scheduled', 'Trial Scheduled'
        ENROLLED = 'enrolled', 'Enrolled'
        CLOSED = 'closed', 'Rejected / Closed'

    class SessionFormat(models.TextChoices):
        ONLINE = 'online', 'Online'
        IN_PERSON = 'in_person', 'Face-to-face'

    student_name = models.CharField(max_length=120)
    parent_name = models.CharField(
        max_length=120, blank=True, help_text='Leave blank for adult students registering themselves.'
    )
    student_age = models.PositiveSmallIntegerField(validators=[MinValueValidator(3), MaxValueValidator(100)])
    phone = models.CharField(max_length=30, validators=[phone_validator])
    email = models.EmailField()
    chess_level = models.CharField(max_length=20, choices=ChessLevel.choices, default=ChessLevel.NONE)
    program = models.ForeignKey(Program, on_delete=models.PROTECT, related_name='registrations')
    # Which rate the enquiry relates to, and a genuine scheduling constraint
    # for whoever follows up. Blank stays allowed so that rows created before
    # this field existed remain valid.
    session_format = models.CharField(
        max_length=20, choices=SessionFormat.choices, blank=True,
        help_text='Whether the enquirer asked about online or face-to-face sessions.',
    )
    preferred_schedule = models.CharField(
        max_length=200, blank=True, help_text='Preferred days/times, in the applicant\'s own words.'
    )
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    staff_notes = models.TextField(blank=True, help_text='Internal notes — never shown to the applicant.')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.student_name} — {self.program} ({self.get_status_display()})'


class ContactSubmission(models.Model):
    """A general enquiry from the contact form."""

    class Status(models.TextChoices):
        NEW = 'new', 'New'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'
        CLOSED = 'closed', 'Closed'

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True, validators=[phone_validator])
    subject = models.CharField(max_length=150)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    staff_notes = models.TextField(blank=True, help_text='Internal notes — never shown to the sender.')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.name} — {self.subject}'

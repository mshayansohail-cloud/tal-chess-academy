from django.contrib import admin

from .models import ContactSubmission, Program, TrialRegistration


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'skill_level', 'age_group', 'price_online', 'price_in_person',
        'is_active', 'display_order',
    )
    list_editable = ('price_online', 'price_in_person', 'is_active', 'display_order')
    list_filter = ('skill_level', 'is_active')
    search_fields = ('name', 'description', 'age_group')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order', 'name')
    fieldsets = (
        (None, {
            'fields': (
                'name', 'slug', 'description', 'highlights', 'skill_level', 'age_group',
                'duration', 'icon', 'cta_label', 'is_active', 'display_order',
            ),
        }),
        ('Session rates', {
            'fields': ('price_online', 'price_in_person', 'session_minutes'),
            'description': (
                'PKR per single session. Leave both blank for programmes quoted '
                'individually — the site then shows the enquiry link instead of a '
                'price, rather than displaying zero.'
            ),
        }),
    )


class SubmissionAdminBase(admin.ModelAdmin):
    """
    Shared behaviour for the two "inbox" models: staff can triage (status,
    notes) but the submitted data itself is read-only, and new rows can only
    ever come from a real public submission — not fabricated in the admin.
    """

    date_hierarchy = 'submitted_at'
    editable_fields = ('status', 'staff_notes')

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields if f.name not in self.editable_fields]


@admin.register(TrialRegistration)
class TrialRegistrationAdmin(SubmissionAdminBase):
    list_display = (
        'student_name', 'program', 'session_format', 'chess_level', 'student_age',
        'status', 'submitted_at',
    )
    list_filter = ('status', 'program', 'session_format', 'chess_level', 'submitted_at')
    search_fields = ('student_name', 'parent_name', 'email', 'phone')
    actions = ['mark_contacted', 'mark_trial_scheduled', 'mark_enrolled', 'mark_closed']

    fieldsets = (
        ('Applicant', {
            'fields': (
                'student_name', 'parent_name', 'student_age', 'phone', 'email',
                'chess_level', 'program', 'session_format', 'preferred_schedule',
                'message', 'submitted_at',
            ),
        }),
        ('Staff use', {
            'fields': ('status', 'staff_notes', 'updated_at'),
        }),
    )

    @admin.action(description='Mark selected as Contacted')
    def mark_contacted(self, request, queryset):
        queryset.update(status=TrialRegistration.Status.CONTACTED)

    @admin.action(description='Mark selected as Trial Scheduled')
    def mark_trial_scheduled(self, request, queryset):
        queryset.update(status=TrialRegistration.Status.TRIAL_SCHEDULED)

    @admin.action(description='Mark selected as Enrolled')
    def mark_enrolled(self, request, queryset):
        queryset.update(status=TrialRegistration.Status.ENROLLED)

    @admin.action(description='Mark selected as Rejected / Closed')
    def mark_closed(self, request, queryset):
        queryset.update(status=TrialRegistration.Status.CLOSED)


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(SubmissionAdminBase):
    list_display = ('name', 'subject', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('name', 'email', 'phone', 'subject', 'message')
    actions = ['mark_in_progress', 'mark_resolved', 'mark_closed']

    fieldsets = (
        ('Enquiry', {
            'fields': ('name', 'email', 'phone', 'subject', 'message', 'submitted_at'),
        }),
        ('Staff use', {
            'fields': ('status', 'staff_notes', 'updated_at'),
        }),
    )

    @admin.action(description='Mark selected as In Progress')
    def mark_in_progress(self, request, queryset):
        queryset.update(status=ContactSubmission.Status.IN_PROGRESS)

    @admin.action(description='Mark selected as Resolved')
    def mark_resolved(self, request, queryset):
        queryset.update(status=ContactSubmission.Status.RESOLVED)

    @admin.action(description='Mark selected as Closed')
    def mark_closed(self, request, queryset):
        queryset.update(status=ContactSubmission.Status.CLOSED)

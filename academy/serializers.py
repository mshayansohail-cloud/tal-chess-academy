from rest_framework import serializers

from .models import ContactSubmission, Program, TrialRegistration


def reject_honeypot(value):
    """The 'website' field is invisible to real users; only bots fill it in."""
    if value:
        raise serializers.ValidationError('Submission rejected.')
    return value


class ProgramSerializer(serializers.ModelSerializer):
    skill_level_display = serializers.CharField(source='get_skill_level_display', read_only=True)

    class Meta:
        model = Program
        fields = [
            'id', 'slug', 'name', 'description', 'skill_level', 'skill_level_display',
            'age_group', 'duration', 'icon', 'cta_label', 'display_order',
        ]


class TrialRegistrationSerializer(serializers.ModelSerializer):
    # Honeypot field: real visitors never see or fill this in (see forms.js).
    # Present in the payload but never stored — validated then discarded.
    website = serializers.CharField(
        required=False, allow_blank=True, write_only=True, validators=[reject_honeypot]
    )
    program = serializers.PrimaryKeyRelatedField(queryset=Program.objects.filter(is_active=True))

    class Meta:
        model = TrialRegistration
        fields = [
            'student_name', 'parent_name', 'student_age', 'phone', 'email', 'chess_level',
            'program', 'preferred_schedule', 'message', 'website',
        ]

    def validate_student_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('This field may not be blank.')
        return value

    def create(self, validated_data):
        validated_data.pop('website', None)
        return TrialRegistration.objects.create(**validated_data)


class ContactSubmissionSerializer(serializers.ModelSerializer):
    website = serializers.CharField(
        required=False, allow_blank=True, write_only=True, validators=[reject_honeypot]
    )

    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'subject', 'message', 'website']

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('This field may not be blank.')
        return value

    def create(self, validated_data):
        validated_data.pop('website', None)
        return ContactSubmission.objects.create(**validated_data)

from rest_framework import generics, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from . import emails
from .models import Program
from .serializers import ContactSubmissionSerializer, ProgramSerializer, TrialRegistrationSerializer
from .throttling import (
    ContactBurstThrottle,
    ContactRateThrottle,
    RegistrationBurstThrottle,
    RegistrationRateThrottle,
)


class ProgramListAPIView(generics.ListAPIView):
    """GET /api/programs/ — public, read-only list of active programs."""

    queryset = Program.objects.filter(is_active=True)
    serializer_class = ProgramSerializer
    permission_classes = [permissions.AllowAny]


class RegistrationCreateAPIView(APIView):
    """
    POST /api/registrations/ — create a trial registration.

    Write-only by design: there is no matching GET/list here, so submitted
    data can never be read back through this endpoint. Staff review
    registrations exclusively through Django admin.
    """

    permission_classes = [permissions.AllowAny]
    # No SessionAuthentication here, deliberately: this view is AllowAny and
    # never needs to know who's logged in, but SessionAuthentication enforces
    # CSRF whenever it resolves a valid session — which would 403 a visitor
    # who happens to be logged into /staff-portal/ in the same browser (e.g.
    # staff testing their own site), since forms.js never sends a CSRF token.
    authentication_classes = []
    throttle_classes = [RegistrationRateThrottle, RegistrationBurstThrottle]
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = TrialRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            # Deliberately returns before recording against the submission
            # throttle: a validation error costs the visitor a correction,
            # not their remaining quota. See academy/throttling.py.
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        registration = serializer.save()
        RegistrationRateThrottle().record(request, self)

        # Best-effort: the record above is already saved regardless of outcome.
        emails.send_registration_notification(registration)
        emails.send_registration_confirmation(registration)

        return Response(
            {
                'success': True,
                'message': "Your trial request has been submitted. We'll be in touch within one business day.",
            },
            status=status.HTTP_201_CREATED,
        )


class ContactCreateAPIView(APIView):
    """
    POST /api/contact/ — create a contact enquiry.

    Write-only by design, for the same reason as registrations above.
    """

    permission_classes = [permissions.AllowAny]
    # See RegistrationCreateAPIView above for why authentication is disabled here.
    authentication_classes = []
    throttle_classes = [ContactRateThrottle, ContactBurstThrottle]
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = ContactSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            # See the note in RegistrationCreateAPIView above.
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        submission = serializer.save()
        ContactRateThrottle().record(request, self)

        emails.send_contact_notification(submission)
        emails.send_contact_confirmation(submission)

        return Response(
            {'success': True, 'message': "Your message has been received. We'll reply within one business day."},
            status=status.HTTP_201_CREATED,
        )

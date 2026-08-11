from django.urls import path

from . import api_views

urlpatterns = [
    path('programs/', api_views.ProgramListAPIView.as_view(), name='api_programs'),
    path('registrations/', api_views.RegistrationCreateAPIView.as_view(), name='api_registrations'),
    path('contact/', api_views.ContactCreateAPIView.as_view(), name='api_contact'),
]

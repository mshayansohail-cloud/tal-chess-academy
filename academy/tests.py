from unittest.mock import patch

from django.core import mail
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ContactSubmission, Program, TrialRegistration


class ProgramAPITests(APITestCase):
    def setUp(self):
        cache.clear()
        self.active = Program.objects.create(
            name='Active Program', slug='active-program', description='desc',
            skill_level=Program.SkillLevel.BEGINNER, age_group='Ages 8+',
        )
        self.inactive = Program.objects.create(
            name='Inactive Program', slug='inactive-program', description='desc',
            skill_level=Program.SkillLevel.ADVANCED, age_group='Ages 8+', is_active=False,
        )

    def test_program_list_returns_only_active_programs(self):
        response = self.client.get('/api/programs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        slugs = [item['slug'] for item in response.json()]
        self.assertIn('active-program', slugs)
        self.assertNotIn('inactive-program', slugs)


class RegistrationAPITests(APITestCase):
    def setUp(self):
        cache.clear()
        self.program = Program.objects.create(
            name='Test Junior', slug='test-junior', description='desc',
            skill_level=Program.SkillLevel.JUNIOR, age_group='Ages 6-11',
        )
        self.valid_payload = {
            'student_name': 'Test Student',
            'parent_name': 'Test Parent',
            'student_age': 10,
            'phone': '+1 555-123-4567',
            'email': 'student@example.com',
            'chess_level': 'beginner',
            'program': self.program.id,
            'preferred_schedule': 'Saturdays',
            'message': 'Excited to start.',
        }

    def test_valid_registration_creates_db_record_and_returns_201(self):
        response = self.client.post('/api/registrations/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json()['success'])
        self.assertTrue(TrialRegistration.objects.filter(email='student@example.com').exists())

    def test_valid_registration_sends_both_notification_emails(self):
        self.client.post('/api/registrations/', self.valid_payload, format='json')
        self.assertEqual(len(mail.outbox), 2)
        recipients = [m.to[0] for m in mail.outbox]
        self.assertIn('student@example.com', recipients)  # confirmation to applicant

    def test_missing_required_fields_returns_400_with_field_errors(self):
        response = self.client.post('/api/registrations/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertFalse(body['success'])
        self.assertIn('student_name', body['errors'])
        self.assertIn('email', body['errors'])
        self.assertIn('program', body['errors'])

    def test_invalid_email_is_rejected(self):
        payload = dict(self.valid_payload, email='not-an-email')
        response = self.client.post('/api/registrations/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.json()['errors'])

    def test_out_of_range_age_is_rejected(self):
        payload = dict(self.valid_payload, student_age=200)
        response = self.client.post('/api/registrations/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('student_age', response.json()['errors'])

    def test_invalid_phone_is_rejected(self):
        payload = dict(self.valid_payload, phone='call me maybe')
        response = self.client.post('/api/registrations/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.json()['errors'])

    def test_nonexistent_program_is_rejected(self):
        payload = dict(self.valid_payload, program=99999)
        response = self.client.post('/api/registrations/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('program', response.json()['errors'])

    def test_inactive_program_is_rejected(self):
        inactive = Program.objects.create(
            name='Closed Program', slug='closed-program', description='desc',
            skill_level=Program.SkillLevel.ADVANCED, age_group='Adults', is_active=False,
        )
        payload = dict(self.valid_payload, program=inactive.id)
        response = self.client.post('/api/registrations/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('program', response.json()['errors'])

    def test_honeypot_field_silently_blocks_spam_submission(self):
        payload = dict(self.valid_payload, website='http://spam.example')
        response = self.client.post('/api/registrations/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(TrialRegistration.objects.filter(student_name='Test Student').exists())

    def test_get_is_not_allowed_registrations_are_never_publicly_listed(self):
        response = self.client.get('/api/registrations/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch('academy.emails.send_mail', side_effect=Exception('SMTP is down'))
    def test_database_save_succeeds_even_if_email_sending_fails(self, mock_send_mail):
        response = self.client.post('/api/registrations/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(TrialRegistration.objects.filter(email='student@example.com').exists())


class ContactAPITests(APITestCase):
    def setUp(self):
        cache.clear()
        self.valid_payload = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'subject': 'Question about fees',
            'message': 'What are your fees for the beginner program?',
        }

    def test_valid_contact_creates_db_record_and_returns_201(self):
        response = self.client.post('/api/contact/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json()['success'])
        self.assertTrue(ContactSubmission.objects.filter(email='jane@example.com').exists())

    def test_valid_contact_sends_both_notification_emails(self):
        self.client.post('/api/contact/', self.valid_payload, format='json')
        self.assertEqual(len(mail.outbox), 2)

    def test_missing_required_fields_returns_400_with_field_errors(self):
        response = self.client.post('/api/contact/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertFalse(body['success'])
        self.assertIn('name', body['errors'])
        self.assertIn('message', body['errors'])

    def test_invalid_email_is_rejected(self):
        payload = dict(self.valid_payload, email='not-an-email')
        response = self.client.post('/api/contact/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.json()['errors'])

    def test_honeypot_field_silently_blocks_spam_submission(self):
        payload = dict(self.valid_payload, website='http://spam.example')
        response = self.client.post('/api/contact/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(ContactSubmission.objects.filter(email='jane@example.com').exists())

    def test_get_is_not_allowed_contact_submissions_are_never_publicly_listed(self):
        response = self.client.get('/api/contact/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ThrottlingTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.valid_payload = {
            'name': 'Rate Limited',
            'email': 'rate@example.com',
            'subject': 'Test',
            'message': 'Testing throttling behaviour.',
        }

    def test_contact_endpoint_throttles_after_configured_rate(self):
        # REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['contact'] = '10/hour'
        for _ in range(10):
            response = self.client.post('/api/contact/', self.valid_payload, format='json')
            self.assertNotEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        response = self.client.post('/api/contact/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class AdminPermissionTests(APITestCase):
    def test_registration_and_contact_admin_cannot_add_new_records(self):
        from django.contrib.admin.sites import site

        self.assertFalse(site._registry[TrialRegistration].has_add_permission(None))
        self.assertFalse(site._registry[ContactSubmission].has_add_permission(None))

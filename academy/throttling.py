"""
Rate limits for the two public write endpoints.

Each endpoint carries two throttles doing different jobs:

  * a *submission* throttle, which counts only submissions that actually
    saved something, and
  * a *burst* throttle, which counts every request that arrives.

The split exists because DRF's stock behaviour conflates the two. A
SimpleRateThrottle records a request during `initial()` — before the
serializer has run — so a rejected submission spends quota exactly like an
accepted one. With the trial form's several validation rules, a parent who
forgets the guardian field, mistypes a phone number, then fixes it, could
exhaust a 5/hour limit and be told "you've submitted too many requests"
without having successfully booked anything at all. Their lead is lost
silently, which is the worst way to lose one.

Counting only successful writes fixes that, but on its own it would let a
bot hammer the endpoint forever with deliberately invalid payloads, since
those would never count. The burst throttle keeps that door shut; the
honeypot field and django-axes cover the rest.
"""

from rest_framework.throttling import AnonRateThrottle


class SubmissionRateThrottle(AnonRateThrottle):
    """
    Checks the window on the way in, but only spends quota on a real write.

    `allow_request` deliberately does not call `throttle_success()` — the
    view calls `record()` after `serializer.save()` instead.
    """

    def allow_request(self, request, view):
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        # Drop entries that have aged out of the window.
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()

        if len(self.history) >= self.num_requests:
            return self.throttle_failure()

        # Allowed, but nothing is charged until the write succeeds.
        return True

    def record(self, request, view):
        """Spend one unit of quota. Call only after a successful save."""
        if self.rate is None:
            return

        key = self.get_cache_key(request, view)
        if key is None:
            return

        now = self.timer()
        history = self.cache.get(key, [])
        while history and history[-1] <= now - self.duration:
            history.pop()

        history.insert(0, now)
        self.cache.set(key, history, self.duration)


class RegistrationRateThrottle(SubmissionRateThrottle):
    """Successful trial bookings per IP — see DEFAULT_THROTTLE_RATES."""

    scope = 'registration'


class ContactRateThrottle(SubmissionRateThrottle):
    """Successful contact enquiries per IP — see DEFAULT_THROTTLE_RATES."""

    scope = 'contact'


class RegistrationBurstThrottle(AnonRateThrottle):
    """Every request to the registration endpoint, valid or not."""

    scope = 'registration_burst'


class ContactBurstThrottle(AnonRateThrottle):
    """Every request to the contact endpoint, valid or not."""

    scope = 'contact_burst'

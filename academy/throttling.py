from rest_framework.throttling import AnonRateThrottle


class RegistrationRateThrottle(AnonRateThrottle):
    """Rate limit for POST /api/registrations/ — see REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']."""

    scope = 'registration'


class ContactRateThrottle(AnonRateThrottle):
    """Rate limit for POST /api/contact/ — see REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']."""

    scope = 'contact'

from django.conf import settings


class NoIndexAdminApiMiddleware:
    """
    Adds X-Robots-Tag: noindex to admin and API responses. robots.txt only
    *requests* crawlers stay away; a page linked from elsewhere can still get
    indexed despite it. This header is a stronger, explicit signal that
    these paths should never appear in search results.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        admin_url = settings.ADMIN_URL
        self.admin_prefix = admin_url if admin_url.startswith('/') else f'/{admin_url}'

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith(self.admin_prefix) or request.path.startswith('/api/'):
            response['X-Robots-Tag'] = 'noindex, nofollow'
        return response

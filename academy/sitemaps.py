from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from . import data


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return ['home', 'about', 'programs', 'coaches', 'achievements', 'events', 'contact', 'faq', 'privacy']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == 'home' else 0.6


class CoachSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return data.COACHES

    def location(self, coach):
        return reverse('coach_detail', args=[coach['slug']])

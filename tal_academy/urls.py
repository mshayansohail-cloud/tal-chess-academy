from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from academy import views
from academy.sitemaps import CoachSitemap, StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'coaches': CoachSitemap,
}

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/', include('academy.api_urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('programs/', views.programs, name='programs'),
    path('coaches/', views.coaches, name='coaches'),
    path('coaches/<slug:slug>/', views.coach_detail, name='coach_detail'),
    path('achievements/', views.achievements, name='achievements'),
    path('events/', views.events, name='events'),
    path('contact/', views.contact, name='contact'),
]

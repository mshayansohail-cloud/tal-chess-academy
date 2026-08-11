from django.contrib import admin
from django.urls import include, path

from academy import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('academy.api_urls')),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('programs/', views.programs, name='programs'),
    path('coaches/', views.coaches, name='coaches'),
    path('coaches/<slug:slug>/', views.coach_detail, name='coach_detail'),
    path('achievements/', views.achievements, name='achievements'),
    path('events/', views.events, name='events'),
    path('contact/', views.contact, name='contact'),
]

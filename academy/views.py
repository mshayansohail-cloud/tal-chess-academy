from django.http import Http404
from django.shortcuts import render

from . import data
from .models import Program


def home(request):
    context = {
        "programs": Program.objects.filter(is_active=True),
        "why_us": data.WHY_US,
        "coaches": data.COACHES,
        "stats": data.STATS,
        "events": data.EVENTS[:3],
        "testimonials": data.TESTIMONIALS,
    }
    return render(request, "academy/home.html", context)


def about(request):
    return render(request, "academy/about.html", {"why_us": data.WHY_US})


def programs(request):
    return render(request, "academy/programs.html", {"programs": Program.objects.filter(is_active=True)})


def coaches(request):
    return render(request, "academy/coaches.html", {"coaches": data.COACHES})


def coach_detail(request, slug):
    for coach in data.COACHES:
        if coach["slug"] == slug:
            return render(request, "academy/coach_detail.html", {"coach": coach})
    raise Http404("Coach not found")


def achievements(request):
    return render(request, "academy/achievements.html", {"stats": data.STATS})


def events(request):
    return render(request, "academy/events.html", {"events": data.EVENTS})


def contact(request):
    """
    Renders the Book a Trial / Contact page shell. Both forms on this page
    submit via JS to the /api/registrations/ and /api/contact/ endpoints
    (see static/js/forms.js) rather than posting back to this view.
    """
    context = {
        "programs": Program.objects.filter(is_active=True),
        "selected_program_slug": request.GET.get("program", ""),
    }
    return render(request, "academy/contact.html", context)

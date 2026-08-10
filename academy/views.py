from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from . import data
from .forms import ContactForm


def home(request):
    context = {
        "programs": data.PROGRAMS,
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
    return render(request, "academy/programs.html", {"programs": data.PROGRAMS})


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
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(
                request,
                "Thank you — your message has been received. A member of our team will be in touch shortly.",
            )
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "academy/contact.html", {"form": form})

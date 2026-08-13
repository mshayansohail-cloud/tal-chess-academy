from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from . import data
from .models import Program


def home(request):
    context = {
        "programs": Program.objects.filter(is_active=True),
        "why_us": data.WHY_US,
        "coaches": data.COACHES,
        "events": data.EVENTS[:3],
        "testimonials": data.TESTIMONIALS,
    }
    return render(request, "academy/home.html", context)


def about(request):
    return render(request, "academy/about.html", {"why_us": data.WHY_US})


def privacy(request):
    return render(request, "academy/privacy.html")


def faq(request):
    return render(request, "academy/faq.html")


def programs(request):
    return render(request, "academy/programs.html", {"programs": Program.objects.filter(is_active=True)})


def coaches(request):
    return render(request, "academy/coaches.html", {"coaches": data.COACHES})


def coach_detail(request, slug):
    for coach in data.COACHES:
        if coach["slug"] == slug:
            return render(request, "academy/coach_detail.html", {"coach": coach})
    raise Http404("Coach not found")


def events(request):
    return render(request, "academy/events.html", {"events": data.EVENTS})


def contact(request):
    """
    Renders the Book a Trial / Contact page shell. Both forms on this page
    submit via JS to the /api/registrations/ and /api/contact/ endpoints
    (see static/js/forms.js) rather than posting back to this view.
    """
    programs = Program.objects.filter(is_active=True)
    selected_program_slug = request.GET.get("program", "")
    selected_program = None
    if selected_program_slug:
        for program in programs:
            if program.slug == selected_program_slug:
                selected_program = program
                break
    context = {
        "programs": programs,
        "selected_program_slug": selected_program_slug,
        "selected_program": selected_program,
    }
    return render(request, "academy/contact.html", context)


def robots_txt(request):
    sitemap_url = request.build_absolute_uri('/sitemap.xml')
    lines = [
        'User-agent: *',
        'Allow: /',
        f'Disallow: {settings.ADMIN_URL if settings.ADMIN_URL.startswith("/") else "/" + settings.ADMIN_URL}',
        'Disallow: /api/',
        '',
        f'Sitemap: {sitemap_url}',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def llms_txt(request):
    """
    https://llmstxt.org/ — a Markdown summary for AI agents/LLMs, pointing
    at the same public page set as the sitemap (see academy/sitemaps.py).
    Links are built with build_absolute_uri() so the domain always matches
    whatever host actually served the request, in dev or production.
    """
    pages = [
        ('home', 'Home', 'Overview of the academy and its programs'),
        ('about', 'About', "The academy's philosophy and teaching approach"),
        ('programs', 'Programs', 'Course offerings by skill level, from first moves to private coaching'),
        ('coaches', 'Coaches', 'FIDE-titled coaching staff'),
        ('events', 'Events', 'Upcoming tournaments and academy events'),
        ('faq', 'FAQ', 'Common questions about programmes, trial lessons, and level placement'),
        ('contact', 'Contact', 'Book a trial lesson or send a general enquiry'),
    ]
    lines = [
        '# TAL Chess Academy',
        '',
        'TAL Chess Academy trains players from first moves to tournament mastery, '
        'led by FIDE-titled coaches in a structured, competitive environment.',
        '',
        '## Pages',
        '',
    ]
    for url_name, label, desc in pages:
        url = request.build_absolute_uri(reverse(url_name))
        lines.append(f'- [{label}]({url}): {desc}')

    return HttpResponse('\n'.join(lines), content_type='text/markdown; charset=utf-8')

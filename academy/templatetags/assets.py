"""
`{% versioned_static %}` — `{% static %}` that a stale browser cache cannot
silently defeat during development.

Django's dev server sends static files with no `Cache-Control` header, so
browsers apply their own heuristic freshness and will happily serve a CSS or
JS file from cache for a long time without even revalidating it. The failure
mode is nasty precisely because it is invisible: the page renders, nothing
errors, and the visible result is simply the *previous* version of the site.
Renaming a CSS class makes it worse still — cached CSS then matches nothing,
so elements fall back to unstyled intrinsic sizes and the layout collapses
rather than merely looking out of date.

Appending the file's modification time to the URL makes each edit a new URL,
so the browser has to fetch it. Only in DEBUG: in production WhiteNoise's
`CompressedManifestStaticFilesStorage` already hashes the filename itself,
which does the same job properly, and adding a query string on top of it
would just defeat far-future caching for no benefit.
"""

import os

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.templatetags.static import static

register = template.Library()

# mtime lookups are cheap but not free, and a page pulls several assets on
# every single request. The dev server reloads this module whenever the code
# changes, and the mtime of an edited file changes anyway, so caching per
# path is safe: the key point is that the *value* is recomputed whenever the
# process restarts, and `_asset_mtime` is only consulted while DEBUG is on.
_mtime_cache = {}


def _asset_mtime(path):
    if path in _mtime_cache:
        return _mtime_cache[path]

    absolute = finders.find(path)
    try:
        stamp = str(int(os.path.getmtime(absolute))) if absolute else ""
    except OSError:
        # A missing or unreadable asset is not this tag's problem to report —
        # fall back to an unversioned URL and let the 404 speak for itself.
        stamp = ""

    _mtime_cache[path] = stamp
    return stamp


@register.simple_tag
def versioned_static(path):
    url = static(path)
    if not settings.DEBUG:
        return url

    stamp = _asset_mtime(path)
    if not stamp:
        return url

    separator = "&" if "?" in url else "?"
    return f"{url}{separator}v={stamp}"

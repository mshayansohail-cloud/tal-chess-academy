(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Mobile nav toggle */
  var navToggle = document.querySelector(".nav-toggle");
  var navLinks = document.querySelector(".nav-links");
  var mobileNavQuery = window.matchMedia("(max-width: 900px)");

  if (navToggle && navLinks) {
    // On mobile, the closed menu is hidden via opacity/pointer-events (so it
    // can transition smoothly) — but that alone leaves its links keyboard-
    // focusable while invisible. `inert` removes them from the tab order
    // and from assistive tech too, matching what's actually on screen. This
    // must only apply in mobile nav mode: on desktop the links are always
    // genuinely visible regardless of the is-open class.
    function syncNavInert() {
      navLinks.inert = mobileNavQuery.matches && !navLinks.classList.contains("is-open");
    }

    syncNavInert();
    mobileNavQuery.addEventListener("change", syncNavInert);
    // Belt and braces: some environments don't reliably fire matchMedia's
    // "change" listener on viewport changes (e.g. devtools/automation-driven
    // resizes) even though real users resizing/rotating a browser do.
    window.addEventListener("resize", syncNavInert, { passive: true });

    function closeNav() {
      navLinks.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
      syncNavInert();
    }

    navToggle.addEventListener("click", function () {
      var isOpen = navLinks.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
      syncNavInert();
    });

    navLinks.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeNav);
    });

    // Click outside the open menu (and outside the toggle button itself,
    // which has its own handler above) closes it.
    document.addEventListener("click", function (event) {
      if (!navLinks.classList.contains("is-open")) return;
      if (navLinks.contains(event.target) || navToggle.contains(event.target)) return;
      closeNav();
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && navLinks.classList.contains("is-open")) {
        closeNav();
        navToggle.focus();
      }
    });
  }

  /* Navbar hairline strengthens after scrolling past the hero */
  var navbar = document.querySelector(".navbar");
  if (navbar) {
    var onScroll = function () {
      navbar.classList.toggle("is-scrolled", window.scrollY > 24);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* Scroll reveal */
  var revealTargets = document.querySelectorAll("[data-reveal], [data-reveal-group]");

  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealTargets.forEach(function (el) {
      el.classList.add("is-visible");
    });
  } else {
    var revealObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
    );

    revealTargets.forEach(function (el) {
      revealObserver.observe(el);
    });
  }

  /* Card carousels (Why Us / Coaches) — CSS overflow + scroll-snap does the
     scrolling and the snapping; JS adds only what CSS cannot: pagination
     dots that drive the track, and that stay in sync when the user moves
     the track themselves. Each [data-carousel] section keeps its state in
     its own closure, so the two carousels never affect one another.
     Deliberately NOT gated behind a matchMedia check: above 900px the
     tracks are plain CSS grids with no overflow, so every handler below
     is inert there (nothing to scroll, dots hidden via CSS) — simpler and
     more robust than tracking the 900px breakpoint in JS as well. */
  document.querySelectorAll("[data-carousel]").forEach(function (carousel) {
    var track = carousel.querySelector("[data-carousel-track]");
    var dots = Array.prototype.slice.call(carousel.querySelectorAll("[data-carousel-dot]"));
    var cards = track ? Array.prototype.slice.call(track.children) : [];
    if (!track || !dots.length || !cards.length) return;

    // The scrollLeft each card needs in order to sit at the track's start
    // edge. The measurement cancels out the current scroll position, so the
    // result doesn't change as the track scrolls and can be cached — worth
    // doing, because the continuous auto-scroll below fires a scroll event
    // every frame, and re-measuring every card each time would force a
    // synchronous layout on every one of them. Invalidated on resize, where
    // it genuinely does change: card widths are percentages and
    // --content-pad is a clamp().
    var cachedTargets = null;

    function scrollTargets() {
      if (cachedTargets) return cachedTargets;
      var trackLeft = track.getBoundingClientRect().left;
      var padLeft = parseFloat(window.getComputedStyle(track).paddingLeft) || 0;
      cachedTargets = cards.map(function (card) {
        return card.getBoundingClientRect().left - trackLeft + track.scrollLeft - padLeft;
      });
      return cachedTargets;
    }

    function setActive(index) {
      dots.forEach(function (dot, i) {
        var isActive = i === index;
        dot.classList.toggle("is-active", isActive);
        dot.setAttribute("aria-current", isActive ? "true" : "false");
      });
    }

    // Whichever card sits closest to the current scroll position wins.
    // Deliberately not an IntersectionObserver: cards are wide enough that
    // two neighbours can straddle any fixed threshold, so which one "wins"
    // ends up depending on callback ordering. Comparing distances is
    // deterministic, and stays correct at the end of the track, where the
    // last card can never actually reach the start edge.
    function syncActive() {
      var current = track.scrollLeft;
      var nearest = 0;
      var shortest = Infinity;
      scrollTargets().forEach(function (target, i) {
        var distance = Math.abs(target - current);
        if (distance < shortest) {
          shortest = distance;
          nearest = i;
        }
      });
      setActive(nearest);
    }

    dots.forEach(function (dot, i) {
      dot.addEventListener("click", function () {
        // scrollTo on the track, not scrollIntoView on the card:
        // scrollIntoView also scrolls every scrollable ancestor, which
        // yanks the whole page down to the section instead of just
        // moving the carousel.
        track.scrollTo({
          left: scrollTargets()[i],
          behavior: reduceMotion ? "auto" : "smooth",
        });
        setActive(i);
      });
    });

    var pendingFrame = null;
    track.addEventListener(
      "scroll",
      function () {
        if (pendingFrame) return;
        pendingFrame = window.requestAnimationFrame(function () {
          pendingFrame = null;
          syncActive();
        });
      },
      { passive: true }
    );

    // Card widths are percentage-based, so a resize or rotation moves every
    // scroll target — drop the cache and re-resolve which dot is current.
    window.addEventListener(
      "resize",
      function () {
        cachedTargets = null;
        syncActive();
      },
      { passive: true }
    );

    // Drag-to-scroll for mouse/trackpad. Touch pointers are skipped on
    // purpose: the browser already scrolls the track natively, and driving
    // scrollLeft from touch-derived events fights that. Pointer capture
    // keeps the gesture bound to the track, so a drag released outside it
    // can't leave the carousel stuck mid-drag.
    var activePointer = null;
    var startX = 0;
    var startScroll = 0;

    track.addEventListener("pointerdown", function (event) {
      if (event.pointerType === "touch" || event.button !== 0) return;
      activePointer = event.pointerId;
      startX = event.clientX;
      startScroll = track.scrollLeft;
    });

    track.addEventListener("pointermove", function (event) {
      if (activePointer !== event.pointerId) return;
      var moved = event.clientX - startX;
      if (!track.hasPointerCapture(event.pointerId)) {
        // Only becomes a drag past a few pixels, so an ordinary click on
        // a coach card still opens that coach's page.
        if (Math.abs(moved) < 4) return;
        track.setPointerCapture(event.pointerId);
        track.classList.add("is-dragging");
      }
      event.preventDefault();
      track.scrollLeft = startScroll - moved;
    });

    function endDrag(event) {
      if (activePointer !== event.pointerId) return;
      if (track.hasPointerCapture(event.pointerId)) {
        track.releasePointerCapture(event.pointerId);
      }
      activePointer = null;
      track.classList.remove("is-dragging");
      syncActive();
    }

    track.addEventListener("pointerup", endDrag);
    track.addEventListener("pointercancel", endDrag);

    /* Continuous auto-scroll.

       The track glides at a constant speed rather than jumping card to
       card, so the time spent crossing a card is proportional to its width
       — pacing follows the space, and cards of different widths never feel
       rushed or laboured relative to one another.

       Deliberately cautious, because a carousel that moves on its own is
       easy to get wrong: it never starts under prefers-reduced-motion, it
       runs only while the cards are on screen and the tab is visible, it
       pauses on hover and while anything inside it has focus, and the first
       genuine interaction stops it for good. Once someone is driving the
       carousel themselves, taking it back mid-read is hostile.

       That last behaviour is also what satisfies WCAG 2.2.2 (Pause, Stop,
       Hide): swiping, dragging, tapping a dot, or moving the track with the
       wheel or arrow keys all halt the motion permanently. */
    var AUTO_SCROLL_PX_PER_SEC = 42;
    var END_PAUSE_MS = 1100;

    var autoStopped = reduceMotion; // reduced motion: never starts at all
    var rafId = null;
    var lastFrameAt = 0;
    var scrollDirection = 1;
    var resumeAt = 0;
    var lastAutoScrollLeft = track.scrollLeft;
    var pausedByHover = false;
    var pausedByFocus = false;
    // Defaults to on-screen so that if the observer below never reports (or
    // isn't supported), the carousel still moves. Failing the other way
    // would silently disable the whole feature.
    var offScreen = false;

    function carouselIsActive() {
      // Above 900px both tracks are plain CSS grids with nothing to scroll.
      return track.scrollWidth > track.clientWidth + 1;
    }

    function mayScroll() {
      return (
        !autoStopped &&
        !pausedByHover &&
        !pausedByFocus &&
        !offScreen &&
        !document.hidden &&
        carouselIsActive()
      );
    }

    function step(now) {
      if (!mayScroll()) {
        // Let the loop go idle rather than burning a callback every frame;
        // whatever un-pauses it calls startScrolling() again.
        rafId = null;
        lastFrameAt = 0;
        return;
      }
      rafId = window.requestAnimationFrame(step);

      // If the track has moved since the last frame by anything other than
      // this loop, the visitor is driving — hand it over for good. Checked
      // here rather than in a scroll listener because scroll events fire
      // asynchronously: by the time one arrived, the next frame had already
      // moved the track and overwritten the reference value, so the
      // divergence went unnoticed and the carousel kept gliding.
      var current = track.scrollLeft;
      if (Math.abs(current - lastAutoScrollLeft) > 4) {
        stopAuto();
        return;
      }

      if (!lastFrameAt) lastFrameAt = now;
      // Clamped so a long gap (background tab, slow frame) can't teleport
      // the track forward in a single jump.
      var elapsed = Math.min(now - lastFrameAt, 100);
      lastFrameAt = now;

      if (now < resumeAt) return;

      var maxScroll = track.scrollWidth - track.clientWidth;
      if (maxScroll <= 0) return;

      var next = current + (AUTO_SCROLL_PX_PER_SEC * elapsed) / 1000 * scrollDirection;

      // Reverse at each end and hold briefly. The alternative — snapping
      // back to the start — needs the cards duplicated in the DOM to look
      // seamless, which this deliberately avoids.
      if (next >= maxScroll) {
        next = maxScroll;
        scrollDirection = -1;
        resumeAt = now + END_PAUSE_MS;
      } else if (next <= 0) {
        next = 0;
        scrollDirection = 1;
        resumeAt = now + END_PAUSE_MS;
      }

      track.scrollLeft = next;
      // Read back rather than trusting `next`: browsers round scrollLeft, and
      // comparing a rounded value against an unrounded one on the next frame
      // would look like the visitor had nudged the track.
      lastAutoScrollLeft = track.scrollLeft;
    }

    function startScrolling() {
      if (autoStopped || rafId !== null) return;
      lastFrameAt = 0;
      rafId = window.requestAnimationFrame(step);
    }

    function stopAuto() {
      autoStopped = true;
      if (rafId !== null) {
        window.cancelAnimationFrame(rafId);
        rafId = null;
      }
      // Hand snapping back to the browser now that the visitor is driving.
      track.classList.remove("is-autoscrolling");
    }

    if (!autoStopped) {
      // Mandatory scroll-snap fights a continuous scroll — the browser keeps
      // pulling the track back to the nearest snap point. Suspended while the
      // carousel drives itself, and restored the moment the visitor takes over
      // so their swipes still settle neatly on a card.
      track.classList.add("is-autoscrolling");

      // Hover pause is for pointing devices only. Touch screens fire
      // synthetic mouseenter without a reliable matching mouseleave, which
      // would leave the carousel paused for good after a single tap.
      if (window.matchMedia("(hover: hover)").matches) {
        track.addEventListener("mouseenter", function () { pausedByHover = true; });
        track.addEventListener("mouseleave", function () {
          pausedByHover = false;
          startScrolling();
        });
      }
      track.addEventListener("focusin", function () { pausedByFocus = true; });
      track.addEventListener("focusout", function () {
        pausedByFocus = false;
        startScrolling();
      });
      document.addEventListener("visibilitychange", startScrolling);

      // Takeover is detected inside step() above, by comparing the track's
      // position against the last value this loop set. Raw input events are
      // the wrong signal — listening for touchstart (an earlier attempt)
      // fired when a finger merely landed on a card to scroll the *page*
      // vertically, killing the motion almost immediately on mobile.
      dots.forEach(function (dot) {
        dot.addEventListener("click", stopAuto);
      });

      // Only run while the cards are actually in view, so they aren't
      // silently gliding past while the visitor is elsewhere on the page.
      // Observes the track at threshold 0 ("any part visible") rather than a
      // fraction of the whole section: a section taller than the viewport can
      // never reach a high ratio, which would pin this off permanently.
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(
          function (entries) {
            entries.forEach(function (entry) {
              offScreen = !entry.isIntersecting;
            });
            startScrolling();
          },
          { threshold: 0 }
        ).observe(track);
      }

      startScrolling();
    }

    syncActive();
  });

  /* Animated stat counters */
  var statValues = document.querySelectorAll("[data-count-to]");

  function animateCount(el) {
    var target = parseInt(el.getAttribute("data-count-to"), 10);
    var suffix = el.getAttribute("data-suffix") || "";

    if (reduceMotion || !target) {
      el.textContent = target + suffix;
      return;
    }

    var duration = 1400;
    var start = null;

    function step(timestamp) {
      if (start === null) start = timestamp;
      var progress = Math.min((timestamp - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(eased * target) + suffix;
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    }

    window.requestAnimationFrame(step);
  }

  if (statValues.length && "IntersectionObserver" in window) {
    var countObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animateCount(entry.target);
            countObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.6 }
    );

    statValues.forEach(function (el) {
      countObserver.observe(el);
    });
  } else {
    statValues.forEach(animateCount);
  }
})();

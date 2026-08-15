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
    // edge. Measured live rather than cached: card widths are percentages
    // and --content-pad is a clamp(), so both change with the viewport.
    function scrollTargets() {
      var trackLeft = track.getBoundingClientRect().left;
      var padLeft = parseFloat(window.getComputedStyle(track).paddingLeft) || 0;
      return cards.map(function (card) {
        return card.getBoundingClientRect().left - trackLeft + track.scrollLeft - padLeft;
      });
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

    // Card widths are percentage-based, so a resize or rotation moves
    // every scroll target — re-resolve which dot is current afterwards.
    window.addEventListener("resize", syncActive, { passive: true });

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

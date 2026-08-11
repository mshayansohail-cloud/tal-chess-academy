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

    navToggle.addEventListener("click", function () {
      var isOpen = navLinks.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
      syncNavInert();
    });

    navLinks.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navLinks.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
        syncNavInert();
      });
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

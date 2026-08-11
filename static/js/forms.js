(function () {
  "use strict";

  /* Tab toggle between "Book a Trial" and "General Enquiry" */
  var tabs = document.querySelectorAll("[data-tab-target]");
  var feedback = document.getElementById("form-feedback");

  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      tabs.forEach(function (other) {
        other.classList.remove("is-active");
        other.setAttribute("aria-selected", "false");
      });
      tab.classList.add("is-active");
      tab.setAttribute("aria-selected", "true");

      document.querySelectorAll(".form-panel").forEach(function (panel) {
        panel.hidden = panel.id !== tab.getAttribute("data-tab-target");
      });

      hideFeedback();
    });
  });

  function showFeedback(message, isError) {
    if (!feedback) return;
    feedback.textContent = message;
    feedback.classList.toggle("form-feedback--error", Boolean(isError));
    feedback.hidden = false;
    feedback.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function hideFeedback() {
    if (!feedback) return;
    feedback.hidden = true;
    feedback.textContent = "";
  }

  function clearFieldErrors(form) {
    form.querySelectorAll("[data-error-for]").forEach(function (el) {
      el.textContent = "";
    });
    form.querySelectorAll(".form-input.has-error").forEach(function (el) {
      el.classList.remove("has-error");
    });
  }

  function showFieldErrors(form, errors) {
    var firstInvalid = null;
    Object.keys(errors).forEach(function (field) {
      var messages = errors[field];
      var text = Array.isArray(messages) ? messages.join(" ") : String(messages);
      var errorEl = form.querySelector('[data-error-for="' + field + '"]');
      var inputEl = form.querySelector('[name="' + field + '"]');

      if (errorEl) {
        errorEl.textContent = text;
      } else if (field !== "website") {
        // Field-less errors (e.g. non_field_errors) surface in the shared banner.
        showFeedback(text, true);
      }

      if (inputEl) {
        inputEl.classList.add("has-error");
        if (!firstInvalid) firstInvalid = inputEl;
      }
    });

    if (firstInvalid) firstInvalid.focus();
  }

  function bindForm(form, successMessage) {
    if (!form) return;
    var submitButton = form.querySelector('button[type="submit"]');
    var defaultLabel = submitButton ? submitButton.textContent : "";
    var isSubmitting = false;

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (isSubmitting) return;

      clearFieldErrors(form);
      hideFeedback();

      var formData = new FormData(form);
      var payload = {};
      formData.forEach(function (value, key) {
        payload[key] = value;
      });

      isSubmitting = true;
      if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = "Submitting…";
      }

      fetch(form.getAttribute("data-api-url"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then(function (response) {
          return response
            .json()
            .catch(function () {
              return null;
            })
            .then(function (body) {
              return { status: response.status, ok: response.ok, body: body };
            });
        })
        .then(function (result) {
          if (result.ok && result.body && result.body.success) {
            showFeedback(result.body.message || successMessage, false);
            form.reset();
            return;
          }

          if (result.status === 400 && result.body && result.body.errors) {
            showFieldErrors(form, result.body.errors);
            showFeedback("Please fix the highlighted fields and try again.", true);
            return;
          }

          if (result.status === 429) {
            showFeedback("You've submitted too many requests recently. Please try again later.", true);
            return;
          }

          showFeedback("Something went wrong on our end. Please try again, or contact us directly by phone or email.", true);
        })
        .catch(function () {
          showFeedback("We couldn't reach the server. Check your connection and try again.", true);
        })
        .finally(function () {
          isSubmitting = false;
          if (submitButton) {
            submitButton.disabled = false;
            submitButton.textContent = defaultLabel;
          }
        });
    });
  }

  bindForm(document.getElementById("trial-form"), "Your trial request has been submitted.");
  bindForm(document.getElementById("contact-form"), "Your message has been received.");
})();

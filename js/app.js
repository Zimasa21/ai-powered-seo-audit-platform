
document.addEventListener("DOMContentLoaded", () => {

  // ==========================================
  // INITIALISE LUCIDE ICONS
  // ==========================================

  if (window.lucide) {
    window.lucide.createIcons();
  }


  // ==========================================
  // SEO WORKSPACE DATE FILTER
  // ==========================================

  const dateButton = document.getElementById("dateFilterButton");
  const dateDropdown = document.getElementById("dateDropdown");
  const dateLabel = document.getElementById("selectedDateLabel");

  const startDate = document.getElementById("startDate");
  const endDate = document.getElementById("endDate");
  const applyDateRange = document.getElementById("applyDateRange");
  const dateError = document.getElementById("dateError");


  // Open and close date dropdown
  if (dateButton && dateDropdown) {

    dateButton.addEventListener("click", () => {
      const isOpen = dateDropdown.classList.toggle("show");

      dateButton.setAttribute("aria-expanded", isOpen);
    });


    // Quick date filters
    document.querySelectorAll("[data-filter]").forEach(button => {

      button.addEventListener("click", () => {

        const filter = button.dataset.filter;

        document.querySelectorAll("[data-filter]").forEach(item => {
          item.classList.remove("active");
        });

        button.classList.add("active");

        if (filter === "today") {
          dateLabel.textContent = "Today";
        } else {
          dateLabel.textContent = `Last ${filter} days`;
        }

        // Clear custom dates
        if (startDate) startDate.value = "";
        if (endDate) endDate.value = "";
        if (dateError) dateError.textContent = "";

        dateDropdown.classList.remove("show");
        dateButton.setAttribute("aria-expanded", "false");

        console.log("Selected date filter:", filter);

      });

    });


    // Apply custom date range
    if (applyDateRange) {

      applyDateRange.addEventListener("click", () => {

        const from = startDate.value;
        const to = endDate.value;

        dateError.textContent = "";

        if (!from || !to) {
          dateError.textContent = "Please select both dates.";
          return;
        }

        if (from > to) {
          dateError.textContent = "The start date cannot be after the end date.";
          return;
        }

        // Remove active quick filter
        document.querySelectorAll("[data-filter]").forEach(item => {
          item.classList.remove("active");
        });

        // Update date label
        dateLabel.textContent = `${from} – ${to}`;

        // Close dropdown
        dateDropdown.classList.remove("show");
        dateButton.setAttribute("aria-expanded", "false");

        console.log("Selected date range:", {
          from: from,
          to: to
        });

      });

    }


    // Close dropdown when clicking outside
    document.addEventListener("click", event => {

      if (!event.target.closest(".date-filter")) {
        dateDropdown.classList.remove("show");
        dateButton.setAttribute("aria-expanded", "false");
      }

    });

  }


  // ==========================================
  // WEBSITE SEO AUDIT FORM
  // ==========================================

  const form = document.getElementById("auditForm");
  const urlInput = document.getElementById("websiteUrl");
  const message = document.getElementById("formMessage");

  if (form && urlInput && message) {

    form.addEventListener("submit", (event) => {

      event.preventDefault();

      const enteredUrl = urlInput.value.trim();
      let parsedUrl;

      try {
        parsedUrl = new URL(enteredUrl);
      } catch {
        message.textContent = "Please enter a valid website URL, including https://";
        message.classList.add("message-error");
        urlInput.focus();
        return;
      }

      if (!["http:", "https:"].includes(parsedUrl.protocol)) {
        message.textContent = "Please use a website address beginning with http:// or https://";
        message.classList.add("message-error");
        return;
      }

      message.classList.remove("message-error");

      message.textContent =
        `Website captured: ${parsedUrl.hostname}. The next development step is connecting this form to the audit API.`;

    });

  }


  // ==========================================
  // NAVIGATION ACTIVE STATE
  // ==========================================

  document.querySelectorAll(".nav-link[href^='#']").forEach(link => {

    link.addEventListener("click", () => {

      document.querySelectorAll(".nav-link").forEach(item => {
        item.classList.remove("active");
      });

      link.classList.add("active");

    });

  });

});


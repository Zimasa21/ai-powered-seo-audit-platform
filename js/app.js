// Front-end interaction only. A real SEO audit needs a backend crawler and analysis API.
document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) window.lucide.createIcons();

  const form = document.getElementById("auditForm");
  const urlInput = document.getElementById("websiteUrl");
  const message = document.getElementById("formMessage");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    

// ==========================================
// SEO WORKSPACE DATE FILTER
// ==========================================

// 1. Get HTML elements
const dateButton = document.getElementById("dateFilterButton");
const dateDropdown = document.getElementById("dateDropdown");
const dateLabel = document.getElementById("selectedDateLabel");

const startDate = document.getElementById("startDate");
const endDate = document.getElementById("endDate");
const applyDateRange = document.getElementById("applyDateRange");
const dateError = document.getElementById("dateError");


// 2. Open and close date dropdown
dateButton.addEventListener("click", () => {
  dateDropdown.classList.toggle("show");
});


// 3. Quick date filters
document.querySelectorAll("[data-filter]").forEach(button => {

  button.addEventListener("click", () => {

    const filter = button.dataset.filter;

    // Remove previous active selection
    document.querySelectorAll("[data-filter]").forEach(item => {
      item.classList.remove("active");
    });

    button.classList.add("active");

    // Update selected date label
    if (filter === "today") {
      dateLabel.textContent = "Today";
    } else {
      dateLabel.textContent = `Last ${filter} days`;
    }

    // Clear custom date inputs and errors
    startDate.value = "";
    endDate.value = "";
    dateError.textContent = "";

    // Close dropdown
    dateDropdown.classList.remove("show");

    // Send selected filter to dashboard
    console.log("Selected date filter:", filter);

  });

});


// 4. Apply custom date range
applyDateRange.addEventListener("click", () => {

  const from = startDate.value;
  const to = endDate.value;

  // Clear previous error
  dateError.textContent = "";

  // Validate both dates
  if (!from || !to) {
    dateError.textContent = "Please select both dates.";
    return;
  }

  // Validate date order
  if (from > to) {
    dateError.textContent = "The start date cannot be after the end date.";
    return;
  }

  // Remove active state from quick filters
  document.querySelectorAll("[data-filter]").forEach(item => {
    item.classList.remove("active");
  });

  // Update dashboard date label
  dateLabel.textContent = `${from} – ${to}`;

  // Close dropdown
  dateDropdown.classList.remove("show");

  // Send selected range to dashboard
  console.log("Selected date range:", {
    from: from,
    to: to
  });

});


// 5. Close dropdown when clicking outside
document.addEventListener("click", event => {

  if (!event.target.closest(".date-filter")) {
    dateDropdown.classList.remove("show");
  }

});

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
    message.textContent = `Website captured: ${parsedUrl.hostname}. The next development step is connecting this form to the audit API.`;
  });

  // Highlight the current navigation item when a section link is selected.
  document.querySelectorAll(".nav-link[href^='#']").forEach((link) => {
    link.addEventListener("click", () => {
      document.querySelectorAll(".nav-link").forEach((item) => item.classList.remove("active"));
      link.classList.add("active");
    });
  });
});

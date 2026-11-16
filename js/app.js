// Front-end interaction only. A real SEO audit needs a backend crawler and analysis API.
document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) window.lucide.createIcons();

  const form = document.getElementById("auditForm");
  const urlInput = document.getElementById("websiteUrl");
  const message = document.getElementById("formMessage");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    
const dateButton = document.getElementById("dateFilterButton");
const dateDropdown = document.getElementById("dateDropdown");
const dateLabel = document.getElementById("selectedDateLabel");
const customDate = document.getElementById("customDate");

dateButton.addEventListener("click", () => {
  dateDropdown.classList.toggle("show");
});

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

    dateDropdown.classList.remove("show");

    // Pass the selected filter to your dashboard filtering logic.
    console.log("Selected date filter:", filter);
  });
});

const startDate = document.getElementById("startDate");
const endDate = document.getElementById("endDate");
const applyDateRange = document.getElementById("applyDateRange");
const dateError = document.getElementById("dateError");

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

  dateLabel.textContent =
    `${from} – ${to}`;

  dateDropdown.classList.remove("show");

  console.log("Selected date range:", {
    from: from,
    to: to
  });

  // Connect this range to your SEO dashboard data filtering.
});

  dateLabel.textContent = new Date(
    customDate.value + "T12:00:00"
  ).toLocaleDateString();

  dateDropdown.classList.remove("show");

  console.log("Selected custom date:", customDate.value);
});

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

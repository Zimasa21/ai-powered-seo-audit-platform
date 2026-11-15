// Front-end interaction only. A real SEO audit needs a backend crawler and analysis API.
document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) window.lucide.createIcons();

  const form = document.getElementById("auditForm");
  const urlInput = document.getElementById("websiteUrl");
  const message = document.getElementById("formMessage");

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

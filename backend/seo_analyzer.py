import json
import ipaddress
import socket
from urllib.parse import urlparse

import http
from bs4 import BeautifulSoup


MAX_PAGE_SIZE = 2 * 1024 * 1024  # 2 MB


def validate_public_url(url: str) -> str:
    """Validate a public HTTP or HTTPS URL before requesting it."""

    parsed = urlparse(url.strip())

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP and HTTPS website URLs are supported.")

    if not parsed.hostname:
        raise ValueError("Please enter a valid website URL.")

    if parsed.username or parsed.password:
        raise ValueError("Website URLs must not contain login credentials.")

    if parsed.port not in (None, 80, 443):
        raise ValueError("Only standard website ports are supported.")

    hostname = parsed.hostname.lower()

    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise ValueError("Localhost addresses cannot be analysed.")

    try:
        addresses = {
            result[4][0]
            for result in socket.getaddrinfo(
                hostname, None, type=socket.SOCK_STREAM
            )
        }
    except socket.gaierror:
        raise ValueError("The website domain could not be found.")

    if not addresses:
        raise ValueError("The website domain could not be found.")

    for address in addresses:
        ip = ipaddress.ip_address(address)

        if not ip.is_global:
            raise ValueError("Private or non-public website addresses cannot be analysed.")

    return url.strip()


def fetch_page(url: str):
    """Download a limited amount of HTML from one public webpage."""

    headers = {
        "User-Agent": "SEOAuditBot/1.0 (+website SEO analysis)",
        "Accept": "text/html,application/xhtml+xml",
    }

    try:
        with http.Client(
            timeout=15.0,
            follow_redirects=False,
            headers=headers,
        ) as client:

            with client.stream("GET", url) as response:

                if 300 <= response.status_code < 400:
                    raise ValueError(
                        "The website redirected this request. Please enter the final destination URL."
                    )

                response.raise_for_status()

                content_type = response.headers.get("content-type", "").lower()

                if "text/html" not in content_type and "application/xhtml+xml" not in content_type:
                    raise ValueError("The URL did not return an HTML webpage.")

                content_length = response.headers.get("content-length")

                if content_length and int(content_length) > MAX_PAGE_SIZE:
                    raise ValueError("This webpage is larger than the 2 MB analysis limit.")

                chunks = []
                total_size = 0

                for chunk in response.iter_bytes():
                    total_size += len(chunk)

                    if total_size > MAX_PAGE_SIZE:
                        raise ValueError("This webpage is larger than the 2 MB analysis limit.")

                    chunks.append(chunk)

                html = b"".join(chunks)

                return (
                    html.decode(response.encoding or "utf-8", errors="replace"),
                    response.status_code,
                    str(response.url),
                )

    except http.TimeoutException:
        raise ValueError("The website took too long to respond.")

    except http.HTTPStatusError as error:
        raise ValueError(
            f"The website returned HTTP status {error.response.status_code}."
        )

    except http.RequestError:
        raise ValueError("Could not connect to this website.")


def analyse_html(html: str, url: str, status_code: int):
    """Analyse one webpage and calculate SEO metrics."""

    soup = BeautifulSoup(html, "html.parser")

    issues = []
    checks = []

    def add_check(name, passed, points, maximum, message):
        checks.append({
            "name": name,
            "passed": bool(passed),
            "points": points if passed else 0,
            "maximum_points": maximum,
            "message": message,
        })

    def add_issue(title, description, severity="warning"):
        issues.append({
            "title": title,
            "description": description,
            "severity": severity,
        })

    # ------------------------------------------
    # TITLE
    # ------------------------------------------

    title_tag = soup.find("title")
    title = title_tag.get_text(" ", strip=True) if title_tag else ""

    title_length = len(title)

    title_ok = 30 <= title_length <= 60

    add_check(
        "Page title",
        title_ok,
        15,
        15,
        f"Title contains {title_length} characters."
    )

    if not title:
        add_issue(
            "Missing page title",
            "Add a descriptive title element to this webpage.",
            "error"
        )
    elif title_length < 30 or title_length > 60:
        add_issue(
            "Review page title length",
            "The title is outside the recommended 30–60 character guideline."
        )

    # ------------------------------------------
    # META DESCRIPTION
    # ------------------------------------------

    description_tag = soup.find(
        "meta",
        attrs={"name": lambda value: value and value.lower() == "description"}
    )

    description = (
        description_tag.get("content", "").strip()
        if description_tag else ""
    )

    description_length = len(description)

    description_ok = 120 <= description_length <= 160

    add_check(
        "Meta description",
        description_ok,
        10,
        10,
        f"Meta description contains {description_length} characters."
    )

    if not description:
        add_issue(
            "Missing meta description",
            "Write a unique description that summarises the webpage.",
            "error"
        )
    elif not description_ok:
        add_issue(
            "Review meta description length",
            "The description is outside the recommended 120–160 character guideline."
        )

    # ------------------------------------------
    # HEADINGS
    # ------------------------------------------

    h1_tags = soup.find_all("h1")
    h1_count = len(h1_tags)

    h1_ok = h1_count == 1

    add_check(
        "H1 heading",
        h1_ok,
        10,
        10,
        f"Found {h1_count} H1 heading(s)."
    )

    if h1_count == 0:
        add_issue(
            "Missing H1 heading",
            "Add one clear main heading describing the page.",
            "error"
        )
    elif h1_count > 1:
        add_issue(
            "Multiple H1 headings",
            "Review the page structure and ensure the main topic is clear."
        )

    headings = {
        level: len(soup.find_all(f"h{level}"))
        for level in range(1, 7)
    }

    heading_structure_ok = headings[1] > 0 and headings[2] > 0

    add_check(
        "Heading structure",
        heading_structure_ok,
        5,
        5,
        "H1 and H2 headings are present."
        if heading_structure_ok
        else "The page should use a clear H1 and H2 heading structure."
    )

    if not heading_structure_ok:
        add_issue(
            "Improve heading structure",
            "Use a clear main heading and descriptive subheadings."
        )

    # ------------------------------------------
    # VIEWPORT
    # ------------------------------------------

    viewport = soup.find(
        "meta",
        attrs={"name": lambda value: value and value.lower() == "viewport"}
    )

    viewport_ok = viewport is not None

    add_check(
        "Mobile viewport",
        viewport_ok,
        5,
        5,
        "A viewport meta tag is present."
        if viewport_ok
        else "No viewport meta tag was found."
    )

    if not viewport_ok:
        add_issue(
            "Missing mobile viewport",
            "Add a responsive viewport meta tag."
        )

    # ------------------------------------------
    # CANONICAL
    # ------------------------------------------

    canonical = soup.find(
        "link",
        rel=lambda value: value and "canonical" in [
            item.lower() for item in (
                value if isinstance(value, list) else value.split()
            )
        ]
    )

    canonical_ok = canonical is not None and bool(canonical.get("href"))

    add_check(
        "Canonical URL",
        canonical_ok,
        5,
        5,
        "A canonical URL is present."
        if canonical_ok
        else "No valid canonical URL was found."
    )

    if not canonical_ok:
        add_issue(
            "Missing canonical URL",
            "Consider adding a canonical link to identify the preferred page URL."
        )

    # ------------------------------------------
    # LANGUAGE
    # ------------------------------------------

    html_tag = soup.find("html")
    language = html_tag.get("lang", "").strip() if html_tag else ""

    language_ok = bool(language)

    add_check(
        "HTML language",
        language_ok,
        5,
        5,
        f"HTML language is {language}."
        if language_ok
        else "No HTML language attribute was found."
    )

    if not language_ok:
        add_issue(
            "Missing HTML language",
            "Add an appropriate lang attribute to the HTML element."
        )

    # ------------------------------------------
    # INDEXABILITY
    # ------------------------------------------

    robots_tag = soup.find(
        "meta",
        attrs={"name": lambda value: value and value.lower() in ("robots", "googlebot")}
    )

    robots_content = (
        robots_tag.get("content", "").lower()
        if robots_tag else ""
    )

    noindex = "noindex" in robots_content
    indexable = not noindex and status_code == 200

    add_check(
        "Indexability",
        indexable,
        10,
        10,
        "No noindex directive was detected."
        if indexable
        else "The page may be blocked from indexing."
    )

    if noindex:
        add_issue(
            "Noindex directive detected",
            "The page contains a robots directive instructing search engines not to index it.",
            "error"
        )

    # ------------------------------------------
    # IMAGE ALT TEXT
    # ------------------------------------------

    images = soup.find_all("img")
    images_without_alt = [
        image for image in images
        if not image.has_attr("alt") or not image.get("alt", "").strip()
    ]

    image_count = len(images)
    missing_alt_count = len(images_without_alt)

    image_score_ok = missing_alt_count == 0

    add_check(
        "Image alternative text",
        image_score_ok,
        10,
        10,
        f"{missing_alt_count} of {image_count} images have missing or empty alt text."
    )

    if missing_alt_count:
        add_issue(
            "Images missing alternative text",
            f"{missing_alt_count} of {image_count} images need descriptive alt text."
        )

    # ------------------------------------------
    # HTTPS
    # ------------------------------------------

    https_ok = urlparse(url).scheme == "https"

    add_check(
        "HTTPS security",
        https_ok,
        10,
        10,
        "The webpage uses HTTPS."
        if https_ok
        else "The webpage uses HTTP instead of HTTPS."
    )

    if not https_ok:
        add_issue(
            "HTTPS not detected",
            "Secure the website with HTTPS.",
            "error"
        )

    # ------------------------------------------
    # STRUCTURED DATA
    # ------------------------------------------

    json_ld_scripts = soup.find_all(
        "script",
        attrs={"type": lambda value: value and value.lower() == "application/ld+json"}
    )

    valid_json_ld = 0

    for script in json_ld_scripts:
        try:
            json.loads(script.string or script.get_text())
            valid_json_ld += 1
        except (json.JSONDecodeError, TypeError):
            pass

    schema_ok = valid_json_ld > 0

    add_check(
        "Structured data",
        schema_ok,
        5,
        5,
        f"Found {valid_json_ld} valid JSON-LD block(s)."
    )

    if not schema_ok:
        add_issue(
            "Structured data not detected",
            "Consider adding relevant Schema.org structured data."
        )

    # ------------------------------------------
    # OPEN GRAPH
    # ------------------------------------------

    og_title = soup.find("meta", property="og:title")
    og_description = soup.find("meta", property="og:description")

    open_graph_ok = og_title is not None and og_description is not None

    add_check(
        "Open Graph metadata",
        open_graph_ok,
        5,
        5,
        "Open Graph title and description are present."
        if open_graph_ok
        else "Open Graph title or description is missing."
    )

    if not open_graph_ok:
        add_issue(
            "Incomplete Open Graph metadata",
            "Add Open Graph title and description tags for social sharing."
        )

    # ------------------------------------------
    # INTERNAL LINKS
    # ------------------------------------------

    parsed_page_url = urlparse(url)
    internal_links = 0
    external_links = 0

    for link in soup.find_all("a", href=True):
        href = link.get("href", "").strip()

        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue

        target = urlparse(href)

        if not target.netloc or target.netloc.lower() == parsed_page_url.netloc.lower():
            internal_links += 1
        else:
            external_links += 1

    links_ok = internal_links > 0

    add_check(
        "Internal links",
        links_ok,
        5,
        5,
        f"Found {internal_links} internal link(s)."
        if links_ok
        else "No internal links were detected."
    )

    if not links_ok:
        add_issue(
            "No internal links detected",
            "Add relevant internal links to help users and search engines navigate the website."
        )

    # ------------------------------------------
    # HTTP RESPONSE
    # ------------------------------------------

    status_ok = status_code == 200

    add_check(
        "HTTP response",
        status_ok,
        5,
        5,
        f"The webpage returned HTTP {status_code}."
    )

    if not status_ok:
        add_issue(
            "Unexpected HTTP response",
            f"The webpage returned HTTP status {status_code}.",
            "error"
        )

    # ------------------------------------------
    # SCORE AND OPPORTUNITIES
    # ------------------------------------------

    total_score = sum(check["points"] for check in checks)
    maximum_score = sum(check["maximum_points"] for check in checks)

    health_score = round((total_score / maximum_score) * 100)

    opportunities = [
        issue for issue in issues
        if issue["title"] in [
            "Missing page title",
            "Review page title length",
            "Missing meta description",
            "Review meta description length",
            "Missing H1 heading",
            "Multiple H1 headings",
            "Improve heading structure",
            "Structured data not detected",
            "Incomplete Open Graph metadata",
        ]
    ]

    # ------------------------------------------
    # GEO / AI READINESS SIGNALS
    # ------------------------------------------

    ai_checks = [
        {
            "name": "Structured data",
            "passed": schema_ok,
            "message": "Valid JSON-LD detected." if schema_ok else "No valid JSON-LD detected."
        },
        {
            "name": "Clear page title",
            "passed": bool(title),
            "message": "Page title is present." if title else "Page title is missing."
        },
        {
            "name": "Descriptive headings",
            "passed": h1_count == 1 and headings[2] > 0,
            "message": "Main heading structure detected." if h1_count == 1 and headings[2] > 0 else "Review the heading structure."
        },
        {
            "name": "Page description",
            "passed": bool(description),
            "message": "Meta description is present." if description else "Meta description is missing."
        },
        {
            "name": "Language information",
            "passed": language_ok,
            "message": "Page language is declared." if language_ok else "Declare the page language."
        },
        {
            "name": "Canonical URL",
            "passed": canonical_ok,
            "message": "Canonical URL is present." if canonical_ok else "Canonical URL is missing."
        },
    ]

    return {
        "url": url,
        "http_status": status_code,
        "seo_health_score": health_score,
        "issues_count": len(issues),
        "content_opportunities": len(opportunities),
        "ai_visibility_checks": len(ai_checks),
        "ai_readiness_passed": sum(1 for item in ai_checks if item["passed"]),
        "title": title,
        "meta_description": description,
        "title_length": title_length,
        "description_length": description_length,
        "headings": headings,
        "images": {
            "total": image_count,
            "missing_alt": missing_alt_count,
        },
        "links": {
            "internal": internal_links,
            "external": external_links,
        },
        "checks": checks,
        "issues": issues,
        "ai_checks": ai_checks,
    }


def analyse_website(url: str):
    """Fetch and analyse one webpage."""

    safe_url = validate_public_url(url)

    html, status_code, final_url = fetch_page(safe_url)

    return analyse_html(html, final_url, status_code)

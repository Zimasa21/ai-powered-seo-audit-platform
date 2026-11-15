# AI-powered SEO Audit and Optimisation Platform

A dark-green dashboard prototype for a platform that aims to combine technical SEO auditing, content opportunities, AI-search/GEO recommendations and before-and-after improvement tracking.

## Current status

**Frontend prototype only.** The dashboard currently displays illustrative sample metrics and a working URL-entry interaction. It does not yet crawl websites, generate AI recommendations, connect to Google Search Console or calculate real improvement results.

## Features represented in the prototype

- SEO health overview
- Website audit entry point
- Technical SEO recommendations
- Keyword and content opportunity areas
- AI search / Generative Engine Optimisation (GEO) area
- Before-and-after improvement tracking workflow
- Responsive dark-green dashboard design

## Run locally

No build tools are required for the frontend prototype.

1. Download or clone this repository.
2. Open the project folder.
3. Open `index.html` in a browser.

For a local development server, you can use Python:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Project structure

```text
ai-powered-seo-audit-platform/
├── index.html
├── css/
│   └── style.css
├── js/
│   └── app.js
└── README.md
```

## Suggested development roadmap

1. Build a Python/FastAPI backend.
2. Create a crawler with URL limits, timeouts, robots.txt handling and safe URL validation.
3. Extract titles, meta descriptions, H1s, canonical tags, status codes and internal links.
4. Add duplicate metadata, broken-link and indexability checks.
5. Store crawl snapshots and recommendations in a database.
6. Add keyword and content opportunity analysis using permitted data sources.
7. Add evidence-based GEO content checks. Avoid claiming that the tool can guarantee AI-search citations or rankings.
8. Re-crawl after implementation and compare the same metrics over time.
9. Add tests, documentation and deployment.

## Important engineering and security notes

- Treat submitted URLs and crawled links as untrusted input.
- Protect the crawler against server-side request forgery (SSRF), including localhost, private network and cloud metadata addresses.
- Apply crawl limits, request timeouts, rate limits and domain restrictions.
- Respect robots.txt, site terms and applicable laws.
- Do not expose API keys in frontend JavaScript or commit secrets to GitHub.
- Distinguish measured results from estimates and recommendations.

## Tech stack direction

- Frontend: HTML, CSS, JavaScript
- Backend: Python and FastAPI
- Crawling and parsing: Requests / HTTPX and BeautifulSoup
- Database: SQLite initially, with PostgreSQL as a possible later option
- Testing: Pytest

## Licence

No licence has been added yet. Choose a licence before inviting others to reuse or contribute to the project.

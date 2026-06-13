# LinkedIn Web Scraper (prototype)

This is a small prototype that provides a frontend to enter keywords and a FastAPI backend that uses a simple web-scraper to discover public LinkedIn profile pages via DuckDuckGo search results.

Important: This project is for educational/demo purposes only. Respect robots.txt, terms of service, and privacy policies. Do not use this to scrape private or protected data.

Features

- Frontend: `frontend/index.html` — a tiny UI to enter a query and show results.
- Backend: `backend/main.py` (FastAPI) and `backend/scraper.py` (simple requests + BeautifulSoup).

Quick start

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the backend:

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

3. Open http://127.0.0.1:8000 in your browser.

Security & secrets

- Keep any API keys, credentials, or tokens out of the repository. Use a `.env` file or environment variables instead. `.env` is included in `.gitignore`.

Limitations & next steps

- This uses public search results only. It does not authenticate to LinkedIn.
- Add rate-limiting, caching, retries, robust HTML parsing and tests before production use.

# linkedin-web-scraper

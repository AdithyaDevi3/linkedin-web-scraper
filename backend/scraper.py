import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def search_linkedin_public_profiles(query: str, limit: int = 5) -> List[Dict]:
    """
    Simple heuristic: use DuckDuckGo site:linkedin.com/search or /in/ public pages.
    This avoids using LinkedIn's private APIs and stays on public pages.
    Returns a list of dicts with title, url, snippet.
    """
    results = []
    # Use DuckDuckGo HTML version to search site:linkedin.com "query"
    params = {
        'q': f"site:linkedin.com/in/ {query}",
        'kl': 'us-en'
    }
    try:
        r = requests.get('https://html.duckduckgo.com/html/', params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except Exception:
        return results

    soup = BeautifulSoup(r.text, 'html.parser')
    # DuckDuckGo returns results in links with class 'result__a' inside 'result'
    anchors = soup.select('a.result__a')
    count = 0
    for a in anchors:
        if count >= limit:
            break
        href = a.get('href')
        title = a.get_text(strip=True)
        # Try to find snippet
        snippet = ''
        parent = a.find_parent()
        if parent:
            s = parent.select_one('.result__snippet')
            if s:
                snippet = s.get_text(strip=True)

        results.append({'title': title, 'url': href, 'snippet': snippet})
        count += 1
        time.sleep(0.5)

    return results

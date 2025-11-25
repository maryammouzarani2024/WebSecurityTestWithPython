import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

session = requests.Session()      # <-- keeps login cookies & headers

visited = set()
api_endpoints = set()

url_regex = r'https?://[^\s"\'<>]+|/[\w\-/]+(?:\.[a-z]+)?'

common_api_paths = [
    "api", "api/v1", "api/v2", "api/v3",
    "auth", "login", "logout", "register",
    "users", "user", "admin", "token",
    "health", "status", "config", "search"
]


# ---------------------- LOGIN HANDLER -------------------------
def login():
    login_url = "https://0a7f00dd04935bf681e0d91800c3001c.web-security-academy.net/login"   # change this

    payload = {
        "username": "wiener",
        "password": "peter"
    }

    # Optional: custom headers
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    print("[+] Logging in...")
    r = session.post(login_url, data=payload, headers=headers)

    if r.status_code == 200:
        print("[+] Login success (HTTP 200).")
    else:
        print(f"[!] Login returned HTTP {r.status_code}. Check credentials.")

# --------------------------------------------------------------


def extract_urls_from_text(text, base_url):
    matches = re.findall(url_regex, text)
    for m in matches:
        full = urljoin(base_url, m)
        if any(x in full for x in ["/api", "/v1", "/v2"]):
            api_endpoints.add(full)


def crawl(url, domain):
    if url in visited:
        return
    visited.add(url)

    try:
        print(f"[+] Crawling: {url}")
        resp = session.get(url, timeout=10)
    except:
        return

    content_type = resp.headers.get("content-type", "")

    # JS file handling
    if "javascript" in content_type:
        extract_urls_from_text(resp.text, url)
        return

    # Only parse HTML
    if "text/html" not in content_type:
        return

    soup = BeautifulSoup(resp.text, "html.parser")

    # JS scripts
    for script in soup.find_all("script", src=True):
        js_url = urljoin(url, script["src"])
        if urlparse(js_url).netloc == domain:
            crawl(js_url, domain)

    # Links
    for link in soup.find_all("a", href=True):
        new_url = urljoin(url, link["href"])
        if urlparse(new_url).netloc == domain:
            crawl(new_url, domain)

    # Extract URLs
    extract_urls_from_text(resp.text, url)


def brute_force_api(base_url):
    print("\n[+] Starting API brute-force with session...")
    for path in common_api_paths:
        url = urljoin(base_url, "/" + path)
        try:
            r = session.get(url, timeout=5)
            if r.status_code < 400:
                print(f"  [FOUND] {url}  ({r.status_code})")
                api_endpoints.add(url)
        except:
            pass


# ======================== MAIN ===============================

start_url = "https://0a7f00dd04935bf681e0d91800c3001c.web-security-academy.net/"
domain = urlparse(start_url).netloc

login()
crawl(start_url, domain)
brute_force_api(start_url)

print("\n==============================")
print("   Discovered API Endpoints")
print("==============================")
for endpoint in sorted(api_endpoints):
    print(endpoint)


import requests
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urljoin, urlparse

def web_crawler(start_url, max_pages=5):
    visited = set()
    queue = deque([start_url])

    domain = urlparse(start_url).netloc

    while queue and len(visited) < max_pages:
        url = queue.popleft()

        if url in visited:
            continue

        if urlparse(url).netloc != domain:
            continue

        try:
            response = requests.get(
                url,
                timeout=5,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            response.raise_for_status()

            if "text/html" not in response.headers.get(
                "Content-Type", ""
            ).lower():
                continue

            visited.add(url)
            soup = BeautifulSoup(response.text, "html.parser")

            print("\nURL:", url)
            print("Title:", soup.title.get_text(strip=True)
                  if soup.title else "No title")

            # Extract hyperlinks
            for tag in soup.find_all("a", href=True):
                link = urljoin(url, tag["href"]).split("#")[0]

                if (urlparse(link).scheme in ("http", "https")
                        and urlparse(link).netloc == domain
                        and link not in visited):
                    queue.append(link)

        except requests.RequestException as error:
            print("Error:", url, error)

    print("\nTotal pages crawled:", len(visited))


start_url = input("Enter starting URL: ").strip()
web_crawler(start_url)

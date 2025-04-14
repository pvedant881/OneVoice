# crawlers/website_crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def crawl_website(base_url, max_pages=100, output_file=None):
    visited = set()
    to_visit = [base_url]
    contents = []

    headers = {"User-Agent": "Mozilla/5.0"}
    count = 0

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = " ".join(soup.stripped_strings)
            content_entry = {"url": url, "text": text[:3000]}
            contents.append(content_entry)
            visited.add(url)
            count += 1

            if count % 100 == 0:
                print(f"[{count}] pages crawled...")

            for link in soup.find_all('a', href=True):
                full_url = urljoin(base_url, link['href'])
                if base_url in full_url and full_url not in visited and full_url not in to_visit:
                    to_visit.append(full_url)
        except Exception as e:
            contents.append({"url": url, "error": str(e)})

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(contents, f, indent=4)

    return [f"--- Content from {item['url']} ---\n{item['text'][:3000]}" for item in contents if 'text' in item]

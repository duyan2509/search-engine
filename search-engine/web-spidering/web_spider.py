import requests
from bs4 import BeautifulSoup
import sqlite3
from urllib.parse import urljoin

def crawler(start_url, max_pages=100):
    connection = sqlite3.connect("crawled_pages.db")
    c = connection.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pages (
        id INTEGER PRIMARY KEY,
        url TEXT UNIQUE,
        html TEXT
        )
    ''')
    connection.commit()
    url_frontier = [start_url]
    visited = set()
    while url_frontier and len(visited) < max_pages:

        url = url_frontier.pop(0)
        if url in visited:
            continue
        print(f"Crawling {url}")
        response = requests.get(url)
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        html_content = str(soup) if soup else ""

        c.execute('INSERT OR IGNORE INTO pages (url,html) VALUES (?,?)', (url,html_content))
        connection.commit()
        links = soup.find_all("a")
        for link in links:
            href = link.get("href")
            if href:
                if href.startswith("#"):
                    continue
                full_url = urljoin(url, href)
                if full_url not in visited and full_url.startswith("http"):
                    url_frontier.append(full_url)

        visited.add(url)
    connection.close()
    print("Crawling complete")
seed_urls = ["https://daa.uit.edu.vn"]
for url in seed_urls:
    crawler(url,50)
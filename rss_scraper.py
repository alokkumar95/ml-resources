import argparse
import feedparser
import requests
from bs4 import BeautifulSoup
from readability import Document
import json
from pathlib import Path
import time


def parse_feed(feed_url):
    try:
        resp = requests.get(
            feed_url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
                "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
                "Referer": "https://www.pib.gov.in/",
            },
        )
        resp.raise_for_status()
        feed = feedparser.parse(resp.content)
    except Exception as e:
        print(f"Failed to fetch or parse feed {feed_url}: {e}")
        return []

    entries = []
    for entry in feed.entries:
        entries.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", ""),
        })
    return entries


def extract_article(url, timeout=10):
    try:
        resp = requests.get(
            url,
            timeout=timeout,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Referer": "https://www.pib.gov.in/",
            },
        )
        resp.raise_for_status()
        doc = Document(resp.text)
        soup = BeautifulSoup(doc.summary(), "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        return {
            "title": doc.title(),
            "content": text[:5000],
        }
    except Exception as e:
        return {"title": "", "content": f"[Error scraping {url}: {e}]"}


def scrape_rss(feed_url, delay=1, output=None):
    entries = parse_feed(feed_url)
    results = []

    for i, entry in enumerate(entries, 1):
        print(f"[{i}/{len(entries)}] {entry['title']}")
        article = extract_article(entry["link"])
        results.append({**entry, "scraped": article})
        time.sleep(delay)

    if output:
        Path(output).write_text(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"\nSaved to {output}")
    else:
        print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape articles from an RSS feed.")
    parser.add_argument("feed_url", help="URL of the RSS feed")
    parser.add_argument("-o", "--output", help="Output JSON file path")
    parser.add_argument("--delay", type=float, default=1, help="Delay between requests in seconds")
    args = parser.parse_args()

    scrape_rss(args.feed_url, delay=args.delay, output=args.output)

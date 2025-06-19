import feedparser
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pdfkit
import os

# === إعداد التاريخ ===
today = datetime.now().strftime("%Y-%m-%d")
output_file = f"daily_report_{today}.md"

# === مصادر RSS ===
feeds = {
    "HackerOne": "https://hackerone.com/hacktivity.rss",
    "Exploit-DB": "https://www.exploit-db.com/rss.xml",
    "PacketStorm": "https://packetstormsecurity.com/files/feed.xml"
}

# === Twitter بديل (Scraping من Nitter) ===
hashtags = {
    "#bugbountytips": "https://nitter.net/search?f=tweets&q=%23bugbountytips",
    "#bugbounty": "https://nitter.net/search?f=tweets&q=%23bugbounty",
    "#infosec": "https://nitter.net/search?f=tweets&q=%23infosec"
}

def fetch_tweets_from_nitter(url, max_tweets=5):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        tweets = soup.find_all("div", class_="tweet-content")
        return [tweet.text.strip() for tweet in tweets[:max_tweets]]
    except Exception as e:
        return [f"_Error fetching tweets: {e}_"]

# === كتابة الملف النهائي ===
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"# 🛡️ Daily Bug Bounty Digest — {today}\n\n")

    # أخبار RSS
    for name, url in feeds.items():
        f.write(f"## 🔍 {name} Updates\n")
        feed = feedparser.parse(url)

        if not feed.entries:
            f.write("_No entries found._\n\n")
            continue

        for entry in feed.entries[:5]:
            title = entry.title
            link = entry.link
            f.write(f"- [{title}]({link})\n")
        f.write("\n")

    # تغريدات من نيتّر
    for tag, url in hashtags.items():
        f.write(f"## 🐦 Tweets from {tag}\n")
        tweets = fetch_tweets_from_nitter(url)
        for tweet in tweets:
            f.write(f"- {tweet}\n")

# === Convert .md to .html then PDF ===
html_file = f"{output_file.replace('.md', '.html')}"
pdf_file = f"{output_file.replace('.md', '.pdf')}"

# Markdown to HTML
with open(output_file, "r", encoding="utf-8") as f:
    content_md = f.read()

import markdown
content_html = markdown.markdown(content_md)

with open(html_file, "w", encoding="utf-8") as f:
    f.write(content_html)

# HTML to PDF (requires wkhtmltopdf)
try:
    pdfkit.from_file(html_file, pdf_file)
    print(f"✅ PDF created: {pdf_file}")
except Exception as e:
    print(f"❌ Failed to generate PDF: {e}")
        f.write("\n")

print(f"✅ Report created: {output_file}")

import feedparser
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pdfkit
import markdown

# التاريخ
today = datetime.now().strftime("%Y-%m-%d")
output_md = f"daily_report_{today}.md"
output_html = output_md.replace(".md", ".html")
output_pdf = output_md.replace(".md", ".pdf")

# مصادر RSS
feeds = {
    "HackerOne": "https://hackerone.com/hacktivity.rss",
    "Exploit-DB": "https://www.exploit-db.com/rss.xml",
    "PacketStorm": "https://packetstormsecurity.com/files/feed.xml"
}

hashtags = {
    "#bugbountytips": "https://nitter.net/search?f=tweets&q=%23bugbountytips",
    "#bugbounty": "https://nitter.net/search?f=tweets&q=%23bugbounty",
    "#infosec": "https://nitter.net/search?f=tweets&q=%23infosec"
}

def fetch_tweets_from_nitter(url, max_tweets=5):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        tweets = soup.find_all("div", class_="tweet-content")
        return [t.text.strip() for t in tweets[:max_tweets]]
    except Exception as e:
        return [f"_Error fetching tweets: {e}_"]

with open(output_md, "w", encoding="utf-8") as f:
    f.write(f"# 🛡️ Daily Bug Bounty Digest — {today}\n\n")
    for name, url in feeds.items():
        f.write(f"## 🔍 {name} Updates\n")
        feed = feedparser.parse(url)
        if not feed.entries:
            f.write("_No entries found._\n\n")
            continue
        for entry in feed.entries[:5]:
            f.write(f"- [{entry.title}]({entry.link})\n")
        f.write("\n")
    for tag, url in hashtags.items():
        f.write(f"## 🐦 Tweets from {tag}\n")
        tweets = fetch_tweets_from_nitter(url)
        for tweet in tweets:
            f.write(f"- {tweet}\n")
        f.write("\n")

# Markdown > HTML > PDF
html_content = markdown.markdown(open(output_md, encoding="utf-8").read())
with open(output_html, "w", encoding="utf-8") as f:
    f.write(html_content)

try:
    pdfkit.from_file(output_html, output_pdf)
except Exception as e:
    print(f"PDF generation failed: {e}")

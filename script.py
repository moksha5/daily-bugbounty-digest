import feedparser
from datetime import datetime

# مصادر الـ RSS
feeds = {
    "HackerOne": "https://hackerone.com/hacktivity.rss",
    "Exploit-DB": "https://www.exploit-db.com/rss.xml"
}

# الملف النهائي
today = datetime.now().strftime("%Y-%m-%d")
output_file = f"daily_report_{today}.md"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"# 🛡️ Daily Bug Bounty Digest — {today}\n\n")

    for name, url in feeds.items():
        f.write(f"## 🔍 {name} Updates\n")
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:  # أول 5 عناصر فقط لكل مصدر
            title = entry.title
            link = entry.link
            f.write(f"- [{title}]({link})\n")

        f.write("\n\n")

print(f"✅ Report generated: {output_file}")

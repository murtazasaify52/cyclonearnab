import os
import requests
import feedparser
from datetime import datetime

# Data source 1: IMD India Meteorological Department RSS (most relevant to your region)
IMD_RSS = "https://cap-sources.s3.amazonaws.com/in-imd-en/rss.xml"
# Data source 2: GDACS global disaster alerts (backup)
GDACS_RSS = "https://www.gdacs.org/xml/rss.xml"

def fetch_feed(url):
    try:
        headers = {'User-Agent': 'CycloneArnab/1.0'}
        response = requests.get(url, headers=headers, timeout=15)
        return feedparser.parse(response.content)
    except Exception as e:
        print(f"Fetch error {url}: {e}")
        return None

def generate_html():
    imd_feed = fetch_feed(IMD_RSS)
    gdacs_feed = fetch_feed(GDACS_RSS)
    
    items_html = ""
    
    # Process IMD data
    if imd_feed and hasattr(imd_feed, 'entries'):
        for entry in imd_feed.entries[:10]:
            title = entry.get('title', 'No Title')
            link = entry.get('link', '#')
            summary = entry.get('summary', '')[:200]
            items_html += f"""
            <div style="border-bottom:1px solid #ddd; padding:15px 0;">
                <h3><a href="{link}" target="_blank">{title}</a></h3>
                <p>{summary}...</p>
                <small>Source: IMD | {datetime.now().strftime('%Y-%m-%d %H:%M')}</small>
            </div>
            """
    
    # Process GDACS data (only take cyclone-related entries)
    if gdacs_feed and hasattr(gdacs_feed, 'entries'):
        for entry in gdacs_feed.entries:
            event_type = entry.get('gdacs_eventtype', '')
            if 'TC' in event_type or 'Cyclone' in str(event_type):
                title = entry.get('title', 'Cyclone Alert')
                link = entry.get('link', '#')
                summary = entry.get('summary', '')[:200]
                items_html += f"""
                <div style="border-bottom:1px solid #ddd; padding:15px 0;">
                    <h3><a href="{link}" target="_blank">{title}</a></h3>
                    <p>{summary}...</p>
                    <small>Source: GDACS | {datetime.now().strftime('%Y-%m-%d %H:%M')}</small>
                </div>
                """

    if not items_html:
        items_html = "<p>No active cyclone warnings at the moment. Please check back later.</p>"

    # SEO-optimized HTML template
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyclone Arnab - Latest Cyclone Warnings & Updates</title>
    <meta name="description" content="Real-time cyclone warnings, updates, and news for the Indian Ocean and surrounding areas. Auto-updated from IMD and GDACS.">
    <meta name="keywords" content="cyclone, India, IMD, weather warning, tropical storm">
    <link rel="canonical" href="https://cyclonearnab.com/">
    <!-- Structured data to help Google understand this is a news/alert page -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "Cyclone Arnab",
      "url": "https://cyclonearnab.com/",
      "description": "Latest cyclone warnings and updates"
    }}
    </script>
</head>
<body style="font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
    <header>
        <h1>🌀 Cyclone Arnab</h1>
        <p><strong>Latest Warnings & Updates (Auto-refreshed)</strong></p>
        <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</p>
        <hr>
    </header>
    <main>
        {items_html}
    </main>
    <footer style="margin-top:40px; font-size:0.8em; color:#666;">
        <p>Data sources: IMD (India Meteorological Department) & GDACS. This site is for informational purposes.</p>
    </footer>
</body>
</html>"""
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html generated successfully.")

if __name__ == "__main__":
    generate_html()

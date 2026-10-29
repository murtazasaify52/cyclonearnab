import requests
import feedparser
from datetime import datetime

IMD_RSS = "https://cap-sources.s3.amazonaws.com/in-imd-en/rss.xml"
GDACS_RSS = "https://www.gdacs.org/xml/rss.xml"
DOMAIN = "https://cyclonearnab.com"

NAV = """<nav>
  <a href="/">Home</a>
  <a href="/about.html">About Us</a>
  <a href="/terms.html">Terms &amp; Conditions</a>
  <a href="/privacy.html">Privacy Policy</a>
  <a href="/contact.html">Contact</a>
</nav>"""

def head(title, desc, url):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{DOMAIN}{url}">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<header><div class="container"><h1><a href="/">🌀 Cyclone Arnab</a></h1>{NAV}</div></header>
<main><div class="container">"""

def foot():
    return f"""</div></main>
<footer><div class="container">
<p>&copy; {datetime.now().year} Cyclone Arnab. All rights reserved.</p>
<p><a href="/about.html">About</a> | <a href="/terms.html">Terms</a> | <a href="/privacy.html">Privacy</a> | <a href="/contact.html">Contact</a></p>
<p style="margin-top:10px;font-size:0.8em;">Data sources: IMD &amp; GDACS. For informational purposes only.</p>
</div></footer>
</body></html>"""

def fetch_feed(url):
    try:
        r = requests.get(url, headers={'User-Agent': 'CycloneArnab/1.0'}, timeout=15)
        return feedparser.parse(r.content)
    except Exception as e:
        print(f"Fetch error {url}: {e}")
        return None

def build_index():
    items = ""
    imd = fetch_feed(IMD_RSS)
    gdacs = fetch_feed(GDACS_RSS)
    if imd and hasattr(imd, 'entries'):
        for e in imd.entries[:10]:
            items += f"""<div class="card"><h3><a href="{e.get('link','#')}" target="_blank" rel="noopener">{e.get('title','No Title')}</a></h3>
            <p>{e.get('summary','')[:220]}...</p><small>Source: IMD | {datetime.now().strftime('%Y-%m-%d %H:%M')}</small></div>"""
    if gdacs and hasattr(gdacs, 'entries'):
        for e in gdacs.entries:
            if 'TC' in str(e.get('gdacs_eventtype','')) or 'Cyclone' in str(e.get('title','')):
                items += f"""<div class="card"><h3><a href="{e.get('link','#')}" target="_blank" rel="noopener">{e.get('title','Cyclone Alert')}</a></h3>
                <p>{e.get('summary','')[:220]}...</p><small>Source: GDACS | {datetime.now().strftime('%Y-%m-%d %H:%M')}</small></div>"""
    if not items:
        items = "<p>No active cyclone warnings at the moment. Please check back later.</p>"
    html = head("Cyclone Arnab - Latest Cyclone Warnings & Updates",
                "Real-time cyclone warnings, updates, and news for the Indian Ocean. Auto-updated from IMD and GDACS.", "/")
    html += f'<div class="updated">Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}</div>'
    html += items + foot()
    open('index.html', 'w', encoding='utf-8').write(html)

def build_static():
    pages = {
        "about.html": ("About Us", "Learn about Cyclone Arnab, our mission, and data sources.", """
<h2>About Cyclone Arnab</h2>
<p>Cyclone Arnab is an independent, non-commercial information website dedicated to providing timely cyclone warnings, track updates, and safety information for the Indian Ocean region and surrounding areas.</p>
<h3>Our Mission</h3>
<p>Our goal is to make official cyclone alerts easier to find and understand for everyone — especially coastal communities that are most vulnerable to tropical cyclones.</p>
<h3>Data Sources</h3>
<ul>
<li><strong>India Meteorological Department (IMD)</strong> — official cyclone warnings for the North Indian Ocean.</li>
<li><strong>GDACS</strong> — global disaster alerts supported by the United Nations.</li>
</ul>
<h3>Important Disclaimer</h3>
<p>This site aggregates publicly available data. It is <strong>not</strong> a substitute for official government warnings. Always follow instructions from your local authorities during a cyclone emergency.</p>
"""),
        "terms.html": ("Terms & Conditions", "Terms and conditions for using Cyclone Arnab.", """
<h2>Terms &amp; Conditions</h2>
<p>By accessing cyclonearnab.com, you agree to the following terms.</p>
<h3>1. Informational Purpose Only</h3>
<p>All content on this website is provided for general informational purposes. It does not constitute official meteorological advice and should not be relied upon as the sole source for emergency decisions.</p>
<h3>2. No Warranty</h3>
<p>While we strive to display accurate and timely information, we make no warranties of any kind regarding accuracy, completeness, or reliability. Data is sourced from third parties and may be delayed or contain errors.</p>
<h3>3. Limitation of Liability</h3>
<p>Cyclone Arnab shall not be liable for any damages arising from the use of, or inability to use, this website or its content.</p>
<h3>4. External Links</h3>
<p>This site contains links to external websites. We are not responsible for the content or privacy practices of those sites.</p>
<h3>5. Changes</h3>
<p>We may update these terms at any time. Continued use of the site constitutes acceptance of the updated terms.</p>
"""),
        "privacy.html": ("Privacy Policy", "Privacy policy for Cyclone Arnab.", """
<h2>Privacy Policy</h2>
<p>Your privacy is important to us. This policy explains what information we collect and how it is used.</p>
<h3>1. Information We Collect</h3>
<p>This is a static website. We do not directly collect, store, or sell personal information. No account registration is required to view content.</p>
<h3>2. Cookies and Third-Party Services</h3>
<p>If advertising or analytics services are enabled in the future, they may use cookies to serve relevant ads. You can disable cookies in your browser settings.</p>
<h3>3. Third-Party Links</h3>
<p>Our content links to external sources such as IMD and GDACS. Their privacy policies apply when you visit them.</p>
<h3>4. Contact</h3>
<p>For privacy-related questions, please use the Contact page.</p>
"""),
        "contact.html": ("Contact Us", "Contact Cyclone Arnab.", """
<h2>Contact Us</h2>
<p>We welcome feedback, corrections, and partnership inquiries.</p>
<h3>Email</h3>
<p>Please reach out to us at: <strong>contact@cyclonearnab.com</strong></p>
<p>(Replace this email with a working address you control, or use a free contact form service such as Formspree.)</p>
<h3>Response Time</h3>
<p>We aim to respond to all messages within 2–3 business days.</p>
"""),
    }
    for fname, (title, desc, body) in pages.items():
        html = head(f"{title} - Cyclone Arnab", desc, f"/{fname}")
        html += f'<div class="page-content">{body}</div>' + foot()
        open(fname, 'w', encoding='utf-8').write(html)

if __name__ == "__main__":
    build_index()
    build_static()
    print("All pages generated successfully.")

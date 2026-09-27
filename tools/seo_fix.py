#!/usr/bin/env python3
"""Post-process a Claude Design export of flavorsofandalucia.com for SEO / AI crawlers.

Claude Design puts <title>, meta, canonical and og/twitter tags inside <helmet> in the
<body>, and only creates the JSON-LD schema with JavaScript at runtime. Crawlers that do
not run JavaScript (most AI crawlers) therefore see no head tags and no schema.

This script, run on the site folder after every new Design download:
  1. moves the SEO tags from <helmet> into the real <head>;
  2. renders every page in headless Chrome, takes the JSON-LD the page builds,
     enriches it (TravelAgency details, TouristTrip duration/location/offer) and writes
     it as static <script type="application/ld+json"> in <head>;
  3. switches off the runtime JSON-LD so the schema is not duplicated.

Pages already processed (marker comment) are skipped, so running it twice is safe.

Usage:  python3 tools/seo_fix.py [site_dir]      (default: the repository root)
"""
import concurrent.futures
import html
import http.server
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time

MARKER = "<!-- seo-fix: static head tags + JSON-LD (tools/seo_fix.py) -->"
SITE_URL = "https://flavorsofandalucia.com/"
AGENCY_ID = SITE_URL + "#travelagency"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Business details for the TravelAgency schema (homepage). Keep in sync with the site.
AGENCY = {
    "legalName": "Come to Spain Events SLU",
    "founder": {"@type": "Person", "name": "Gunvor Guttormsen"},
    "telephone": "+34 637 87 87 68",
    "email": "hello@flavorsofandalucia.com",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Milano Govinda 35",
        "postalCode": "41020",
        "addressLocality": "Sevilla",
        "addressCountry": "ES",
    },
    "identifier": {
        "@type": "PropertyValue",
        "propertyID": "Licencia de agencia de viajes (Junta de Andalucía)",
        "value": "C.I.AN-41-7397-2",
    },
    "knowsLanguage": ["en", "no", "sv", "da"],
    "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer service",
        "telephone": "+34 637 87 87 68",
        "email": "hello@flavorsofandalucia.com",
        "availableLanguage": ["en", "no", "sv", "da"],
    },
}

# Head tags that belong in the real <head>.
HEAD_TAG_RE = re.compile(
    r"""\s*(<title>.*?</title>"""
    r"""|<meta\s+(?:name|property)="(?:description|robots|og:[^"]+|twitter:[^"]+)"[^>]*>"""
    r"""|<link\s+rel="(?:canonical|icon|apple-touch-icon)"[^>]*>)""",
    re.S,
)
LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def pages(root):
    for d, _, files in os.walk(root):
        if "/." in d or "/tools" in d:
            continue
        if "index.html" in files:
            p = os.path.join(d, "index.html")
            yield p, "/" + os.path.relpath(d, root).replace(".", "").strip("/")


def serve(root):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=root, **k)

        def log_message(self, *a):
            pass

    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Quiet)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def render(url, profile):
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as out:
        pass
    with open(out.name, "w") as fh:
        p = subprocess.Popen(
            [CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
             "--virtual-time-budget=8000", f"--user-data-dir={profile}", "--dump-dom", url],
            stdout=fh, stderr=subprocess.DEVNULL)
        for _ in range(120):  # Chrome often keeps running after dumping the DOM: stop once it is complete
            time.sleep(0.5)
            fh.flush()
            if p.poll() is not None or open(out.name).read().rstrip().endswith("</html>"):
                break
        p.kill()
    dom = open(out.name).read()
    os.unlink(out.name)
    return dom


FACT_RE = re.compile(
    r'text-transform: uppercase[^>]*><span class="sc-interp">([^<]{2,30})</span></span>\s*'
    r'<span[^>]*>(?:<span class="sc-interp">)?([^<]{1,300})<')


def facts(dom):
    """Label/value pairs from the tour info box (Duration, Where, Meeting point, Price...)."""
    out = {}
    for label, value in FACT_RE.findall(dom):
        out.setdefault(html.unescape(label).strip(), html.unescape(value).strip())
    return out


def iso_duration(s):
    if not s:
        return None
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:-|–|to)?\s*(\d+(?:[.,]\d+)?)?\s*hours?", s)
    if m:
        h = float(m.group(1).replace(",", "."))
        return f"PT{int(h)}H" + (f"{int(round((h % 1) * 60))}M" if h % 1 else "")
    if re.search(r"full day", s, re.I):
        return "PT8H"
    return None


def offer_from(price_text, url):
    """Return (Offer or None). Only uses numbers that are printed on the page."""
    if not price_text or not re.search(r"\d", price_text):
        return None
    nums = [float(n.replace(".", "").replace(",", ".")) for n in re.findall(r"(\d[\d.,]*)\s*€", price_text)]
    if not nums:
        return None
    offer = {"@type": "Offer", "priceCurrency": "EUR", "url": url,
             "availability": "https://schema.org/InStock", "description": price_text}
    per_person = re.findall(r"(\d[\d.,]*)\s*€\s*(?:per|a|/)\s*(?:person|pax|guest)", price_text)
    if len(nums) == 1 or (per_person and len(nums) == 1):
        offer["price"] = f"{nums[0]:.2f}"
    else:
        # Several numbers (e.g. guide fee + per person): state the lowest printed figure as a "from" price.
        offer["priceSpecification"] = {"@type": "PriceSpecification", "priceCurrency": "EUR",
                                       "minPrice": f"{min(nums):.2f}"}
    return offer


def enrich(ld, path, fx):
    t = ld.get("@type")
    if t == "TravelAgency" and path == "/":
        ld["@id"] = AGENCY_ID
        ld.update(AGENCY)
        if "Andalucía" not in ld.get("areaServed", []):
            ld.setdefault("areaServed", []).insert(0, "Andalucía")
        for o in ld.get("makesOffer", []):
            item = o.get("itemOffered", {})
            if item.get("url") and not item["url"].startswith("http"):
                item["url"] = SITE_URL + item["url"].lstrip("./")
    if t == "TouristTrip":
        url = ld.get("url") or SITE_URL + path.strip("/") + "/"
        ld["provider"] = {"@type": "TravelAgency", "@id": AGENCY_ID, "name": "Flavors of Andalucía",
                          "url": SITE_URL, "telephone": AGENCY["telephone"]}
        dur = iso_duration(fx.get("Duration"))
        if dur and "duration" not in ld:
            ld["duration"] = dur
        where = fx.get("Where") or fx.get("Meeting point")
        if "location" not in ld:
            ld["location"] = {"@type": "Place", "name": where or "Seville",
                              "address": {"@type": "PostalAddress", "addressRegion": "Andalucía",
                                          "addressCountry": "ES"}}
        off = offer_from(fx.get("Price"), url)
        if off and "offers" not in ld:
            ld["offers"] = off
    return ld


def process(root, only_report=False):
    httpd = serve(root)
    base = f"http://127.0.0.1:{httpd.server_address[1]}"
    report = {"processed": [], "skipped": [], "tours_without_price": [], "warnings": []}
    todo = []
    for fpath, path in sorted(pages(root)):
        if MARKER in open(fpath, encoding="utf-8").read():
            report["skipped"].append(path)
        else:
            todo.append((fpath, path))
    # render in parallel (each Chrome gets its own profile)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        doms = list(ex.map(lambda t: render(base + (t[1].rstrip("/") + "/" if t[1] != "/" else "/"),
                                            tempfile.mkdtemp(prefix="seo-chrome-")), todo))
    for (fpath, path), dom in zip(todo, doms):
        src = open(fpath, encoding="utf-8").read()
        if len(dom) < 1000:
            report["warnings"].append(f"{path}: could not render")
            continue
        fx = facts(dom)
        lds = []
        for raw in LD_RE.findall(dom):
            try:
                lds.append(enrich(json.loads(raw), path, fx))
            except json.JSONDecodeError:
                report["warnings"].append(f"{path}: invalid JSON-LD from runtime")
        for l in lds:
            off = l.get("offers") if isinstance(l.get("offers"), dict) else None
            if off and off.get("price") is not None:
                m = re.search(r"[Ff]rom (\d[\d.,]*) €", off.get("description", ""))
                if m and float(m.group(1).replace(",", ".")) != float(off["price"]):
                    report["warnings"].append(
                        f"{path}: offer price {off['price']} € but description says 'From {m.group(1)} €' (fix in Claude Design)")
        if path.startswith("/tour/") and not any(l.get("@type") == "TouristTrip" and l.get("offers") for l in lds):
            report["tours_without_price"].append(f"{path}  (Price: {fx.get('Price') or '—'})")

        # 1. move SEO head tags out of <helmet>
        hs, he = src.find("<helmet"), src.find("</helmet>")
        if hs < 0 or he < 0:
            report["warnings"].append(f"{path}: no <helmet> found")
            continue
        helmet = src[hs:he]
        head_tags = [m.group(1) for m in HEAD_TAG_RE.finditer(helmet)]
        helmet = HEAD_TAG_RE.sub("", helmet)
        body = src[:hs] + helmet + src[he:]
        # 2. switch off runtime JSON-LD (everything after </head> is page/runtime code)
        cut = body.find("</head>")
        body = body[:cut] + body[cut:].replace('"application/ld+json"', '"application/x-ld-json-static-in-head"')
        # 3. static tags + JSON-LD into <head>
        ld_html = "".join(
            '\n<script type="application/ld+json">' + json.dumps(l, ensure_ascii=False).replace("</", "<\\/") + "</script>"
            for l in lds)
        insert = "\n" + MARKER + "\n" + "\n".join(head_tags) + ld_html + "\n"
        vp = body.find(">", body.find('<meta name="viewport"')) + 1
        body = body[:vp] + insert + body[vp:]
        if not only_report:
            open(fpath, "w", encoding="utf-8").write(body)
        report["processed"].append(f"{path}  ({len(head_tags)} head tags, {len(lds)} JSON-LD)")
    httpd.shutdown()
    return report


if __name__ == "__main__":
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), ".."))
    r = process(root, only_report="--dry-run" in sys.argv)
    for k, v in r.items():
        print(f"\n== {k} ({len(v)})")
        for line in v:
            print("  " + line)

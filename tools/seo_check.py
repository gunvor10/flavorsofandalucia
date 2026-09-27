#!/usr/bin/env python3
"""SEO guard for flavorsofandalucia.com — fails (exit 1) if a page breaks SEO-RULES.md.

Checks every index.html (static HTML, what crawlers without JavaScript see):
  - <title> and meta description are inside the real <head>
  - the head tags and JSON-LD come from tools/seo_fix.py (marker present)
  - all JSON-LD in <head> is valid JSON
  - homepage has TravelAgency schema; every /tour/ page has TouristTrip schema
  - no {{ ... }} template placeholder leaked into <head> (titles, meta, schema)
  - sitemap.xml exists and lists every page
Runs locally before each push and in GitHub Actions on every push.

Usage:  python3 tools/seo_check.py [site_dir]
"""
import json
import os
import re
import sys

root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), ".."))
errors = []

sitemap_path = os.path.join(root, "sitemap.xml")
sitemap = open(sitemap_path).read() if os.path.exists(sitemap_path) else None
if sitemap is None:
    errors.append("sitemap.xml is missing")

count = 0
for d, dirs, files in os.walk(root):
    dirs[:] = [x for x in dirs if not x.startswith(".") and x not in ("tools", "uploads")]
    if "index.html" not in files:
        continue
    count += 1
    rel = "/" + os.path.relpath(d, root).strip(".").strip("/")
    rel = rel if rel == "/" else rel + "/"
    src = open(os.path.join(d, "index.html"), encoding="utf-8").read()
    head = src[: src.find("</head>")] if "</head>" in src else ""
    if "seo-fix: static head tags" not in head:
        errors.append(f"{rel}: not processed by tools/seo_fix.py")
    if not re.search(r"<title>[^<{]+</title>", head):
        errors.append(f"{rel}: <title> missing from <head>")
    if not re.search(r'<meta name="description" content="[^"{]+"', head):
        errors.append(f"{rel}: meta description missing from <head>")
    if "{{" in head:
        errors.append(f"{rel}: {{{{ ... }}}} placeholder inside <head>")
    types = set()
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', head, re.S):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            errors.append(f"{rel}: invalid JSON-LD ({e})")
            continue
        types.add(data.get("@type"))
    if rel == "/" and "TravelAgency" not in types:
        errors.append("/: TravelAgency schema missing on homepage")
    if rel.startswith("/tour/") and "TouristTrip" not in types:
        errors.append(f"{rel}: TouristTrip schema missing")
    if sitemap is not None and f"https://flavorsofandalucia.com{rel}</loc>" not in sitemap:
        errors.append(f"{rel}: not in sitemap.xml")

if errors:
    print(f"SEO check FAILED ({len(errors)} problems in {count} pages):")
    for e in errors:
        print("  - " + e)
    sys.exit(1)
print(f"SEO check passed: {count} pages OK.")

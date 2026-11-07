#!/usr/bin/env python3
"""Google Ads conversion tracking: one conversion per successfully sent enquiry form.

Run on the site folder after every new Claude Design download, AFTER
tools/analytics_consent.py (it builds on its Google tag and cookie banner):
  1. Head: adds gtag('config', 'AW-…') next to the Google Analytics config.
  2. Forms: every enquiry/contact form fires the Ads conversion when the form
     endpoint answers OK (the "Thank you — … will reply within 24 hours" moment).
     There is no thank-you page, so a page-view conversion would count every visit.
  3. Cookie banner: asks for statistics + ad-measurement cookies. "Accept" now grants
     analytics_storage, ad_storage and ad_user_data (not ad_personalization: no
     remarketing). Visitors who accepted the old statistics-only banner ('yes') are
     asked again; new accept is stored as 'all'.

Safe to run twice (every step checks whether it was already done).

Usage:  python3 tools/google_ads.py [site_dir]
"""
import glob
import os
import sys

ADS_ID = "AW-18561575179"
CONVERSION = "AW-18561575179/8K0OCNfA7rMdEIvS7JJF"

GA_CFG = "gtag('config','G-JNQWKVPPLZ');"
ADS_CFG = "gtag('config','" + ADS_ID + "');"

FORM_OK = "if (r.ok) { form.reset();"
FORM_OK_ADS = ("if (r.ok) { if (window.gtag) gtag('event','conversion',{send_to:'" + CONVERSION +
               "',value:1.0,currency:'EUR'}); form.reset();")

# (old, new) replacements in the consent code written by analytics_consent.py
CONSENT = [
    ("analytics_storage:c==='yes'?'granted':'denied'});",
     "analytics_storage:(c==='yes'||c==='all')?'granted':'denied'});"
     "if(c==='all')gtag('consent','update',{ad_storage:'granted',ad_user_data:'granted'});"),
    ("We use Google Analytics cookies to see how visitors use our website. Do you accept statistics cookies?",
     "We use Google cookies to see how visitors use our website and to measure our Google Ads. "
     "Do you accept statistics and ad-measurement cookies?"),
    ('data-v="yes"', 'data-v="all"'),
    ("if(!v)b.hidden=false;", "if(!v||v==='yes')b.hidden=false;"),
    ("if(x==='yes')gtag('consent','update',{analytics_storage:'granted'});",
     "if(x==='all')gtag('consent','update',{analytics_storage:'granted',ad_storage:'granted',ad_user_data:'granted'});"),
    ("gtag('consent','update',{analytics_storage:'denied'});",
     "gtag('consent','update',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied'});"),
    ("n.indexOf('_gat')===0)", "n.indexOf('_gat')===0||n.indexOf('_gcl')===0)"),
]


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..")
    pages = sorted(glob.glob(os.path.join(root, "**", "*.html"), recursive=True))
    changed = forms = 0
    for path in pages:
        text = open(path, encoding="utf-8").read()
        new = text
        if GA_CFG not in new:
            print("WARNING: no Google tag (run analytics_consent.py first):", os.path.relpath(path, root))
            continue
        if ADS_CFG not in new:
            new = new.replace(GA_CFG, GA_CFG + ADS_CFG, 1)
        if CONVERSION not in new:
            new = new.replace(FORM_OK, FORM_OK_ADS)
        if "if (r.ok)" in new and CONVERSION not in new:
            print("WARNING: form found but success code not recognised:", os.path.relpath(path, root))
        forms += CONVERSION in new
        for old, rep in CONSENT:
            if rep not in new:
                new = new.replace(old, rep)
        if new != text:
            open(path, "w", encoding="utf-8").write(new)
            changed += 1
    print(f"{changed} of {len(pages)} pages updated; {forms} pages with a form send the Ads conversion")


if __name__ == "__main__":
    main()

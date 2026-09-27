# SEO rules — flavorsofandalucia.com

The site is designed in **Claude Design** and exported as a zip. Every new export replaces
all pages, so the rules below are enforced by two scripts in `tools/` that run on every update.

## How an update is published
1. Download the new version from Claude Design (zip lands in `~/Downloads`).
2. Copy the zip's `site/` contents over this folder (do **not** delete `tools/`, `.github/`, `SEO-RULES.md`).
3. `python3 tools/seo_fix.py` — moves head tags into `<head>`, writes static JSON-LD, switches off the runtime copy.
4. `python3 tools/seo_check.py` — must say "passed" before pushing.
5. Commit and push → Plesk deploys automatically (GitHub webhook). The same check also runs on GitHub on every push.

## Rules
- **Head tags must be in the real `<head>`, never in the body.** `<title>`, meta description, canonical, robots and all og/twitter tags. (Design puts them in `<helmet>` inside the body; `seo_fix.py` moves them.)
- **Never remove JSON-LD schema; keep it in sync** with tour names, prices and durations. Homepage: `TravelAgency` (+ `WebSite`, `FAQPage`). Every tour page: `TouristTrip` with duration, location, provider and an `Offer` when the page shows a price. Schema is static in `<head>` so crawlers that do not run JavaScript (most AI crawlers) can read it. Business details live in `AGENCY` at the top of `tools/seo_fix.py`.
- **No visible `{{ ... }}` placeholders.** The `{{ ... }}` in the page code are Claude Design's live bindings (menu, slider, form messages) — they are filled in by `support.js` and must *not* be removed. What must never happen is a placeholder in the head tags or schema, or one showing on the rendered page.
- **Keep all existing URLs; add new pages to `sitemap.xml`.**
- **Important text must be real HTML text**, not text inside images.
- **All images need alt text.**
- **Brand focus:** Flavors of Andalucía is about food and wine. Groups/MICE link to DMC Seville Event (https://dmcsevilleevent.com), weddings to Sevilla Event (https://sevillaevent.com).

## Change log
### 2026-09-27
- Content (done in Claude Design, export "design-5"): new homepage H1 "Private Food Tours & Tailor-Made Food Experiences in Seville"; testimonials intro now says we work with travel advisors and agencies on net rates; Wedding Planner / Destination Management blocks replaced by one line linking to DMC Seville Event and Sevilla Event; "Book your experience" rewritten; footer © 2026 on all pages.
- Technical: added `tools/seo_fix.py` (static head tags + JSON-LD on all pages; TravelAgency with legal name, licence C.I.AN-41-7397-2, address, founder, languages en/no/sv/da; TouristTrip duration, location, provider and offers), `tools/seo_check.py`, GitHub Action `SEO check`, this file.

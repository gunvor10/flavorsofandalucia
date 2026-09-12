# Flavors of Andalucia — rebuild handoff

## Where we are (read this first)

**25 pages built.** 11 site pages + 14 tour pages, all cross-linked: every nav dropdown,
tour card and "related tours" row points at local files, so nothing bounces to the old
WordPress site. Canonical and og:url tags still carry the real live URLs.

Open items, in order of urgency:

1. **Photos are hotlinked, not copied.** The yacht, paella, flamenco, Jerez/Cádiz,
   olive-oil, Santa Cruz and carriage pages load images from `sevillapanorsk.com/uploads/`.
   Move them into the project before launch.
2. **Three prices unconfirmed** — Jerez/Cádiz, horse carriage, and Private Tapas Tour all
   say "on request". Paella and flamenco are affiliate, so they legitimately have none.
3. **Private Tapas Tour** also needs meeting point, duration (assumed 4 h, evenings) and
   number of bars (assumed 4–5) confirmed.
4. **Horse carriage** duration (3 h) and carriage capacity (4 per carriage) are assumptions.
5. Galleries on the Santa Cruz sightseeing, carriage and flamenco pages have only 2–3
   photos each and look thin. More photos would help.
6. ~~Tour card language strings~~ — **done.** Every listing card (Homepage, Food
   Experiences, Foodie Day Tours, Tailor Made, Travel Agencies) now carries a per-tour
   meta line derived from that tour page's own fact strip: duration · type · languages
   (or price where it is the more useful third item). Foodie Day Tours and Tailor Made
   had one hardcoded string for every card; both now read `{{ t.meta }}` per item.
   Also fixed: Aracena price on the homepage (182 € → 201 €), the wrong thumbnail on
   the Travel Agencies wine-tasting card, two related-tour durations, and two related
   links that still pointed at the live site.

Rebuilding flavorsofandalucia.com (WordPress + Elementor) as hand-built pages, to be
hosted on Git. Content and structure follow the live site; visual treatment is more
premium. All copy is taken **verbatim** from the live pages unless noted.

## Design system

- Type: **Prata** (headings + hero eyebrow) + **Heebo** (body, 400/500/600) — both from the logo.
  Prata has only one weight and **no italic**, so the former italic pull quotes and hero
  taglines are now Prata regular. Tracking is deliberately open: `.008em` on display
  headings, `.012em` on body, body line-height 1.75, body weight 400 (not 300).
  Previously Bodoni Moda + Public Sans; Rufina was tried and rejected.
- Grounds: cream `#FAF8F4`, warm cream `#F1EBE0`, cobalt `#0E2440`, footer `#0A1A2E`.
- Accents: gold `#BC8B2E`, bronze `#9A6F1E` (gold on cream — contrast), turquoise `#1AC5B6`
  (on dark), deep turquoise `#0C7A71` / `#0A6058` (turquoise on cream — contrast).
  All four drawn from the mosaic tile logo.
- Section headings alternate turquoise / bronze down each page for rhythm.
- Eyebrow labels: 14–15px, uppercase, `.24em` tracking.
- No icons — tried, removed; they read as SaaS, not luxury.
- Photos: rounded 6–8px, `loading="lazy"` + `decoding="async"` below the fold,
  `fetchpriority="high"` on heroes.

## Pages built (17)

| File | Live URL |
|---|---|
| Homepage.dc.html | / |
| Food Experiences.dc.html | /best-private-tours-seville/ |
| Foodie Day Tours.dc.html | /food-destinations/ |
| Tailor Made.dc.html | /luxury-experiences-seville/ |
| Bespoke Tours.dc.html | /bespoke-private-tours-spain/ |
| Spanish Traditions.dc.html | /spanish-tradition-experiences/ |
| Food Wine Experiences.dc.html | /food-wine-experiences-in-andalucia/ |
| Make Your Choice.dc.html | /tailor-made-holiday-spain/ |
| Travel Agencies.dc.html | /travel-agencies-and-group-travel-seville/ |
| Inspiration Blog.dc.html | /gastronomy-art-blog-sevilla/ |
| Blog Post.dc.html | /2024/01/16/6-great-food-shops-in-seville/ |
| Tour Template.dc.html | /tour/… (one layout for all 17 tours) |
| About Us.dc.html | /about-us/ |
| Travel Guarantee.dc.html | /travel-guarantee-flavors-of-andalucia/ |
| Contact.dc.html | /contact/ |
| Tour Aracena Iberian Ham.dc.html | /tour/private-aracena-iberian-ham-tour/ |
| Tour Wine Tasting Dinner.dc.html | /tour/spanish-wine-tasting-with-dinner-seville/ |

**Not built:** 6 tour pages (see "Tours" below).

## URL map for deployment (must not change)

Every indexed URL must stay byte-identical, trailing slash included. On Git hosting,
serve each file as `index.html` inside a folder named after the live path:

| File | Deploy as | Live URL |
|---|---|---|
| Homepage.dc.html | `/index.html` | / |
| Food Experiences.dc.html | `/best-private-tours-seville/index.html` | /best-private-tours-seville/ |
| Foodie Day Tours.dc.html | `/food-destinations/index.html` | /food-destinations/ |
| Tailor Made.dc.html | `/luxury-experiences-seville/index.html` | /luxury-experiences-seville/ |
| Bespoke Tours.dc.html | `/bespoke-private-tours-spain/index.html` | /bespoke-private-tours-spain/ |
| Spanish Traditions.dc.html | `/spanish-tradition-experiences/index.html` | /spanish-tradition-experiences/ |
| Food Wine Experiences.dc.html | `/food-wine-experiences-in-andalucia/index.html` | /food-wine-experiences-in-andalucia/ |
| Make Your Choice.dc.html | `/tailor-made-holiday-spain/index.html` | /tailor-made-holiday-spain/ |
| Travel Agencies.dc.html | `/travel-agencies-and-group-travel-seville/index.html` | /travel-agencies-and-group-travel-seville/ |
| Inspiration Blog.dc.html | `/gastronomy-art-blog-sevilla/index.html` | /gastronomy-art-blog-sevilla/ |
| Blog Post.dc.html | `/2024/01/16/6-great-food-shops-in-seville/index.html` | same |
| About Us.dc.html | `/about-us/index.html` | /about-us/ |
| Travel Guarantee.dc.html | `/travel-guarantee-flavors-of-andalucia/index.html` | /travel-guarantee-flavors-of-andalucia/ |
| Contact.dc.html | `/contact/index.html` | /contact/ |
| Tour Template.dc.html | `/tour/tasting-market-tapas-lunch-tour/index.html` | /tour/tasting-market-tapas-lunch-tour/ |
| Tour Aracena Iberian Ham.dc.html | `/tour/private-aracena-iberian-ham-tour/index.html` | same |
| Tour Wine Tasting Dinner.dc.html | `/tour/spanish-wine-tasting-with-dinner-seville/index.html` | same |

Each page's `<link rel="canonical">` and `og:url` already point at these live URLs.
Internal links currently point at the local `.dc.html` files and must be rewritten to
the paths above at deploy time. No 301s are needed if the paths are kept.

Page text and keywords do **not** have to match the originals word for word; what
must not change is the URL, and the main keyword in each `<title>` and `<h1>`
(e.g. "private tours Seville", "travel guarantee", "food wine experiences Andalucia").

## Conventions

- Shared header + footer are duplicated in each page (menu with hover dropdowns on
  desktop, burger below ~1100px). Menu links point at local `.dc.html` files.
- Every page carries: title tag, meta description, `<link rel="canonical">` and
  `og:url` pointing at the **live flavorsofandalucia.com URL** (never the local file),
  OG + Twitter tags, and JSON-LD (`TravelAgency`, `Service`, `ItemList`, `Tour`,
  `BlogPosting`, `FAQPage` as appropriate).
- GA4 measurement ID to add on launch: **G-JNQWKVPPLZ**.
- Tailor Made sub-pages share one layout: per section, a 3:4 vertical photo with text
  beside it and three 4:3 photos below, zigzagging left/right, with an italic pull
  quote between sections 2 and 3.
## Tours

`Tour Template.dc.html` **is** the Tasting/Market/tapas lunch tour and the master
layout. Build each new tour by copying it and swapping content — the script pattern
used for the last two is: replace head meta, hero (image/eyebrow/h1/tagline/WhatsApp
text), lede + body paragraphs, h2, the 2-image row, the 7 mosaic `<img>` sources
(keep each one's `grid-` span style), meeting point, enquiry + CTA copy, then the
whole data block (`facts`, `assurances`, `included`, `reviews`, `faqs`,
`itinerary`, `related`, JSON-LD).

Also parameterise per tour (currently hand-fixed after generating): the gallery
heading ("The day in pictures"), the related heading, and the itinerary eyebrow +
heading ("Hour by hour" / "How the day unfolds"). Defaults in the template are
morning/Seville-specific and read wrong on day trips and evening experiences.

### Tour page anatomy

**Gallery lightbox.** The mosaic grid carries `data-gallery="1"`; the logic class binds a
click on every `<img>` inside it and shows a fixed overlay (`lbVals()` in the logic,
markup at the end of the template) with prev/next, click-anywhere and Esc to close,
arrow keys to step. Copy all four pieces when generating a new tour: the `data-gallery`
attribute, the overlay markup, `lbAt: null` in `state`, and `...this.lbVals()` in
`renderVals`.

Hero (eyebrow, h1, tagline, two CTAs, "no prepayment" line) → fact strip → four
assurance ticks → guide block → description with read-more → 2-image row → vertical
itinerary timeline (gold dots) → what's included → mosaic gallery (4×3 rectangle,
max-width 820px, one 2×2 + one 2-tall + five small) → reviews as side-by-side cards →
meeting point with Open in maps → FAQ → compact enquiry form (max 420px) → related
tours → closing CTA. Sticky booking card in the right column; floating WhatsApp button
(+34 637878768).

**Guide variants.** A `guidedBy` prop (`"gunvor"` | `"partner"`) switches the guide
block between "guided by me, Gunvor" and "one of our trusted partner guides — licensed,
local and chosen by me personally". Set per tour; Gunvor will say which.

**All tours are private.** Never write "small group" — the fact strip says
"Private, your party only".

### Built

| Tour | File | Guide | Price |
|---|---|---|---|
| Tasting, Market, tapas lunch | Tour Template.dc.html | Gunvor | depends on group size |
| Private Aracena Iberian ham | Tour Aracena Iberian Ham.dc.html | Gunvor | from 201 €/pp |
| Spanish wine tasting with dinner | Tour Wine Tasting Dinner.dc.html | partner | 87 €/pp |
| Seville sightseeing, ham, cheese, wine | Tour Sightseeing Ham Cheese Wine.dc.html | Gunvor | from 138 €/pp (min 2) |
| Private Tapas Tour | Tour Private Tapas.dc.html | Gunvor | **NOT CONFIRMED** |

Deploy paths for the two new ones: `/tour/seville-sightseeing-ham-cheese-wine-tasting/`
and `/tour/best-tapas-tour/`.

**Sightseeing/ham/cheese/wine** was translated from sevillapanorsk `tur-historie-tapas.html`
(2 h on foot, hotel pick-up, old town + Santa Cruz, NO/SE/DK/EN, from 138 €/pp min 2,
2026 prices, +49 €/pp turns it into a full tapas lunch or evening with 8 tastings and
4 drinks, monument tickets not included, VISA/Mastercard). Its photos come from
sevillapanorsk (`santa-cruz-plass-sevilla.jpg`, `tapas-lunsj-sevilla.jpg`,
`gater-i-santa-cruz-sevilla.jpg`) — **move these into the project before launch**.

**Private Tapas Tour** has no sevillapanorsk source, so its copy was written from scratch.
Still to confirm with Gunvor: **price** (currently "depends on group size"), **meeting
point** (currently "central Seville, exact point on confirmation"), duration (assumed 4 h,
evenings) and the number of bars (assumed four to five).

### Still to build (0) — all tour pages now exist

Text and photos come from **sevillapanorsk.com** (English version) — Gunvor's other
site. Rewrite, don't copy: sevillapanorsk is personal and first-person; Flavors is
close to it but more service-minded, luxury-leaning, and always mentions that things
can be tailor-made. Gunvor must paste the page URLs in chat — the fetch tools cannot
reach a domain that has not appeared in the conversation.

Source URLs she supplied (all fetchable, English versions):

| Tour | sevillapanorsk source |
|---|---|
| Sherry Bodega & Cádiz | `/en/bloggposter/day-trip-jerez-cadiz.html` |
| Private Paella Cooking Lesson | `/en/bloggposter/paella-cooking-class-seville.html` |
| Luxury dinner in Yacht Seville | `/en/tour-yacht-dinner-seville.html` |
| (already built) Aracena ham | `/en/tour-aracena-iberian-ham.html` |
| (already built) Wine tasting dinner | `/en/tour-wine-tasting-dinner-seville.html` |
| (already built) Sightseeing/ham/cheese/wine | `/en/tour-history-and-tapas-seville.html` |
| **Olive oil estate — no Flavors page yet** | `/en/tour-olive-oil-estate-seville.html` |

All built this round:

| Page | File | Deploy slug | Price |
|---|---|---|---|
| Olive oil estate visit | Tour Olive Oil Estate.dc.html | /tour/olive-oil-estate-visit-seville/ | from 55 €/pp |
| Sherry Bodega & Cádiz | Tour Sherry Bodega Cadiz.dc.html | /tour/private-day-trip-to-jerez-and-cadiz-from-seville/ | **on request — confirm** |
| Luxury dinner aboard a yacht | Tour Yacht Dinner.dc.html | /tour/luxury-dinner-in-yacht-seville-2/ | from 120 €/pp sharing |
| Private paella cooking lesson | Tour Paella Cooking Lesson.dc.html | /tour/private-paella-cooking-lesson/ | partner booking page (AFFILIATE) |
| Horse carriage & tapas in Santa Cruz | Tour Horse Carriage Tapas Santa Cruz.dc.html | /tour/horse-carriage-and-tapas-in-santa-cruz/ | **on request — confirm** |
| Tapas & flamenco evening | Tour Tapas Flamenco.dc.html | /tour/tapas-flamenco-performance/ | partner booking page |

**Paella class** is also an AFFILIATE activity, not Gunvor's own. Affiliate link:
`partners.cookingpaella.com/r/flavorsofandalucia`. All three CTA clusters lead with it
("See dates & prices", "same price as booking direct"); the secondary CTA asks for the
whole terrace privately. Trust row changed to partner-run / 10 people / ingredients
included — it no longer claims "private, never shared".

**Tapas & flamenco** is an AFFILIATE activity, not Gunvor's own tour. Source:
sevillapanorsk `/en/bloggposter/tapas-and-flamenco-seville.html`; run in English by
Devour Tours. The primary CTAs point at the affiliate link
(`devourtours.com/tours/seville-tapas-flamenco-tour/?tap_a=29774-b9abbb&tap_s=8255545-ec6e63`)
with "same price as booking direct"; the secondary CTA asks for a private version with
Gunvor guiding. The trust row on this page was changed accordingly (partner-run, small
group, ticket included) — it does not claim "private, never shared". Added to the Food
Experiences nav dropdown, which it was previously missing from.

**Horse carriage:** Gunvor asked for the two old Flavors carriage tours (`horse-carriage-and-santa-cruz-tour`
and `private-horse-carriage-and-tapas-tour`) to be replaced by ONE page, "Horse carriage
and tapas in Santa Cruz". Both old URLs now redirect to the new file across the site, the
nav label is updated, and the duplicate card was removed from Tailor Made. It has no
sevillapanorsk source — copy written from scratch; duration (3 h) and party size (4 per
carriage) are assumptions to confirm.

**Photos:** the yacht, paella, Jerez/Cádiz, olive-oil and Santa Cruz pages all hotlink
sevillapanorsk images. Move them into the project before launch. Carriage page uses two
Flavors images and two sevillapanorsk Santa Cruz shots — it has no photo of the carriage
in Santa Cruz itself, which is the one image it really wants.

**Olive oil estate** exists on sevillapanorsk but has no Flavors URL. Ask Gunvor whether
she wants it added to Flavors, and under which slug.

Excluded on Gunvor's instruction: **Luxury Villa Dinner**. Tapas Tour and Horse
Carriage have no sevillapanorsk page — build from the Flavors text.

Ask per tour: which guide, meeting point, price, and any photos to add.
- Contact: `hello@flavorsofandalucia.com` · +34 637 87 87 68 · Milano Govinda 35, 41020 Sevilla.

### Languages (Gunvor's own wording)

Gunvor is a licensed guide and guides in **English and Norwegian**, and can also guide
**Swedish and Danish**. Partner guides cover **French, German, Italian, Portuguese,
Spanish and Polish**. About Us states this and its `knowsLanguage` JSON-LD lists only en/no/sv/da
(the partner languages belong to the partners, not to her). The tour cards still carry
older language strings ("EN / NO", "EN / FR / DE") — audit those against this.
Audited and corrected; the Travel Agencies stat block now reads NO · EN · SE · DK.
Still unverified: the paella class (EN / ES) and flamenco (EN) language claims, which
come from the partner pages, and the wine tasting, whose sommelier's languages are
unknown (card currently says "2 hours · Sommelier-hosted · Up to 14").

## Recent additions

- **Travel advisor language** (US market): Travel Agencies has a "For travel advisors"
  section (net rates, written programmes, FAM visits, one contact on the ground).
  **Rates are net and NOT commissionable** — the advisor adds their own margin. Never
  write "commissionable" anywhere. **Verify FAM visits is true before launch.** Homepage
  and Contact carry a line pointing advisors there.
- **Contact page** has the licence numbers, Gunvor's portrait and the enquiry form.
- **Nav** is a top horizontal menu with hover dropdowns, **always visible** — no burger
  at any width (Gunvor's call). It wraps to a second row and scales its type down
  (`clamp(9.5px,.78vw,11px)`) on narrow screens. The burger markup is still in each page
  but permanently `display:none`; delete it if it's never wanted back.

## Open items

1. **Photos.** Many images are Elementor thumbnail crops (`-394x394`, `-605x605`,
   `elementor/thumbs/…`) and look soft. Needed as full-size originals: the 9 on Tailor
   Made and 4 day-trip shots. The Gunvor portrait now uses the full-size
   `2025/01/Gunvor-web.jpg` (1200×1600) on About Us; a newer portrait would still help. Pasting `wp-content/uploads/YYYY/MM/…` URLs in chat
   works as well as uploading.
2. **Blog post list** — Inspiration Blog shows 3 real posts; the rest need URLs.
3. **Contact form** is front-end only — no submit endpoint yet. Needs a form handler
   (Formspree/Netlify Forms/PHP) before launch, plus the newsletter signup.
4. **FAQ blocks** exist on About Us, Travel Guarantee, Contact, Travel Agencies and the
   three tour pages (visible text + `FAQPage` JSON-LD — this is what AI search reads).
   Still to add: Homepage, Tailor Made, Foodie Day Tours, the blog.
5. **Titles/descriptions on the other 11 pages** have not been audited against the live
   originals. Text may differ; the main keyword in each `<title>` and `<h1>` must not.
6. **Migration.** Keep every indexed URL byte-identical, trailing slash included; 301
   anything that changes. Static hosting means no WP editor — decide whether the blog
   stays on WordPress.
7. Yoast sitemap was erroring (output before the XML declaration) — unresolved, worth
   fixing whatever happens, since Google can't read it.

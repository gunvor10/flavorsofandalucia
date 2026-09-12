# Flavors of Andalucia — static site

Deploy the contents of this folder as the web root. Every page is an `index.html`
inside a folder named after its live URL, so all indexed URLs stay byte-identical.

- `support.js` must stay at the web root.
- `/uploads/` holds the local images.
- `.nojekyll` is there so GitHub Pages serves folders starting with underscores.
- `sitemap.xml` and `robots.txt` are at the root.

36 pages: 13 site pages, 12 tour pages, 11 blog posts.

## Publishing on GitHub Pages

1. Create a repo and push this folder's **contents** at the top level (not the
   `site/` folder itself).
2. Settings → Pages → Source: "Deploy from a branch", branch `main`, folder `/ (root)`.
3. Add the custom domain in Settings → Pages, and point the DNS A records at
   GitHub's Pages IPs. GitHub then writes a `CNAME` file into the repo.

Netlify or Cloudflare Pages work the same way: drag the folder in, no build command.

## Done

- Contact, tour-enquiry and newsletter forms post to Formspree
  (`https://formspree.io/f/xjyvdbbe`) by fetch, with a hidden
  `site=flavorsofandalucia.com` field and a `_gotcha` honeypot.
- GA4 `G-JNQWKVPPLZ` is on all 36 pages.

## Before pointing DNS at this

- **290 images still load from flavorsofandalucia.com/wp-content and
  sevillapanorsk.com.** They break if WordPress goes down. Heaviest: Bespoke Tours (23),
  Tailor Made (21), Spanish Traditions (20), Make Your Choice (19), Homepage (17),
  and the flamenco / Semana Santa / 10-things / restaurants / white-villages blog posts
  (13–16 each). The tour pages are nearly clean (1–3 each).
- Three prices say "on request": Jerez/Cádiz, horse carriage, Private Tapas Tour.
- Titles and meta descriptions on 11 pages have not been audited against the originals.
- Add `flavorsofandalucia.com` to the Formspree form's allowed domains, and mark the
  test submissions as "not spam".

# Flavors of Andalucia

Website for **flavorsofandalucia.com**.

## Folder layout

| Path | What it holds |
|------|---------------|
| `index.html` | Front page |
| `en/` | English pages |
| `bloggposter/` | Blog posts (create as needed) |
| `bilder/` | Images used across the site |
| `uploads/` | Photos exported from Claude / Claude Design |
| `css/style.css` | Site styles |
| `CNAME` | Custom domain for GitHub Pages (`flavorsofandalucia.com`) |
| `.nojekyll` | Tells GitHub Pages to serve files as-is |
| `publiser.sh` | One-click publish: takes the newest Claude zip from Downloads and pushes it live |

## Publishing

1. In Claude / Claude Design, export the site and let it download as a `.zip` into `~/Downloads`.
2. Double-click `publiser.sh` (or run `bash ~/Desktop/flavors-of-andalucia/publiser.sh`).
3. Wait a couple of minutes; the live site updates.

`publiser.sh` will not do anything if it cannot find a matching zip or if the files do not look like this site.

## First-time GitHub setup (once)

```bash
cd ~/Desktop/flavors-of-andalucia
git add -A
git commit -m "First version"
# create an empty repo named flavors-of-andalucia on github.com/gunvor10 first, then:
git remote add origin https://github.com/gunvor10/flavors-of-andalucia.git
git push -u origin main
```

Then in the repo's **Settings → Pages**, set the source to `main` / root. The `CNAME`
file already points the site at `flavorsofandalucia.com` — point that domain's DNS at
GitHub Pages to finish.

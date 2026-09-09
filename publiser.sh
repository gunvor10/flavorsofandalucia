#!/bin/bash
# Publiser Flavors of Andalucia
# Bruk: dobbeltklikk, eller skriv  bash ~/Desktop/flavors-of-andalucia/publiser.sh  i terminalen
#
# Skriptet finner den nyeste zip-filen fra Claude i Nedlastinger,
# pakker den ut, kopierer filene inn i repoet og laster opp til GitHub.
# Det stopper av seg selv hvis noe ser feil ut.

set -e

REPO="$HOME/Desktop/flavors-of-andalucia"
TMP="$HOME/Downloads/.publiser-flavors-tmp"

echo "──────────────────────────────────────────"
echo "  Publiserer Flavors of Andalucia"
echo "──────────────────────────────────────────"

# 1. Finn repoet
if [ ! -d "$REPO/.git" ]; then
  echo "STOPP: fant ikke $REPO"
  exit 1
fi

# 2. Finn nyeste zip fra Claude
ZIP=$(ls -t "$HOME/Downloads/"*.zip 2>/dev/null | head -1)
if [ -z "$ZIP" ]; then
  echo "STOPP: fant ingen zip-fil i Nedlastinger."
  echo "Last ned mappa fra Claude først."
  exit 1
fi
echo "Bruker: $(basename "$ZIP")"

# 3. Pakk ut
rm -rf "$TMP"
mkdir -p "$TMP"
unzip -q -o "$ZIP" -d "$TMP"

# 4. Finn mappa med index.html
SRC=$(find "$TMP" -maxdepth 2 -name index.html | head -1 | xargs dirname 2>/dev/null || true)
if [ -z "$SRC" ] || [ ! -f "$SRC/index.html" ]; then
  echo "STOPP: fant ikke nettsidefilene i zip-filen."
  exit 1
fi
echo "Fant $(ls "$SRC"/*.html 2>/dev/null | wc -l | tr -d ' ') sider"

# 5. Rydd bort Finder-dubletter fra tidligere
cd "$REPO"
find . -name "* [0-9].*" -not -path "./.git/*" -delete 2>/dev/null || true
rm -rf Library System usr bin sbin etc var home private 2>/dev/null || true

# 6. Kopier inn (behold CNAME, .nojekyll og .git)
cp -R "$SRC"/. "$REPO"/
echo "flavorsofandalucia.com" > "$REPO/CNAME"
touch "$REPO/.nojekyll"
echo "Filene er kopiert inn."

# 7. Last opp
git add -A
if git diff --cached --quiet; then
  echo "Ingenting nytt å laste opp — nettsiden er allerede oppdatert."
  exit 0
fi
git commit -m "Oppdatering fra Claude $(date '+%d.%m.%Y %H:%M')"
git push origin main

echo "──────────────────────────────────────────"
echo "  Ferdig. Nettsiden er oppdatert om"
echo "  et par minutter."
echo "──────────────────────────────────────────"

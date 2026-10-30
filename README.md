# IFFECTA — brand site

Static landing for the IFFECTA pink cleansing foam (IFF-01) + four legal pages.
No build step, no framework: plain HTML + CSS + a few lines of JS. Purchases go to Wildberries.

## Layout

```
public/              ← site docroot, upload as-is (Beget: /iffecta/public_html)
  index.html         ← landing
  privacy/ terms/ consent/ oferta/   ← legal pages (generated, do not edit by hand)
  css/site.css       ← layout and tokens (1:1 with the handoff)
  css/motion.css     ← animation layer: hero intro, scroll reveal, hovers; off under prefers-reduced-motion
  js/site.js         ← hero video switch, scroll reveal (IntersectionObserver), hero parallax
  assets/            ← brand logo, photos, ingredient images, bottles, hero/lotus video
  robots.txt  sitemap.xml  llms.txt  og-image.jpg  site.webmanifest  404.html  .htaccess
                     ← SEO/GEO layer, see docs/SEO.md
scripts/build_legal.py   ← rebuilds public/<slug>/index.html from docs/legal/*.md
scripts/build_sitemap.py ← rebuilds public/sitemap.xml (lastmod from git)
scripts/build_favicon.py ← rebuilds favicon.ico / favicon-32.png / apple-touch-icon.png / icon-*.png
                           («IF» from the wordmark on a pink rounded square)
docs/legal/*.md      ← legal texts (source of truth); placeholders marked [УКАЗАТЬ: ...]
docs/LINKS.md        ← official social + Wildberries links used on the site
docs/DEPLOY.md       ← hosting / domain / FTP plan
docs/SEO.md          ← SEO/GEO checklist: what is done, what waits for Webmaster/GSC accounts
design/HANDOFF.md    ← design handoff spec (tokens, sections, interactions)
design/landing-prototype.dc.html   ← original prototype, reference only
```

## Editing

- Landing texts and links: edit `public/index.html` directly.
- Legal texts: edit `docs/legal/<name>.md`, then run

  ```bash
  python scripts/build_legal.py
  ```

  The revision date shown on the pages is `REVISION_DATE` in the script.
- Local preview: any static server from `public/`, e.g. `python -m http.server 8765 --directory public`.

## Links on the site

| Place | Target |
|---|---|
| All «Купить» buttons, «Купить на Wildberries» | pink foam card on WB (863391328) |
| Lineup cards (hover «Купить») | pink 863391328 · yellow 863396761 · blue 863400750 |
| Footer «Wildberries» | brand page 312291079-iffecta |
| «@iffecta_» (UGC), footer socials | Instagram, TikTok, YouTube — see docs/LINKS.md |
| Footer «Документы» | /privacy/ /terms/ /consent/ /oferta/ |

## Known TODOs

- `assets/video/hero-mobile.mp4` is ~22 MB (uncompressed); hero-desktop is already compressed.
- Photos are served as JPEG; WebP/AVIF + `srcset` still to do.
- Legal pages contain `[УКАЗАТЬ: ...]` placeholders (highlighted in pink) — fill in before launch.

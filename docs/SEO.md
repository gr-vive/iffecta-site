# SEO / GEO checklist for iffecta.ru

Source of the recommendations: the Credyt GEO audits
(`credyt-marketing/GEO-AUDIT-REPORT.md`, `credyt-marketing/docs/gtm-reference/ai-billing-site/tasks/geo-audit-fixes.md`),
filtered down to what applies to a static brand landing. Applied 2026-10-30.

## Done (on-site)

| Item | Where |
|---|---|
| robots.txt — everything allowed, 11 AI crawlers named explicitly, sitemap referenced | `public/robots.txt` |
| sitemap.xml with `lastmod` (git commit date) and priorities | `public/sitemap.xml`, regenerate with `python scripts/build_sitemap.py` |
| llms.txt — brand, products, composition, pages, socials for AI systems | `public/llms.txt` |
| Canonical URL on every page, one URL form (`/privacy/` with trailing slash) | page heads + `.htaccess` redirect |
| Meta description ≤155 chars, title ≤60 chars on every page | page heads |
| Open Graph + Twitter Card on every page, `og:locale ru_RU`, `og:site_name` | page heads |
| OG image 1200×630 (`public/og-image.jpg`, three bottles) | generated from `assets/photos/1144.jpg` |
| JSON-LD on the landing: Organization (legalName, PostalAddress, email, logo as ImageObject, sameAs), Brand, WebSite, WebPage (dateModified, speakable), 3× Product (sku, size, colour, WB card as sameAs), ItemList | `public/index.html` |
| JSON-LD on legal pages: WebPage (datePublished/dateModified) + BreadcrumbList with `item` on every entry | `scripts/build_legal.py` |
| Legal pages indexable (`index, follow`), revision date shown as pills and in schema | `scripts/build_legal.py` |
| Security headers: X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy, CSP, HSTS | `public/.htaccess` |
| HTTPS + non-www 301 (only on iffecta.ru, Beget preview subdomain unaffected) | `public/.htaccess` |
| Cache-Control / Expires for assets, gzip for text | `public/.htaccess` |
| Custom 404 page (noindex) | `public/404.html` |
| Web app manifest + full favicon set, theme-color | `public/site.webmanifest`, `scripts/build_favicon.py` |
| `lang="ru"`, semantic headings H1 → H2 → H3, descriptive alt on product photos, `preconnect` to Google Fonts | `public/index.html` |

## Deferred (needs accounts or an owner decision)

- **Яндекс Вебмастер** — verify the domain, submit `sitemap.xml`. Add the verification meta tag to all pages (one line in `index.html` and `scripts/build_legal.py`).
- **Google Search Console** — same: verify, submit sitemap.
- **Bing Webmaster Tools + IndexNow** — optional; IndexNow key file + ping after deploy.
- **Яндекс Метрика** — add the counter and update `docs/legal/privacy.md` §5.2 (the placeholder is already there), then rebuild legal pages.
- **Product prices in schema** — `Offer` with `price` was left out on purpose: Google requires a price for Product rich results and a price-less Offer shows as an error in Search Console. Add `offers` when a price can be kept current.
- **Off-site entity signals** (from the audit's Brand Authority section): fill the WB brand page, keep Instagram/TikTok/YouTube handles consistent, consider a Wikidata entry for the brand once it has press coverage.
- **Content depth**: the landing is deliberately short (design is final). If organic search becomes a goal, add an FAQ block (with FAQPage schema) and a page per foam colour.

## How to keep it green

1. Edit texts → `python scripts/build_legal.py` (legal pages) and bump `REVISION_DATE` there when the legal text changes.
2. Commit → `python scripts/build_sitemap.py` (lastmod comes from git), commit the sitemap too.
3. After deploy, open `https://iffecta.ru/robots.txt`, `/sitemap.xml`, `/llms.txt`, and run
   https://search.google.com/test/rich-results and https://validator.schema.org on the homepage.

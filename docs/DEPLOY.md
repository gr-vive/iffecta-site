# IFFECTA site — hosting & domain plan

Status: plan (2026-10-30). Hosting: Beget, the SAME account that holds the beautycevtika.com VPS
(one business). NOT the drivemani account — drivemani is an unrelated client; its deploy script is
reused only as a code pattern. Domain: registered at a different provider — name and registrar TBD.

## 1. Domain → Beget: two options

**Option A (recommended): delegate NS to Beget.**
At the registrar, set the domain's nameservers to `ns1.beget.com` and `ns2.beget.com`
(`ns1.beget.pro` / `ns2.beget.pro` are also valid). Beget then owns the DNS zone:
A/AAAA records, `www`, free Let's Encrypt SSL with auto-renewal, and mail records if needed.
Domain stays paid/owned at the registrar — only DNS management moves.

Before switching: check the registrar's current DNS zone. If the domain already has MX
(mail) or other records in use, re-create them in Beget's DNS first, otherwise mail breaks.

**Option B: keep DNS at the registrar, point A records to Beget.**
In cp.beget.com → «Домены и поддомены» the account's server IP is shown. At the registrar create
`A @ → <IP>` and `A www → <IP>` (or `CNAME www → <domain>`). SSL still works via Beget, but
every future DNS change happens at the registrar. Use only if the registrar's DNS must stay
(e.g. corporate mail already configured there).

Propagation: usually 1–3 h, up to 24 h.

## 2. Beget panel steps (cp.beget.com)

1. «Сайты» → «Добавить сайт» → name `iffecta`. Beget creates `/iffecta/public_html`.
2. «Домены и поддомены» → «Добавить домен» → «Домен уже зарегистрирован» → enter the domain →
   link it to site `iffecta`. Enable «www» alias.
3. After DNS propagates: «SSL» → Let's Encrypt (free) for domain + www → enable
   «Перенаправление на HTTPS».
4. Optional, for preview before DNS switch: Beget gives a technical subdomain
   `<login>.beget.tech`; a subdomain like `iffecta.<login>.beget.tech` can be attached to the
   same site folder to check the build live.

## 3. FTP / deploy

- Credentials: from the BeautyCevtika Beget account (cp.beget.com → «FTP»). Current access is
  only root SSH to the VPS; panel login or a dedicated FTP user is still needed — see §5.
- Create a dedicated FTP user restricted to `/iffecta` so the deploy can touch nothing else.
- Local file: `.env.deploy` (gitignored), template in `.env.deploy.example`.
- Deploy script: port `../drivemani/scripts/deploy.mjs` (basic-ftp, upload-only, no deletes,
  auto-reconnect, staging copy in temp). Drop the PHP-handler part unless the site gets a
  form; add it back if a Telegram lead form is needed.

## 4. Open questions

- Domain name and registrar (needed for exact NS/A instructions).
- Does the domain currently serve mail or anything else?
- ~~Site stack~~ — decided 2026-10-30: plain static HTML/CSS/JS, docroot is `public/`
  (no build step; legal pages regenerated with `python scripts/build_legal.py`).
  The deploy script only needs to upload `public/` to `FTP_REMOTE_DIR`.

## 5. Decision 2026-10-30: same Beget account as BeautyCevtika (one business)

beautycevtika.com runs on a Beget **VPS** (193.42.124.42, Ubuntu + nginx + Bitrix, root SSH
for Glafira, maintained by Sergey). One Beget account can hold both a VPS and shared-hosting
sites, so "same account" has two shapes:

**Option 1 (recommended): shared-hosting site on the same account.**
cp.beget.com → «Сайты» → add site `iffecta` → attach domain → Let's Encrypt. Deploy by FTP
(sections 2–3 above). Same account, same invoice, but fully isolated from the Bitrix VPS:
a bad deploy or nginx typo cannot take beautycevtika.com down. Costs ~200–300 ₽/month if the
account has no shared tariff yet.

What Claude can do with current access: nothing in the panel (root SSH to the VPS does not
give panel/API rights). Two ways forward:
  a) Glafira does steps 1–3 of §2 in cp.beget.com herself, creates an FTP user for `/iffecta`,
     and puts host/user/password into `iffecta-site/.env.deploy`. Claude then handles deploys.
  b) Glafira puts the Beget panel login + password into `.env.deploy` (BEGET_LOGIN /
     BEGET_PASSWORD); Claude creates the site and links the domain via api.beget.com
     (`site/add`, `domain/addVirtual`, `domain/linkVirtual`), read-only `site/getList` first.

**Option 2: second nginx vhost on the beautycevtika VPS.**
Zero extra cost, but the two sites share one server and one nginx. Procedure:
1. Tell Sergey; agree on a window.
2. `ssh root@193.42.124.42`, read-only check first: `nginx -t`, `ls /etc/nginx/sites-enabled`,
   `df -h`, `certbot certificates`.
3. `mkdir -p /var/www/iffecta` (owner = nginx user, usually `www-data`).
4. `/etc/nginx/sites-available/iffecta.conf`:
   ```
   server {
       listen 80;
       server_name iffecta.ru www.iffecta.ru;
       root /var/www/iffecta;
       index index.html;
       location / { try_files $uri $uri/ $uri.html =404; }
   }
   ```
   `ln -s` into sites-enabled → `nginx -t` → only then `systemctl reload nginx`.
5. DNS at the registrar: `A iffecta.ru → 193.42.124.42`, `A www → 193.42.124.42`
   (same pattern beautycevtika uses via Timeweb DNS).
6. After DNS resolves: `certbot --nginx -d iffecta.ru -d www.iffecta.ru`.
7. Deploy = `rsync -az --delete out/ root@193.42.124.42:/var/www/iffecta/` (scoped to that
   folder only). Backups, if any, go to `/root/iffecta-backups/`, never under /var/www.
Never touch `/var/www/beautycevtika/` or its nginx config in the process.

Either way the domain stays at its registrar; only an A record (or NS delegation for
option 1) changes.

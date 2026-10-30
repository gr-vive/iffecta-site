"""Build the four legal pages (public/<slug>/index.html) from docs/legal/*.md.

The markdown files are the source of truth for the legal texts; the HTML template follows
design/HANDOFF.md section 11 (LegalPage). Re-run after editing any text:

    python scripts/build_legal.py
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "legal"
OUT = ROOT / "public"

REVISION_DATE = "30.10.2026"  # shown in the two pills under the H1
SITE = "https://iffecta.ru"

DOCS = [
    # slug, md file, H1 on the page, short label for nav, meta description
    ("privacy", "privacy.md", "Политика конфиденциальности", "Политика конфиденциальности",
     "Политика в отношении обработки персональных данных пользователей сайта iffecta.ru."),
    ("terms", "terms.md", "Пользовательское соглашение", "Пользовательское соглашение",
     "Пользовательское соглашение сайта iffecta.ru."),
    ("consent", "consent.md", "Согласие на обработку персональных данных", "Согласие на обработку ПД",
     "Согласие на обработку персональных данных пользователей сайта iffecta.ru."),
    ("oferta", "oferta.md", "Публичная оферта", "Оферта",
     "Публичная оферта о продаже товаров дистанционным способом. IFFECTA."),
]

REQUISITES = {
    "name": "ЗАО «Вакуумные Ионные Технологии»",
    "address": "143502, Московская область, м.о. Истра, г. Истра, ул. Почтовая, д. 31, офис 206",
    "codes": "ОГРН 1025001820425 · ИНН 5017008889 · КПП 501701001",
    "email": "hello@iffecta.ru",
}


# ---------- inline formatting ----------

URL_RE = re.compile(r"https?://[^\s)»]+")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
PLACEHOLDER_RE = re.compile(r"\[УКАЗАТЬ[^\]]*\]")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def inline(text: str) -> str:
    """Escape text, then turn urls / emails / bold / placeholders into HTML."""
    text = html.escape(text, quote=False)
    tokens: list[str] = []

    def stash(fragment: str) -> str:
        tokens.append(fragment)
        return f"\x00{len(tokens) - 1}\x00"

    def url(m: re.Match) -> str:
        raw = m.group(0)
        trailing = ""
        while raw and raw[-1] in ".,;:":
            trailing = raw[-1] + trailing
            raw = raw[:-1]
        href = raw
        if href.startswith(SITE):
            path = href[len(SITE):] or "/"
            href = path if path.endswith("/") or path == "/" else path + "/"
        return stash(f'<a href="{href}">{raw}</a>') + trailing

    text = URL_RE.sub(url, text)
    text = EMAIL_RE.sub(lambda m: stash(f'<a href="mailto:{m.group(0)}">{m.group(0)}</a>'), text)
    text = PLACEHOLDER_RE.sub(lambda m: stash(f"<mark>{m.group(0)}</mark>"), text)
    text = BOLD_RE.sub(lambda m: f"<strong>{m.group(1)}</strong>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: tokens[int(m.group(1))], text)


# ---------- markdown parsing ----------

def parse(md: str) -> dict:
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    md = md.split("\n---", 1)[0]  # consent.md: checkbox labels live after the rule
    lines = md.splitlines()

    title = subtitle = ""
    intro: list[str] = []
    sections: list[dict] = []
    current: dict | None = None
    buf: list[str] = []
    blocks: list[tuple[str, object]] = []

    def flush() -> None:
        nonlocal buf
        if not buf:
            return
        if buf[0].lstrip().startswith("- "):
            items, item = [], ""
            for ln in buf:
                if ln.lstrip().startswith("- "):
                    if item:
                        items.append(item)
                    item = ln.lstrip()[2:].strip()
                else:
                    item += " " + ln.strip()
            if item:
                items.append(item)
            blocks.append(("ul", items))
        else:
            blocks.append(("p", " ".join(ln.strip() for ln in buf)))
        buf = []

    def close_section() -> None:
        nonlocal blocks
        flush()
        if current is not None:
            current["blocks"] = blocks
        blocks = []

    for ln in lines:
        if ln.startswith("# "):
            title = ln[2:].strip()
            continue
        if ln.startswith("## "):
            subtitle = ln[3:].strip()
            continue
        m = re.match(r"^### (\d+)\.\s*(.+)$", ln)
        if m:
            close_section()
            current ={"num": int(m.group(1)), "title": m.group(2).strip()}
            sections.append(current)
            continue
        if ln.strip().startswith("Дата публикации"):
            continue
        if ln.strip() == "":
            flush()
            if current is None and blocks:
                intro.extend(b[1] for b in blocks if b[0] == "p")
                blocks = []
            continue
        buf.append(ln)
    close_section()
    if current is None and blocks:
        intro.extend(b[1] for b in blocks if b[0] == "p")
    return {"title": title, "subtitle": subtitle, "intro": intro, "sections": sections}


# ---------- rendering ----------

def render_blocks(blocks: list) -> str:
    out = []
    for kind, val in blocks:
        if kind == "p":
            out.append(f"        <p>{inline(val)}</p>")
        else:
            lis = "".join(f"\n          <li>{inline(i)}</li>" for i in val)
            out.append(f"        <ul>{lis}\n        </ul>")
    return "\n".join(out)


def render_requisites(blocks: list) -> str:
    """Last section: company card instead of plain paragraphs (per the design)."""
    extra = []
    for kind, val in blocks:
        if kind != "p":
            continue
        for part in re.split(r"\s(?=(?:Банковские реквизиты|Телефон):)", val):
            if part.startswith(("Банковские реквизиты", "Телефон")):
                extra.append(f"          <div>{inline(part)}</div>")
    r = REQUISITES
    rows = [
        f"          <strong>{html.escape(r['name'])}</strong>",
        f"          <div>{html.escape(r['address'])}</div>",
        f"          <div>{html.escape(r['codes'])}</div>",
        *extra,
        f"          <a href=\"mailto:{r['email']}\">{r['email']}</a>",
    ]
    return "        <div class=\"requisites\">\n" + "\n".join(rows) + "\n        </div>"


def nav_html(active: str, cls: str) -> str:
    items = []
    for slug, _, _, label, _ in DOCS:
        cur = ' aria-current="page"' if slug == active else ""
        items.append(f'    <a href="/{slug}/"{cur}>{html.escape(label)}</a>')
    return f'  <nav class="{cls}">\n' + "\n".join(items) + "\n  </nav>"


FOOTER = """<footer class="footer">
  <div class="footer__big"><div>Эмоции first!</div></div>
  <div class="footer__cols">
    <div class="footer__col footer__col--brand">
      <img src="/assets/brand/logo-oneline-black.png" alt="IFFECTA">
      <p>Make cosmetics fun again</p>
    </div>
    <div class="footer__col">
      <div class="label">Соцсети</div>
      <a href="https://www.instagram.com/iffecta_" target="_blank" rel="noopener">Instagram</a>
      <a href="https://www.tiktok.com/@iffecta" target="_blank" rel="noopener">TikTok</a>
      <a href="https://www.youtube.com/@Iffecta" target="_blank" rel="noopener">YouTube</a>
    </div>
    <div class="footer__col">
      <div class="label">Где купить</div>
      <a href="https://www.wildberries.ru/brands/312291079-iffecta" target="_blank" rel="noopener">Wildberries</a>
      <a href="/#lineup">Все пенки</a>
    </div>
    <div class="footer__col">
      <div class="label">Документы</div>
      <a href="/privacy/">Политика конфиденциальности</a>
      <a href="/terms/">Пользовательское соглашение</a>
      <a href="/consent/">Согласие на обработку персональных данных</a>
      <a href="/oferta/">Оферта</a>
    </div>
  </div>
  <div class="footer__bottom">
    <span>© 2026 IFFECTA. Все права защищены.</span>
    <a href="mailto:hello@iffecta.ru">hello@iffecta.ru</a>
  </div>
</footer>"""


def render(slug: str, h1: str, description: str, doc: dict) -> str:
    secs = list(doc["sections"])
    # Every document ends with the company card (design §11). If the text has no
    # «Реквизиты» section (consent.md), add a synthetic «Контакты оператора».
    if not re.search(r"Реквизит", secs[-1]["title"]):
        secs.append({"num": secs[-1]["num"] + 1, "title": "Контакты оператора", "blocks": []})
    toc = "\n".join(
        f'        <li><a href="#s{s["num"]}">{s["num"]}. {html.escape(s["title"])}</a></li>' for s in secs
    )
    body = []
    for i, s in enumerate(secs):
        last = i == len(secs) - 1
        content = render_requisites(s["blocks"]) if last else render_blocks(s["blocks"])
        body.append(
            f'      <section id="s{s["num"]}" class="doc__section">\n'
            f'        <h2><span>{s["num"]:02d}</span>{html.escape(s["title"])}</h2>\n'
            f"{content}\n"
            f"      </section>"
        )
    intro_html = "\n".join(f'      <p class="doc__intro">{inline(p)}</p>' for p in doc["intro"])
    if not intro_html and doc["subtitle"]:
        intro_html = f'      <p class="doc__intro">{inline(doc["subtitle"])}</p>'

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(h1)} — IFFECTA</title>
<meta name="description" content="{html.escape(description, quote=True)}">
<meta name="robots" content="noindex, follow">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta name="theme-color" content="#F7C7DD">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/site.css">
</head>
<body>
<div class="page">

<header class="header">
  <a href="/" class="header__logo"><img src="/assets/brand/logo-oneline-black.png" alt="IFFECTA"></a>
{nav_html(slug, "nav nav--docs")}
  <a href="/#buy" class="btn btn--black">Купить</a>
</header>

<main class="card">
  <div class="doc-head">
    <a href="/" class="doc-head__back"><span>←</span><span>На главную</span></a>
    <div class="label">Документы</div>
    <h1 class="doc-head__title">{html.escape(h1)}</h1>
    <div class="pills">
      <span class="pill">Редакция от {REVISION_DATE}</span>
      <span class="pill">Действует с {REVISION_DATE}</span>
    </div>
  </div>

  <div class="doc-body">
    <aside class="toc">
      <div class="label">Содержание</div>
      <ol>
{toc}
      </ol>
    </aside>

    <article class="doc">
{intro_html}
{chr(10).join(body)}
    </article>
  </div>
</main>

{FOOTER}

</div>
</body>
</html>
"""


def main() -> None:
    for slug, md_name, h1, _label, description in DOCS:
        doc = parse((SRC / md_name).read_text(encoding="utf-8"))
        out_dir = OUT / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(render(slug, h1, description, doc), encoding="utf-8")
        print(f"{slug:8s} {len(doc['sections']):2d} sections -> public/{slug}/index.html")


if __name__ == "__main__":
    main()

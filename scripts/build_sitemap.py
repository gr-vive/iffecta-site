"""Write public/sitemap.xml from the index.html files under public/.

lastmod = the file's last git commit date (falls back to the file mtime).

    python scripts/build_sitemap.py
"""
from __future__ import annotations

import datetime as dt
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
SITE = "https://iffecta.ru"

PRIORITY = {"/": "1.0"}
DEFAULT_PRIORITY = "0.3"


def lastmod(path: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path.relative_to(ROOT))],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            return out
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return dt.date.fromtimestamp(path.stat().st_mtime).isoformat()


def main() -> None:
    pages = sorted(PUBLIC.rglob("index.html"), key=lambda p: len(p.parts))
    rows = []
    for page in pages:
        rel = page.relative_to(PUBLIC).parent.as_posix()
        url = "/" if rel == "." else f"/{rel}/"
        rows.append(
            "  <url>\n"
            f"    <loc>{SITE}{url}</loc>\n"
            f"    <lastmod>{lastmod(page)}</lastmod>\n"
            f"    <priority>{PRIORITY.get(url, DEFAULT_PRIORITY)}</priority>\n"
            "  </url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n"
    )
    (PUBLIC / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"sitemap.xml: {len(rows)} urls")


if __name__ == "__main__":
    main()

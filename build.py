#!/usr/bin/env python3
"""Static-site builder for SkinRx by Burds Family Practice.

Builds:
  - Core pages from src/pages/*.html -> dist/*.html
  - Learning Hub comparison guides from src/learn/*.html -> dist/learn/*.html
  - Blog articles from src/blog/*.html -> dist/blog/*.html
  - Static assets, sitemap.xml, and robots.txt

Usage:
  python3 build.py          # build all pages into dist/
  python3 build.py serve    # build, then serve dist/ on http://localhost:8080
"""
import datetime
import hashlib
import html as html_lib
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
SITE_BASE = os.environ.get("SITE_BASE", "/")
SITE = os.environ.get("SITE_URL", "https://www.burdsskinrx.com/").rstrip("/") + "/"

NAV = [
    ("treatments", "treatments.html", "Treatments"),
    ("packages", "packages.html", "Packages"),
    ("skincare", "skincare.html", "Skincare"),
    ("financing", "financing.html", "Financing"),
    ("about", "about.html", "Team"),
    ("resources", "resources.html", "Guides & FAQ"),
    ("contact", "contact.html", "Contact"),
]

META_RE = re.compile(r"^\s*<!--(.*?)-->\s*", re.S)


def parse_meta(text):
    """Parse leading HTML metadata comment into a dict and remaining body."""
    m = META_RE.match(text)
    if not m:
        raise ValueError("page is missing its leading metadata comment")
    meta = {}
    for part in m.group(1).split("|"):
        key, sep, value = part.partition(":")
        if sep:
            meta[key.strip().lower()] = value.strip()
    return meta, text[m.end():]


def nav_html(active, base=""):
    """Build primary navigation list items with active page indicator."""
    items = []
    for key, href, label in NAV:
        current = ' aria-current="page"' if key == active else ""
        items.append(f'<li><a href="{base}{href}"{current}>{label}</a></li>')
    return "\n          ".join(items)


def _asset_hash(rel_path):
    """Return a short content hash for cache-busting static CSS/JS links."""
    target = SRC / rel_path
    if not target.exists():
        return "dev"
    return hashlib.sha256(target.read_bytes()).hexdigest()[:10]


def _format_date(date_str):
    """Format an ISO date (YYYY-MM-DD) for display, falling back cleanly."""
    if not date_str:
        return ""
    try:
        dt = datetime.date.fromisoformat(date_str.strip())
        return dt.strftime("%B %-d, %Y")
    except ValueError:
        return date_str.strip()


def _mangomint_cta_band(base="../"):
    """Standard warm CTA strip linking to Mangomint booking and clinic locations."""
    return (
        '    <section class="cta-band">\n'
        '      <div class="container">\n'
        '        <div>\n'
        '          <h2>Ready for a personalized treatment plan?</h2>\n'
        '          <p>Book a consultation or aesthetic visit in Peosta or Dyersville, or call (563) 588-6659 with questions.</p>\n'
        '        </div>\n'
        '        <div class="btn-row">\n'
        '          <a class="btn btn--warm" href="https://booking.mangomint.com/437183" target="_blank" rel="noopener">Book Online</a>\n'
        f'          <a class="btn btn--ghost-light" href="{base}contact.html">Hours &amp; Locations</a>\n'
        '        </div>\n'
        '      </div>\n'
        '    </section>'
    )


def render_page(layout, *, title, description, path, nav_key, base, content, css_v="", js_v=""):
    """Populate layout placeholders and verify no unreplaced tokens remain."""
    full_title = (
        title if "SkinRx" in title else f"{title} | SkinRx by Burds Family Practice"
    )
    rendered = (
        layout.replace("{{title}}", html_lib.escape(full_title, quote=True))
        .replace("{{description}}", html_lib.escape(description, quote=True))
        .replace("{{path}}", path)
        .replace("{{base}}", base)
        .replace("{{css_v}}", css_v)
        .replace("{{js_v}}", js_v)
        .replace("{{nav}}", nav_html(nav_key, base=base))
        .replace("{{content}}", content.replace("{{base}}", base))
    )
    leftover = re.findall(r"\{\{\w+\}\}", rendered)
    if leftover:
        raise ValueError(f"{path}: unreplaced placeholders {leftover}")
    return rendered


def _wrap_article(body, *, meta, back_href, back_label, default_eyebrow, is_blog=False):
    """Wrap a native learn or blog HTML fragment with breadcrumb, prose container, and CTA."""
    title = meta.get("title", "")
    eyebrow = html_lib.escape(meta.get("category", default_eyebrow))
    has_shell = "article-shell" in body
    has_h1 = bool(re.search(r"<h1\b", body, re.I))
    has_prose = "prose-guide" in body
    has_cta = ("booking.mangomint.com" in body) or ('class="cta-band"' in body)

    breadcrumb = (
        '    <div class="learn-breadcrumb-bar">\n'
        '      <div class="container">\n'
        f'        <a class="breadcrumb" href="{back_href}">&larr; {back_label}</a>\n'
        '      </div>\n'
        '    </div>\n'
    )

    if has_shell:
        inner = body
    else:
        head_html = ""
        if not has_h1 and title:
            meta_row = ""
            if is_blog:
                date_iso = meta.get("date", "")
                date_label = meta.get("date_label") or _format_date(date_iso)
                author = meta.get("author", "Jenny Burds, DNP, ARNP · Peosta & Dyersville, IA")
                date_span = (
                    f'<span>Published <time datetime="{html_lib.escape(date_iso)}">{html_lib.escape(date_label)}</time></span>'
                    if date_label
                    else ""
                )
                meta_row = (
                    '\n              <div class="article-meta">\n'
                    f'                {date_span}\n'
                    f'                <span>{html_lib.escape(author)}</span>\n'
                    '              </div>'
                )
            head_html = (
                '          <header class="article-head">\n'
                f'            <span class="eyebrow">{eyebrow}</span>\n'
                f'            <h1>{html_lib.escape(title)}</h1>{meta_row}\n'
                '          </header>\n'
            )
        prose_block = body if has_prose else f'<div class="prose prose-guide">\n{body}\n          </div>'
        inner = (
            '    <section class="article-shell">\n'
            '      <div class="container">\n'
            '        <article class="article-wrap">\n'
            f'{head_html}'
            f'          {prose_block}\n'
            '        </article>\n'
            '      </div>\n'
            '    </section>\n'
        )

    cta_html = "" if has_cta else f"\n{_mangomint_cta_band(base='../')}\n"
    return f"{breadcrumb}{inner}{cta_html}"


def build_learn_pages(layout, css_v="", js_v=""):
    """Build native Learning Hub comparison guides from src/learn/*.html."""
    learn_dir = SRC / "learn"
    if not learn_dir.exists():
        return 0
    out_dir = DIST / "learn"
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for src_file in sorted(learn_dir.glob("*.html")):
        meta, body = parse_meta(src_file.read_text(encoding="utf-8"))
        title = meta.get("title") or src_file.stem.replace("-", " ").title()
        content = _wrap_article(
            body,
            meta=meta,
            back_href="../resources.html#guides",
            back_label="Back to Guides &amp; FAQ",
            default_eyebrow="Treatment Guide",
            is_blog=False,
        )
        html = render_page(
            layout,
            title=title,
            description=meta.get("description", ""),
            path=f"learn/{src_file.name}",
            nav_key=meta.get("nav", "resources"),
            base="../",
            content=content,
            css_v=css_v,
            js_v=js_v,
        )
        (out_dir / src_file.name).write_text(html, encoding="utf-8")
        count += 1
    return count


def build_blog_pages(layout, css_v="", js_v=""):
    """Build native clinic blog articles from src/blog/*.html."""
    blog_dir = SRC / "blog"
    if not blog_dir.exists():
        return 0
    out_dir = DIST / "blog"
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for src_file in sorted(blog_dir.glob("*.html")):
        meta, body = parse_meta(src_file.read_text(encoding="utf-8"))
        title = meta.get("title") or src_file.stem.replace("-", " ").title()
        content = _wrap_article(
            body,
            meta=meta,
            back_href="../resources.html#blog",
            back_label="Back to Guides &amp; Blog",
            default_eyebrow="SkinRx Journal",
            is_blog=True,
        )
        html = render_page(
            layout,
            title=title,
            description=meta.get("description", ""),
            path=f"blog/{src_file.name}",
            nav_key=meta.get("nav", "resources"),
            base="../",
            content=content,
            css_v=css_v,
            js_v=js_v,
        )
        (out_dir / src_file.name).write_text(html, encoding="utf-8")
        count += 1
    return count


def write_sitemap():
    """Emit sitemap.xml (every built page except 404) and robots.txt."""
    urls = []
    for f in sorted(DIST.rglob("*.html")):
        rel = f.relative_to(DIST).as_posix()
        if rel == "404.html" or rel.startswith("review/"):
            continue
        urls.append(SITE + ("" if rel == "index.html" else rel))
    body = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n</urlset>\n",
        encoding="utf-8",
    )
    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n",
        encoding="utf-8",
    )


def build():
    """Cleanly rebuild dist/ from src/."""
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True, exist_ok=True)

    if (SRC / "assets").exists():
        shutil.copytree(SRC / "assets", DIST / "assets")

    css_v = _asset_hash("assets/css/styles.css")
    js_v = _asset_hash("assets/js/main.js")
    layout = (
        (SRC / "layout.html")
        .read_text(encoding="utf-8")
        .replace("{{css_v}}", css_v)
        .replace("{{js_v}}", js_v)
    )

    pages_dir = SRC / "pages"
    pages = sorted(pages_dir.glob("*.html")) if pages_dir.exists() else []
    for page in pages:
        meta, body = parse_meta(page.read_text(encoding="utf-8"))
        html = render_page(
            layout,
            title=meta["title"],
            description=meta.get("description", ""),
            path="" if page.name == "index.html" else page.name,
            nav_key=meta.get("nav", ""),
            base=SITE_BASE if page.name == "404.html" else "",
            content=body,
            css_v=css_v,
            js_v=js_v,
        )
        (DIST / page.name).write_text(html, encoding="utf-8")

    if (SRC / "review").exists():
        shutil.copytree(SRC / "review", DIST / "review")

    learn_count = build_learn_pages(layout, css_v=css_v, js_v=js_v)
    blog_count = build_blog_pages(layout, css_v=css_v, js_v=js_v)
    write_sitemap()
    total = len(pages) + learn_count + blog_count
    print(
        f"Built {total} pages ({len(pages)} core, {learn_count} learn guides, {blog_count} blog posts) into {DIST}"
    )


def serve(port=8080):
    """Serve dist/ locally with cache headers disabled for verification."""
    import functools
    import http.server

    class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            super().end_headers()

    handler = functools.partial(NoCacheHandler, directory=str(DIST))
    with http.server.ThreadingHTTPServer(("0.0.0.0", port), handler) as httpd:
        print(f"Serving on http://localhost:{port}  (Ctrl+C to stop)")
        httpd.serve_forever()


if __name__ == "__main__":
    build()
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        serve()

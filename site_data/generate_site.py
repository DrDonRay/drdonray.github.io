#!/usr/bin/env python3
"""
Regenerate the entire website from site_data/manifest.json.

Essay body text is never touched: for each essay page, the existing
<article class="essay-body">...</article> block is extracted verbatim from
the file currently on disk and spliced back in unchanged. Everything else
on every page (breadcrumbs, eyebrow numbering, continue-reading nav chains,
back-to-category links, tag lists, category listings, categories/index.html,
sitemap.xml, and the homepage's "Recently added" strip) is rebuilt fresh
from the manifest, so it can never drift out of sync with it.
"""
import re, os, sys, json, html, datetime, email.utils
sys.path.insert(0, os.path.dirname(__file__))
from common import (
    load_manifest, SITE, category_order, label,
    ordered_memberships, category_members_sorted, position_and_count, neighbors,
    HEAD_ESSAY_TMPL, HEAD_CATEGORY_TMPL, head_extra, SITE_URL, FOOTER_NOTICE, LICENSE_URL, LICENSE_NAME,
)

ESSAY_DIR = os.path.join(SITE, "essays")
CAT_DIR = os.path.join(SITE, "categories")

def esc(s):
    if s is None:
        return ""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def esc_attr(s):
    return esc(s).replace('"', "&quot;")

def extract_body(slug):
    path = os.path.join(ESSAY_DIR, f"{slug}.html")
    text = open(path, encoding="utf-8").read()
    m = re.search(r'(<article class="essay-body">.*?</article>)', text, re.S)
    if not m:
        raise ValueError(f"could not find essay-body in {slug}.html")
    return "  " + m.group(1)

def build_breadcrumb(m, slug, title):
    memberships = ordered_memberships(m, slug)
    lines = ['  <a href="../index.html">Home</a><span class="sep">/</span>',
             '  <a href="../categories/index.html">Categories</a><span class="sep">/</span>']
    if len(memberships) == 1:
        cat = memberships[0][0]
        lines.append(f'  <a href="../categories/{cat}.html">{esc(label(m, cat))}</a><span class="sep">/</span>')
    lines.append(f'  <span class="current">{esc(title)}</span>')
    return "\n".join(lines)

def build_eyebrow(m, slug):
    parts = []
    for cat, rank in ordered_memberships(m, slug):
        pos, count = position_and_count(m, cat, slug)
        parts.append(f"{label(m, cat)} · No. {pos} of {count}")
    return " &nbsp;·&nbsp; ".join(esc(p) for p in parts)

def build_also_in(m, slug):
    memberships = ordered_memberships(m, slug)
    if len(memberships) != 1:
        return ""
    cat = memberships[0][0]
    return (f'\n    <div class="also-in">\n'
            f'      <div class="label">Filed only under {esc(label(m, cat))}</div>\n'
            f'    </div>')

def nav_cell(direction, arrow_text, slug_or_none, title_by_slug):
    if slug_or_none is None:
        return (f'      <span class="nav-cell disabled">\n'
                f'        <span class="dir">{arrow_text}</span>\n'
                f'        <span class="title">—</span>\n'
                f'      </span>')
    cls = "nav-cell next" if direction == "next" else "nav-cell"
    title = title_by_slug(slug_or_none)
    return (f'      <a class="{cls}" href="{slug_or_none}.html">\n'
            f'        <span class="dir">{arrow_text}</span>\n'
            f'        <span class="title">{esc(title)}</span>\n'
            f'      </a>')

def build_continue_groups(m, slug):
    def title_of(s):
        return m["essays"][s]["title"]
    blocks = []
    for cat, rank in ordered_memberships(m, slug):
        prev_slug, next_slug = neighbors(m, cat, slug)
        prev_cell = nav_cell("prev", "← Previous", prev_slug, title_of)
        next_cell = nav_cell("next", "Next →", next_slug, title_of)
        blocks.append(
            f'    <div class="continue-label">Continue in {esc(label(m, cat))}</div>\n'
            f'    <div class="continue-group essay-nav">\n{prev_cell}\n{next_cell}\n    </div>'
        )
    return "\n\n".join(blocks) + "\n"

def build_back_links(m, slug):
    parts = []
    for i, (cat, rank) in enumerate(ordered_memberships(m, slug)):
        arrow = "↑ " if i == 0 else ""
        parts.append(f'<a href="../categories/{cat}.html">{arrow}All of {esc(label(m, cat))}</a>')
    return '<span class="sep">·</span>'.join(parts)

def generate_essay_page(m, slug):
    e = m["essays"][slug]
    title = e["title"]
    body = extract_body(slug)
    page = HEAD_ESSAY_TMPL.format(
        title=esc(title),
        slug=slug,
        head_extra=head_extra(),
        footer_notice=FOOTER_NOTICE,
        meta_description=esc_attr(e.get("meta_description") or ""),
        og_description=esc_attr(e.get("og_description") or ""),
        breadcrumb=build_breadcrumb(m, slug, title),
        eyebrow=build_eyebrow(m, slug),
        also_in=build_also_in(m, slug),
        body=body,
        continue_groups=build_continue_groups(m, slug),
        back_links=build_back_links(m, slug),
    )
    with open(os.path.join(ESSAY_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(page)

def build_tag_list(m, cat_slug, slug):
    others = [c for c, r in ordered_memberships(m, slug) if c != cat_slug]
    if not others:
        return f'        <span class="tag" style="opacity:.6;">{esc(label(m, cat_slug))} only</span>'
    # spans, not links: a link inside the row's own <a> is invalid HTML and makes
    # browsers break the row apart (the tags spilled out of the card as full-width bars)
    lines = [f'        <span class="tag">{esc(label(m, c))}</span>' for c in others]
    return "\n".join(lines)

ROW_TMPL = """    <a class="essay-row" href="../essays/{slug}.html">
      <span class="pos">{pos}</span>
      <span>
        <h3>{title}</h3>
        <p class="excerpt">“{excerpt}”</p>
        <span class="tag-list">
{tags}
        </span>
      </span>
    </a>
"""

def generate_category_page(m, cat_slug):
    cat = m["categories"][cat_slug]
    members = category_members_sorted(m, cat_slug)
    rows = []
    # Arc (chapter) headings: categories[cat].arcs = [{"label", "starts_at": essay slug}]
    arc_at = {a["starts_at"]: a["label"] for a in cat.get("arcs", [])}
    member_slugs = {s for s, _ in members}
    for a in cat.get("arcs", []):
        if a["starts_at"] not in member_slugs:
            raise SystemExit(f"arc '{a['label']}' in {cat_slug} starts at {a['starts_at']}, which is not in that category")
    for i, (slug, rank) in enumerate(members, start=1):
        e = m["essays"][slug]
        excerpt = e["memberships"][cat_slug]["excerpt"]
        if slug in arc_at:
            rows.append(f'    <h2 class="arc-heading">{esc(arc_at[slug])}</h2>\n')
        rows.append(ROW_TMPL.format(
            slug=slug, pos=i, title=esc(e["title"]), excerpt=esc(excerpt),
            tags=build_tag_list(m, cat_slug, slug),
        ))
    page = HEAD_CATEGORY_TMPL.format(
        label=esc(cat["label"]),
        slug=cat_slug,
        head_extra=head_extra(),
        footer_notice=FOOTER_NOTICE,
        meta_description=esc_attr(cat.get("meta_description") or ""),
        og_description=esc_attr(cat.get("og_description") or ""),
        lede=esc(cat.get("lede") or ""),
        rows="\n".join(rows),
    )
    with open(os.path.join(CAT_DIR, f"{cat_slug}.html"), "w", encoding="utf-8") as f:
        f.write(page)

# The one-line category descriptions on the homepage and categories/index.html
# cards now live in the manifest as categories[slug]["blurb"] (Oct 20, 2026).

CATEGORIES_INDEX_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Categories — The Reassuring Universe</title>
<meta name="description" content="All seven essay categories in The Reassuring Universe, a collection by Don Ray: poetry, purpose, spirituality, observation, vision, and personal perspective.">
<link rel="canonical" href="https://drdonray.github.io/categories/">
<meta property="og:type" content="website">
<meta property="og:title" content="Categories — The Reassuring Universe">
<meta property="og:description" content="All seven essay categories in The Reassuring Universe, a collection by Don Ray.">
<meta property="og:url" content="https://drdonray.github.io/categories/">
{head_extra}<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="site-header-inner">
    <a class="brand" href="../index.html">The Reassuring Universe
      <span class="brand-sub">Essays by Don Ray</span>
    </a>
    <nav class="primary-nav" aria-label="Primary">
      <a href="../index.html">Home</a>
      <a href="index.html" aria-current="page">Categories</a>
      <a href="../search.html">Search</a>
    </nav>
  </div>
</header>

<p class="breadcrumbs">
  <a href="../index.html">Home</a><span class="sep">/</span><span class="current">Categories</span>
</p>

<main id="main">
  <div class="page-head">
    <h1>Categories</h1>
    <p class="lede">Every essay is filed under one or more of these seven categories, and ordered within each by conceptual dependency — simpler or more concrete pieces first, building toward the more abstract. An essay that fits more than one theme appears, in full, on every category page it belongs to.</p>
  </div>

  <div class="category-grid">

{cards}
  </div>
</main>

<footer class="site-footer">
  <div class="site-footer-inner">
    {footer_notice}
    <nav aria-label="Footer">
      <a href="../index.html">Home</a>
      <a href="../feed.xml">RSS feed</a>
    </nav>
  </div>
</footer>

</body>
</html>
"""


def generate_categories_index(m):
    cards = []
    for cat_slug in CATEGORY_CARD_ORDER:
        cat = m["categories"][cat_slug]
        count = len(category_members_sorted(m, cat_slug))
        noun = "poems" if cat_slug == "poetry" else "essays"
        cards.append(
            f'    <a class="category-card is-live" href="{cat_slug}.html" id="{cat_slug}">\n'
            f'      <span class="status-pill live">Live</span>\n'
            f'      <h2>{esc(cat["label"])}</h2>\n'
            f'      <p>{esc(cat["blurb"])}</p>\n'
            f'      <span class="count">{count} {noun}</span>\n'
            f'    </a>\n'
        )
    page = CATEGORIES_INDEX_TMPL.format(cards="\n".join(cards), head_extra=head_extra(), footer_notice=FOOTER_NOTICE)
    with open(os.path.join(CAT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)

def generate_sitemap(m):
    urls = ["https://drdonray.github.io/", "https://drdonray.github.io/categories/"]  # categories/index.html's canonical address
    for cat_slug in category_order(m):
        urls.append(f"https://drdonray.github.io/categories/{cat_slug}.html")
    for slug in sorted(m["essays"].keys()):
        urls.append(f"https://drdonray.github.io/essays/{slug}.html")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append(f"  <url><loc>{u}</loc></url>")
    lines.append("</urlset>")
    with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

RECENT_CARD_TMPL = """      <a class="recent-card" href="essays/{slug}.html">
        <span class="eyebrow">{cat_label}</span>
        <h3>{title}</h3>
        <p>“{excerpt}”</p>
      </a>"""

def generate_homepage_recent_strip(m):
    path = os.path.join(SITE, "index.html")
    text = open(path, encoding="utf-8").read()
    cards = []
    for slug in m["homepage_recent"]:
        e = m["essays"][slug]
        # Prefer showing "Poetry" as the eyebrow when the essay is a poem
        # (that's usually *why* it's newly featured); otherwise fall back
        # to its first canonical-order category.
        memberships = ordered_memberships(m, slug)
        cat = "poetry" if "poetry" in e["memberships"] else memberships[0][0]
        excerpt = e["memberships"][cat]["excerpt"]
        cards.append(RECENT_CARD_TMPL.format(
            slug=slug, cat_label=esc(label(m, cat)), title=esc(e["title"]), excerpt=esc(excerpt),
        ))
    new_grid_inner = "\n\n".join(cards)
    new_text, n = re.subn(
        r'(<div class="recent-grid">\n\n).*?(\n\n    </div>)',
        lambda mm: mm.group(1) + new_grid_inner + mm.group(2),
        text, flags=re.S,
    )
    if n != 1:
        raise ValueError("homepage recent-grid block not found/replaced exactly once")
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)

# ---------- Homepage category cards ----------

# Card order on the homepage and on categories/index.html (author's choice,
# Oct 20, 2026); independent of the canonical category order.
CATEGORY_CARD_ORDER = [
    "observations-of-human-life", "structure-of-the-purpose-and-destiny-of-life",
    "spiritual-without-religion", "spiritual-with-religion",
    "transcendent-conversations-and-vision", "poetry", "personal-perspective",
]

def generate_homepage_categories(m):
    path = os.path.join(SITE, "index.html")
    text = open(path, encoding="utf-8").read()
    cards = []
    for cat_slug in CATEGORY_CARD_ORDER:
        cat = m["categories"][cat_slug]
        count = len(category_members_sorted(m, cat_slug))
        noun = "poems" if cat_slug == "poetry" else "essays"
        cards.append(
            f'      <a class="category-card" href="categories/{cat_slug}.html">\n'
            f'        <h3>{esc(cat["label"])}</h3>\n'
            f'        <p>{esc(cat["blurb"])}</p>\n'
            f'        <span class="count">{count} {noun}</span>\n'
            f'      </a>\n'
        )
    new_text, n = re.subn(
        r'(<!-- home-categories:start[^>]*-->\n).*?(<!-- home-categories:end -->)',
        lambda mm: mm.group(1) + "".join(cards) + mm.group(2),
        text, flags=re.S,
    )
    if n != 1:
        raise ValueError("homepage category block markers not found exactly once")
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)

# ---------- Site search (static, client-side) ----------
# assets/search-index.js holds every essay's title, categories and plain body text;
# assets/search.js (hand-written) searches it in the reader's browser. No server needed.

def plain_text(body_html):
    t = re.sub(r'<br\s*/?>', ' ', body_html)
    t = re.sub(r'</(p|div|li|ul)>', ' ', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t).replace('\xa0', ' ')
    return ' '.join(t.split())

def generate_search_index(m):
    docs = []
    for slug in sorted(m["essays"]):
        e = m["essays"][slug]
        body = extract_body(slug)
        inner = re.search(r'<article class="essay-body">(.*)</article>', body, re.S).group(1)
        docs.append({
            "slug": slug,
            "title": e["title"],
            "cats": [label(m, c) for c, _ in ordered_memberships(m, slug)],
            "text": plain_text(inner),
        })
    js = ("/* Generated by site_data/generate_site.py from the essay pages; do not edit by hand. */\n"
          "window.SEARCH_INDEX = " + json.dumps(docs, ensure_ascii=False, separators=(",", ":")) + ";\n")
    with open(os.path.join(SITE, "assets", "search-index.js"), "w", encoding="utf-8") as f:
        f.write(js)

SEARCH_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Search — The Reassuring Universe</title>
<meta name="description" content="Search the essays and poems of The Reassuring Universe by Don Ray.">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://drdonray.github.io/search.html">
<!--HEAD_EXTRA--><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="site-header-inner">
    <a class="brand" href="index.html">The Reassuring Universe
      <span class="brand-sub">Essays by Don Ray</span>
    </a>
    <nav class="primary-nav" aria-label="Primary">
      <a href="index.html">Home</a>
      <a href="categories/index.html">Categories</a>
      <a href="search.html" aria-current="page">Search</a>
    </nav>
  </div>
</header>

<p class="breadcrumbs">
  <a href="index.html">Home</a><span class="sep">/</span><span class="current">Search</span>
</p>

<main id="main">
  <div class="page-head">
    <h1>Search</h1>
    <form class="site-search" id="search-form" action="search.html" method="get" role="search">
      <input type="search" id="search-q" name="q" placeholder="Search the essays" aria-label="Search the essays" autocomplete="off">
      <button type="submit" class="btn btn-primary">Search</button>
    </form>
    <p class="search-help">Finds essays and poems that contain all of your words. Put a phrase in quotation marks to search for it exactly.</p>
    <noscript><p class="search-status">Search needs JavaScript turned on in your browser. You can also browse by <a href="categories/index.html">category</a>.</p></noscript>
    <p class="search-status" id="search-status" aria-live="polite"></p>
  </div>
  <div class="essay-list" id="search-results"></div>
</main>

<footer class="site-footer">
  <div class="site-footer-inner">
    <!--FOOTER_NOTICE-->
    <nav aria-label="Footer">
      <a href="categories/index.html">All categories</a>
      <a href="feed.xml">RSS feed</a>
    </nav>
  </div>
</footer>
<script src="assets/search-index.js"></script>
<script src="assets/search.js"></script>
</body>
</html>
"""

def generate_search_page(m):
    with open(os.path.join(SITE, "search.html"), "w", encoding="utf-8") as f:
        f.write(SEARCH_TMPL.replace("<!--HEAD_EXTRA-->", head_extra()).replace("<!--FOOTER_NOTICE-->", FOOTER_NOTICE))


# ---------- Homepage <head> additions ----------
def generate_homepage_head(m):
    path = os.path.join(SITE, "index.html")
    text = open(path, encoding="utf-8").read()
    new_text, n = re.subn(
        r'(<!-- head-extra:start[^>]*-->\n).*?(<!-- head-extra:end -->)',
        lambda mm: mm.group(1) + head_extra() + mm.group(2),
        text, flags=re.S,
    )
    if n != 1:
        raise ValueError("homepage head-extra markers not found exactly once")
    new_text, n = re.subn(
        r'(<!-- footer-notice:start[^>]*-->\n).*?(\s*<!-- footer-notice:end -->)',
        lambda mm: mm.group(1) + "    " + FOOTER_NOTICE + mm.group(2),
        new_text, flags=re.S,
    )
    if n != 1:
        raise ValueError("homepage footer-notice markers not found exactly once")
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)

# ---------- RSS feed (Oct 25, 2026) ----------
# feed.xml lists every essay and poem. Its date is essays[slug]["added"] (YYYY-MM-DD)
# when present, otherwise the manifest's "site_launched" date. Give each NEW essay an
# "added" date so it shows up as new in readers' feed apps.
FEED_DESCRIPTION = "A personal collection of essays on purpose, spirit, and everyday wonder, organized by theme."

def xml_esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def rfc822(day):
    d = datetime.date.fromisoformat(day)
    return email.utils.format_datetime(datetime.datetime(d.year, d.month, d.day, 12, 0, tzinfo=datetime.timezone.utc))

def generate_feed(m):
    launched = m["site_launched"]
    # reading order for same-day items: card order, then rank within each category
    reading = []
    for cat_slug in CATEGORY_CARD_ORDER:
        for slug, _ in category_members_sorted(m, cat_slug):
            if slug not in reading:
                reading.append(slug)
    assert set(reading) == set(m["essays"])
    dated = [(m["essays"][s].get("added", launched), i, s) for i, s in enumerate(reading)]
    dated.sort(key=lambda t: (-datetime.date.fromisoformat(t[0]).toordinal(), t[1]))
    newest = dated[0][0]
    items = []
    for day, _, slug in dated:
        e = m["essays"][slug]
        url = f"{SITE_URL}/essays/{slug}.html"
        cats = "".join(f"\n      <category>{xml_esc(label(m, c))}</category>" for c, _ in ordered_memberships(m, slug))
        items.append(
            f"    <item>\n"
            f"      <title>{xml_esc(e['title'])}</title>\n"
            f"      <link>{url}</link>\n"
            f"      <guid isPermaLink=\"true\">{url}</guid>\n"
            f"      <pubDate>{rfc822(day)}</pubDate>\n"
            f"      <dc:creator>Don Ray</dc:creator>{cats}\n"
            f"      <description>{xml_esc(e.get('meta_description'))}</description>\n"
            f"    </item>"
        )
    feed = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        '  <channel>\n'
        '    <title>The Reassuring Universe</title>\n'
        f'    <link>{SITE_URL}/</link>\n'
        f'    <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>\n'
        f'    <description>{xml_esc(FEED_DESCRIPTION)}</description>\n'
        '    <language>en</language>\n'
        f'    <copyright>© Don Ray. Licensed {LICENSE_NAME}: {LICENSE_URL}</copyright>\n'
        f'    <lastBuildDate>{rfc822(newest)}</lastBuildDate>\n'
        + "\n".join(items) + "\n"
        '  </channel>\n'
        '</rss>\n'
    )
    with open(os.path.join(SITE, "feed.xml"), "w", encoding="utf-8") as f:
        f.write(feed)

# ---------- "Page not found" page (Oct 25, 2026) ----------
# GitHub Pages shows 404.html for any address that doesn't exist, at whatever depth the
# missing address was, so every link and asset on it is root-absolute ("/...").
NOT_FOUND_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found — The Reassuring Universe</title>
<meta name="robots" content="noindex">
<!--HEAD_EXTRA--><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="site-header-inner">
    <a class="brand" href="/">The Reassuring Universe
      <span class="brand-sub">Essays by Don Ray</span>
    </a>
    <nav class="primary-nav" aria-label="Primary">
      <a href="/">Home</a>
      <a href="/categories/">Categories</a>
      <a href="/search.html">Search</a>
    </nav>
  </div>
</header>

<main id="main">
  <div class="page-head">
    <h1>Page not found</h1>
    <p class="lede">Sorry — there is no page at this address. The link may be old, or the address may have a typing error. Every essay and poem is still here, and you can find it by searching or by browsing the categories.</p>
    <form class="site-search" action="/search.html" method="get" role="search">
      <input type="search" name="q" placeholder="Search the essays" aria-label="Search the essays">
      <button type="submit" class="btn btn-primary">Search</button>
    </form>
    <p class="search-help">If you followed a link from one of Don Ray’s earlier websites or blogs, the essays now live here, at The Reassuring Universe.</p>
    <p class="not-found-links"><a href="/">Go to the home page</a><span class="sep">·</span><a href="/categories/">Browse all categories</a></p>
  </div>
</main>

<footer class="site-footer">
  <div class="site-footer-inner">
    <!--FOOTER_NOTICE-->
    <nav aria-label="Footer">
      <a href="/categories/">All categories</a>
      <a href="/feed.xml">RSS feed</a>
    </nav>
  </div>
</footer>

</body>
</html>
"""

def generate_not_found_page(m):
    with open(os.path.join(SITE, "404.html"), "w", encoding="utf-8") as f:
        f.write(NOT_FOUND_TMPL.replace("<!--HEAD_EXTRA-->", head_extra()).replace("<!--FOOTER_NOTICE-->", FOOTER_NOTICE))

def main():
    m = load_manifest()
    for slug in m["essays"]:
        generate_essay_page(m, slug)
    for cat_slug in category_order(m):
        generate_category_page(m, cat_slug)
    generate_categories_index(m)
    generate_sitemap(m)
    generate_homepage_recent_strip(m)
    generate_homepage_categories(m)
    generate_search_index(m)
    generate_search_page(m)
    generate_homepage_head(m)
    generate_feed(m)
    generate_not_found_page(m)
    print("Regenerated", len(m["essays"]), "essay pages,", len(m["categories"]), "category pages, categories/index.html, sitemap.xml, the homepage recent strip and categories, search.html and its index, feed.xml and 404.html.")

if __name__ == "__main__":
    main()

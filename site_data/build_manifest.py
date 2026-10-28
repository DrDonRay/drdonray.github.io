#!/usr/bin/env python3
"""
One-time reverse-engineering pass: parse the current website_proto tree and
build manifest.json, the single source of truth for site structure from now
on. After this runs and is verified, manifest.json (not the HTML) is what
gets hand-edited to insert or reorder material; generate_site.py turns it
back into HTML.
"""
import re, json, os, html

SITE = os.environ.get("SITE_ROOT", "/home/claude/website_proto")
CAT_DIR = os.path.join(SITE, "categories")
ESSAY_DIR = os.path.join(SITE, "essays")
OUT = os.path.join(SITE, "site_data", "manifest.json")

CATEGORIES = [
    ("personal-perspective", "Personal Perspective"),
    ("transcendent-conversations-and-vision", "Transcendent Conversations and Vision"),
    ("structure-of-the-purpose-and-destiny-of-life", "Structure of the Purpose and Destiny of Life"),
    ("spiritual-without-religion", "Spiritual, Without Overt Mention of Religion"),
    ("spiritual-with-religion", "Spiritual With Mention of Religion"),
    ("observations-of-human-life", "Observations of Human Life"),
    ("poetry", "Poetry"),
]
CAT_LABEL = dict(CATEGORIES)

ROW_RE = re.compile(
    r'<a class="essay-row" href="\.\./essays/([a-z0-9-]+)\.html">\s*'
    r'<span class="pos">(\d+)</span>\s*'
    r'<span>\s*'
    r'<h3>(.*?)</h3>\s*'
    r'<p class="excerpt">(.*?)</p>\s*'
    r'<span class="tag-list">(.*?)</span>\s*'
    r'</span>\s*</a>',
    re.S,
)

def unescape(s):
    return html.unescape(s).strip()

def strip_quotes(s):
    # remove one layer of wrapping curly/straight quotes, already-unescaped
    s = s.strip()
    if len(s) >= 2 and s[0] in "“\"" and s[-1] in "”\"":
        s = s[1:-1]
    return s

def parse_category_page(slug):
    path = os.path.join(CAT_DIR, f"{slug}.html")
    text = open(path, encoding="utf-8").read()
    lede_m = re.search(r'<p class="lede">(.*?)</p>', text, re.S)
    desc_m = re.search(r'<meta name="description" content="(.*?)">', text, re.S)
    ogdesc_m = re.search(r'<meta property="og:description" content="(.*?)">', text, re.S)
    rows = []
    for m in ROW_RE.finditer(text):
        eslug, pos, h3, excerpt, taglist = m.groups()
        rows.append({"slug": eslug, "title": unescape(h3), "excerpt": strip_quotes(unescape(excerpt))})
    return {
        "lede": unescape(lede_m.group(1)) if lede_m else None,
        "meta_description": unescape(desc_m.group(1)) if desc_m else None,
        "og_description": unescape(ogdesc_m.group(1)) if ogdesc_m else None,
        "rows": rows,
    }

def parse_essay_page(slug):
    path = os.path.join(ESSAY_DIR, f"{slug}.html")
    text = open(path, encoding="utf-8").read()
    title_m = re.search(r'<title>(.*?)\s*—\s*The Reassuring Universe', text, re.S)
    desc_m = re.search(r'<meta name="description" content="(.*?)">', text, re.S)
    ogdesc_m = re.search(r'<meta property="og:description" content="(.*?)">', text, re.S)
    body_m = re.search(r'(<article class="essay-body">.*?</article>)', text, re.S)
    if not body_m:
        raise ValueError(f"No essay-body found in {slug}")
    return {
        "title": unescape(title_m.group(1)) if title_m else None,
        "meta_description": unescape(desc_m.group(1)) if desc_m else None,
        "og_description": unescape(ogdesc_m.group(1)) if ogdesc_m else None,
        "body_html": body_m.group(1),
    }

def main():
    cat_pages = {slug: parse_category_page(slug) for slug, _ in CATEGORIES}

    essays = {}
    for slug, _ in CATEGORIES:
        for i, row in enumerate(cat_pages[slug]["rows"]):
            e = essays.setdefault(row["slug"], {"title": row["title"], "memberships": {}})
            e["memberships"][slug] = {"rank": (i + 1) * 10, "excerpt": row["excerpt"]}

    # enrich with each essay's own page data (title/meta/og/body) -- body_html
    # is kept OUT of manifest.json (too large, and it's the verbatim essay
    # text) and instead left in place in essays/*.html; the generator will
    # re-extract it directly from the existing file at generation time.
    missing_pages = []
    for slug, e in essays.items():
        path = os.path.join(ESSAY_DIR, f"{slug}.html")
        if not os.path.exists(path):
            missing_pages.append(slug)
            continue
        page = parse_essay_page(slug)
        e["title"] = page["title"] or e["title"]
        e["meta_description"] = page["meta_description"]
        e["og_description"] = page["og_description"]

    manifest = {
        "categories": {
            slug: {
                "label": CAT_LABEL[slug],
                "lede": cat_pages[slug]["lede"],
                "meta_description": cat_pages[slug]["meta_description"],
                "og_description": cat_pages[slug]["og_description"],
            }
            for slug, _ in CATEGORIES
        },
        "category_order": [s for s, _ in CATEGORIES],
        "homepage_recent": ["breeze-of-mystery", "no-time-for-grief", "freedom-from-opportunity"],
        "essays": essays,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False, sort_keys=True)

    print("Wrote", OUT)
    print("Total unique essays:", len(essays))
    print("Per-category counts:", {slug: len(cat_pages[slug]["rows"]) for slug, _ in CATEGORIES})
    print("Missing essay pages (row exists on a category page, no essays/*.html found):", missing_pages)

if __name__ == "__main__":
    main()

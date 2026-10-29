#!/usr/bin/env python3
"""
Standalone invariant checker for website_proto. Run after every regeneration
(or any hand edit) to catch the class of bug that's shown up repeatedly in
this project's history: stale numbers, orphaned pending-category markers,
broken nav chains, mismatched counts. Exits non-zero and prints every
failure if anything is wrong; prints a clean summary if not.
"""
import re, os, sys, json

SITE = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("SITE_ROOT", "/home/claude/website_proto")
CAT_DIR = os.path.join(SITE, "categories")
ESSAY_DIR = os.path.join(SITE, "essays")
MANIFEST = os.path.join(SITE, "site_data", "manifest.json")

with open(MANIFEST, encoding="utf-8") as _f:
    _M = json.load(_f)
CATS = _M["category_order"]  # canonical order; slugs match the category names since Oct 29, 2026

errors = []
warnings = []

def err(msg):
    errors.append(msg)

def warn(msg):
    warnings.append(msg)

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

# ---- gather ground truth from the category pages themselves ----
cat_rows = {}          # cat -> [(slug, pos, title)]
essay_membership = {}  # slug -> {cat: pos}
for cat in CATS:
    text = read(os.path.join(CAT_DIR, f"{cat}.html"))
    rows = re.findall(
        r'<a class="essay-row" href="\.\./essays/([a-z0-9-]+)\.html">\s*<span class="pos">(\d+)</span>',
        text)
    cat_rows[cat] = rows
    seen_pos = set()
    for slug, pos in rows:
        pos = int(pos)
        essay_membership.setdefault(slug, {})[cat] = pos
        if pos in seen_pos:
            err(f"[{cat}.html] duplicate position {pos}")
        seen_pos.add(pos)
    expected = set(range(1, len(rows) + 1))
    if seen_pos != expected:
        err(f"[{cat}.html] positions not a clean 1..N sequence: have {sorted(seen_pos)}")

# ---- categories/index.html card counts match actual row counts ----
idx_text = read(os.path.join(CAT_DIR, "index.html"))
card_counts = dict(re.findall(r'href="([a-z0-9-]+)\.html" id="[a-z0-9-]+">.*?<span class="count">(\d+)', idx_text, re.S))
pending = re.findall(r'status-pill pending', idx_text)
if pending:
    warn(f"categories/index.html still has {len(pending)} 'pending' pill(s)")
for cat in CATS:
    actual = len(cat_rows[cat])
    card = int(card_counts.get(cat, -1))
    if card != actual:
        err(f"categories/index.html card for {cat} says {card}, actual row count is {actual}")

# ---- per-essay checks ----
all_essay_files = sorted(f[:-5] for f in os.listdir(ESSAY_DIR) if f.endswith(".html"))
for slug in all_essay_files:
    path = os.path.join(ESSAY_DIR, f"{slug}.html")
    text = read(path)
    memberships = essay_membership.get(slug, {})
    n_cats = len(memberships)

    if n_cats == 0:
        err(f"{slug}.html: not listed on any category page")
        continue

    # eyebrow numbers
    eyebrow_m = re.search(r'<span class="eyebrow">(.*?)</span>', text, re.S)
    eyebrow = eyebrow_m.group(1) if eyebrow_m else ""
    for cat in memberships:
        expected_total = len(cat_rows[cat])
        expected_pos = memberships[cat]
        needle = f"No. {expected_pos} of {expected_total}"
        if needle not in eyebrow:
            err(f"{slug}.html: eyebrow missing/incorrect '{needle}' for category {cat} — eyebrow is: {eyebrow!r}")

    # breadcrumb drop rule
    crumb_m = re.search(r'<p class="breadcrumbs">(.*?)</p>', text, re.S)
    n_crumb_links = len(re.findall(r"<a href=", crumb_m.group(1))) if crumb_m else 0
    has_crumb_cat = n_crumb_links >= 3  # Home, Categories, + this essay's own category
    if n_cats == 1 and not has_crumb_cat:
        err(f"{slug}.html: single-category essay but breadcrumb doesn't show its category")
    if n_cats >= 2 and has_crumb_cat:
        err(f"{slug}.html: multi-category essay but breadcrumb still shows a category segment")

    # also-in / "filed only under" block
    has_also_in = "also-in" in text
    if n_cats == 1 and not has_also_in:
        err(f"{slug}.html: single-category essay missing 'Filed only under' block")
    if n_cats >= 2 and has_also_in:
        err(f"{slug}.html: multi-category essay has a leftover 'also-in' block (should have none once all categories are live)")

    # no stale not-yet-live anchors
    if "not yet live" in text or re.search(r'href="(\.\./)?categories/index\.html#', text) or 'href="index.html#' in text:
        err(f"{slug}.html: contains a stale/pending category reference")

    # continue-groups present for exactly n_cats categories, each with a nav-cell pair
    n_groups = len(re.findall(r'continue-group essay-nav', text))
    if n_groups != n_cats:
        err(f"{slug}.html: has {n_groups} continue-groups but is filed under {n_cats} categories")

    # back-to-category link count matches n_cats
    n_back = len(re.findall(r'back-to-category">.*', text))
    back_m = re.search(r'<p class="back-to-category">(.*?)</p>', text, re.S)
    if back_m:
        n_back_links = len(re.findall(r"<a href=", back_m.group(1)))
        if n_back_links != n_cats:
            err(f"{slug}.html: back-to-category has {n_back_links} links but is filed under {n_cats} categories")
    else:
        err(f"{slug}.html: no back-to-category paragraph found")

# ---- nav chain reciprocity: for each category, walk sorted positions and
# confirm each essay's prev/next hrefs in that category's continue-group
# match its actual neighbors ----
for cat in CATS:
    rows = sorted(((int(p), s) for s, p in cat_rows[cat]), key=lambda t: t[0])
    slugs_in_order = [s for _, s in rows]
    for i, slug in enumerate(slugs_in_order):
        text = read(os.path.join(ESSAY_DIR, f"{slug}.html"))
        # isolate this essay's continue-group for `cat`
        label_pat = re.compile(
            r'<div class="continue-label">Continue in [^<]*</div>\s*'
            r'<div class="continue-group essay-nav">(.*?)</div>', re.S)
        groups = label_pat.findall(text)
        # find the group whose links point at this category's neighbors (match by expected neighbor slugs)
        expected_prev = slugs_in_order[i - 1] if i > 0 else None
        expected_next = slugs_in_order[i + 1] if i < len(slugs_in_order) - 1 else None
        match_found = False
        for g in groups:
            prev_href = re.search(r'nav-cell"\s+href="([a-z0-9-]+)\.html"', g)
            next_href = re.search(r'nav-cell next" href="([a-z0-9-]+)\.html"', g)
            prev_disabled = 'nav-cell disabled' in g.split('</a>')[0] if '</a>' in g else 'disabled' in g
            got_prev = prev_href.group(1) if prev_href else None
            got_next = next_href.group(1) if next_href else None
            if got_prev == expected_prev and got_next == expected_next:
                match_found = True
                break
            if expected_prev is None and got_prev is None and got_next == expected_next:
                match_found = True
                break
            if expected_next is None and got_next is None and got_prev == expected_prev:
                match_found = True
                break
        if not match_found:
            err(f"{slug}.html: no continue-group matches expected {cat} neighbors (prev={expected_prev}, next={expected_next})")

# ---- sitemap check ----
sitemap = read(os.path.join(SITE, "sitemap.xml"))
sitemap_urls = set(re.findall(r"<loc>([^<]+)</loc>", sitemap))
expected_urls = {"https://drdonray.github.io/", "https://drdonray.github.io/categories/"}  # canonical address of categories/index.html
for cat in CATS:
    expected_urls.add(f"https://drdonray.github.io/categories/{cat}.html")
for slug in all_essay_files:
    expected_urls.add(f"https://drdonray.github.io/essays/{slug}.html")
missing = expected_urls - sitemap_urls
extra = sitemap_urls - expected_urls
if missing:
    err(f"sitemap.xml missing {len(missing)} URL(s): {sorted(missing)[:5]}")
if extra:
    err(f"sitemap.xml has {len(extra)} unexpected URL(s): {sorted(extra)[:5]}")

# ---- RSS feed, 404 page, Google verification file (Oct 25, 2026) ----
import xml.etree.ElementTree as ET
try:
    feed = ET.parse(os.path.join(SITE, "feed.xml")).getroot()
    feed_links = [i.findtext("link") for i in feed.iter("item")]
    want = {f"https://drdonray.github.io/essays/{s}.html" for s in all_essay_files}
    if len(feed_links) != len(set(feed_links)):
        err("feed.xml lists an essay more than once")
    if set(feed_links) != want:
        err(f"feed.xml items don't match the essay pages ({len(set(feed_links) - want)} extra, {len(want - set(feed_links))} missing)")
except (OSError, ET.ParseError) as ex:
    err(f"feed.xml missing or not well-formed XML: {ex}")
nf = os.path.join(SITE, "404.html")
if not os.path.exists(nf):
    err("404.html is missing")
elif re.search(r'(href|src|action)="(?!/|https?:|#)', read(nf)):
    err("404.html has a relative link; GitHub Pages serves it at any depth, so links must start with /")
GOOGLE_FILE = "googled8b37a9a18da5204.html"
gpath = os.path.join(SITE, GOOGLE_FILE)
if not os.path.exists(gpath) or read(gpath).strip() != f"google-site-verification: {GOOGLE_FILE}":
    err(f"{GOOGLE_FILE} (Google Search Console ownership file) is missing or altered; keep it at the site root")

# ---- sharing notice on every page (Oct 25, 2026) ----
import glob
for page in [os.path.join(SITE, "index.html"), os.path.join(SITE, "search.html"), os.path.join(SITE, "404.html")] + \
            glob.glob(os.path.join(CAT_DIR, "*.html")) + glob.glob(os.path.join(ESSAY_DIR, "*.html")):
    t = read(page) if os.path.exists(page) else ""
    if "redirect-stub" in t:
        continue
    if t.count('rel="license"') != 2:
        err(f"{os.path.relpath(page, SITE)}: missing the license link in <head> or the sharing notice in the footer")

# ---- redirects from former category addresses (Oct 29, 2026) ----
cat_files = {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(CAT_DIR, "*.html"))}
expected_stubs = {}
for slug, cat in _M["categories"].items():
    for old in cat.get("former_slugs", []):
        expected_stubs[old] = slug
for old, new in expected_stubs.items():
    p = os.path.join(CAT_DIR, f"{old}.html")
    t = read(p) if os.path.exists(p) else ""
    if "redirect-stub" not in t or f'url={new}.html"' not in t or f'href="https://drdonray.github.io/categories/{new}.html"' not in t:
        err(f"categories/{old}.html should be a redirect to {new}.html")
stray = cat_files - set(CATS) - set(expected_stubs) - {"index"}
if stray:
    err(f"unexpected page(s) in categories/: {sorted(stray)}")
for page in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True):
    if "/.git/" in page or "redirect-stub" in read(page):
        continue
    for old in expected_stubs:
        if f"categories/{old}.html" in read(page):
            err(f"{os.path.relpath(page, SITE)} still links to the former address categories/{old}.html")
            break

# ---- report ----
print(f"Checked {len(all_essay_files)} essay pages, {len(CATS)} category pages.")
if warnings:
    print(f"\n{len(warnings)} warning(s):")
    for w in warnings:
        print(" -", w)
if errors:
    print(f"\n{len(errors)} FAILURE(S):")
    for e in errors:
        print(" -", e)
    sys.exit(1)
else:
    print("\nAll invariants pass: clean.")

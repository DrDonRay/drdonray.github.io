import re, json, os

# Override with SITE_ROOT env var to run the toolchain against a scratch
# copy (e.g. to preview a change before it's applied to the real site).
SITE = os.environ.get("SITE_ROOT", "/home/claude/website_proto")
MANIFEST_PATH = os.path.join(SITE, "site_data", "manifest.json")

def load_manifest():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        return json.load(f)

def save_manifest(m):
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(m, f, indent=2, ensure_ascii=False)  # keep the manifest's own key order
        f.write("\n")

def category_order(manifest):
    return manifest["category_order"]

def label(manifest, cat_slug):
    return manifest["categories"][cat_slug]["label"]

def ordered_memberships(manifest, slug):
    """Return this essay's memberships as (cat_slug, rank) tuples, in
    canonical site-wide category order (not rank order)."""
    e = manifest["essays"][slug]
    return [(c, e["memberships"][c]["rank"]) for c in category_order(manifest) if c in e["memberships"]]

def category_members_sorted(manifest, cat_slug):
    """All essay slugs in a category, sorted by rank, as (slug, rank)."""
    items = []
    for slug, e in manifest["essays"].items():
        if cat_slug in e["memberships"]:
            items.append((slug, e["memberships"][cat_slug]["rank"]))
    items.sort(key=lambda t: t[1])
    return items

def position_and_count(manifest, cat_slug, slug):
    members = category_members_sorted(manifest, cat_slug)
    slugs = [s for s, r in members]
    pos = slugs.index(slug) + 1
    return pos, len(slugs)

def neighbors(manifest, cat_slug, slug):
    """Return (prev_slug_or_None, next_slug_or_None) within a category."""
    members = category_members_sorted(manifest, cat_slug)
    slugs = [s for s, r in members]
    i = slugs.index(slug)
    prev_slug = slugs[i - 1] if i > 0 else None
    next_slug = slugs[i + 1] if i < len(slugs) - 1 else None
    return prev_slug, next_slug

HEAD_ESSAY_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — The Reassuring Universe</title>
<meta name="description" content="{meta_description}">
<link rel="canonical" href="https://drdonray.github.io/essays/{slug}.html">
<meta property="og:type" content="article">
<meta property="og:title" content="{title} — The Reassuring Universe">
<meta property="og:description" content="{og_description}">
<meta property="og:url" content="https://drdonray.github.io/essays/{slug}.html">
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
      <a href="../categories/index.html">Categories</a>
      <a href="../search.html">Search</a>
    </nav>
  </div>
</header>

<p class="breadcrumbs">
{breadcrumb}
</p>

<main id="main">
  <div class="essay-head">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>{also_in}
  </div>

{body}

  <nav class="continue-reading" aria-label="Essay navigation">
{continue_groups}  </nav>

  <p class="back-to-category">{back_links}</p>
</main>

<footer class="site-footer">
  <div class="site-footer-inner">
    {footer_notice}
    <nav aria-label="Footer">
      <a href="../index.html">Home</a>
      <a href="../categories/index.html">All categories</a>
      <a href="../feed.xml">RSS feed</a>
    </nav>
  </div>
</footer>

</body>
</html>
"""

HEAD_CATEGORY_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{label} — The Reassuring Universe</title>
<meta name="description" content="{meta_description}">
<link rel="canonical" href="https://drdonray.github.io/categories/{slug}.html">
<meta property="og:type" content="website">
<meta property="og:title" content="{label} — The Reassuring Universe">
<meta property="og:description" content="{og_description}">
<meta property="og:url" content="https://drdonray.github.io/categories/{slug}.html">
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
  <a href="../index.html">Home</a><span class="sep">/</span>
  <a href="index.html">Categories</a><span class="sep">/</span>
  <span class="current">{label}</span>
</p>

<main id="main">
  <div class="page-head">
    <h1>{label}</h1>
    <p class="lede">{lede}</p>
  </div>

  <div class="essay-list">

{rows}  </div>
</main>

<footer class="site-footer">
  <div class="site-footer-inner">
    {footer_notice}
    <nav aria-label="Footer">
      <a href="../index.html">Home</a>
      <a href="index.html">All categories</a>
      <a href="../feed.xml">RSS feed</a>
    </nav>
  </div>
</footer>

</body>
</html>
"""

# ---------- Shared <head> additions (Oct 25, 2026) ----------
# RSS discovery link, site name, and the share (preview) image used when a page
# is posted to social media or a messaging app. The image tags are only written
# when assets/share-image.jpg exists, so a missing image never yields a broken preview.
SITE_URL = "https://drdonray.github.io"
SHARE_IMAGE = "assets/share-image.jpg"
SHARE_IMAGE_ALT = "The diamond ring of a total solar eclipse: the last bead of sunlight shining at the edge of the Moon."

def head_extra():
    lines = [
        f'<link rel="alternate" type="application/rss+xml" title="The Reassuring Universe" href="{SITE_URL}/feed.xml">',
        '<meta property="og:site_name" content="The Reassuring Universe">',
        f'<link rel="license" href="{LICENSE_URL}">',
    ]
    if os.path.exists(os.path.join(SITE, SHARE_IMAGE)):
        lines += [
            f'<meta property="og:image" content="{SITE_URL}/{SHARE_IMAGE}">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            f'<meta property="og:image:alt" content="{SHARE_IMAGE_ALT}">',
            '<meta name="twitter:card" content="summary_large_image">',
        ]
    return "\n".join(lines) + "\n"

# ---------- Copyright and sharing notice (Oct 25, 2026, at the author's request) ----------
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (author's choice, Oct 25, 2026,
# replacing BY-NC-ND the same day so that translations are allowed): anyone may copy, share,
# translate or adapt the essays, with credit, not for profit, and changed versions must
# carry the same license. Shown in every page's footer, declared
# in every page's <head> (rel="license"), and in feed.xml (<copyright>).
LICENSE_URL = "https://creativecommons.org/licenses/by-nc-sa/4.0/"
LICENSE_NAME = "CC BY-NC-SA 4.0"
FOOTER_NOTICE = ('<span class="footer-notice">© Don Ray. You may copy, share and translate these essays '
                 'and poems, with credit to Don Ray, not for profit, and on these same terms '
                 f'(<a href="{LICENSE_URL}" rel="license">{LICENSE_NAME}</a>).</span>')

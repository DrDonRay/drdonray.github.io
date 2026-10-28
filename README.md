# The Reassuring Universe — website prototype

A static, multi-page site for **https://drdonray.github.io**, built to replace donray.weebly.com. Plain HTML/CSS, no build step, no JavaScript — every page can be opened directly or served as-is from GitHub Pages.

## How to view it

Unzip the whole folder first (don't open `index.html` from inside the zip — the CSS and internal links live in sibling folders and won't resolve from a virtual zip view). Then open `index.html` from the extracted folder in any browser.

## Status: 7 of 7 categories live

- **Personal Perspective** (6 essays) — live
- **Transcendence** (12 essays) — live
- **Foundation – Purpose – Meaning – Destiny** (34 essays) — live
- **The Nameless Spiritual** (48 essays) — live
- **Naming the Spiritual** (66 essays) — live
- **Seeing Life** (47 essays) — live
- **Poetry** (21 poems) — live

(Category names as of Oct 19, 2026. The page URLs keep the original slugs, for example `categories/spiritual-without-religion.html`, so existing links keep working.)

**All seven categories are now built.** Poetry was intentionally built last, once its compilation was finalized through the separate essay-editing pipeline (Uploaded material → Editing proposals → author review → Finalized material), so it wouldn't need to be rebuilt mid-stream. With Poetry live, every category on the site's plan now has a page.

## Update of October 25, 2026 (later): sharing notice

At the author's request, every page's footer now reads: "© Don Ray. You may copy, share and translate these essays and poems, with credit to Don Ray, not for profit, and on these same terms (CC BY-NC-SA 4.0)." The last part links to the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 license, https://creativecommons.org/licenses/by-nc-sa/4.0/, which gives the full terms. Every page's `<head>` also declares it (`<link rel="license">`), and `feed.xml` carries it as `<copyright>`.

The author first chose CC BY-NC-ND 4.0 (copies only, unchanged) and switched the same day, before uploading, to BY-NC-SA so that translations are allowed. No Creative Commons license allows translations alone: BY-NC-SA allows any adaptation (translation, excerpt, edit), provided it credits the author, says that changes were made, is not for profit, and is shared under the same license. The author keeps his copyright and remains free to publish the essays himself, including the KDP books. The notice text lives in one place, `FOOTER_NOTICE` in `site_data/common.py`; the homepage footer is filled in between the `footer-notice` markers. The validator checks every page for it.

## Update of October 25, 2026: RSS feed, "page not found" page, share image, Google file

Requested by the author on Oct 25, 2026, after the site went live on GitHub Pages.

- **RSS feed.** `feed.xml` lists every essay and poem: title, link, categories and the page's short description. People who use a feed reader can subscribe and see new essays as they are added. Each page's `<head>` has a hidden link to the feed, and the footer of every page now has an "RSS feed" link. The feed's dates come from the manifest: `site_launched` (2026-10-21, approximate) for everything already on the site, or `essays[slug].added` (YYYY-MM-DD), which should be set for each new essay so readers see it as new.
- **"Page not found" page.** `404.html` is what GitHub Pages shows for any address that doesn't exist, for example a mistyped link or an old address. It has a short apology, a search box, links to the home page and the categories, and a note for visitors arriving from the author's earlier websites and blogs. It carries `noindex` and is not in the sitemap. Because GitHub can show it at any depth of address, all its links start with `/`.
- **Share (preview) image.** The generator adds `og:image` and `twitter:card` tags to every page once `assets/share-image.jpg` exists; until then it adds none, so a missing picture can never produce a broken preview. The author chose a photograph of the "diamond ring" of a total solar eclipse, as a sign that more light is on the way. `site_data/make_share_image.py PHOTO` crops a photo to the 1200 × 630 shape link previews use. The author supplied the photo on Oct 25 (1280 × 719, no credit embedded in the file); it was cropped to `assets/share-image.jpg` (1200 × 630). Source, confirmed by the author: NASA (assets.science.nasa.gov). NASA imagery is generally not copyrighted; NASA asks that it be credited to NASA and not used to suggest NASA endorsement.
- **Google Search Console file.** `googled8b37a9a18da5204.html` proves the author's ownership of the site to Google Search Console and must stay at the site root. The validator now fails if it is missing or altered.
- **Hidden additions:** `og:site_name` on every page.
- **Sitemap:** the Categories page is now listed under its canonical address, `https://drdonray.github.io/categories/`, matching the page's own canonical tag (it was listed as `categories/index.html`).
- **Footer spacing:** the footer links now have a small gap between them (before, "Home" and "All categories" ran together).
- **Validator:** also checks that `feed.xml` is well-formed and lists every essay exactly once, that `404.html` exists and uses only `/`-rooted links, and the Google file. It now also accepts `SITE_ROOT`, like the generator.
- **Toolchain:** `save_manifest` no longer re-sorts the manifest's keys, so a scripted change shows only the lines it really changed.

## Update of October 20, 2026 (later): category card order

At the author's request, the homepage category cards now read, left to right: Seeing Life, Foundation – Purpose – Meaning – Destiny, The Nameless Spiritual, Naming the Spiritual, Transcendence, Poetry, Personal Perspective. At the author's request, the Categories page (`categories/index.html`) now uses the same order. Both pages take it from `CATEGORY_CARD_ORDER` in `generate_site.py`. The canonical category order used in essay headers and navigation is unchanged.

## Update of October 20, 2026: new category descriptions

The author supplied new descriptions in "Category header_ descriptions" (Google Drive). Each replaces the whole description under the category title on its category page:

- The Nameless Spiritual: "An essay journey launched in ordinary moments, carried by tides and winds of life’s storms, finally landing in the Light of Mystery."
- Naming the Spiritual: "Unorthodox perspectives of realistic faith."
- Seeing Life: "Harshness, beauty, despair, Hope."
- Poetry: "…or unorthodox attempts at poetry."
- Transcendence: "Futile attempts to capture the ineffable."

Foundation – Purpose – Meaning – Destiny and Personal Perspective keep their descriptions. At the author's request, every description now ends with a period, so three lines gained one: Seeing Life, Poetry and Transcendence.

The one-line descriptions on the homepage and Categories-page cards now match the new descriptions for the same five categories. For Transcendence, this replaces "Seeing beyond the ordinary." Foundation and Personal Perspective keep their card lines. The card lines have moved from `CATEGORY_BLURBS` in `generate_site.py` into the manifest, as `categories[slug].blurb`. The hidden search-engine and social-preview descriptions (`meta_description`, `og_description`) of the same five categories were rewritten and approved by the author the same day. Each one says plainly what the page holds, ends in the author's own wording, and stays within about 150–160 characters.

## Update of October 19, 2026: category names, homepage, search, footer

Requested by the author in "Website changes 19 Oct 2026" (Google Drive).

- **Category names.** The display names changed as follows. The page addresses (slugs) are unchanged, so links and bookmarks keep working.

  | Old name | New name |
  | --- | --- |
  | Spiritual, Without Overt Mention of Religion | The Nameless Spiritual |
  | Transcendent Conversations and Vision | Transcendence |
  | Structure of the Purpose and Destiny of Life | Foundation – Purpose – Meaning – Destiny (en dashes since Oct 19; first typed with hyphens) |
  | Observations of Human Life | Seeing Life |
  | Spiritual With Mention of Religion | Naming the Spiritual |

  Transcendence's one-line description (shown on the homepage and the Categories page) is now "Seeing beyond the ordinary." Every other description and lede is unchanged.
- **Dashes in the Foundation name** (author's choice, Oct 19): the name uses en dashes, with a no-break space before each one so a dash never starts a line.
- **Drive file headers:** the new names are now also the names used in the `CATEGORIES:` header of Drive files. Older files may still carry the former descriptive names, which are recorded in the manifest as `categories[slug].former_header_names`.
- **Arc headings renamed:**
  - The Nameless Spiritual: Presence in Light and Nature; Fear, suffering, and charades; Hardship, madness, and growth; Harshness and storms, creation and birth.
  - Seeing Life: Common Madness.
  - Naming the Spiritual: Defiant faith; Reality's Lessons; From the Garden to Home; Love Out of Madness; In Search of the Authentic.
  - Poetry: Liminal touch.
- **Homepage.** The seven categories now appear directly under the introduction as cards, each with its description and essay count. The cards are generated from the manifest, between the `home-categories` markers in `index.html`. "Recently added" now comes below the categories. Removed: the "Browse by category" and "See recent essays" buttons, and the old "Design proposal / prototype" note, which still listed the former category names. A search box sits where the buttons were.
- **Search.** Added `search.html` plus "Search" in every page's header. The search runs entirely in the reader's browser, so no server is needed.
  - The generator writes `assets/search-index.js`, which holds every page's title, categories and plain text. `assets/search.js` is the hand-written search code.
  - A result must contain every word of the query, or each "quoted phrase".
  - Matching ignores case, accents, and curly versus straight quotes. A word also matches longer words that begin with it, so "faith" finds "faithful".
  - Rarer words count for more. Pieces that contain the whole query as a phrase, or match in the title, rank first.
  - Each result shows a short passage with the matches highlighted.
  - The search page carries `noindex`, and it is deliberately left out of `sitemap.xml`.
- **Footer.** "Essays reproduced with the author's permission" was removed from every page, so the footer now reads "© Don Ray".
- **Conversation with an Angel.** The doubled word "appearing appearing" was removed, matching the author's corrected Drive final, and the listing excerpt is the full sentence again.

## Update of October 18, 2026: second-pass text, new ordering, arc headings

**Essay text rebuilt from the second editing pass.** Every essay page outside Poetry (109 pages) was checked word for word against the author's resolved 2nd-pass final in the Drive folder "2nd pass finalized material"; 98 pages changed and 11 were already identical. The 21 Poetry pages were not part of the second pass and are unchanged. How the text was carried over:

- Only words change. Each page's existing markup (paragraphs, line breaks, `.poem` blocks, `<em>`) is kept, and the changed words are placed into it. A script then confirmed that every rebuilt page reads word for word like its final.
- Where a page and its final differ only in a quote or dash glyph, the typographic form is kept, whichever side has it (curly quotes, en and em dashes). Literal Markdown asterisks in the finals (`*The Room Where It Happened*`, `***sex***`, the bullets in Three Principles) are not shown; the page's existing italics and list carry that emphasis.
- Titles the finals no longer repeat as the first line of the body were removed from the body as well: Digitally Fractured Beliefs, For the Children, Impact of Refugees, Inevitable War?, Judgement Daze, Many Truths, Material Separation, Reality Gap, Terlingua, Trust Your Robot. (This supersedes the build notes below that list these as preserved artifacts.)
- Paragraph changes the author made in the second pass were applied: Digital Disruption (now 8 paragraphs) and Oblivious to the Obvious (now 3); Shock Prayer (each "Don't let us…" line on its own); Do Not Cling to the Light (two lines joined); Temporally Senseless (a mid-sentence break removed). Elsewhere, single line breaks in a final that were already present in the first-pass source keep the paragraphing the page already had.
- Deer and Coyotes was substantially revised by the author ("Updated final version by author"), so its body was rebuilt from that final paragraph by paragraph. The two artifacts noted under Content fidelity below (a mid-sentence line break and a stray leading period) are gone because the author's revision removed them.
- Six listing excerpts were updated to match the new wording: Childish Questions, Conversation with an Angel (both categories), Destructive Gentleness, Intention of Attention, The Fledging of Downy Woodpeckers, and Deer and Coyotes ("gambolling" in the excerpt corrected to the essay's own "gamboling").

**New order within every category.** The author approved a fresh, unconstrained ordering of all seven categories on Oct 18, 2026, with Poetry woven into the other categories by meaning, and six rewritten category ledes (Personal Perspective's lede is unchanged). `site_data/manifest.json` is now the authoritative ordering record for the website and the books; the Drive "Ordering Tracker" files are retired.

**Arc headings.** Each category's order is grouped into named arcs ("Glimpses in Nature", "The shape of a life", …). They are stored in the manifest as `categories[slug].arcs`, a list of `{"label", "starts_at": essay slug}`, and shown as small headings on each category page. Numbering still runs 1 to N through the whole category. Because an arc is anchored to its first essay, a new essay inserted mid-arc joins that arc automatically. The author noted that the arcs can also serve as chapter headings in the books. Ordering rationale from the approved review is kept beside the order: `categories[slug].ordering_notes` (cluster-level) and `memberships[cat].note` (for individual placements).

**Fixed: tag pills on category pages.** Each listing row is a link, and the category tags inside it were links too. A link inside a link is invalid HTML, so browsers split every multi-category row, and its tags spilled out below the card as full-width bars. The tags are now plain labels inside the card, as the design intended. The essay pages' own category links are unchanged.

## Adding or reordering material (manifest-driven build)

Through the Poetry launch, every category's HTML was hand-patched directly — new rows spliced into a category page with a script written for that one build, position numbers renumbered with a regex, nav links relinked by hand. It worked, but every one of those launches produced at least one bug that had to be caught and fixed afterward (a stale "not yet live" link left behind, a capitalization mismatch, an empty leftover block) — not because of carelessness, but because hand-patching HTML has no way to guarantee consistency across ~150 interlinked files.

As of this build, the site is generated from a single source of truth instead: **`site_data/manifest.json`**. It lists every essay, which categories it belongs to, and its position in each (as an integer "rank" with gaps of 10 between existing items — 10, 20, 30… — so a new item can slot in at, say, 15 without touching anyone else's rank). Two scripts turn that file into the actual site:

- **`site_data/generate_site.py`** rebuilds every page from the manifest: category listings, eyebrow position numbers, breadcrumbs, the "Continue reading" prev/next chains, back-to-category links, `categories/index.html`, `sitemap.xml`, and the homepage's "Recently added" strip. An essay's own body text is never touched by this — it's extracted verbatim from the existing page and spliced back in unchanged, every time.
- **`site_data/validate_site.py`** checks the result against the rules that matter (position numbers match actual order, nav links point at real neighbors and are reciprocal, no stale pending-category markers, category counts agree everywhere, sitemap is complete) and fails loudly, with specifics, if anything's off. It was tested by deliberately breaking a position number, a nav link, and by planting a stale anchor — it caught all three.

**To add a new essay** (single- or multi-category): give it a `slug`, `title`, `meta_description`, `og_description`, and a `memberships` entry per category with a rank number that falls where it belongs (between two existing ranks, or above/below all of them) and its excerpt text for that category's listing. Create its `essays/{slug}.html` page (head/breadcrumb/eyebrow/nav can be left as placeholders — the generator overwrites all of that; only the `<article class="essay-body">…</article>` block needs to be right, since that's the one thing it preserves rather than generates). Then run the generator and the validator.

**To reorder or re-categorize existing material** — the thing that used to be the risky part — edit the rank number(s) in its manifest entry (or add/remove a `memberships` entry to move it into or out of a category) and run the generator. Every position number and nav link affected by the move is recomputed from scratch, correctly, every time; there's nothing to hand-patch and nothing to forget. Moving a poem to a genuinely different position in a category with N items touches on the order of N files (every essay whose displayed position shifted), but it's one command and one validation pass, not a manual find-and-replace — the same operation whether it touches 2 files or 50.

**To preview a change before committing to it**, run both scripts against a scratch copy first by setting `SITE_ROOT` to that copy's path (`SITE_ROOT=/path/to/copy python3 site_data/generate_site.py`), so nothing touches the real site until you're ready. This was used to test the reorder workflow itself before writing these instructions.

The site folder is now a git repository (it wasn't before). Every regeneration should be reviewed with `git diff` before being treated as final — a clean, explicable diff (or none at all) is the actual proof that a change did only what was intended, the same way it was used to verify this refactor introduced zero content drift (see the commit history).

**What this doesn't automate, on purpose**: the prose in each category's lede paragraph and meta description sometimes states its essay count in words ("Twenty-one poems…") — that's hand-written text, not mechanically regenerated, since rewriting natural-language prose safely isn't a mechanical operation. If a category's count changes, check its lede/description by hand; the validator doesn't currently check this specific case, since anything it could infer well enough to fix automatically, it would fix rather than merely flag.

### Structure of the Purpose and Destiny of Life — build notes

The Ordering Tracker's source table for this category lists 34 rows, but row 1, "INTRODUCTION TO PURPOSE OF LIFE," carries an explicit author instruction in its own Drive source: *"CLAUDE: USE THIS AS INTRODUCTION AT BEGINNING OF THE 'STRUCTURE OF THE PURPOSE AND DESTINY OF LIFE' SECTION OF WEBSITE AND OF BOOKS IN THAT CATEGORY"* — i.e., it's the category page's lede paragraph, not essay No. 1. The category page uses it that way, and the remaining 33 rows are numbered 1–33. Nine of those 33 essays already existed as pages from Personal Perspective and/or Transcendent Conversations and Vision (At the ranch, Deer and coyotes, Frantic, Hillside, Seeing Through Our Dreams and Scars, Fledging, Faith Madness, Currency of the Soul, Storm of Creation) and gained an additional `.continue-group`, an additional breadcrumb-dropping trigger, and an additional `.back-to-category` link rather than a new page. Hillside and Fledging are now in three live categories at once; Storm of Creation, Currency of the Soul, and the other six are in two.

### Spiritual, Without Overt Mention of Religion — build notes

This category's Ordering Tracker table has a clean 40 rows (no lede-only entry to exclude, unlike Structure). Of the 40, 20 already existed as pages from Personal Perspective, Transcendent Conversations and Vision, and/or Structure of the Purpose and Destiny of Life, and gained another `.continue-group`, tag update, and `.back-to-category` link rather than a new page. Hillside and Fledging are now each in **four** live categories at once — the first essays to reach that count. Nine essays (At the ranch, Deer and coyotes, Frantic, Seeing Through Our Dreams and Scars, Faith Madness, Currency of the Soul, Storm of Creation, plus Hillside and Fledging) moved from two or three live categories to three or four; eleven single-category Structure essays (Overlapping Projections of Gods, The Scrum of Perfection, Three Principles, Small World, Beauty in the Madness, Did We Love?, Would We Miss Death, Stream of Consciousness, Impossible Yearning, Bridges of Sound and Light, Forgiving God) went from one live category to two, which also triggered the breadcrumb-dropping rule for them for the first time.

### Spiritual With Mention of Religion — build notes

This is the largest category launched so far: a clean 61 rows (no lede-only entry to exclude), of which 19 were new pages and **42** already existed as pages from one or more of the four other live categories — by far the largest retrofit batch to date (more than double the next-largest, the 20-essay Spiritual/without launch). Hillside and Fledging now each carry **five** `.continue-group` blocks, the first essays to reach that count. Twenty-three essays that had been single-live-category through the Spiritual/without launch (Silken Tide, Worship, Stop for a Moment, Save the World a Little Later, Alternative Path Home, Flightless Souls on Walkabout, Recognizing Beauty, Apprenticed to God, Conversation with an angel, Our Ancient Birth, Knowledge of Good and Evil, The Bass Voice of God, Crumbling Temples Crumbling Lessons, The Death of Personal Growth, Successful Disaster, Life Adrift or Navigating Life, Heart Blindness, Inexorable Life, More Than Meat, Terrifying Passage from the Garden to the Kin'dom, Pachinko Minds, Unlocked Door of our Solitary Confinement, That Person Next to You) moved to two live categories, triggering the breadcrumb-dropping rule for them for the first time; the remaining nineteen moved from two, three, or four live categories to one more. The category naming is deliberately asymmetric from its sibling: "Spiritual With Mention of Religion" (no comma), distinct from "Spiritual, Without Overt Mention of Religion."

### Observations of human life — build notes

This category's Ordering Tracker table lists 46 rows: 41 new pages and 5 retrofits (Crumbling Temples, Crumbling Lessons; The Bass Voice of God; Enduring Consciousness; Bridges of Sound and Light; Small World), each gaining another `.continue-group`, tag update, and `.back-to-category` link rather than a new page. Enduring Consciousness moved from one live category to two, triggering the breadcrumb-dropping rule for it for the first time; the other four were already in two or more live categories. Only a handful of the 46 rows carry an explicit author confirmation of ordering (Oblivious to the Obvious as opener, Digital Storm as epigraph to Digital Disruption, Impact of Refugees and Syrian Ceasefire's war/displacement placement, Coyote Tales and Red Moon Omen/Our Nature/Alate Assist's nature-observation grouping, and Blanket Man/Pre-dawn Ragged Blanket's concrete-then-abstract pairing); the remaining sequence and thematic clustering (media/belief/digital-life, subjective-reality, contemplation-vs-busyness, war/displacement, nature-observation field vignettes, noise-vs-hope) is proposed only, per the tracker, and awaits author review like any other proposed ordering.

Two content-fidelity artifacts are preserved as-is rather than corrected: "Inevitable War?" repeats its own title as a plain line at the top of its body and again ahead of an embedded four-line poem stanza ("Beware your beliefs..."), both kept verbatim as separate paragraphs; "Material Separation" opens with its title repeated as a line followed by an italicized subtitle ("*(Sorrow for the rich, warning to those who would follow)*"), rendered as two separate paragraphs with the italics kept as `<em>`. Several other essays (Digitally Fractured Beliefs, For the Children, Judgement Daze, Many Truths, Reality Gap, Terlingua, Trust Your Robot, Impact of Refugees) similarly open with their own title repeated as the first line of body text; all are kept verbatim. "Ripples in Time" preserves a literal footnote-style asterisk marker in the body text and its footnote paragraph, rather than being converted to a superscript or link. "Digital Storm" is set in `.poem` style in full. "Digital Disruption" carries an author-confirmed canonical name (its old source slug was "superficial-society"). Two field-journal-style pieces (The Fledging of Downy Woodpeckers, Coyote Tales and Red Moon Omen) keep their diary formatting — short standalone timestamp and scene lines as separate paragraphs — consistent with the diary format already used elsewhere on the site.

### Poetry — build notes

Poetry's finalized compilation comprised 21 poems total: 16 brand-new pages, plus 5 poems that had already been published as essay pages under other categories and were retrofitted with a Poetry eyebrow entry, a Poetry `.continue-group`, and a Poetry `.back-to-category` link (Silken Tide, Storm of Creation, Worship, Truth.....Any Takers?, Overlapping Projections of Gods — Worship's addition to Poetry was confirmed separately by the author in its own Drive note). Of the 16 new poems, 6 were multi-category from the outset and gained rows on one or more existing category pages in addition to their own new Poetry page: Silken Tide and Breeze of Mystery (Spiritual, Without Overt Mention of Religion + Spiritual With Mention of Religion), Symphony of Chance (Spiritual, Without Overt Mention of Religion), No Time for Grief (Observations of Human Life), Just a Moment / Another Fresh Start / Mere Faith to Move Mountains (Transcendent Conversations and Vision), Conveniently Rational Munitions / You Will Be Touched / Ghost of Perfection (Spiritual, Without + Spiritual With), Portal of Your Soul (Spiritual, Without Overt Mention of Religion), Edge (Transcendent + Spiritual, Without), Shadow Embrace (Structure + Transcendent), and Incarnationalism (Transcendent). This is why Transcendent Conversations and Vision doubled from 6 to 12 essays, and why Structure (33→34), Spiritual/without (40→48), Spiritual/with (61→66), and Observations (46→47) all grew — every existing member essay in a category that gained a new row also had its "No. X of Y" eyebrow denominator updated to the new total.

Poetry's internal ordering — both the sequence on the Poetry category page and the insertion point of new poems within each host category's list (all appended at the end, so no existing essay's position number changed, only totals) — is **proposed only**. The Ordering Tracker (still at the version last confirmed Sept 17) contains no Poetry-specific guidance, unlike several other categories where the author confirmed specific placements; the Poetry ordering here goes short nature vignettes → personal reflection → faith and struggle → transcendent encounter → poems about mystery and understanding, and awaits author review like any proposed sequence.

Two verbatim-transcription notes: six poem titles arrived in ALL CAPS in their Drive sources (PORTAL OF YOUR SOUL, JUST A MOMENT, ANOTHER FRESH START, LAUGHS OF GRASS, YOU WILL BE TOUCHED, LESSONS OF THE MYSTERY) and were normalized to Title Case to match the sitewide title convention — the body text itself was left untouched. Four poems (Conveniently Rational Munitions, Ghost of Perfection, Portal of Your Soul, Shadow Embrace) had a stray zero-width-space character left over from their plain-text export, which was stripped as a non-visible formatting artifact rather than content.

While building Poetry, a pre-existing bug from the earlier Observations of Human Life launch was caught and fixed: 10 instances of `href="index.html#observations-of-human-life"` (the "not yet live" placeholder anchor) had been left un-updated across three category pages — Structure of the Purpose and Destiny of Life, Spiritual With Mention of Religion, and Spiritual, Without Overt Mention of Religion — instead of being repointed to the live `observations-of-human-life.html` page after that category went live. All 10 were corrected as part of this build.

### Manifest-driven rebuild — cosmetic normalizations

Reverse-engineering `manifest.json` out of the existing HTML (see above) surfaced about a dozen small text inconsistencies that had accumulated because each category's HTML was hand-authored in its own build session, with no single place recording "what is this category actually called." None of these touch essay body text; all are chrome (eyebrows, tags, nav labels) that the generator now derives from one canonical label per category (each category's own page heading) and applies everywhere:

- Category names varied by which page referenced them — e.g. an essay's eyebrow might say "Personal perspective" or "Transcendent conversations & vision" while that category's own page heading said "Personal Perspective" or "Transcendent Conversations and Vision." Every reference sitewide now matches the category's own heading exactly.
- Two essays — "At the Ranch" and "Deer and Coyotes" — had their own `<h1>` disagreeing with their own `<title>` tag (lowercase "ranch"/"coyotes" in the heading, Title Case in the tab title). Both now consistently use the Title Case form everywhere, including on the Personal Perspective category page, which had been listing them lowercase.
- Tag-list order on category pages now matches the canonical category order used in eyebrows and back-to-category links, rather than whatever order a given build session happened to add them in.
- `sitemap.xml`'s essay URLs are now alphabetical instead of build-chronological — sitemap order has no effect on search indexing, so this is a purely internal tidiness change.

Every one of these was verified mechanically before being accepted: essay body text was confirmed byte-for-byte identical file-by-file, and each essay's category membership and position within every category was confirmed unchanged, both before and after regeneration (see the git history in `website_proto/`, which is now a real repository — this refactor is its first two commits).

## Design choices

- **Palette**: warm cream paper background, dark warm-charcoal ink, and a single muted teal accent — chosen to feel like a well-made book page rather than a tech product, and to stay legible and calm across a large body of reflective, spiritually-themed writing. Full dark-mode variant included.
- **Type**: Lora (serif) for headings and essay body, Inter (sans) for navigation/UI/tags — a common, readable pairing for long-form reading sites.
- **One shared stylesheet** (`assets/style.css`), linked by every page, so a single change updates the whole site. Per project convention, only the affected essay's page and its category index page(s) get regenerated for a content update — not the whole site.
- **SEO/best-practice basics** on every page: unique title and meta description, canonical URL, Open Graph tags, semantic landmarks (`header`/`nav`/`main`/`article`/`footer`), one `<h1>` per page, a skip-to-content link, `sitemap.xml`, `robots.txt`.

## One essay, one page — even across categories

An essay that belongs to more than one category (e.g. *Hillside* is filed under five) gets exactly **one** physical HTML page, linked from every category page it belongs to. This avoids duplicate-content SEO problems and means there's only ever one copy of the text to keep verbatim. On the essay page itself, categories that aren't live yet appear as an "Also filed under (not yet live)" tag list (pointing at that category's coming-soon card); once a category goes live, its tag becomes a working link.

### Multiple live categories: the "Continue reading" pattern

Once an essay belongs to **two or more live categories** — the first case is *Hillside* and *Fledging*, both in Personal Perspective and now also in Transcendent Conversations and Vision — a single hard-coded "previous/next" pair on the essay page would be misleading, because the correct neighbor depends on which category the reader is following. Rather than adding JavaScript or query-parameter logic to guess which category a reader arrived from, the site handles this with plain, static HTML: the navigation area at the bottom of the essay is wrapped in a `.continue-reading` container that can hold more than one `.continue-group` block, each clearly labeled ("Continue in Personal Perspective," "Continue in Transcendent Conversations and Vision") and each showing that category's own honest previous/next essay. An essay in only one live category still gets exactly one such block — no visual change from before.

**Maintenance implication**: when a not-yet-built category goes live and an already-published essay belongs to it, that essay's page needs another `.continue-group` added (and its "Also filed under" tag for that category, if any, updated from an inert reference to a live link). This happened four times — Structure of the Purpose and Destiny of Life added a `.continue-group` to nine essay pages, Spiritual, Without Overt Mention of Religion added one to twenty more (nine of them for the second time), Observations of Human Life added one to five more (Crumbling Temples Crumbling Lessons, The Bass Voice of God, Bridges of Sound and Light, and Small World for at least the third time; Enduring Consciousness for the first time), and Poetry added one to five more (Silken Tide, Storm of Creation, Worship, Truth.....Any Takers?, Overlapping Projections of Gods). Hillside and Fledging are still the record-holders at up to five `.continue-group` blocks each — neither Observations nor Poetry's retrofits touched them. With all seven categories now live, this pattern is complete; a future new essay would only add rows to categories it already belongs to.

**Breadcrumb rule for multi-category essays**: once an essay belongs to two or more live categories, its breadcrumb trail drops the category segment entirely and shows only "Home / Categories / EssayTitle" — showing just one of several correct parent categories would be misleading. This started with Hillside and Fledging, extended to seven more essays with the Structure launch, to eleven more with the Spiritual, Without Overt Mention of Religion launch, and to one more (Truth.....Any Takers?) with the Poetry launch.

## "Recently added" on the homepage

The old single "Featured essay" section has been replaced with a "Recently added" strip showing the three most recently added essays. As of the manifest-driven rebuild, the strip is an explicit editorial list: the `homepage_recent` array in `site_data/manifest.json` (three essay slugs, newest first). `generate_site.py` renders those three cards, showing "Poetry" as the eyebrow for any poem and otherwise the essay's first category. Update the list by hand when new material is added and should be featured. (It used to be derived from each file's Google Drive `createdTime`, but that data was only ever available for part of the site, so an explicit list is more honest.)

## Content fidelity

Essay text is reproduced verbatim from the finalized Google Drive source — never silently rewritten or paraphrased. Two known formatting artifacts in "Deer and coyotes" (a mid-sentence line break, and a stray leading period before "It is a good morning") are preserved as-is rather than corrected, per the project's fidelity rule. (Oct 18, 2026: both are gone, because the author's revised final of that essay removed them; see the update section above.) Poems and poem-like passages (all of "Storm of Creation," "Currency of the Soul," and "Overlapping Projections of Gods"; the seven-line opening of "Seeing Through Our Dreams and Scars"; all of "Digital Storm"; the closing stanza of "Inevitable War?") use a `.poem` style that preserves the source's exact line and stanza breaks instead of re-flowing them into justified prose paragraphs. "Three Principles" reproduces its source's literal bulleted list as an `<ul>`. All 21 Poetry poems use the `.poem` style, with hanging/indented lines from the source preserved via non-breaking spaces rather than being left to collapse. See the Observations of human life build notes above for that category's additional preserved artifacts (repeated in-body titles, an embedded footnote marker in "Ripples in Time," and an italicized subtitle in "Material Separation"), and the Poetry build notes for that category's title-case normalizations and stripped zero-width-space artifacts.

## File layout

```
index.html
404.html                                      ("page not found"; generated)
feed.xml                                      (RSS feed; generated)
googled8b37a9a18da5204.html                   (Google Search Console ownership file; keep)
search.html
sitemap.xml
robots.txt
categories/
  index.html                                  (all 7 categories, all live)
  personal-perspective.html
  transcendent-conversations-and-vision.html
  structure-of-the-purpose-and-destiny-of-life.html
  spiritual-without-religion.html
  spiritual-with-religion.html
  observations-of-human-life.html
  poetry.html
essays/
  at-the-ranch.html
  deer-and-coyotes.html
  cuddling-and-carnivores.html
  frantic.html
  hillside.html
  fledging.html
  seeing-through-our-dreams-and-scars.html
  currency-of-the-soul.html
  faith-madness.html
  storm-of-creation.html
  overlapping-projections-of-gods.html
  three-principles.html
  the-scrum-of-perfection.html
  small-world.html
  a-higher-perspective.html
  beauty-in-the-madness.html
  knowledge-of-good-and-evil.html
  would-we-miss-death.html
  did-we-love.html
  summary-of-life.html
  whats-left-after-conforming.html
  winning-with-the-stacked-deck-of-life.html
  impossible-yearning.html
  stream-of-consciousness.html
  our-ancient-birth.html
  inexorable-life.html
  the-inevitable-and-the-certain.html
  our-actions-coerced-compelled-chosen.html
  terrifying-passage-from-the-garden-to-the-kindom.html
  dark-matter-and-the-light-of-love.html
  forgiving-god.html
  apprenticed-to-god.html
  bridges-of-sound-and-light.html
  pray-alone-that-you-may-love-together.html
  truth-any-takers.html
  silken-tide.html
  worship.html
  stop-for-a-moment.html
  save-the-world-a-little-later.html
  alternative-path-home.html
  flightless-souls-on-walkabout.html
  recognizing-beauty.html
  the-death-of-personal-growth.html
  successful-disaster.html
  life-adrift-or-navigating-life.html
  heart-blindness.html
  enduring-consciousness.html
  unlocked-door-of-our-solitary-confinement.html
  more-than-meat.html
  that-person-next-to-you.html
  conversation-with-an-angel.html
  crumbling-temples-crumbling-lessons.html
  the-bass-voice-of-god.html
  pachinko-minds.html
  shock-prayer.html
  do-not-cling-to-the-light.html
  intention-of-attention.html
  accept-what-you-want.html
  painful-prayer.html
  personalized-scripture.html
  boring-angels.html
  temporally-senseless.html
  palm-sunday-anti-climax.html
  question-revealing-truth.html
  following-the-unseeable.html
  defiant-subversive-seditious-christmas.html
  ontological-meaning-of-salvation.html
  heaven-with-a-little-help-from-me-friends.html
  powerless-triumph.html
  indefensible-hope.html
  combat-and-compassion.html
  collapse-of-worldly-wisdom.html
  role-of-a-life-in-the-purpose-of-life.html
  oblivious-to-the-obvious.html
  digital-storm.html
  digital-disruption.html
  machine-mirrors.html
  mindfield.html
  digitally-fractured-beliefs.html
  digital-migrations.html
  artificial-intelligence-and-real-stupidity.html
  judgement-daze.html
  many-truths.html
  overlapping-realities.html
  reality-gap.html
  childish-questions.html
  antithetical-societal-solution.html
  material-separation.html
  inevitable-war.html
  for-the-children.html
  impact-of-refugees.html
  syrian-ceasefire.html
  terlingua.html
  the-curse-of-approval.html
  trust-your-robot.html
  cynical-encouragement.html
  faith-crisis-faith-freedom.html
  the-fledging-of-downy-woodpeckers.html
  coyote-creation.html
  coyote-tales-and-red-moon-omen.html
  our-nature.html
  in-need-of-meadow.html
  ripples-in-time.html
  contact-eternity.html
  alate-assist.html
  blanket-man.html
  pre-dawn-ragged-blanket.html
  soul-music-i.html
  soul-music-ii.html
  whispering-hope.html
  unnatural-peace.html
  tracer-bullets-over-your-life-path.html
  destructive-gentleness.html
  spark-of-progress.html
  laughs-of-grass.html
  breeze-of-mystery.html
  symphony-of-chance.html
  no-time-for-grief.html
  freedom-from-opportunity.html
  just-a-moment.html
  another-fresh-start.html
  mere-faith-to-move-mountains.html
  conveniently-rational-munitions.html
  portal-of-your-soul.html
  edge.html
  you-will-be-touched.html
  shadow-embrace.html
  ghost-of-perfection.html
  incarnationalism.html
  lessons-of-the-mystery.html
assets/
  style.css
site_data/
  manifest.json          (source of truth — edit this to add/reorder essays)
  common.py
  build_manifest.py       (one-time: rebuilt manifest.json from HTML; re-run only if the manifest and site ever diverge)
  generate_site.py        (run after editing manifest.json)
  validate_site.py        (run after generate_site.py)
sitemap.xml
robots.txt
.gitignore
```

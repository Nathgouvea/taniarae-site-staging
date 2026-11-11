# AGENTS.md: rules for any AI bot editing Tania Rae's website

You are editing a small static website: plain HTML, CSS and a little vanilla
JavaScript. **No build step, no framework, no npm.** What is in this repo is
exactly what visitors get. Keep it that way.

## 0. The golden rules

1. **Always change staging first.** Edit only this repo (`taniarae-site-staging`).
   Never edit `taniarae-site` (production) directly. Production changes only
   through the **Publish to production** workflow.
2. **Never remove** the consent checkbox, `alt` text, form `<label>`s, the
   honeypot field (`_gotcha`), the skip link, or focus styles
   (`:focus-visible` rules). Never set `outline: none` without an equally
   visible replacement.
3. **Use relative paths** (`assets/css/styles.css`, `privacy.html`, `./`).
   Never start a path with `/`: staging lives in a sub folder.
   The only exception is `404.html`, which uses a `<base href>` with the full site URL.
4. **Keep facts in sync.** When prices, FAQ, languages, location or services
   change, update all of: the visible text in `index.html`, the JSON-LD in the
   `<head>` of `index.html`, and `llms.txt`.
5. **Update `sitemap.xml`** `<lastmod>` (YYYY-MM-DD) for every page whose
   content you change.
6. **No cookies, trackers, embeds or third-party scripts**, and no fonts from
   Google or another CDN (GDPR). If analytics are wanted, suggest a cookie-free
   tool (for example Plausible, Fathom or GoatCounter), update `privacy.html`,
   and ask Tania before adding anything.
7. Leave content placeholders such as `[CERTIFICATION]` visible until Tania
   gives the real text.
8. Do not edit anything inside `<!-- STAGING-ONLY -->` … `<!-- /STAGING-ONLY -->`
   except to keep it working; the publish script removes those blocks.

## 1. Where everything lives

| File | What it is |
|---|---|
| `index.html` | The landing page ("the letter"). Each part starts with a `<!-- SECTION: … -->` comment. |
| `privacy.html` | Privacy policy (draft, Tania must review). |
| `404.html` | "Page not found". Uses `<base href>` with the full site URL. |
| `assets/css/styles.css` | All styles. **Design tokens at the top** (`:root`). |
| `assets/js/form.js` | Contact form logic only (validation, Formspree, thank-you message). |
| `assets/fonts/` | Self-hosted Figtree, Instrument Serif, Caveat (OFL licence). |
| `assets/images/` | Photos (AVIF/WebP/JPEG sizes), `og-image.jpg`, icons. |
| `site.config.json` | Values that differ between staging and production. |
| `robots.txt` | Staging: blocks everything. |
| `robots.production.txt` | Becomes `robots.txt` on production. |
| `sitemap.xml`, `llms.txt`, `site.webmanifest` | SEO, AI-answer summary, app manifest. |
| `scripts/make-production.py` | Used by the publish workflow. |
| `scripts/make-images.py` | Regenerates all images from the original photos (needs Pillow). |

Sections in `index.html`, in order: Header · Hero ("Dear you,") · Maybe this
sounds familiar (post-it notes) · This works best if you're ready (yellow band
+ checklist) · What we work on (cards) · How it works (steps) · A little about
me · The practical part (prices) · Shall we talk? (contact form) · P.S. (FAQ) · Footer.

## 2. Adding or deleting repeatable items

Every item of a kind uses identical markup. **To add:** copy one block and
change the text. **To delete:** remove the whole block. Tilts, colours,
numbers and ticks are applied automatically by CSS.

**Post-it note** (in `<ul class="postits">`). More than three wrap onto the next line.
```html
<li class="postit"><p>“Your quote here.”</p></li>
```

**"Ready" checklist point** (in `<ul class="ticks">`):
```html
<li>You’re ready to try something new.</li>
```

**"What we work on" card** (in `<ul class="cards">`). Copy an existing card's
`<svg>` icon, or draw a new 64×64 line icon in the same style
(`stroke="#26408F"`, a yellow circle behind, `aria-hidden="true"`).
```html
<li class="card">
  <svg …copy an icon… aria-hidden="true"></svg>
  <h3>Boundaries</h3>
  <p>Saying no kindly, and meaning it.</p>
</li>
```

**Step** (in `<ol class="steps">`). The number is automatic.
```html
<li class="step">
  <h3>Step title</h3>
  <p>Step text.</p>
</li>
```

**P.S. question** (inside the FAQ section). **Also** add the same question and
answer, word for word, to the `FAQPage` block in the JSON-LD.
```html
<details>
  <summary>Your question?</summary>
  <p>Your answer.</p>
</details>
```
```json
{
  "@type": "Question",
  "name": "Your question?",
  "acceptedAnswer": { "@type": "Answer", "text": "Your answer." }
}
```

## 3. Colours, fonts and contrast

All tokens are at the top of `assets/css/styles.css`. Change one line there.
Some SVG icons in `index.html` and the data-URI images in `styles.css`
repeat the hex values `#26408F`, `#1E2B45`, `#F6C94C` and `#E8B423`. If you change
one of those colours, search and replace the hex value in both files.

| Token | Value | Used for | Contrast rule |
|---|---|---|---|
| `--color-paper` | `#FBF8F1` | Background | |
| `--color-ink` | `#1E2B45` | Text, focus outlines | ≥ 4.5:1 on paper, band, white and yellow |
| `--color-muted` | `#59606F` | Secondary text | ≥ 4.5:1 on paper and white |
| `--color-hand` | `#26408F` | Handwriting, icons | ≥ 4.5:1 on paper and band |
| `--color-yellow` | `#F6C94C` | Buttons, tape, highlights | Background only: text on it must be ink |
| `--color-yellow-deep` | `#E8B423` | Circles, squiggles | Decoration only, never text |
| `--color-band` | `#FFF4D6` | Yellow band | |
| `--color-input-border` | `#8A806F` | Field borders | ≥ 3:1 against paper/white (UI) |
| `--color-error` | `#A3271F` | Errors | ≥ 4.5:1 on paper and white |

Rules: normal text needs **4.5:1**, large text (24px+, or 18.5px+ bold) and
UI parts (borders, icons, focus rings) need **3:1** (WCAG 2.2 AA). Check any new
colour with a contrast checker before using it. Never convey meaning by colour alone.

Fonts: `--font-body` (Figtree), `--font-serif` (Instrument Serif),
`--font-hand` (Caveat). New fonts must be self-hosted `.woff2` files in `assets/fonts/`.

## 4. Contact form

- Fields in order: Name*, Email*, Phone (optional), message (optional), consent checkbox*.
- Required fields: `required` + `<span class="req" aria-hidden="true">*</span>`.
  Optional: `<span class="opt">(optional)</span>`. A required field needs a
  matching `<p class="error" id="ID-error" hidden></p>` and an entry in
  `MESSAGES` in `form.js`.
- The form posts to Formspree. The form ID and email subject differ per
  environment (`site.config.json`).

## 5. Staging → production

- Staging: `https://[GITHUB_USERNAME].github.io/taniarae-site-staging/`
  (noindex, `robots.txt` blocks all, "Staging preview" ribbon, `[STAGING]` email subject).
- Production: `https://[DOMAIN]/`.

Flow: **change staging › push › review the staging URL › run "Publish to production"**
(GitHub › `taniarae-site` › Actions › Publish to production › Run workflow).

The workflow runs `scripts/make-production.py`, which copies the site files,
removes `STAGING-ONLY` blocks, swaps the URL, form ID and subject from
`site.config.json`, installs `robots.production.txt`, keeps `CNAME`, and
**fails** if any `[STAGING]`, `noindex`, `github.io` or setup placeholder is left.
Content placeholders (e.g. `[LANGUAGES]`) only produce warnings.

If you change the site URL, form ID or subject: change `site.config.json`
**and** the matching text in the HTML/XML/TXT files.

## 6. Search engines and AI crawlers

`robots.production.txt` allows Googlebot, Bingbot, Google-Extended, GPTBot,
OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot and PerplexityBot.
To block one, change its `Allow: /` to `Disallow: /`. Example, to stop OpenAI
from using the site for training but keep it in ChatGPT search:
```
User-agent: GPTBot
Disallow: /
```
(Google-Extended controls Gemini training; blocking it does not affect Google Search.)

Keep the same name and description everywhere: "Tania Rae, relationship
coach", one to one relationship coaching online worldwide and in person in Porto
on communication, conflict and attachment patterns.

## 7. Pre-publish checklist

Run before every "Publish to production":

- [ ] axe shows **0 violations** (`npx @axe-core/cli <staging URL>`)
- [ ] Lighthouse **95+ on mobile** in all categories
      (note: staging scores lower on SEO because of noindex; that is expected)
- [ ] **No horizontal scroll at 375px**
- [ ] The form works on staging (**real test submission received**)
- [ ] **JSON-LD validates** (Google Rich Results Test + validator.schema.org)
- [ ] **No broken links**
- [ ] The page still matches the approved design at **390px and 1280px**
- [ ] `sitemap.xml` lastmod updated; JSON-LD and `llms.txt` match the visible text

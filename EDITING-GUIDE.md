# Editing your website: a guide for Tania

Your website is a handful of simple files. You change it by asking your AI bot
in plain words. This guide shows you how, and what to ask.

## How a change goes live (always these three steps)

1. **Ask your bot for the change.** It edits the *staging* copy of your site
   (the practice version). Nobody else sees it, and Google ignores it.
2. **Look at the staging site** in your browser:
   https://nathgouvea.github.io/taniarae-site-staging/
   It has a small dark "Staging preview" label in the bottom corner, so you
   always know where you are. Check it on your phone too. Changes can take a
   minute or two to appear.
3. **Happy? Publish.** On GitHub, open the `taniarae-site` repository, click
   **Actions**, then **Publish to production**, then **Run workflow**. A
   minute or two later your real site (https://[DOMAIN]/) is updated.
   You can also ask your bot: "Run Publish to production".

If something looks wrong on staging, just tell the bot what to fix, and check again.
Nothing reaches your real site until you publish.

## Things you can ask for

Copy and adapt these:

**Words**
- "Change the headline to: …"
- "In 'A little about me', replace [COUNTRIES OR CITIES] with Brazil, London and Porto."
- "Replace [CERTIFICATION] with ICF Associate Certified Coach."
- "Replace [LANGUAGES] with English and Portuguese, everywhere it appears."

**Post-it notes ("Maybe this sounds familiar")**
- "Add a fourth post-it that says 'We only talk about logistics now.'"
- "Delete the second post-it."

**The "ready" checklist**
- "Add a point: 'You can make time for one session every two weeks.'"

**"What we work on"**
- "Add a card called 'Boundaries' with the text '…' and a fitting icon."

**Steps ("How it works")**
- "Add a fourth step called '…' with the text '…'."

**P.S. questions**
- "Add a question 'Can we meet in person?' with the answer '…'."
  (The bot also updates the hidden information Google uses. That's in its rules.)

**Prices**
- "Change the 6-session price to €660." (The bot updates the page, Google's
  data and the AI summary in one go.)

**Look and feel**
- "Change the yellow to a softer yellow, but keep the text readable."
- "Make the handwritten notes a bit bigger."
- "Use a different font for headings." (Fonts must be stored on the site
  itself, not loaded from Google.)

**Photo**
- "Here is a new photo of me [attach it]. Please use it for 'A little about me'
  and the header avatar, and regenerate the image sizes and sharing image."

**Search engines and AI**
- "Block ChatGPT from training on my site, but keep it in ChatGPT search."

## Things the bot will refuse or double-check (on purpose)

- Removing the consent tick box, the privacy link, image descriptions, or
  keyboard focus outlines. These keep the site legal and usable for everyone.
- Adding cookies, tracking, Google Fonts, video embeds or other outside scripts.
  These would need a cookie banner and a privacy policy update.
- Editing the live site directly instead of staging first.

## Still to fill in

Ask your bot to replace these when you have the answers:

- `[COUNTRIES OR CITIES]`: where you have lived
- `[CERTIFICATION]`: your coaching certification
- `[ONE REAL, SPECIFIC DETAIL]`: what you do when you're not working
- `[LANGUAGES]`: languages you coach in
- `[TIME ZONES]`: time zones you can serve
- In the privacy policy: `[EMAIL PROVIDER]` and how long you keep messages (`[6 MONTHS]`),
  then ask the bot to remove the "Draft" note once you (or a lawyer) have checked it.

## Suggested Instagram bio (same words as the website)

> Tania Rae · Relationship coach
> 1:1 coaching on communication, conflict & attachment patterns.
> Online worldwide · in person in Porto 🇵🇹
> Free 20 min call ↓
> [DOMAIN]

## Checking your contact form

After any change to the form, send yourself a test message on the **staging**
site. It arrives with **[STAGING]** in the subject, so you can tell test
messages from real ones.

# Getting RTL email to render right

What breaks, why, and the rule that fixes it. Written for someone composing an
email in Hebrew, Arabic, Farsi or Urdu for the first time.

The bidi mechanics below are identical across those scripts — they are handled
by the same Unicode algorithm and the same HTML attributes. Only the font stack
and the register conventions differ, and those are called out separately.

Verified in Chromium on 5 August 2026 by rendering `examples/` with
`scripts/preview.sh`. **Outlook behaviour is from established email-development
practice and is not verified here** — this repo has no Outlook to test against.
Untested claims say so.

## The one rule

**Never send an RTL body as plain text. Always HTML, always with an explicit
`dir="rtl"`.**

Plain-text email carries no direction metadata of any kind. There is no header,
no marker, nothing in the format that says "this is right-to-left". The client
guesses from the characters.

That guess is the whole problem:

- **Gmail** guesses per-paragraph and is usually right for solid RTL prose.
- **Outlook** frequently renders LTR.
- **Mixed content is where everything fails.** A paragraph containing a URL, an
  account number, a product name or an email address gives the heuristic enough
  Latin to change its mind.

The failure is not a crash. Lines start at the left, and the punctuation that
should close a sentence sits at the wrong end. It stays readable — which is
exactly why it survives review. Nobody notices until the recipient does, and
what they notice is that the message looks machine-generated.

There is no message short enough for plain text to be the right call. A one-line
reply gets the same treatment as a formal complaint.

## Set `dir` twice: as an attribute and as CSS

```html
<div dir="rtl" lang="he" style="direction:rtl;text-align:right;">
```

Both, not either:

- **Outlook on Windows renders through the Word engine.** It honours the `dir`
  HTML attribute reliably and CSS `direction` less so. *(Established practice;
  untested here.)*
- **Gmail, Apple Mail and webmail clients** honour the CSS.

Setting both costs nothing and is the difference between "renders everywhere"
and "renders in the client that happened to be tested".

Set `lang` too — `he`, `ar`, `fa`, `ur`. It does not affect direction, but it
drives font selection and hyphenation, and screen readers use it to pick a
voice.

## Repeat `dir="rtl"` on every block

Not just the wrapper. Every `<p>`, every `<td>`, every `<div>` holding RTL text:

```html
<p dir="rtl">שורה ראשונה.</p>
<p dir="rtl">שורה שנייה.</p>
```

Direction inheritance from a container into children is not reliable across
clients and viewports, and mail clients rewrite HTML aggressively before
display — Gmail strips and rebuilds, Outlook re-flows. An attribute sitting on
the element itself survives that; an inherited property may not.

This is the rule most often skipped, because it looks redundant in a browser,
where it *is* redundant. The browser is not the target.

## Latin and numbers inside RTL text

Once the block is `dir="rtl"`, the Unicode bidi algorithm handles embedded Latin
correctly **in the middle of a paragraph**. URLs, brand names, statute citations
and email addresses need nothing.

Two places it goes wrong:

**1. A Latin or numeric run at the very start or end of a paragraph.** Trailing
punctuation jumps to the wrong side. Wrap the run:

```html
<p dir="rtl">מספר האסמכתא הוא <span dir="ltr">REF/2026-08-05</span>.</p>
```

**2. Multi-part numbers anywhere.** A bare figure in RTL prose is fine — a
single number is a single neutral run. But anything with internal separators
will reorder them:

- account and branch numbers
- phone numbers
- IBANs
- date ranges
- version numbers

```html
<td dir="ltr" align="right">02-376-3631</td>
```

This bites hardest in exactly the mail that can least afford it. A corrupted
account number in a complaint to a bank is worse than an ugly layout: it is the
string the recipient uses to find the file.

**Arabic-Indic digits** (٠١٢٣٤٥٦٧٨٩, U+0660–0669) are context-sensitive in bidi
and behave differently from ASCII digits. If a message mixes them with ASCII
digits, isolate each run rather than assuming either default.

## The signature goes in its own LTR block

A Latin-script signature under an RTL body belongs in `dir="ltr"`:

```html
<div dir="rtl" lang="he">…RTL body…</div>
<div dir="ltr">…signature…</div>
```

This is correct and is what RTL business mail actually looks like. Do not force
the signature RTL to "match" — a Latin name and email address in an RTL block
will have their punctuation reordered for no gain.

## Fonts

Lead with a face that has **complete coverage of the target script**, because a
font missing the script falls back **per character** — a word can render in two
faces and look visibly broken.

| Script | Lead with | Notes |
|---|---|---|
| Hebrew | `Arial` | Complete coverage everywhere that matters. |
| Arabic | `Tahoma`, then `Arial` | Tahoma has the better Arabic on Windows; both are present cross-platform. |
| Farsi / Urdu | `Tahoma`, then `Arial` | Urdu ideally wants a Nastaliq face, which is not reliably installed — do not depend on it. |

Do not lead with Roboto or a bare `-apple-system` stack for RTL text; coverage
varies by version and platform.

```
font-family: Arial, 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
```

Webfonts are not worth it — most clients strip `@font-face`, and no display face
justifies the failure modes.

## Line height

Give RTL text more leading than you would give Latin: **1.7**, not 1.4.

Hebrew has no ascenders or descenders to speak of, and Arabic scripts carry
diacritics and dot clusters above and below the baseline. Both look cramped at
Latin defaults. This is the one purely typographic setting in these templates
that is not about correctness, and it is the one that most changes whether the
mail looks native.

## Subject lines

Subjects are a header, not the body, and are MIME-encoded. Gmail handles pure
RTL subjects natively; they need nothing.

Mixed subjects can display in the wrong direction in the inbox list. Two fixes,
in order of preference:

1. **Put the RTL text first.** Usually enough, and costs nothing.
2. **Prefix with U+200F (RLM).** Forces RTL. Invisible, but it is a real
   character — some systems that log or filter on subject prefixes will see it.

## Plain-text fallback

Include one in the send call for completeness. Do not rely on it to render.

Prefixing each paragraph with U+200F improves the odds in text-only clients.
Treat it as best-effort: it is a hint to a heuristic, not a directive. See
`assets/templates/plain-fallback.txt`.

## Layout: no card, no fixed width

A 600px centred card is what a newsletter looks like. One-to-one mail should
look like a person typed it. Gmail's composer renders a fixed-width container
as a floating box with a large gutter — and in an RTL message that gutter lands
on the wrong side, so the message reads as broken rather than merely styled.

Full-width paragraphs, no wrapper table, no background panel.

## Checking your work

Render it and look:

```bash
./scripts/preview.sh examples/formal-complaint-he.html
```

The four things to check, in order:

1. Text is right-aligned and sentences start at the right.
2. Full stops and colons sit at the **left** end of their line.
3. Account numbers, phone numbers and dates read in the correct order —
   character by character, against the source.
4. The signature block is left-aligned below the RTL text.

A browser render only proves the markup is sound. It cannot prove Outlook is
happy — that is what the `dir` attributes are insurance against.

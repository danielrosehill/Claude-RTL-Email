---
name: send-rtl-email
description: Compose and send an email whose body is in a right-to-left script — Hebrew, Arabic, Farsi or Urdu. Use for ANY RTL-bodied email regardless of recipient or formality, including one-line replies, formal correspondence to banks, insurers, utilities and government bodies, and covering notes for an attached letter. Sends via Google Workspace MCP (Gmail) or Resend MCP. Required because a plain-text RTL body renders left-to-right in many clients; this skill wraps the body in a dir="rtl" HTML template that renders correctly everywhere.
---

# Send an RTL email

Composes an email in Hebrew, Arabic, Farsi or Urdu and sends it through Gmail
(Google Workspace MCP) or Resend.

## Why this skill exists

**Plain-text email carries no direction metadata.** There is no header and no
marker that says "this is right-to-left" — the client guesses from the
characters. Gmail usually guesses right for solid RTL prose. Outlook frequently
does not. Any paragraph containing a URL, an account number or a Latin product
name gives the heuristic enough to change its mind.

The failure mode is quiet: lines start at the left and sentence-final
punctuation lands at the wrong end. It stays readable, so it survives review —
and what the recipient notices is that the message looks machine-generated.

So: **RTL bodies are always sent as HTML with an explicit `dir="rtl"`.** There
is no message short or throwaway enough for plain text to be the right call.

Read `references/bidi-rules.md` before composing. The three rules that cause
almost every visible failure:

1. Set `dir` **both** as an HTML attribute and as CSS `direction`. Outlook
   honours the attribute; webmail honours the CSS.
2. Repeat `dir="rtl"` on **every** block element, not just the wrapper. Mail
   clients rewrite HTML before display and inherited direction does not reliably
   survive.
3. Wrap multi-part numbers — account numbers, phone numbers, IBANs, dates — in
   `<span dir="ltr">`. Without it the separators reorder, corrupting exactly the
   strings the recipient uses to find the file.

## Workflow

### 1. Detect the script and pick the template

If the body will be primarily RTL, this skill applies. Mixed RTL/Latin where RTL
dominates also applies.

| Situation | Template |
|---|---|
| Ordinary mail — a person, a vendor, a colleague | `assets/templates/base.html` |
| A bank, insurer, utility, municipality, government body, regulator; or a covering note for an attached letter | `assets/templates/formal.html` |

Set `{{LANG}}` (`he`, `ar`, `fa`, `ur`) and `{{FONT_STACK}}` per
`references/bidi-rules.md` § Fonts. Hebrew leads with Arial; Arabic and Farsi
lead with Tahoma.

### 2. Compose at the right register

Read `references/register.md`. The trap: **Hebrew ordinary mail is markedly more
informal than its English equivalent** (second-person singular, היי, תודה as a
sign-off, never translated corporate boilerplate) — but **formal Hebrew is a
different register entirely** (לכבוד, הנדון:, בכבוד רב, and the filing
identifiers in the body, not only in the attachment).

Getting this backwards is as visible as getting the direction wrong.

### 3. Build the body HTML

Every paragraph:

```html
<p dir="rtl">…</p>
```

Every identifier — account number, phone, reference, IBAN, date range:

```html
<span dir="ltr">02-376-3631</span>
```

For `formal.html`, fill `{{DETAILS_ROWS}}` with the identifiers the recipient
files by:

```html
<tr>
  <td style="padding:2px 0 2px 12px;color:#5f5f5f;">LABEL</td>
  <td style="padding:2px 0;" dir="ltr" align="right">VALUE</td>
</tr>
```

### 4. Preview before sending

```bash
./scripts/preview.sh /tmp/draft.html
```

Check, in order: text right-aligned; full stops at the **left** end of the line;
identifiers reading correctly character by character against the source;
signature left-aligned below.

This proves the markup is sound. It cannot prove Outlook is happy — the `dir`
attributes are the insurance for that.

### 5. Send

**Google Workspace MCP (Gmail).** Tool names vary by server build; the common
one is `send_gmail_message`. Pass:

- `body` — the substituted HTML
- `body_format: "html"` — **the whole point; omitting it sends plain text**
- `subject` — see below
- `to`, and `user_google_email` if the server requires it

**Resend MCP.** Use its send tool with `html` set to the substituted template.
Resend does not auto-append a signature, so `{{SIGNATURE_HTML}}` must be filled.

**Attachments.** Both transports generally accept a URL fetched server-side as
well as inline base64. Prefer a URL for anything over ~100 KB — base64 of a
multi-page PDF is large enough to be worth avoiding.

### 6. Subject lines

Pure RTL subjects need nothing — they are MIME-encoded and handled natively.

Mixed subjects can display in the wrong direction in the inbox list. Put the RTL
text first; if that is not enough, prefix U+200F (RLM).

### 7. Plain-text fallback

Include one where the transport accepts both parts, using
`assets/templates/plain-fallback.txt`. Prefixing paragraphs with U+200F improves
the odds in text-only clients. It is best-effort — a hint to a heuristic, not a
directive. HTML is the real answer.

## Common mistakes

- **Calling the send tool directly without loading this skill.** This is the
  actual origin of the bug the plugin exists to prevent — the guidance was
  present but nothing routed the send through it. If you are about to send and
  any part of the body is RTL, come here first.
- **`dir` on the wrapper only.** Looks fine in a browser, which is not the
  target.
- **Forcing the signature RTL to "match".** A Latin signature belongs in its own
  `dir="ltr"` block. That is what RTL business mail looks like.
- **A 600px centred card.** In an RTL message the gutter lands on the wrong
  side and reads as a bug rather than a style.
- **Translated English boilerplate.** No natural Hebrew equivalent exists for
  "I hope this email finds you well".

---
name: send-rtl-personal-email
description: Send a personal email whose body is in a right-to-left script — Hebrew, Arabic, Farsi or Urdu — to a person, friend, family member, vendor or colleague. Signs with the user's personal profile. Use for ANY personal RTL-bodied email including one-line replies, because a plain-text RTL body renders left-to-right in many clients. Sends via Google Workspace MCP (Gmail) or Resend MCP.
---

# Send a personal RTL email

Signs with the **`personal`** profile.

## Why this skill exists

**Plain-text email carries no direction metadata.** No header, no marker —
the client guesses from the characters. Gmail usually guesses right for solid
RTL prose; Outlook frequently renders LTR; and one URL or account number in a
paragraph is enough to flip the heuristic either way.

The failure is quiet. Lines start at the left, sentence-final punctuation lands
at the wrong end. It stays readable, so it survives review — and what the
recipient notices is that the message looks machine-generated.

So RTL bodies are always sent as HTML with an explicit `dir="rtl"`. There is no
message short enough for plain text to be the right call, including a one-line
reply.

## Procedure

Follow `references/composing.md` — it carries the full sequence and is shared
with the business variant. In summary:

1. Load the `personal` profile from
   `${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/rtl-email/config.json`.
   **If it is missing, run `configure-rtl-signatures` first** — never invent a
   signature and never send with `{{SIGNATURE_HTML}}` unfilled.
2. Template: `assets/templates/base.html` by default. If this personal message
   happens to be going to an institution — a bank, a utility, a government
   office — use `formal.html` instead. The recipient decides the register, not
   the profile.
3. Compose informally. See `references/register.md`: Hebrew personal mail is
   markedly *more* informal than its English equivalent — second-person
   singular, היי, תודה as a sign-off. Do not translate English boilerplate;
   "I hope this email finds you well" has no natural Hebrew equivalent.
4. `dir="rtl"` on every block; `<span dir="ltr">` around every multi-part number.
   See `references/bidi-rules.md`.
5. Preview with `./scripts/preview.sh` and look at it.
6. Send with **`body_format: "html"`** (Gmail) or as `html` (Resend). Omitting
   it undoes everything above.
   **On Resend, BCC the profile's own email address** on every message unless it is
   already a recipient. Resend sends never appear in a Gmail Sent folder, so the BCC
   is the user's only copy to proof the render.

## Style and contact basics

Inline copy of `references/email-style.md` in Google-Workspace-Plugin (local clone
`~/repos/github/ai-agents-and-prompts/ai-claude-plugins/Google-Workspace-Plugin`).
That file is canonical; keep this block in sync with it. Set 2026-10-19.

**Style** — for anything sent as Daniel:

- **Short sentences**, under about 15 words, one idea each. Email is not the essay voice: no long asides, ellipses or rhetorical questions.
- **To the point.** The first sentence says why you are writing. No "Hope this finds you well" or "Just reaching out".
- **Respectful, not deferential.** Say please and thank you where they belong. Don't grovel and don't flatter.
- **Not promotional.** No superlatives, no "excited to" or "passionate about", and no sales pitch nobody asked for. A link to the website does the selling.
- **No emojis**, anywhere, including subject lines. At most one exclamation mark per email.
- **Ground it in basics:** what, when, how much, and one clear ask near the end. Most emails run 3–8 sentences.
- First person singular ("I", not "we"). Sign off with "Regards," by default, or "Thanks," when asking a favour.

**Contact basics** — use these when relevant, not pasted in by default:

| What | Value |
| --- | --- |
| Personal website | https://danielrosehill.com |
| Business website (DSR Holdings) | https://dsrholdings.cloud |
| AI consultancy (Carrot Cake AI) | https://carrotcakeai.com |
| Meeting request (Daniel, also for DSR Holdings) | https://www.danielrosehill.com/book-meeting |
| Meeting request (Carrot Cake AI) | https://www.carrotcakeai.com/book-meeting |
| Mobile | 050-328-6767, or +972 50-328-6767 for international recipients (`tel:+972503286767`) |

The meeting pages are **request forms**, not instant booking: Daniel replies with an invitation. Write "You can request a time here: <link>", never "book directly". When proposing a meeting, offer the link and the mobile number, e.g. "Would a 30-minute call next week work? You can request a time here: <link>. Or call me on +972 50-328-6767."

**Hebrew bodies:** the same rules apply. Wrap phone numbers and URLs in `<span dir="ltr">` so the hyphens don't reorder.

## Do not

- Call the send tool directly without coming through here.
- **Entity-escape the HTML body.** Pass raw `<div dir="rtl">`, never
  `&lt;div dir="rtl"&gt;`. Escaped markup sends without error and renders as
  visible tags in the recipient's window. This has happened in real
  correspondence — see `references/composing.md`.
- **Send anything formal without reading the message back.** One
  `get_gmail_message_content` call on the returned ID catches both the
  escaping bug and a dropped `body_format` in ten seconds. That is the exact
  failure this plugin was built from: the guidance existed, nothing routed the
  send through it.
- Set `dir` on the wrapper only. It looks fine in a browser, which is not the
  target.
- Force the signature RTL to match the body. It belongs in its own `dir="ltr"`
  block, which the templates already provide.

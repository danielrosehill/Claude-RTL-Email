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

## Do not

- Call the send tool directly without coming through here. That is the exact
  failure this plugin was built from: the guidance existed, nothing routed the
  send through it.
- Set `dir` on the wrapper only. It looks fine in a browser, which is not the
  target.
- Force the signature RTL to match the body. It belongs in its own `dir="ltr"`
  block, which the templates already provide.

---
name: send-rtl-business-email
description: Send a business or formal email whose body is in a right-to-left script — Hebrew, Arabic, Farsi or Urdu — to a client, supplier, bank, insurer, utility, municipality, government body or regulator, including covering notes for an attached letter. Signs with the user's business profile and its organisation identifiers. Use for ANY business RTL-bodied email, because a plain-text RTL body renders left-to-right in many clients and corrupts account and reference numbers. Sends via Google Workspace MCP (Gmail) or Resend MCP.
---

# Send a business RTL email

Signs with the **`business`** profile, including its organisation identifiers.

## Why this skill exists

**Plain-text email carries no direction metadata**, so the client guesses.
Outlook frequently guesses LTR — and Outlook is what institutional recipients
run.

For business mail the cosmetic problem is the smaller one. **Multi-part numbers
reorder their separators when they are not isolated**: account numbers, branch
numbers, IBANs, company and VAT numbers, invoice references, date ranges. A
corrupted reference number is not an aesthetic issue. It is the string the
recipient uses to find the file, and it will be quoted back wrong or not found
at all.

## Procedure

Follow `references/composing.md`. In summary:

1. Load the `business` profile from
   `${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/rtl-email/config.json`.
   **If it is missing, run `configure-rtl-signatures` first.**
2. Template: `assets/templates/formal.html` by default — addressee line, subject
   line, identifier block, formal closing. Drop to `base.html` only for genuinely
   routine exchanges with someone you deal with regularly.
3. Compose formally. See `references/register.md`: Hebrew wants לכבוד to open,
   a הנדון: line, בכבוד רב to close, and no second-person-singular familiarity.
   Arabic formal correspondence is Modern Standard Arabic, not dialect.
4. Fill `{{DETAILS_ROWS}}` from the profile's `identifiers` **plus whatever this
   matter files under** — the account number, case number or invoice reference.
   Every value gets `dir="ltr"`.
5. **Assume the attachment will not be opened before the mail is routed.**
   Whoever reads it first is often deciding which desk it goes to. The body must
   carry the subject, the identifier and the request on its own.
6. Preview with `./scripts/preview.sh`. **Check every identifier character by
   character against the source**, then show the render to the user before
   sending anything formal.
7. Send with **`body_format: "html"`** (Gmail) or as `html` (Resend).
   **On Resend, BCC the profile's own email address** on every message unless it is
   already a recipient. Resend sends never appear in a Gmail Sent folder, so the BCC
   is the user's only copy to proof the render.

## Do not

- Call the send tool directly without coming through here.
- **Entity-escape the HTML body.** Pass raw `<div dir="rtl">`, never
  `&lt;div dir="rtl"&gt;`. Escaped markup sends without error and renders as
  visible tags in the recipient's window. This has happened in real
  correspondence — see `references/composing.md`.
- **Send anything formal without reading the message back.** One
  `get_gmail_message_content` call on the returned ID catches both the
  escaping bug and a dropped `body_format` in ten seconds.
- Let a number with internal separators sit unwrapped in RTL text.
- Rely on the plain-text fallback to carry a reference number. It cannot.

## AI-assistance line

If the profile has `ai_line`, append it as the last element, after the signature: its own
`<p dir="rtl" lang="<lang>">` in small grey italics, inside the RTL wrapper and outside the
signature block. Skip it only when the user says to leave it off for this send. If the
profile has no `ai_line`, add nothing.

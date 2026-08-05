# Composing and sending an RTL email

The shared mechanics behind `send-rtl-personal-email` and
`send-rtl-business-email`. Both skills do the same thing and differ only in
which profile they load and which register they write in.

Read `bidi-rules.md` first if you have not. This file assumes it.

## 1. Load the profile

```bash
CFG="${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/rtl-email/config.json"
```

Read the profile named by the calling skill — `personal` or `business`. It
supplies the signature, the display name in both scripts, the default language,
and for business profiles the organisation identifiers.

**If the file does not exist, or the profile is missing from it, stop and run
the `configure-rtl-signatures` skill.** Do not invent a signature, and do not
send with the signature placeholder unfilled. An email that closes with
`{{SIGNATURE_HTML}}` is worse than one that renders LTR.

## 2. Pick the template

| Situation | Template |
|---|---|
| A person, a vendor, a colleague — ordinary correspondence | `assets/templates/base.html` |
| A bank, insurer, utility, municipality, government body, regulator; or a covering note for an attached letter | `assets/templates/formal.html` |

The profile's `register` field is the default, but the recipient overrides it. A
personal profile writing to a bank still uses `formal.html`; a business profile
thanking a long-standing supplier does not have to.

Set `{{LANG}}` from the profile (`he`, `ar`, `fa`, `ur`) and `{{FONT_STACK}}`
per `bidi-rules.md` § Fonts — Hebrew leads with Arial, Arabic and Farsi with
Tahoma.

## 3. Compose at the right register

`register.md` has the detail. The trap worth repeating: **ordinary Hebrew mail is
markedly more informal than its English equivalent** — second-person singular,
היי, תודה as a sufficient sign-off, and never translated English boilerplate.
**Formal Hebrew is a different register entirely** — לכבוד, הנדון:, בכבוד רב.

Getting this backwards is as visible to a native reader as getting the direction
wrong.

## 4. Build the body

Every paragraph carries its own direction:

```html
<p dir="rtl">…</p>
```

Every multi-part number is isolated:

```html
<span dir="ltr">02-000-0000</span>
```

For `formal.html`, fill `{{DETAILS_ROWS}}` from the profile's `identifiers`,
plus anything specific to this matter (an account number, a case reference):

```html
<tr>
  <td style="padding:2px 0 2px 12px;color:#5f5f5f;">LABEL</td>
  <td style="padding:2px 0;" dir="ltr" align="right">VALUE</td>
</tr>
```

## 5. Preview

```bash
./scripts/preview.sh /tmp/draft.html
```

Check: right-aligned; full stops at the **left** end of the line; identifiers
correct character by character against the source; signature left-aligned below.

For anything formal, or anything quoting an account number, show the render to
the user before sending.

## 6. Send

**Google Workspace MCP (Gmail).** Tool names vary by server build; commonly
`send_gmail_message`. Pass the substituted HTML as `body` and — the whole point —
**`body_format: "html"`**. Omitting it sends plain text and undoes everything
above. Include `to`, `subject`, and `user_google_email` if the server requires
it.

**Resend MCP.** Pass the substituted template as `html`. Resend never
auto-appends a signature, so the profile's signature must be filled in.

**Attachments.** Both transports generally accept a server-side-fetched URL as
well as inline base64. Prefer a URL above ~100 KB.

## 7. Subject line

Pure RTL subjects need nothing. For mixed subjects put the RTL text first; if
that is not enough, prefix U+200F (RLM).

## 8. Record what was sent

If the profile sets `log_dir`, append a one-line record — date, recipient,
subject, profile used. Formal correspondence tends to acquire a reference number
later, and a sent-log is what makes that findable.

---
name: configure-rtl-signatures
description: Set up or change the user's RTL email profiles — their preferred signature, display name in both scripts, contact details and organisation identifiers — and persist them so later sends reuse them without asking again. Use on first RTL send, when the user asks to change their email signature, add a business or personal profile, or when a send skill reports that no profile is configured.
---

# Configure RTL email profiles

Collects the user's signature and identity details once and writes them to a
config file, so `send-rtl-personal-email` and `send-rtl-business-email` stop
asking.

## Where it lives

```bash
CFG="${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/rtl-email/config.json"
```

Use that resolver string verbatim. **Do not** write to `~/.claude/` — that is
the config surface, and `~/.claude/plugins/<plugin>/` is the install directory,
which is clobbered on plugin update.

The signature is small settings data, so it belongs in `config.json` directly.
If the user keeps their correspondence in a repo or a documents folder, store
only a *pointer* to it as `log_dir` — never copy their files under the plugin
data root.

## What to ask

Ask only for what is missing. If a profile already exists, show it and ask what
to change rather than re-collecting everything.

**Per profile** (`personal` and `business` are the two the send skills expect;
more can be added and named freely):

| Field | Notes |
|---|---|
| `display_name` | Latin script, as it should appear in the signature |
| `display_name_rtl` | The same name in the RTL script. **Ask — do not transliterate it yourself.** People have a spelling of their own name and being given a plausible alternative reads badly. |
| `lang` | `he`, `ar`, `fa`, `ur` |
| `register` | `informal` for personal, `formal` for business — the default only; recipient overrides |
| `email`, `phone` | Phone in the form the user actually gives out |
| `identifiers` | Business only, and optional: national ID, company number, VAT number. Label/value pairs that go in the formal template's details block |
| `org`, `org_rtl` | Business only |
| `log_dir` | Optional pointer to where sent correspondence is recorded |
| `ai_line` | Optional. A short AI-assistance note in the profile's language (e.g. (מייל זה נכתב בעזרת עוזר בינה מלאכותית.)). If set, the send skills append it after the signature on every send unless the user says to leave it off. Ask whether they want one; never set it on their behalf |

**Ask whether the signature should be in Latin or RTL script.** A Latin-script
signature under an RTL body is normal and correct, and it is what most bilingual
senders use — but it is the user's call, not a default to assume silently.

## Writing it

```json
{
  "version": 1,
  "default_profile": "personal",
  "profiles": {
    "personal": {
      "lang": "he",
      "register": "informal",
      "display_name": "Ada Lovelace",
      "display_name_rtl": "עדה לאבלייס",
      "email": "ada@example.com",
      "phone": "02-000-0000",
      "signature_html": "<div>Ada Lovelace<br><a href=\"mailto:ada@example.com\">ada@example.com</a><br>02-000-0000</div>"
    },
    "business": {
      "lang": "he",
      "register": "formal",
      "display_name": "Ada Lovelace",
      "display_name_rtl": "עדה לאבלייס",
      "org": "Example Ltd",
      "org_rtl": "דוגמה בע\"מ",
      "email": "ada@example.com",
      "phone": "02-000-0000",
      "identifiers": [
        { "label": "ח.פ.", "value": "000000000" }
      ],
      "signature_html": "<div>Ada Lovelace<br>Example Ltd<br><a href=\"mailto:ada@example.com\">ada@example.com</a><br>02-000-0000</div>"
    }
  }
}
```

Create the directory with `mkdir -p` before writing. Write the file with
permissions the user's other config has; do not do anything special to it.

**Build `signature_html` as a plain `<div>` with `<br>` breaks.** It is rendered
inside a `dir="ltr"` container by the templates, so it needs no direction
attributes of its own. Keep it to name, organisation, email and phone — a
signature with a logo, a quote and three social links is a different problem and
not one this plugin solves.

## Confirm by rendering

Do not just report success. Substitute the new signature into
`assets/templates/base.html` with a one-line body, render it, and show the user:

```bash
./scripts/preview.sh /tmp/sig-check.html
```

A signature is the part of an email the user will see thousands of times. It is
worth thirty seconds to confirm it looks the way they meant, and it catches a
mis-typed RTL name immediately, while it is still cheap to fix.

## Changing it later

Re-run this skill. Read the existing file, show the current values, change what
the user names, write it back. Never silently drop a profile that was already
there — if the user asks to change the business signature, the personal one
survives untouched.

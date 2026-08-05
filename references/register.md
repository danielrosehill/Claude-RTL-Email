# Register: formal vs ordinary RTL correspondence

Bidi handling is mechanical and identical across scripts. Register is not, and
getting it wrong is the other way an RTL email announces that it was not written
by someone who writes RTL email.

## Hebrew

**Ordinary mail — vendors, colleagues, friends, family — is markedly more
informal than its English equivalent.** This surprises English speakers:

- Second-person singular: אתה / את. There is no polite plural in living use.
- Open with שלום or היי. Not לכבוד.
- תודה is a complete and sufficient sign-off.
- **Do not translate English corporate boilerplate.** "I hope this email finds
  you well" has no natural Hebrew equivalent and reads stilted and foreign in
  every attempt.

**Formal correspondence is a genuinely different register, and the informal
defaults are wrong for it.** Anything to a bank, insurer, health fund,
municipality, government office, regulator or tribunal — and anything that
accompanies a typeset letter:

- Open **לכבוד** + the name of the body.
- A **הנדון:** line naming the matter.
- Close **בכבוד רב,** — not תודה.
- No contractions, no second-person-singular familiarity.
- Include the identifiers the body files by — ת"ז, account number, case or own
  reference — in a details block, not only in an attachment.
- Ask explicitly for an acknowledgement and a reference number.

## Arabic

The formal/informal split is wider than in Hebrew and is carried by the choice
of variety, not only by wording:

- **Formal correspondence is Modern Standard Arabic.** Dialect in a letter to an
  institution reads as a category error.
- Open **السيد المحترم / السادة المحترمون** or **إلى**; **الموضوع:** for the
  subject line.
- Close **وتفضلوا بقبول فائق الاحترام،**.
- Ordinary mail between people who know each other is a different matter and
  may reasonably use dialect.

## Farsi and Urdu

Both have formal registers with honorific systems more elaborate than either of
the above. This plugin does not attempt to encode them: the templates handle
direction and layout, and the wording is the sender's.

The mechanical rules in `bidi-rules.md` apply unchanged.

## Choosing

Usually obvious from the recipient. Where it is genuinely unclear, **formal is
the safer error**: an over-formal email to a plumber reads slightly stiff; an
over-familiar email to a bank's complaints commissioner undercuts the complaint
it is carrying.

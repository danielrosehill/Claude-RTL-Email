#!/usr/bin/env python3
"""Render the worked examples from the templates.

The examples exist to be looked at, but if they were hand-written they would
drift from the templates they claim to demonstrate. Generating them means a
change to a template shows up in the examples on the next run, and a template
that cannot be substituted cleanly fails here rather than in someone's outbox.

    ./scripts/build-examples.py && ./scripts/preview.sh examples/formal-he.html
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TPL = ROOT / "assets" / "templates"
OUT = ROOT / "examples"

HEBREW_FONTS = "Arial,'Segoe UI',-apple-system,BlinkMacSystemFont,sans-serif"
ARABIC_FONTS = "Tahoma,Arial,'Segoe UI',sans-serif"


def fill(template: str, values: dict) -> str:
    """Substitute {{TOKENS}} and fail loudly on any left behind.

    A silently unsubstituted placeholder is the one failure that would actually
    reach a recipient — {{SIGNATURE_HTML}} sitting in a sent email — so this
    refuses to write the file instead of warning about it.
    """
    text = (TPL / template).read_text(encoding="utf-8")
    # Drop the leading HTML comment; it is documentation for whoever opens the
    # template, not part of the message.
    text = re.sub(r"^<!--.*?-->\s*", "", text, flags=re.S)
    for key, value in values.items():
        text = text.replace("{{%s}}" % key, value)
    leftover = re.findall(r"\{\{(\w+)\}\}", text)
    if leftover:
        raise SystemExit(f"{template}: unsubstituted placeholders: {sorted(set(leftover))}")
    return text


def page(body: str) -> str:
    return (
        '<!doctype html><meta charset="utf-8">'
        '<body style="margin:24px;background:#fff;width:640px">' + body + "</body>"
    )


SIGNATURE = (
    '<div>Ada Lovelace<br>'
    '<a href="mailto:ada@example.com">ada@example.com</a><br>'
    '02-000-0000</div>'
)

# Formal Hebrew: a complaint to a bank. Chosen because it exercises everything
# at once — an addressee line, a הנדון, numbered identifiers that must not
# reorder, and a body that has to stand on its own if the attachment is never
# opened.
formal_he = fill(
    "formal.html",
    {
        "LANG": "he",
        "FONT_STACK": HEBREW_FONTS,
        "ADDRESSEE": "לכבוד נציבות פניות הציבור, בנק לדוגמה,",
        "SUBJECT_LABEL": "הנדון",
        "SUBJECT_LINE": "גביית עמלות בחשבון לאחר הגשת בקשה לסגירתו",
        "BODY_HTML": "\n".join(
            [
                '<p dir="rtl">לפני למעלה מחודש הגשתי בקשה לסגירת החשבון ומילאתי את טופס '
                "הסגירה, והעברתי את מלוא ההרשאות לחיוב חשבון לבנק אחר בהתאם לדרישתכם.</p>",
                '<p dir="rtl">החשבון לא נסגר, ובחודש יולי נגבו בו עמלות בסך 75.74 ש"ח. '
                "הניסיון לפנות בכתב לבנקאי דרך תיבת ההודעות באתר נכשל בהודעת שגיאה.</p>",
                '<p dir="rtl">אבקש לסגור את החשבון לאלתר, לזכות אותי בעמלות שנגבו, '
                'ולמסור לי אישור בכתב. מספר האסמכתא שלי הוא <span dir="ltr">REF/2026-08-05</span>.</p>',
            ]
        ),
        # Every value dir="ltr" — this is the block that demonstrates why.
        "DETAILS_ROWS": "\n".join(
            '<tr><td style="padding:2px 0 2px 12px;color:#5f5f5f;">%s</td>'
            '<td style="padding:2px 0;" dir="ltr" align="right">%s</td></tr>' % row
            for row in [
                ('ת"ז', "000000000"),
                ("מספר חשבון", "362433"),
                ("סניף", "517"),
                ("טלפון", "02-000-0000"),
            ]
        ),
        "CLOSING": "בכבוד רב,",
        "SIGNATURE_HTML": SIGNATURE,
    },
)

# Informal Hebrew, on base.html: the everyday case, and a reminder that the
# register here is much lighter than an English equivalent would be.
base_he = fill(
    "base.html",
    {
        "LANG": "he",
        "FONT_STACK": HEBREW_FONTS,
        "BODY_HTML": "\n".join(
            [
                '<p dir="rtl">היי,</p>',
                '<p dir="rtl">תודה על ההצעה. אפשר לקבוע לשבוע הבא? נוח לי ביום שלישי '
                "אחרי הצהריים.</p>",
                '<p dir="rtl">אפשר להשיג אותי במספר <span dir="ltr">02-000-0000</span>.</p>',
                '<p dir="rtl">תודה,</p>',
            ]
        ),
        "SIGNATURE_HTML": SIGNATURE,
    },
)

# Arabic, to show the templates are not Hebrew-only. Same markup, different
# font stack and closing formula.
formal_ar = fill(
    "formal.html",
    {
        "LANG": "ar",
        "FONT_STACK": ARABIC_FONTS,
        "ADDRESSEE": "السادة المحترمون، قسم خدمة العملاء،",
        "SUBJECT_LABEL": "الموضوع",
        "SUBJECT_LINE": "طلب إغلاق الحساب واسترداد الرسوم",
        "BODY_HTML": "\n".join(
            [
                '<p dir="rtl">تقدمت بطلب إغلاق الحساب قبل أكثر من شهر، ولم يتم الإغلاق '
                "حتى تاريخه.</p>",
                '<p dir="rtl">أرجو إغلاق الحساب وإفادتي بتأكيد خطي. رقم المرجع الخاص بي '
                'هو <span dir="ltr">REF/2026-08-05</span>.</p>',
            ]
        ),
        "DETAILS_ROWS": "\n".join(
            '<tr><td style="padding:2px 0 2px 12px;color:#5f5f5f;">%s</td>'
            '<td style="padding:2px 0;" dir="ltr" align="right">%s</td></tr>' % row
            for row in [("رقم الحساب", "362433"), ("الهاتف", "02-000-0000")]
        ),
        "CLOSING": "وتفضلوا بقبول فائق الاحترام،",
        "SIGNATURE_HTML": SIGNATURE,
    },
)

OUT.mkdir(exist_ok=True)
for name, html in [
    ("formal-he.html", formal_he),
    ("base-he.html", base_he),
    ("formal-ar.html", formal_ar),
]:
    (OUT / name).write_text(page(html), encoding="utf-8")
    print("wrote examples/" + name)

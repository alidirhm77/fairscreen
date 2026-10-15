"""
Blind-review anonymiser.

Removes identity signals and proxies (name, contact details, IC number, gender words,
race/religion, family status, age, address, and the NAME of the institution — while
keeping the QUALIFICATION LEVEL, which is job-relevant).

Returns the redacted text plus a list of what was removed, so the recruiter can see
exactly what the system hid and why (transparency > magic).
"""
import re
from .taxonomy import PROTECTED_TERMS

# Language skills contain race words ("Bahasa Cina", "Chinese language", "Bahasa Melayu").
# Protect them before redaction so a language skill is never mistaken for ethnicity.
LANGUAGE_GUARDS = [
    (r"\bbahasa\s+melayu\b", "LANG_BM"),
    (r"\bbahasa\s+malaysia\b", "LANG_BM"),
    (r"\bmalay\s+language\b", "LANG_BM"),
    (r"\bbahasa\s+cina\b", "LANG_MANDARIN"),
    (r"\bchinese\s+language\b", "LANG_MANDARIN"),
    (r"\bmandarin\b", "LANG_MANDARIN"),
    (r"\bbahasa\s+inggeris\b", "LANG_EN"),
    (r"\btamil\s+language\b", "LANG_TAMIL"),
    (r"\bbahasa\s+tamil\b", "LANG_TAMIL"),
]
LANGUAGE_RESTORE = {"LANG_BM": "Bahasa Melayu", "LANG_MANDARIN": "Mandarin",
                    "LANG_EN": "English", "LANG_TAMIL": "Tamil language"}

LABEL_LINES = re.compile(
    r"^\s*(gender|jantina|sex|race|bangsa|religion|agama|ethnicity|keturunan|nationality|warganegara|"
    r"age|umur|date of birth|tarikh lahir|dob|marital status|status perkahwinan|address|alamat|"
    r"ic no\.?|no\.? ic|nric|mykad|phone|telefon|tel|email|e-mel|emel)\s*[:\-].*$",
    re.IGNORECASE | re.MULTILINE,
)
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"\+\d{1,3}[\s-]?\(?\d{1,4}\)?(?:[\s-]?\d{2,4}){2,4}"            # international, e.g. +967 774 640 570
                   r"|(?:\+?6?0)[\s-]?1\d[\s-]?\d{3,4}[\s-]?\d{4}|\b0\d{1,2}[\s-]?\d{3,4}[\s-]?\d{4}\b")
MYKAD = re.compile(r"\b\d{6}-\d{2}-\d{4}\b")
URL = re.compile(r"https?://\S+|www\.\S+|\b(?:linkedin\.com|github\.com|gitlab\.com|orcid\.org)/\S+", re.IGNORECASE)
# Referees and other people named with a title (Dr. / Prof.) — a name reveals origin and networks.
TITLED_NAME = re.compile(r"\b(?:Assoc\.?\s+Prof|Prof(?:essor)?|Dr|Ir|Ts)\.?\s+[.\-]?[A-Z][\w.'’-]*(?:\s+(?:[.\-]?[A-Z][\w.'’-]*|binti\b|bin\b|a/l|a/p)){0,5}")
# Countries and home cities act as nationality proxies.
PLACES = re.compile(r"\b(" + "|".join([
    "malaysia", "yemen", "sana'a", "sana’a", "sanaa", "aden", "taiz", "ibb", "egypt", "cairo", "saudi arabia", "riyadh", "jeddah",
    "indonesia", "jakarta", "bangladesh", "dhaka", "pakistan", "karachi", "lahore", "nigeria", "lagos", "china", "beijing",
    "iran", "tehran", "iraq", "baghdad", "syria", "damascus", "sudan", "khartoum", "somalia", "jordan", "amman", "libya",
    "oman", "muscat", "uae", "dubai", "qatar", "kuwait", "philippines", "manila", "vietnam", "hanoi", "thailand", "bangkok",
    "myanmar", "nepal", "kathmandu", "sri lanka", "colombo", "singapore", "brunei", "turkey", "istanbul", "algeria",
    "morocco", "tunisia", "palestine", "lebanon", "afghanistan", "kenya", "ethiopia", "uzbekistan", "kazakhstan"]) + r")\b",
    re.IGNORECASE)
POSTCODE_STATE = re.compile(
    r"\b\d{5}\s+[A-Za-z .]*(selangor|kuala lumpur|penang|pulau pinang|johor|perak|kedah|kelantan|terengganu|"
    r"pahang|melaka|negeri sembilan|sabah|sarawak|perlis|putrajaya|labuan)\b",
    re.IGNORECASE,
)
INSTITUTION = re.compile(
    r"\b(?i:universiti|university|kolej|college|politeknik|polytechnic|institut|institute|akademi|academy|"
    r"ikm|ikbn|adtec|ilp)\b(?:\s+(?:(?i:of the|of|malaysia|teknologi|sains|kebangsaan|putra|utara|islam|antarabangsa|"
    r"tun|hussein|onn|sultan|abdul|aziz|azlan|shah|idris|zainal|abidin|pendidikan)\b|[A-Z][\w&'-]*))*"
    r"|\b[A-Z][\w&'-]*(?:\s+[A-Z][\w&'-]*)*\s+(?:University|College|Polytechnic|Institute)\b"
    r"|\b(?:UM|UKM|UPM|USM|UTM|UiTM|UUM|UIAM|IIUM|UTP|MMU|UTAR|UCSI|APU|INTI|SEGi|Taylor's|Sunway|Monash|"
    r"Nottingham|UNIMAS|UMS|UTeM|UMP|UniMAP|UTHM|UPSI|UMT|UniSZA|UMK|USIM|UNITEN|UNIKL|Help)\b"
)


def _word_pattern(words):
    return re.compile(r"\b(" + "|".join(re.escape(w) for w in sorted(words, key=len, reverse=True)) + r")\b",
                      re.IGNORECASE)


_PROTECTED = {k: _word_pattern(v) for k, v in PROTECTED_TERMS.items()}


def guess_name(text: str) -> str | None:
    m = re.search(r"^\s*(?:name|nama)\s*[:\-]\s*(.+)$", text, re.IGNORECASE | re.MULTILINE)
    if m:
        return m.group(1).strip()
    for line in text.splitlines():
        s = line.strip()
        if s:
            # First line looks like a name: 2-6 words, letters only, no digits
            if 1 < len(s.split()) <= 6 and not re.search(r"\d|@|:", s):
                return s
            return None
    return None


def anonymize(text: str) -> tuple[str, list[dict]]:
    removed: list[dict] = []

    def log(kind, value):
        removed.append({"type": kind, "value": value.strip()})

    out = text
    for pat, token in LANGUAGE_GUARDS:
        out = re.sub(pat, token, out, flags=re.IGNORECASE)

    name = guess_name(out)
    if name:
        log("name", name)
        # remove full name and each distinctive token (skip connectors like bin/binti/a/l)
        out = re.sub(re.escape(name), "[CANDIDATE]", out, flags=re.IGNORECASE)
        for tok in name.split():
            if len(tok) > 2 and tok.lower() not in {"bin", "binti", "bt", "a/l", "a/p", "anak", "van", "de"}:
                out = re.sub(rf"\b{re.escape(tok)}\b", "[CANDIDATE]", out)
        out = re.sub(r"^\s*(?:name|nama)\s*[:\-].*$", "", out, flags=re.IGNORECASE | re.MULTILINE)

    for m in LABEL_LINES.finditer(out):
        log("personal field", m.group(0))
    out = LABEL_LINES.sub("", out)

    for pat, kind, rep in [(EMAIL, "email", "[EMAIL]"), (MYKAD, "IC number", "[IC]"), (PHONE, "phone", "[PHONE]"),
                           (URL, "link", "[LINK]"), (TITLED_NAME, "referee / named person", "[PERSON]"),
                           (POSTCODE_STATE, "address", "[LOCATION]")]:
        for m in pat.finditer(out):
            log(kind, m.group(0))
        out = pat.sub(rep, out)

    for m in INSTITUTION.finditer(out):
        if m.group(0).strip():
            log("institution name", m.group(0))
    out = INSTITUTION.sub("[INSTITUTION]", out)

    for m in PLACES.finditer(out):
        log("country / city (nationality proxy)", m.group(0))
    out = PLACES.sub("[LOCATION]", out)

    for kind, pat in _PROTECTED.items():
        for m in pat.finditer(out):
            log(kind.replace("_", "/"), m.group(0))
        out = pat.sub("[REDACTED]", out)

    for token, restore in LANGUAGE_RESTORE.items():
        out = out.replace(token, restore)

    out = re.sub(r"(\[INSTITUTION\][\s,]*){2,}", "[INSTITUTION] ", out)
    out = re.sub(r"\n{3,}", "\n\n", out).strip()
    # de-duplicate the removal log while keeping order
    seen, uniq = set(), []
    for r in removed:
        key = (r["type"], r["value"].lower())
        if key not in seen:
            seen.add(key)
            uniq.append(r)
    return out, uniq

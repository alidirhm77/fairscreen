"""
Malaysian Twin Test — counterfactual fairness testing.

For a CV, create "twins" that are identical except for ONE protected attribute
(name/ethnicity signal, gender, institution, a family-care career break).
A fair screener must give every twin the same score. Any difference is measured
bias — evidence, not opinion.
"""
import re
from dataclasses import dataclass
from .anonymize import guess_name

# Fictional but realistic Malaysian name combinations.
NAMES = {
    ("Malay", "F"): "Nur Aisyah binti Kamarudin",
    ("Malay", "M"): "Muhammad Hafiz bin Rahman",
    ("Chinese", "F"): "Tan Mei Ling",
    ("Chinese", "M"): "Lim Wei Jie",
    ("Indian", "F"): "Priya a/p Subramaniam",
    ("Indian", "M"): "Arjun a/l Rajendran",
    ("Sabah/Sarawak", "F"): "Grace Anak Jimbun",
    ("Sabah/Sarawak", "M"): "Jeffrey Gimbang",
}
INSTITUTIONS = {
    "Research university (public)": "Universiti Malaya",
    "Regional public university": "Universiti Malaysia Sabah",
    "Private university": "UCSI University",
    "Polytechnic / TVET": "Politeknik Ungku Omar",
}
GENDER_SWAP = [
    (r"\bshe\b", "he"), (r"\bhe\b", "she"), (r"\bher\b", "his"), (r"\bhis\b", "her"), (r"\bhim\b", "her"),
    (r"\bMs\.?\b", "Mr"), (r"\bMr\.?\b", "Ms"), (r"\bPuan\b", "Encik"), (r"\bEncik\b", "Puan"),
    (r"\bfemale\b", "male"), (r"\bmale\b", "female"), (r"\bperempuan\b", "lelaki"), (r"\blelaki\b", "perempuan"),
]
INST_LINE = re.compile(
    r"(?i:universiti|university|politeknik|polytechnic|kolej|college)(?:[ \t]+[A-Z][A-Za-z'&]*){0,4}"
    r"|\b(?:UM|UKM|UPM|USM|UTM|UiTM|UUM|IIUM|UTAR|UCSI|APU|MMU|INTI|SEGi|Taylor's|Sunway)\b"
)


@dataclass
class Twin:
    group: str        # which attribute was changed
    label: str        # human-readable variant label
    text: str


def _swap_name(text: str, new_name: str) -> str:
    old = guess_name(text)
    if not old:
        return f"{new_name}\n{text}"
    out = text.replace(old, new_name)
    old_first = old.split()[0]
    if len(old_first) > 2:
        out = re.sub(rf"\b{re.escape(old_first)}\b", new_name.split()[0], out)
    return out


def _swap_gender(text: str) -> str:
    # two-phase swap so he→she doesn't get swapped back
    out = text
    for i, (pat, _) in enumerate(GENDER_SWAP):
        out = re.sub(pat, f"@@G{i}@@", out, flags=re.IGNORECASE)
    for i, (_, rep) in enumerate(GENDER_SWAP):
        out = out.replace(f"@@G{i}@@", rep)
    return out


def _swap_institution(text: str, new_inst: str) -> str:
    return INST_LINE.sub(new_inst, text, count=0)


def _add_career_break(text: str) -> str:
    line = "Career break (family care / maternity), 2 years"
    m = re.search(r"^\s*(work experience|experience|employment|pengalaman( kerja)?)\b.*$", text,
                  re.IGNORECASE | re.MULTILINE)
    if m:
        return text[:m.end()] + "\n" + line + text[m.end():]
    return text + "\n\nEXPERIENCE\n" + line


def make_twins(text: str, gender: str = "F", ethnicity: str = "Malay") -> list[Twin]:
    twins = [Twin("Original", "Original CV", text)]
    for (eth, g), name in NAMES.items():
        if g == gender:
            twins.append(Twin("Name / ethnicity", f"{eth} name — {name}", _swap_name(text, name)))
    other = "M" if gender == "F" else "F"
    twins.append(Twin("Gender", "Opposite gender (name + pronouns)",
                      _swap_gender(_swap_name(text, NAMES.get((ethnicity, other), NAMES[("Malay", other)])))))
    if INST_LINE.search(text):
        for tier, inst in INSTITUTIONS.items():
            twins.append(Twin("Institution", f"{tier} — {inst}", _swap_institution(text, inst)))
    twins.append(Twin("Career break", "Adds a 2-year family-care career break", _add_career_break(text)))
    return twins

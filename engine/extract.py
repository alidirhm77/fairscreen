"""
Feature extraction from (anonymised) CV text — bilingual EN / BM.

Only JOB-RELEVANT features are extracted: skills (with the exact evidence line),
years of relevant experience, qualification LEVEL, and evidence of work
(projects, portfolio, certifications). Career gaps are deliberately NOT a feature.
"""
import re
from dataclasses import dataclass, field
from datetime import date
from .taxonomy import SKILLS

LEVELS = {1: "SPM / secondary", 2: "Certificate / SKM", 3: "Diploma", 4: "Bachelor's degree",
          5: "Master's degree", 6: "PhD"}
LEVEL_PATTERNS = [  # order matters: most specific first
    (6, r"\b(phd|ph\.d|doctor of philosophy|kedoktoran)\b"),
    (4, r"\b(sarjana muda|ijazah sarjana muda)\b"),
    (5, r"\b(master'?s?|msc|m\.sc|mba|sarjana)\b"),
    (4, r"\b(bachelor'?s?|bsc|b\.sc|bcs|b\.eng|beng|degree|ijazah)\b"),
    (3, r"\b(diploma|advanced diploma)\b"),
    (2, r"\b(skm|sijil kemahiran malaysia|certificate|sijil|tvet|dkm)\b"),
    (1, r"\b(spm|stpm|o-level|a-level)\b"),
]
SECTION_HEADERS = {
    "experience": r"^\s*(work experience|experience|employment|pengalaman( kerja)?|internship|latihan industri)\b",
    "education": r"^\s*(education|academic|pendidikan|kelayakan akademik|qualifications?)\b",
    "projects": r"^\s*(projects?|projek|portfolio)\b",
    "skills": r"^\s*(skills?|kemahiran|technical skills)\b",
    "certifications": r"^\s*(certifications?|certificates?|sijil|pensijilan|courses?|kursus)\b",
}
MONTHS = r"(jan|feb|mar|apr|may|mei|jun|jul|aug|ogos|sep|oct|okt|nov|dec|dis)[a-z]*"
RANGE = re.compile(
    rf"(?:{MONTHS}\s+)?((?:19|20)\d\d)\s*(?:-|–|—|to|hingga|until)\s*(?:{MONTHS}\s+)?((?:19|20)\d\d|present|now|current|kini|sekarang)",
    re.IGNORECASE,
)
YEARS_STATED = re.compile(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?|tahun)\b", re.IGNORECASE)
BEGINNER = re.compile(r"\b(learning|basic|beginner|currently studying|belajar|asas|sedang mempelajari)\b", re.I)
BREAK_WORDS = re.compile(r"\b(career break|cuti|break|sabbatical|family care|jagaan keluarga|maternity|bersalin|gap year)\b", re.I)


@dataclass
class SkillHit:
    skill: str
    evidence: str          # the exact line from the CV that proves it
    source: str = "rules"  # "rules" or "ai"
    beginner: bool = False  # only evidence is "learning"/"basic" wording


@dataclass
class Profile:
    skills: dict[str, SkillHit] = field(default_factory=dict)
    years_experience: float = 0.0
    level: int = 0
    projects: int = 0
    certifications: int = 0

    @property
    def level_name(self):
        return LEVELS.get(self.level, "Not stated")


def split_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {"other": []}
    current = "other"
    for line in text.splitlines():
        hit = None
        for name, pat in SECTION_HEADERS.items():
            if re.match(pat, line, re.IGNORECASE) and len(line.strip()) < 40:
                hit = name
                break
        if hit:
            current = hit
            sections.setdefault(current, [])
            continue
        if line.strip():
            sections.setdefault(current, []).append(line.strip())
    return sections


# Phrases that contain a skill word but mean something else (e.g. "SQL Accounting" is accounting software).
NOT_THIS_SKILL = {
    "SQL": re.compile(r"\bsql\s+accounting\b", re.I),
    "Excel": re.compile(r"\bexcel+en\w*", re.I),
    "Java": re.compile(r"\bjava\s*script\b", re.I),
}


def find_skills(text: str, extra: dict | None = None) -> dict[str, SkillHit]:
    """extra = recruiter-defined custom skills {name: [synonyms]} merged with the built-in taxonomy."""
    hits: dict[str, SkillHit] = {}
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for skill, forms in {**SKILLS, **(extra or {})}.items():
        forms = [f for f in forms if f.strip()]
        if not forms:
            continue
        pat = re.compile(r"(?<![\w])(" + "|".join(re.escape(f) for f in sorted(forms, key=len, reverse=True)) + r")(?![\w])",
                         re.IGNORECASE)
        fallback = None
        for line in lines:
            probe = NOT_THIS_SKILL[skill].sub(" ", line) if skill in NOT_THIS_SKILL else line
            if pat.search(probe):
                if BEGINNER.search(line):
                    fallback = fallback or SkillHit(skill, line[:160], beginner=True)
                    continue
                hits[skill] = SkillHit(skill, line[:160])
                break
        else:
            if fallback:
                hits[skill] = fallback
    return hits


def experience_years(sections: dict[str, list[str]], today: date | None = None) -> float:
    today = today or date.today()
    exp_lines = sections.get("experience", [])
    intervals = []
    for line in exp_lines:
        if BREAK_WORDS.search(line):
            continue  # a career break is neither counted nor penalised
        for m in RANGE.finditer(line):
            start = int(m.group(2))
            end_raw = m.group(4).lower()
            end = today.year if not end_raw[:1].isdigit() else int(end_raw)
            if 1970 <= start <= end <= today.year + 1:
                intervals.append((start, max(end, start + 0.5)))
    if intervals:
        intervals.sort()
        merged = [list(intervals[0])]
        for s, e in intervals[1:]:
            if s <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], e)
            else:
                merged.append([s, e])
        return round(sum(e - s for s, e in merged), 1)
    stated = [float(m.group(1)) for l in exp_lines for m in YEARS_STATED.finditer(l)]
    return max(stated) if stated else 0.0


def qualification_level(text: str) -> int:
    best = 0
    low = text.lower()
    for lvl, pat in LEVEL_PATTERNS:
        if re.search(pat, low):
            best = max(best, lvl)
        if lvl == 4 and "sarjana muda" in pat:
            low = re.sub(r"(ijazah )?sarjana muda", "ijazah", low)  # so "sarjana" alone means Master's
    return best


def build_profile(text: str, extra: dict | None = None) -> Profile:
    sections = split_sections(text)
    edu_text = "\n".join(sections.get("education", [])) or text
    proj = len([l for l in sections.get("projects", []) if len(l) > 15])
    certs = len([l for l in sections.get("certifications", []) if len(l) > 5])
    return Profile(
        skills=find_skills(text, extra),
        years_experience=experience_years(sections),
        level=qualification_level(edu_text),
        projects=min(proj, 5),
        certifications=min(certs, 5),
    )


MUST_CUES = re.compile(r"\b(required|requirements?|must|mandatory|essential|wajib|diperlukan|syarat|keperluan|minimum)\b", re.I)
NICE_CUES = re.compile(r"\b(advantage|advantageous|preferred|preferably|nice to have|plus|bonus|kelebihan|diutamakan|added)\b", re.I)


def skills_from_job_ad(ad: str, extra: dict | None = None) -> tuple[list[str], list[str]]:
    """Read any job advertisement (EN or BM) and suggest must-have vs nice-to-have skills.
    Lines with 'advantage / preferred / kelebihan' go to nice-to-have; everything else to must-have."""
    must, nice = [], []
    section_nice = False
    for line in [l for l in ad.splitlines() if l.strip()]:
        if NICE_CUES.search(line) and len(line) < 60:
            section_nice = True          # a heading like "Added advantage:" switches the following lines
        elif MUST_CUES.search(line) and len(line) < 60:
            section_nice = False
        found = find_skills(line, extra)
        target = nice if (section_nice or NICE_CUES.search(line)) else must
        for s in found:
            if s not in must and s not in nice:
                target.append(s)
    return must, nice


def parse_custom_skills(text: str) -> dict[str, list[str]]:
    """'AutoCAD Civil 3D / civil 3d, Primavera P6 / primavera' -> {name: [synonyms]}; one skill per comma or line."""
    out = {}
    for chunk in re.split(r"[,\n;]", text or ""):
        parts = [p.strip() for p in chunk.split("/") if p.strip()]
        if parts:
            out[parts[0]] = [p.lower() for p in parts]
    return out

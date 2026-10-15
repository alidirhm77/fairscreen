"""
SIMULATED legacy screener — used only as a comparison baseline in the Twin Test.

It is clearly labelled in the app as illustrative. It models two rules that hiring
research and practice commonly report: filtering on institution prestige and
penalising employment gaps. It reads the RAW, un-anonymised CV.

FairScreen never uses this to rank anyone.
"""
import re
from .extract import find_skills, split_sections, experience_years, BREAK_WORDS, RANGE
from .scoring import Job

PRESTIGE = ["universiti malaya", "university of malaya", "universiti kebangsaan malaysia", "ukm", "universiti putra malaysia",
            "upm", "universiti sains malaysia", "usm", "universiti teknologi malaysia", "utm", "monash", "nottingham",
            "taylor's", "sunway university"]


def _has_gap(text: str) -> bool:
    if BREAK_WORDS.search(text):
        return True
    spans = sorted((int(m.group(2)), int(m.group(4)) if m.group(4)[:1].isdigit() else 2100)
                   for m in RANGE.finditer(text))
    reach = None
    for s, e in spans:
        if reach is not None and s - reach >= 2:
            return True
        reach = e if reach is None else max(reach, e)
    return False


def legacy_score(raw_text: str, job: Job) -> tuple[float, list[str]]:
    low = raw_text.lower()
    reasons = []
    skills = find_skills(raw_text, job.custom_skills)
    kw = sum(1 for s in job.must_have + job.nice_to_have if s in skills)
    base = 70 * kw / max(len(job.must_have + job.nice_to_have), 1)
    reasons.append(f"Keyword hits: {kw}")
    yrs = experience_years(split_sections(raw_text))
    base += min(yrs, 3) * 4
    if any(re.search(rf"\b{re.escape(p)}\b", low) for p in PRESTIGE):
        base += 12
        reasons.append("+12 'top university' bonus")
    if _has_gap(raw_text):
        base -= 15
        reasons.append("−15 employment-gap penalty")
    return round(max(0.0, min(base, 100.0)), 1), reasons

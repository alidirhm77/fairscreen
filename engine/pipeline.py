"""
End-to-end evaluation of one CV, and file loading.
"""
import io
from dataclasses import dataclass
from .anonymize import anonymize, guess_name
from .extract import build_profile, Profile, SkillHit
from .scoring import score, Job, Result
from .legacy import legacy_score


@dataclass
class Evaluation:
    cid: str
    display_name: str
    raw: str
    anon: str
    removed: list
    profile: Profile
    result: Result
    legacy: float
    legacy_reasons: list
    ai_rejected: int = 0


def evaluate(cid: str, raw: str, job: Job, ai_skills: list[dict] | None = None, ai_rejected: int = 0) -> Evaluation:
    anon, removed = anonymize(raw)
    profile = build_profile(anon, job.custom_skills)
    for item in ai_skills or []:
        if item["skill"] not in profile.skills:
            profile.skills[item["skill"]] = SkillHit(item["skill"], item["evidence"], "ai")
    res = score(profile, job)
    leg, why = legacy_score(raw, job)
    return Evaluation(cid, guess_name(raw) or cid, raw, anon, removed, profile, res, leg, why, ai_rejected)


def fairscreen_score_text(raw: str, job: Job) -> float:
    """Full pipeline (anonymise → extract → score) on a piece of text. Used by the Twin Test."""
    anon, _ = anonymize(raw)
    return score(build_profile(anon, job.custom_skills), job).score


def read_upload(name: str, data: bytes) -> str:
    low = name.lower()
    if low.endswith(".pdf"):
        from pypdf import PdfReader
        return "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(data)).pages)
    if low.endswith(".docx"):
        import docx
        return "\n".join(p.text for p in docx.Document(io.BytesIO(data)).paragraphs)
    return data.decode("utf-8", errors="ignore")

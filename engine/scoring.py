"""
Explainable, additive scoring.

Score = sum of transparent contributions. Because the model is additive, each
contribution IS the feature's exact Shapley value relative to an empty profile —
so explanations are mathematically exact, not approximations.

Also provides:
  * transferable-skill credit (e.g. Tableau counts partially toward Power BI)
  * counterfactual recourse: "if this candidate gained skill X, score would rise by Y"
"""
from dataclasses import dataclass, field
from .extract import Profile

# Partial credit between closely related skills (skills-based hiring, not keyword hunting).
ADJACENT = {
    "Power BI": {"Tableau": 0.6, "Excel": 0.3},
    "Tableau": {"Power BI": 0.6, "Excel": 0.3},
    "Python": {"R": 0.5},
    "R": {"Python": 0.5},
    "SQL": {"Excel": 0.2},
    "Data Visualisation": {"Power BI": 0.8, "Tableau": 0.8, "Excel": 0.4},
    "Machine Learning": {"Statistics": 0.3},
    "Statistics": {"Machine Learning": 0.5, "R": 0.4},
    "JavaScript": {"Python": 0.2},
}


@dataclass
class Job:
    title: str
    must_have: list[str]
    nice_to_have: list[str]
    min_years: float = 0.0
    target_years: float = 2.0
    min_level: int = 3
    description: str = ""
    custom_skills: dict = field(default_factory=dict)   # recruiter-defined skills {name: [synonyms]}
    weights: dict = field(default_factory=lambda: {"must": 60, "nice": 15, "experience": 15, "qualification": 5, "evidence": 5})


@dataclass
class Contribution:
    factor: str
    points: float
    max_points: float
    detail: str
    kind: str  # must / nice / experience / qualification / evidence


@dataclass
class Result:
    score: float
    contributions: list[Contribution]
    missing_must: list[str]
    recourse: list[tuple[str, float]]


def _skill_credit(skill: str, profile: Profile) -> tuple[float, str]:
    if skill in profile.skills:
        hit = profile.skills[skill]
        if hit.beginner:
            return 0.5, f"Beginner level (50%) — evidence says learning/basic: “{hit.evidence}”"
        return 1.0, f"Evidence: “{hit.evidence}”"
    best, via = 0.0, None
    for other, w in ADJACENT.get(skill, {}).items():
        if other in profile.skills and w > best:
            best, via = w, other
    if via:
        return best, f"Partial credit ({int(best*100)}%) via related skill {via}"
    return 0.0, "No evidence found"


def score(profile: Profile, job: Job) -> Result:
    W = job.weights
    contribs: list[Contribution] = []
    missing = []

    per_must = W["must"] / max(len(job.must_have), 1)
    for s in job.must_have:
        c, why = _skill_credit(s, profile)
        contribs.append(Contribution(s, round(per_must * c, 1), round(per_must, 1), why, "must"))
        if c == 0:
            missing.append(s)
        elif c < 1.0:
            missing.append(f"{s} (partial)")

    per_nice = W["nice"] / max(len(job.nice_to_have), 1) if job.nice_to_have else 0
    for s in job.nice_to_have:
        c, why = _skill_credit(s, profile)
        contribs.append(Contribution(s, round(per_nice * c, 1), round(per_nice, 1), why, "nice"))

    yrs = profile.years_experience
    exp_ratio = min(yrs / job.target_years, 1.0) if job.target_years else 1.0
    contribs.append(Contribution("Relevant experience", round(W["experience"] * exp_ratio, 1), W["experience"],
                                 f"{yrs:g} year(s) of dated work/internship experience (target {job.target_years:g}). "
                                 "Career breaks are not penalised.", "experience"))

    meets = profile.level >= job.min_level
    contribs.append(Contribution("Meets qualification level", W["qualification"] if meets else 0.0, W["qualification"],
                                 f"Highest level found: {profile.level_name}. Higher degrees earn no extra points "
                                 "(no over-credentialing); institution name is ignored.", "qualification"))

    ev = min((profile.projects + profile.certifications) / 3, 1.0)
    contribs.append(Contribution("Evidence of work", round(W["evidence"] * ev, 1), W["evidence"],
                                 f"{profile.projects} project(s), {profile.certifications} certification(s)/course(s).",
                                 "evidence"))

    total = round(min(sum(c.points for c in contribs), 100.0), 1)

    recourse = []
    for c in contribs:
        if c.kind in ("must", "nice") and c.points < c.max_points:
            recourse.append((c.factor, round(c.max_points - c.points, 1)))
    recourse.sort(key=lambda x: -x[1])
    return Result(total, contribs, missing, recourse)


def band(score: float) -> tuple[str, str]:
    if score >= 75:
        return "Strong match", "#16a34a"
    if score >= 55:
        return "Good match", "#2563eb"
    if score >= 40:
        return "Partial match", "#d97706"
    return "Low match", "#64748b"

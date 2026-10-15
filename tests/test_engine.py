"""Run with:  python -m pytest -q   (or  python tests/test_engine.py)"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine import llm
from engine.anonymize import anonymize
from engine.audit import AuditLog
from engine.pipeline import evaluate, fairscreen_score_text
from engine.sample_data import CANDIDATES, JOBS
from engine.twins import make_twins

JOB = JOBS["Junior Data Analyst (Penang, hybrid)"]


def test_anonymiser_removes_identity_but_keeps_skills():
    anon, removed = anonymize(CANDIDATES[0]["cv"])
    assert "Siti" not in anon and "012-345" not in anon and "Female" not in anon
    assert "Politeknik Seberang Perai" not in anon
    assert "Power BI" in anon and "Diploma" in anon and "Bahasa Melayu" in anon  # language kept, not mistaken for race
    assert {"name", "institution name"} <= {r["type"] for r in removed}


def test_international_cv_leaks_are_removed():
    cv = ("Test Person\nORCID: https://orcid.org/0000-0001\nNO: +967774640570\n"
          "Referee: Dr. Redhwan M.A.Saad, Cairo, Egypt\nBachelor, Ibb University, Yemen\nSkills: Python, SQL")
    anon, _ = anonymize(cv)
    for leak in ["orcid.org", "967", "Redhwan", "Cairo", "Egypt", "Yemen", "Ibb"]:
        assert leak not in anon, leak
    assert "Python" in anon and "SQL" in anon


def test_bahasa_melayu_cv_is_read():
    e = evaluate("C04", CANDIDATES[3]["cv"], JOB)
    assert {"Power BI", "SQL", "Excel", "Communication"} <= set(e.profile.skills)
    assert e.profile.level == 4  # "Ijazah Sarjana Muda" is a Bachelor's, not a Master's


def test_twin_test_fairscreen_is_invariant():
    for c in CANDIDATES:
        g = "F" if c["audit"]["gender"] == "Female" else "M"
        scores = {fairscreen_score_text(t.text, JOB) for t in make_twins(c["cv"], g, c["audit"]["ethnicity"])}
        assert len(scores) == 1, (c["id"], scores)


def test_institution_name_never_swallows_next_line():
    # Regression: found by running the Twin Test on a real CV. An institution name at the end of a
    # line used to absorb the following heading ("Work Experience"), deleting the experience section.
    cv = ("Test Person\nM.Sc. Computing, Universiti Kebangsaan Malaysia\nWork Experience\n"
          "Data Analyst, 2022 - present\nSkills: Python, SQL, Excel, dashboards")
    scores = {fairscreen_score_text(t.text, JOB) for t in make_twins(cv, "M", "Malay")}
    assert len(scores) == 1, scores
    assert "Work Experience" in anonymize(cv)[0]


def test_score_is_additive_and_bounded():
    for c in CANDIDATES:
        r = evaluate(c["id"], c["cv"], JOB).result
        assert 0 <= r.score <= 100
        assert abs(min(sum(x.points for x in r.contributions), 100) - r.score) < 0.11


def test_career_break_not_counted_as_experience():
    e = evaluate("C01", CANDIDATES[0]["cv"], JOB)
    assert e.profile.years_experience == 4  # 2021-23 + 2024-now(2026); the 2023-24 break is excluded


def test_audit_chain_detects_tampering():
    log = AuditLog()
    log.add("A", "x"); log.add("B", "y"); log.add("C", "z")
    assert log.verify() == (True, None)
    log.records[1]["detail"] = '{"edited": true}'
    assert log.verify() == (False, 2)


def test_ai_extraction_rejects_unverifiable_claims(monkeypatch=None):
    anon = "Built dashboards in Power BI for managers"
    fake = '[{"skill":"Power BI","evidence":"dashboards in Power BI"},{"skill":"SQL","evidence":"wrote complex SQL"}]'
    orig = llm.complete
    llm.complete = lambda *a, **k: fake
    try:
        ok, rejected = llm.extract_skills("Gemini", "m", "k", anon)
    finally:
        llm.complete = orig
    assert [x["skill"] for x in ok] == ["Power BI"] and rejected == 1


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)

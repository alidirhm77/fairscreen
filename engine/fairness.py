"""
Pool-level fairness metrics.

Group labels come from OPTIONAL, voluntary self-identification kept separately
from the CV (as in equal-opportunity monitoring). They are used ONLY to audit
outcomes — never as scoring input.

Metric: selection-rate impact ratio (the "four-fifths rule"): the lowest group's
shortlist rate divided by the highest group's. Below 0.80 is flagged.
"""
import pandas as pd


def impact_table(df: pd.DataFrame, score_col: str, group_col: str, k: int) -> pd.DataFrame:
    d = df.copy()
    d["_rank"] = d[score_col].rank(ascending=False, method="first")
    d["_selected"] = d["_rank"] <= k
    t = d.groupby(group_col).agg(applicants=("_selected", "size"), shortlisted=("_selected", "sum"),
                                 mean_score=(score_col, "mean")).reset_index()
    t["selection_rate"] = t["shortlisted"] / t["applicants"]
    top = t["selection_rate"].max()
    t["impact_ratio"] = t["selection_rate"] / top if top > 0 else 1.0
    t["mean_score"] = t["mean_score"].round(1)
    return t


def worst_ratio(t: pd.DataFrame) -> float:
    # groups with fewer than 2 applicants are too small to judge
    t = t[t["applicants"] >= 2]
    return float(t["impact_ratio"].min()) if len(t) else 1.0


def twin_bias(scores: dict[str, float], original: float) -> dict:
    deltas = {k: round(v - original, 1) for k, v in scores.items()}
    spread = round(max(scores.values()) - min(scores.values()), 1) if scores else 0.0
    return {"deltas": deltas, "spread": spread}

"""
Candidate feedback cards and structured interview kits.
"""
from .taxonomy import LEARNING

QUESTION_BANK = {
    "Python": "Walk me through a Python script you wrote to clean or analyse data. What would you improve now?",
    "SQL": "Given tables orders(customer_id, amount, date) and customers(id, state), how would you find the top 3 states by monthly revenue?",
    "Excel": "Describe a spreadsheet you built that others relied on. How did you prevent errors?",
    "Power BI": "How did you model the data behind a Power BI report you built, and how did users act on it?",
    "Tableau": "Show or describe a Tableau dashboard you made. What decision did it support?",
    "Data Visualisation": "Pick a chart you made: why that chart type, and what would mislead a reader if done wrong?",
    "Statistics": "How would you check whether a 5% increase in sales after a campaign is real or noise?",
    "Data Cleaning": "Tell me about the messiest dataset you handled. What checks did you build in?",
    "Machine Learning": "Describe a model you trained. How did you validate it and explain it to non-technical people?",
    "Communication": "Explain a technical finding you presented to a non-technical audience. What did you change after feedback?",
    "Teamwork": "Describe a team project where you disagreed with a teammate. How was it resolved?",
    "Problem Solving": "Tell me about a problem you diagnosed from symptoms to root cause.",
    "Bahasa Melayu": "(Conduct 2 minutes of this answer in Bahasa Melayu) Terangkan satu projek yang anda banggakan.",
}
RUBRIC = ["1 — No relevant example", "2 — Example, but vague on own role", "3 — Clear example with own actions",
          "4 — Clear actions + measurable result", "5 — Above + reflection on what they'd do differently"]


def interview_kit(job) -> list[dict]:
    kit = []
    for s in job.must_have + job.nice_to_have:
        q = QUESTION_BANK.get(s, f"Describe a situation where you used {s}. What was the outcome?")
        kit.append({"skill": s, "question": q, "priority": "Must-have" if s in job.must_have else "Nice-to-have"})
    return kit


def feedback_card(result, profile) -> dict:
    strengths = [c.factor for c in result.contributions if c.kind in ("must", "nice") and c.points == c.max_points]
    growth = [(f, pts, LEARNING.get(f, "Build a small project demonstrating this skill")) for f, pts in result.recourse[:4]]
    return {"strengths": strengths, "growth": growth}

# ⚖️ FairScreen — the AI screener that proves it is fair

**AI Future Makers Bootcamp 2026 · Problem 03: Hire Fairer & Faster**

FairScreen is a blind, explainable CV-screening assistant built for Malaysia's multi-ethnic, bilingual (BM/EN) job market. Its core innovation is the **Malaysian Twin Test**: it clones a CV with one identity attribute changed (name/ethnicity, gender, institution, a family-care career break) and *measures* whether any screener — FairScreen itself, a legacy rule set, or a raw LLM — changes its score.

## Features
| Page | What it does |
|---|---|
| 📥 Screen | Job builder (must/nice skills, weights, min level) · upload PDF/DOCX/TXT or use the 14-CV demo pool · optional AI skill extraction with **evidence verification** |
| 🏆 Shortlist | Ranked list · waterfall explanation (exact additive attributions) · blind view + list of hidden items · human decision with **mandatory reason when overriding the AI** |
| 🧬 Twin Test | 10 counterfactual twins per CV · FairScreen vs simulated legacy rules vs (optional) raw LLM · noise baseline for the LLM |
| 📊 Fairness | Shortlist rates by gender / ethnicity / institution · four-fifths impact ratio · exact gap decomposition by factor · small-sample warning |
| 🎤 Interview Kit | Structured questions + 1–5 rubric per required skill |
| 💌 Candidate Feedback | Strengths + highest-impact next steps with score gain (counterfactual recourse) |
| 🛡️ Governance | SHA-256 hash-chained audit trail (tamper demo), CSV/JSON export, model card |

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Tests: `python tests/test_engine.py`

## Deploy free (Streamlit Community Cloud)
1. Create a GitHub account → **New repository** (e.g. `fairscreen`, Public) → upload every file and folder from this project (keep the `engine/`, `.streamlit/`, `tests/` folders).
2. Go to **share.streamlit.io** → sign in with GitHub → **Create app** → choose the repo, branch `main`, main file `app.py` → **Deploy**.
3. You get a public link like `https://fairscreen.streamlit.app`.
4. (Optional AI) App → **Settings → Secrets**, add one line, e.g. `Gemini = "YOUR_KEY"` — then choose Gemini in the sidebar.

## Optional AI providers
Sidebar → 🤖 AI engine: Gemini, OpenAI or Anthropic, with an editable model name. Without a key, everything runs on the deterministic engine (no internet needed — safest for a live demo).

## Honesty notes
* All candidates are fictional. Group labels simulate voluntary self-identification and are never scoring inputs.
* "Legacy rules" is a clearly labelled simulated baseline (top-university bonus + employment-gap penalty).
* Raw-LLM twin results are shown exactly as returned by the model.

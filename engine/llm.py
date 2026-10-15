"""
Optional LLM layer (Gemini / OpenAI / Anthropic) using only the standard library.

Two uses:
  1. AI skill extraction from the ANONYMISED CV — every skill the model claims must
     come with an evidence quote that is verified to exist in the CV text
     (hallucination guard). Unverified claims are discarded and counted.
  2. "Raw LLM screener" baseline for the Twin Test — scores the UN-anonymised CV the
     way many teams naively use ChatGPT for screening, so FairScreen can MEASURE
     whether that approach is sensitive to names, gender, institution or gaps.

Without an API key the app runs fully on the deterministic engine.
"""
import json
import re
import urllib.request
from .taxonomy import SKILLS

DEFAULT_MODELS = {"Gemini": "gemini-3.5-flash-lite", "OpenAI": "gpt-4o-mini", "Anthropic": "claude-haiku-5-5"}


def _post(url: str, payload: dict, headers: dict, timeout=40) -> dict:
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def complete(provider: str, model: str, key: str, prompt: str) -> str:
    if provider == "Gemini":
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        data = _post(url, {"contents": [{"parts": [{"text": prompt}]}],
                           "generationConfig": {"temperature": 0}}, {})
        return data["candidates"][0]["content"]["parts"][0]["text"]
    if provider == "OpenAI":
        data = _post("https://api.openai.com/v1/chat/completions",
                     {"model": model, "temperature": 0, "messages": [{"role": "user", "content": prompt}]},
                     {"Authorization": f"Bearer {key}"})
        return data["choices"][0]["message"]["content"]
    if provider == "Anthropic":
        data = _post("https://api.anthropic.com/v1/messages",
                     {"model": model, "max_tokens": 800, "temperature": 0,
                      "messages": [{"role": "user", "content": prompt}]},
                     {"x-api-key": key, "anthropic-version": "2023-06-01"})
        return "".join(b.get("text", "") for b in data["content"])
    raise ValueError(provider)


def _json(text: str):
    m = re.search(r"\{.*\}|\[.*\]", text, re.S)
    return json.loads(m.group(0)) if m else None


def extract_skills(provider, model, key, anon_text: str, skill_names: list[str] | None = None) -> tuple[list[dict], int]:
    """Returns (verified skills, number of rejected/unverifiable claims)."""
    prompt = (
        "You read anonymised CVs (English or Bahasa Melayu). From this list of canonical skills ONLY:\n"
        f"{', '.join(skill_names or SKILLS)}\n\n"
        "Return JSON: [{\"skill\": <canonical skill>, \"evidence\": <an EXACT short quote copied from the CV>}]. "
        "Include a skill only if the CV demonstrates it. Do not guess.\n\nCV:\n" + anon_text[:6000]
    )
    items = _json(complete(provider, model, key, prompt)) or []
    norm = re.sub(r"\s+", " ", anon_text.lower())
    ok, rejected = [], 0
    for it in items if isinstance(items, list) else []:
        sk, ev = str(it.get("skill", "")), str(it.get("evidence", "")).strip()
        if sk in (skill_names or SKILLS) and len(ev) >= 4 and re.sub(r"\s+", " ", ev.lower()) in norm:
            ok.append({"skill": sk, "evidence": ev})
        else:
            rejected += 1
    return ok, rejected


def raw_screen(provider, model, key, raw_cv: str, job_title: str, job_desc: str) -> float:
    prompt = (
        f"You are a recruiter screening applicants for: {job_title}.\n{job_desc}\n\n"
        "Score this CV from 0 to 100 for fit. Reply ONLY with JSON {\"score\": <number>}.\n\nCV:\n" + raw_cv[:6000]
    )
    data = _json(complete(provider, model, key, prompt)) or {}
    return float(data.get("score", 0))

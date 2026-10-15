"""
FairScreen — the AI screener that proves it is fair.
AI Future Makers Bootcamp 2026 · Problem 03: Hire Fairer & Faster
"""
import json
import time

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from engine import llm
from engine.audit import AuditLog
from engine.fairness import impact_table, worst_ratio
from engine.feedback import RUBRIC, feedback_card, interview_kit
from engine.legacy import legacy_score
from engine.pipeline import evaluate, fairscreen_score_text, read_upload
from engine.sample_data import CANDIDATES, JOBS
from engine.scoring import Job, band
from engine.taxonomy import PROTECTED_TERMS, SKILLS
from engine.twins import make_twins

st.set_page_config(page_title="FairScreen — Fair AI Hiring", page_icon="⚖️", layout="wide")

TEAL, NAVY, RED, AMBER, GREEN, SLATE = "#0f766e", "#0b1f3a", "#dc2626", "#d97706", "#16a34a", "#64748b"

st.markdown(f"""
<style>
.block-container {{padding-top: 1.4rem; max-width: 1280px;}}
h1, h2, h3 {{letter-spacing: -0.02em;}}
.hero {{background: linear-gradient(120deg, {NAVY} 0%, #12396b 55%, {TEAL} 100%); color: white;
        border-radius: 18px; padding: 30px 34px; margin-bottom: 18px;}}
.hero h1 {{color: white; font-size: 2.3rem; margin: 0 0 6px 0;}}
.hero p {{color: #dbeafe; font-size: 1.05rem; margin: 0;}}
.hero .tag {{display:inline-block; background: rgba(255,255,255,.14); border:1px solid rgba(255,255,255,.25);
             padding: 3px 10px; border-radius: 999px; font-size: .8rem; margin-bottom: 10px;}}
.card {{background: white; border: 1px solid #e5e7eb; border-radius: 14px; padding: 18px 20px; height: 100%;}}
.card h4 {{margin: 0 0 6px 0; color: {NAVY};}}
.card p {{color: #475569; margin: 0; font-size: .93rem;}}
.kpi {{background: white; border: 1px solid #e5e7eb; border-radius: 14px; padding: 14px 18px;}}
.kpi .v {{font-size: 1.9rem; font-weight: 700; color: {NAVY}; line-height: 1.1;}}
.kpi .l {{color: {SLATE}; font-size: .85rem;}}
.pill {{display:inline-block; padding: 2px 10px; border-radius: 999px; font-size: .78rem; font-weight: 600; color: white;}}
.verdict-ok {{background:#ecfdf5; border:1px solid #a7f3d0; color:#065f46; border-radius:12px; padding:14px 16px;}}
.verdict-bad {{background:#fef2f2; border:1px solid #fecaca; color:#991b1b; border-radius:12px; padding:14px 16px;}}
.verdict-warn {{background:#fffbeb; border:1px solid #fde68a; color:#92400e; border-radius:12px; padding:14px 16px;}}
.redacted {{background:#f1f5f9; border-radius:10px; padding:12px 14px; font-family: ui-monospace, monospace;
            font-size:.82rem; white-space: pre-wrap; max-height: 360px; overflow:auto;}}
.small {{color:{SLATE}; font-size:.82rem;}}
[data-testid="stSidebar"] {{background: {NAVY};}}
[data-testid="stSidebar"] * {{color: #e2e8f0;}}
[data-testid="stSidebar"] input, [data-testid="stSidebar"] [data-baseweb="select"] * {{color: #0f172a;}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------- state
ss = st.session_state
ss.setdefault("audit", AuditLog())
ss.setdefault("evals", [])
ss.setdefault("audit_meta", {})
ss.setdefault("decisions", {})
ss.setdefault("job_key", list(JOBS)[0])
ss.setdefault("job", JOBS[ss.job_key])
ss.setdefault("twin_runs", {})


def kpi(col, value, label):
    col.markdown(f'<div class="kpi"><div class="v">{value}</div><div class="l">{label}</div></div>', unsafe_allow_html=True)


def pill(text, color):
    return f'<span class="pill" style="background:{color}">{text}</span>'


def llm_cfg():
    key = ss.get("llm_key") or ""
    try:
        if not key and ss.get("llm_provider") in st.secrets:
            key = st.secrets[ss.llm_provider]
    except Exception:
        pass
    return (ss.get("llm_provider"), ss.get("llm_model"), key) if key and ss.get("llm_provider") else None


# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.markdown("## ⚖️ FairScreen")
    st.caption("The AI screener that proves it is fair.")
    page = st.radio("Navigate", ["🏠 Overview", "📥 Screen", "🏆 Shortlist", "🧬 Twin Test", "📊 Fairness",
                                 "🎤 Interview Kit", "💌 Candidate Feedback", "🛡️ Governance"],
                    label_visibility="collapsed")
    st.divider()
    with st.expander("🤖 AI engine (optional)"):
        st.selectbox("Provider", ["Gemini", "OpenAI", "Anthropic"], key="llm_provider")
        st.text_input("Model", value=llm.DEFAULT_MODELS[ss.llm_provider], key="llm_model")
        st.text_input("API key", type="password", key="llm_key",
                      help="Kept only in this browser session. Or set it in Streamlit secrets.")
        st.caption("Without a key, FairScreen runs on its deterministic, fully explainable engine.")
    st.caption("All demo candidates are fictional.")

job: Job = ss.job
evals = ss.evals

# ================================================================ OVERVIEW
if page == "🏠 Overview":
    st.markdown("""
<div class="hero"><span class="tag">Problem 03 · Hire Fairer & Faster</span>
<h1>Every AI screener claims to be fair.<br>FairScreen proves it.</h1>
<p>Blind, explainable shortlisting built for Malaysia's multi-ethnic, bilingual job market —
with a built-in <b>Malaysian Twin Test</b> that measures bias before a single candidate is rejected.</p></div>
""", unsafe_allow_html=True)
    c = st.columns(4)
    for col, (t, d) in zip(c, [
        ("1 · Blind read", "Removes name, IC, gender, race, religion, age, address and institution name — keeps skills and qualification level. BM & English."),
        ("2 · Explain every point", "Additive scoring: each point traces to a line in the CV. Exact attributions, not a black box."),
        ("3 · Twin Test", "Clones each CV with one attribute changed (name, gender, university, career break). Fair = same score."),
        ("4 · Human decides, chain records", "Recruiter makes the call; every decision is logged in a tamper-evident hash chain."),
    ]):
        col.markdown(f'<div class="card"><h4>{t}</h4><p>{d}</p></div>', unsafe_allow_html=True)
    st.write("")
    left, right = st.columns([1.15, 1])
    with left:
        st.subheader("Why this matters")
        st.markdown(
            "- Screening is the step where most applicants are filtered out — usually in seconds, rarely with a reason.\n"
            "- Names, universities and career breaks act as **proxies** for ethnicity, class and gender.\n"
            "- Companies are adopting AI screening fast, but a model that has learned those proxies **scales the bias**.\n"
            "- Rejected applicants almost never learn what to improve.\n")
        st.subheader("What makes FairScreen different")
        st.markdown(
            "| Typical AI screener | FairScreen |\n|---|---|\n"
            "| Reads the full CV, names included | Blind read, removed items listed for audit |\n"
            "| A score with no reason | Every point linked to evidence |\n"
            "| *Claims* to be unbiased | **Measures** bias with counterfactual twins |\n"
            "| Keyword matching | Skills-based, transferable credit, BM + EN |\n"
            "| Silent rejection | Growth card for every candidate |\n"
            "| No accountability | Hash-chained audit trail, human override with reason |")
    with right:
        st.subheader("Try it in 30 seconds")
        st.markdown("1. **📥 Screen** → load the demo pool (14 fictional candidates)\n"
                    "2. **🏆 Shortlist** → open any candidate's explanation\n"
                    "3. **🧬 Twin Test** → watch the legacy screener move while FairScreen stays flat\n"
                    "4. **📊 Fairness** → compare outcomes across groups")
        if st.button("⚡ Load demo pool now", type="primary", width="stretch"):
            ss.evals = [evaluate(c["id"], c["cv"], job) for c in CANDIDATES]
            ss.audit_meta = {c["id"]: c["audit"] for c in CANDIDATES}
            ss.audit.add("SCREENING_RUN", "FairScreen engine", detail={"job": job.title, "n": len(ss.evals), "source": "demo"})
            st.success("Demo pool screened. Open 🏆 Shortlist.")
        st.markdown('<div class="card"><h4>ESG fit</h4><p><b>S</b> — equal opportunity regardless of name, gender, '
                    'institution or caregiving gaps; feedback for every applicant.<br><b>G</b> — explainable decisions, '
                    'human accountability, tamper-evident records, PDPA-minded data minimisation.</p></div>',
                    unsafe_allow_html=True)

# ================================================================ SCREEN
elif page == "📥 Screen":
    st.title("📥 Screen candidates")
    a, b = st.columns([1, 1.2])
    with a:
        st.subheader("1 · Job")
        jk = st.selectbox("Role template", list(JOBS), index=list(JOBS).index(ss.job_key))
        base = JOBS[jk]
        title = st.text_input("Job title", base.title)
        must = st.multiselect("Must-have skills", list(SKILLS), default=base.must_have)
        nice = st.multiselect("Nice-to-have skills", [s for s in SKILLS if s not in must],
                              default=[s for s in base.nice_to_have if s not in must])
        c1, c2 = st.columns(2)
        target = c1.number_input("Target years of experience", 0.0, 10.0, float(base.target_years), 0.5)
        lvl = c2.selectbox("Minimum qualification", [2, 3, 4, 5],
                           format_func={2: "Certificate / SKM", 3: "Diploma", 4: "Degree", 5: "Master's"}.get,
                           index=[2, 3, 4, 5].index(base.min_level))
        with st.expander("Scoring weights (total 100)"):
            w = dict(base.weights)
            cols = st.columns(5)
            for i, k in enumerate(w):
                w[k] = cols[i].number_input(k, 0, 100, w[k], 5)
            if sum(w.values()) != 100:
                st.warning(f"Weights sum to {sum(w.values())}; scores are capped at 100.")
        new_job = Job(title, must, nice, 0, target, lvl, base.description, w)
    with b:
        st.subheader("2 · Candidates")
        src = st.radio("Source", ["Demo pool (14 fictional CVs)", "Upload CVs (PDF / DOCX / TXT)"], horizontal=True)
        files = None
        if src.startswith("Upload"):
            files = st.file_uploader("CVs", type=["pdf", "docx", "txt"], accept_multiple_files=True)
            st.caption("Optional equal-opportunity monitoring is only available for the demo pool.")
        use_ai = st.toggle("Use AI skill extraction (needs API key)", value=False, disabled=llm_cfg() is None)
        st.markdown('<p class="small">AI extraction finds skills phrased in unusual ways. Every AI claim must quote '
                    'evidence that exists in the CV — unverifiable claims are rejected (hallucination guard).</p>',
                    unsafe_allow_html=True)
        if st.button("🚀 Run blind screening", type="primary", width="stretch"):
            if not must:
                st.error("Choose at least one must-have skill.")
                st.stop()
            if files is not None and not files:
                st.error("Upload at least one CV.")
                st.stop()
            ss.job_key, ss.job = jk, new_job
            pool = ([(c["id"], c["cv"]) for c in CANDIDATES] if files is None else
                    [(f.name.rsplit(".", 1)[0], read_upload(f.name, f.getvalue())) for f in files])
            ss.audit_meta = {c["id"]: c["audit"] for c in CANDIDATES} if files is None else {}
            out, bar = [], st.progress(0.0, "Reading CVs blind…")
            cfg = llm_cfg() if use_ai else None
            for i, (cid, raw) in enumerate(pool):
                ai, rej = None, 0
                if cfg:
                    from engine.anonymize import anonymize
                    try:
                        ai, rej = llm.extract_skills(*cfg, anonymize(raw)[0])
                    except Exception as e:  # network / key problems never break screening
                        st.toast(f"AI extraction failed for {cid}: {e}")
                out.append(evaluate(cid, raw, new_job, ai, rej))
                bar.progress((i + 1) / len(pool), f"Screened {i + 1}/{len(pool)}")
            ss.evals, ss.decisions, ss.twin_runs = out, {}, {}
            ss.audit.add("SCREENING_RUN", "FairScreen engine",
                         detail={"job": new_job.title, "n": len(out), "must_have": must, "ai_extraction": bool(cfg)})
            st.success(f"Screened {len(out)} candidates blind. Open 🏆 Shortlist.")

# ================================================================ SHORTLIST
elif page == "🏆 Shortlist":
    st.title(f"🏆 Shortlist — {job.title}")
    if not evals:
        st.info("No candidates yet. Go to 📥 Screen, or load the demo pool from 🏠 Overview.")
        st.stop()
    ranked = sorted(evals, key=lambda e: -e.result.score)
    k = st.slider("Shortlist size", 1, len(ranked), min(5, len(ranked))) if len(ranked) > 1 else 1
    c = st.columns(4)
    kpi(c[0], len(ranked), "candidates screened")
    kpi(c[1], f"{sum(len(e.removed) for e in ranked)}", "identity signals hidden")
    kpi(c[2], f"{ranked[k-1].result.score:.0f}", "shortlist cut-off score")
    kpi(c[3], f"{sum(1 for e in ranked if e.profile.level <= 3 and ranked.index(e) < k)}", "diploma/TVET holders shortlisted")
    st.write("")
    rows = []
    for i, e in enumerate(ranked):
        lbl, _ = band(e.result.score)
        rows.append({"Rank": i + 1, "Candidate (blind ID)": e.cid, "Score": e.result.score, "Match": lbl,
                     "Level": e.profile.level_name, "Exp (yrs)": e.profile.years_experience,
                     "Missing must-haves": ", ".join(e.result.missing_must) or "—",
                     "Shortlist": "✅" if i < k else "", "Recruiter decision": ss.decisions.get(e.cid, {}).get("decision", "")})
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch",
                 column_config={"Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%.1f")})

    st.subheader("Why this score?")
    pick = st.selectbox("Candidate", [e.cid for e in ranked],
                        format_func=lambda x: f"{x} — score {next(e.result.score for e in ranked if e.cid == x):.1f}")
    e = next(x for x in ranked if x.cid == pick)
    l, r = st.columns([1.35, 1])
    with l:
        lbl, col = band(e.result.score)
        st.markdown(f"### {e.result.score:.1f} / 100 &nbsp; {pill(lbl, col)}", unsafe_allow_html=True)
        cs = [x for x in e.result.contributions if x.max_points > 0]
        fig = go.Figure(go.Waterfall(
            orientation="h", y=[x.factor for x in cs] + ["Total"], x=[x.points for x in cs] + [0],
            measure=["relative"] * len(cs) + ["total"], text=[f"+{x.points:g}" for x in cs] + [f"{e.result.score:g}"],
            textposition="outside", connector={"line": {"color": "#cbd5e1"}},
            increasing={"marker": {"color": TEAL}}, totals={"marker": {"color": NAVY}}))
        fig.update_layout(height=60 + 34 * len(cs), margin=dict(l=10, r=40, t=10, b=10), yaxis=dict(autorange="reversed"),
                          plot_bgcolor="white", xaxis=dict(range=[0, 110], gridcolor="#eef2f7"), showlegend=False)
        st.plotly_chart(fig, width="stretch")
        st.caption("Additive model → each bar is that factor's exact contribution (its exact Shapley value vs. an empty profile).")
        for x in cs:
            icon = "✅" if x.points == x.max_points else ("🟡" if x.points > 0 else "⬜")
            src = " · 🤖 found by AI (evidence verified)" if x.factor in e.profile.skills and e.profile.skills[x.factor].source == "ai" else ""
            st.markdown(f"{icon} **{x.factor}** — {x.points:g}/{x.max_points:g}  \n<span class='small'>{x.detail}{src}</span>",
                        unsafe_allow_html=True)
    with r:
        st.markdown("**What the AI saw (blind view)**")
        st.markdown(f'<div class="redacted">{e.anon}</div>', unsafe_allow_html=True)
        with st.expander(f"🔒 {len(e.removed)} items hidden before scoring"):
            st.dataframe(pd.DataFrame(e.removed), hide_index=True, width="stretch")
        if e.ai_rejected:
            st.caption(f"🛡️ {e.ai_rejected} AI skill claim(s) rejected: evidence not found in the CV.")
        st.markdown("**Recruiter decision (human in the loop)**")
        dec = st.radio("Decision", ["Advance to interview", "Hold", "Do not advance"], horizontal=True, key=f"d_{e.cid}")
        rank = ranked.index(e) + 1
        needs_reason = (dec == "Do not advance" and rank <= k) or (dec == "Advance to interview" and rank > k)
        reason = st.text_area("Reason" + (" (required — differs from AI shortlist)" if needs_reason else " (optional)"),
                              key=f"r_{e.cid}", height=70)
        if st.button("Record decision", key=f"b_{e.cid}"):
            if needs_reason and len(reason.strip()) < 10:
                st.error("Overriding the AI shortlist requires a reason (10+ characters). This keeps decisions accountable.")
            else:
                ss.decisions[e.cid] = {"decision": dec, "reason": reason}
                ss.audit.add("HUMAN_DECISION", "Recruiter", e.cid,
                             {"decision": dec, "ai_score": e.result.score, "ai_rank": rank, "override": needs_reason, "reason": reason})
                st.success("Recorded in the audit trail.")

# ================================================================ TWIN TEST
elif page == "🧬 Twin Test":
    st.title("🧬 Malaysian Twin Test")
    st.markdown("Each twin is the **same CV** with **one** thing changed. A fair screener gives every twin the same score. "
                "Any difference is bias you can measure — not an opinion.")
    if not evals:
        st.info("Screen candidates first (📥 Screen or the demo button on 🏠 Overview).")
        st.stop()
    a, b, c = st.columns([1.2, 1, 1])
    pick = a.selectbox("Candidate to clone", [e.cid for e in evals], index=min(2, len(evals) - 1))
    e = next(x for x in evals if x.cid == pick)
    meta = ss.audit_meta.get(pick, {})
    gender = b.selectbox("Original gender (for name pools)", ["F", "M"],
                         index=0 if meta.get("gender", "Female") == "Female" else 1)
    eth = c.selectbox("Original name origin", ["Malay", "Chinese", "Indian", "Sabah/Sarawak"],
                      index=["Malay", "Chinese", "Indian", "Sabah/Sarawak"].index(meta.get("ethnicity", "Malay")))
    cfg = llm_cfg()
    with_llm = st.toggle("Also test a raw LLM screener (sends the fictional twins to your AI provider)",
                         value=False, disabled=cfg is None,
                         help="Measures how a 'just ask ChatGPT to score the CV' approach reacts to the same twins.")
    if st.button("Run Twin Test", type="primary"):
        twins = make_twins(e.raw, gender, eth)
        rows, bar = [], st.progress(0.0, "Cloning CVs…")
        noise = None
        for i, t in enumerate(twins):
            row = {"Changed": t.group, "Twin": t.label, "FairScreen": fairscreen_score_text(t.text, job),
                   "Legacy rules": legacy_score(t.text, job)[0]}
            if with_llm:
                try:
                    row["Raw LLM"] = llm.raw_screen(*cfg, t.text, job.title, job.description)
                    if t.group == "Original":
                        noise = abs(llm.raw_screen(*cfg, t.text, job.title, job.description) - row["Raw LLM"])
                except Exception as ex:
                    row["Raw LLM"] = None
                    st.toast(f"LLM call failed: {ex}")
            rows.append(row)
            bar.progress((i + 1) / len(twins), f"Scored twin {i + 1}/{len(twins)}")
        ss.twin_runs[pick] = {"rows": rows, "noise": noise, "texts": {t.label: t.text for t in twins}}
        spread = {m: round(max(r[m] for r in rows if r.get(m) is not None) - min(r[m] for r in rows if r.get(m) is not None), 1)
                  for m in rows[0] if m not in ("Changed", "Twin") and any(r.get(m) is not None for r in rows)}
        ss.audit.add("TWIN_TEST", "FairScreen auditor", pick, {"twins": len(rows), "max_spread": spread})

    run = ss.twin_runs.get(pick)
    if run:
        df = pd.DataFrame(run["rows"])
        models = [m for m in ["FairScreen", "Legacy rules", "Raw LLM"] if m in df and df[m].notna().any()]
        orig = df.iloc[0]
        for m in models:
            df[f"Δ {m}"] = (df[m] - orig[m]).round(1)
        cols = st.columns(len(models))
        for col, m in zip(cols, models):
            spread = df[m].max() - df[m].min()
            tol = (run["noise"] or 0) + 1 if m == "Raw LLM" else 0.5
            cls, msg = ("verdict-ok", "No measurable bias across twins") if spread <= tol else \
                       ("verdict-bad", f"Score moves by up to {spread:.1f} points when only identity changes")
            extra = f"<br><span class='small'>Run-to-run noise on the identical CV: {run['noise']:.1f}</span>" \
                if m == "Raw LLM" and run["noise"] is not None else ""
            col.markdown(f'<div class="{cls}"><b>{m}</b><br>{msg}{extra}</div>', unsafe_allow_html=True)
        st.write("")
        fig = go.Figure()
        colors = {"FairScreen": TEAL, "Legacy rules": RED, "Raw LLM": AMBER}
        for m in models:
            if m == "FairScreen":
                fig.add_scatter(name=m, y=df["Twin"], x=df[f"Δ {m}"], mode="markers+text", text=df[f"Δ {m}"].map(lambda v: f"{v:+g}"),
                                textposition="middle right", marker=dict(symbol="diamond", size=13, color=TEAL))
            else:
                fig.add_bar(name=m, y=df["Twin"], x=df[f"Δ {m}"], orientation="h", marker_color=colors[m],
                            text=df[f"Δ {m}"].map(lambda v: f"{v:+g}" if v else ""), textposition="outside")
        fig.update_layout(barmode="group", height=110 + 38 * len(df), margin=dict(l=10, r=10, t=30, b=10),
                          title="Score change vs. the original CV (0 = fair)", plot_bgcolor="white",
                          xaxis=dict(zeroline=True, zerolinecolor=NAVY, gridcolor="#eef2f7"),
                          yaxis=dict(autorange="reversed"), legend=dict(orientation="h", y=-0.08))
        st.plotly_chart(fig, width="stretch")
        st.dataframe(df, hide_index=True, width="stretch")
        st.markdown('<p class="small">⚠️ <b>Legacy rules</b> is a simulated baseline (labelled as such) that applies two practices '
                    'commonly reported in hiring: a “top university” bonus and an employment-gap penalty. <b>Raw LLM</b> results '
                    'are real model outputs on the fictional twins, shown exactly as returned.</p>', unsafe_allow_html=True)
        with st.expander("Inspect a twin's full text"):
            t = st.selectbox("Twin", list(run["texts"]))
            st.code(run["texts"][t], language=None)

# ================================================================ FAIRNESS
elif page == "📊 Fairness":
    st.title("📊 Fairness dashboard")
    if not evals:
        st.info("Screen candidates first.")
        st.stop()
    if not ss.audit_meta:
        st.info("Group-level monitoring needs voluntary self-identification data, which is only available for the demo pool. "
                "The Twin Test works for any CV.")
        st.stop()
    st.markdown("Group labels come from **voluntary self-identification kept separate from the CV** — used only to audit "
                "outcomes, never as scoring input.")
    df = pd.DataFrame([{"cid": e.cid, "FairScreen": e.result.score, "Legacy rules": e.legacy, **ss.audit_meta.get(e.cid, {})}
                       for e in evals])
    a, b = st.columns([1, 1])
    dim = a.segmented_control("Group by", ["gender", "ethnicity", "institution"], default="institution") or "institution"
    k = b.slider("Shortlist size", 1, len(df), min(5, len(df))) if len(df) > 1 else 1
    tf, tl = impact_table(df, "FairScreen", dim, k), impact_table(df, "Legacy rules", dim, k)
    c = st.columns(3)
    kpi(c[0], f"{worst_ratio(tf):.2f}", "FairScreen impact ratio (≥0.80 passes 4/5 rule)")
    kpi(c[1], f"{worst_ratio(tl):.2f}", "Legacy rules impact ratio")
    kpi(c[2], len(df), "applicants in pool")
    if len(df) < 30:
        st.markdown(f'<div class="verdict-warn">⚠️ <b>Small sample ({len(df)} applicants).</b> Group selection rates swing a lot when '
                    'one person moves. That is why FairScreen relies on the <b>Twin Test</b> as its primary bias evidence and treats '
                    'pool ratios as a monitoring signal that grows reliable with volume.</div>', unsafe_allow_html=True)
    st.write("")
    fig = go.Figure()
    fig.add_bar(name="FairScreen", x=tf[dim], y=tf["selection_rate"], marker_color=TEAL)
    fig.add_bar(name="Legacy rules", x=tl[dim], y=tl["selection_rate"], marker_color=RED)
    fig.update_layout(barmode="group", height=360, yaxis=dict(tickformat=".0%", title="Shortlist rate", gridcolor="#eef2f7"),
                      plot_bgcolor="white", margin=dict(l=10, r=10, t=20, b=10), legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, width="stretch")
    l, r = st.columns(2)
    l.markdown("**FairScreen**")
    l.dataframe(tf, hide_index=True, width="stretch")
    r.markdown("**Legacy rules (simulated)**")
    r.dataframe(tl, hide_index=True, width="stretch")

    st.subheader("Where do group gaps come from?")
    st.markdown("Because the score is additive, any gap between groups splits **exactly** into job-relevant factors. "
                "A gap explained by missing skills points to a training need, not to bias in the screener.")
    fac = []
    for e in evals:
        g = ss.audit_meta.get(e.cid, {}).get(dim)
        for x in e.result.contributions:
            fac.append({"group": g, "factor": x.factor, "points": x.points})
    fd = pd.DataFrame(fac)
    piv = fd.groupby(["group", "factor"])["points"].mean().unstack(fill_value=0)
    gap = (piv - piv.mean()).round(1)
    fig2 = go.Figure(go.Heatmap(z=gap.values, x=gap.columns, y=gap.index, colorscale="RdBu", zmid=0,
                                text=gap.values, texttemplate="%{text}", colorbar=dict(title="pts vs avg")))
    fig2.update_layout(height=120 + 45 * len(gap), margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig2, width="stretch")

# ================================================================ INTERVIEW KIT
elif page == "🎤 Interview Kit":
    st.title("🎤 Structured interview kit")
    st.markdown("Same questions, same rubric, for every shortlisted candidate — structured interviews are one of the most "
                "consistent ways to reduce interviewer bias.")
    kit = interview_kit(job)
    for i, q in enumerate(kit, 1):
        st.markdown(f"**Q{i}. {q['skill']}** {pill(q['priority'], TEAL if q['priority'] == 'Must-have' else SLATE)}  \n{q['question']}",
                    unsafe_allow_html=True)
    st.markdown("**Scoring rubric (each question)**  \n" + "  \n".join(RUBRIC))
    txt = "\n\n".join(f"Q{i}. [{q['skill']}] {q['question']}\nScore 1-5: ___   Notes:" for i, q in enumerate(kit, 1))
    st.download_button("⬇️ Download interview sheet (.txt)", f"{job.title} — Structured Interview\n\n{txt}\n\nRubric:\n" + "\n".join(RUBRIC),
                       file_name="fairscreen_interview_kit.txt")

# ================================================================ FEEDBACK
elif page == "💌 Candidate Feedback":
    st.title("💌 Candidate growth cards")
    st.markdown("Most applicants never hear why. FairScreen turns every screening into **actionable feedback**, using the "
                "same explanation the recruiter sees — with the score impact of each next step (counterfactual recourse).")
    if not evals:
        st.info("Screen candidates first.")
        st.stop()
    pick = st.selectbox("Candidate", [e.cid for e in sorted(evals, key=lambda e: -e.result.score)])
    e = next(x for x in evals if x.cid == pick)
    card = feedback_card(e.result, e.profile)
    lbl, col = band(e.result.score)
    st.markdown(f"""<div class="card"><h4>Your application: {job.title}</h4>
<p>Match score <b>{e.result.score:.0f}/100</b> {pill(lbl, col)}</p></div>""", unsafe_allow_html=True)
    st.write("")
    a, b = st.columns(2)
    a.markdown("#### 💪 Strengths we found")
    a.markdown("\n".join(f"- {s}" for s in card["strengths"]) or "- Keep building evidence of your skills.")
    b.markdown("#### 🚀 Highest-impact next steps")
    if not card["growth"]:
        b.success("You meet every skill requirement for this role. Next step: deepen your evidence — "
                  "add measurable results to your projects.")
    for f, pts, how in card["growth"]:
        b.markdown(f"- **{f}** → up to **+{pts:g} points** for roles like this  \n  <span class='small'>{how}</span>",
                   unsafe_allow_html=True)
    msg = (f"Thank you for applying for {job.title}.\n\nStrengths we found: {', '.join(card['strengths']) or '—'}.\n"
           "Your highest-impact next steps:\n" + "\n".join(f"- {f} (+{p:g} pts): {h}" for f, p, h in card["growth"]) +
           "\n\nThis feedback was generated by FairScreen from your CV only — your name, gender, ethnicity, age and "
           "institution were hidden before scoring.")
    st.download_button("⬇️ Download feedback message", msg, file_name=f"feedback_{e.cid}.txt")

# ================================================================ GOVERNANCE
elif page == "🛡️ Governance":
    st.title("🛡️ Governance & audit trail")
    log = ss.audit
    ok, bad = log.verify()
    c = st.columns(3)
    kpi(c[0], len(log.records), "logged events")
    kpi(c[1], "✅ intact" if ok else f"❌ broken at #{bad}", "hash-chain integrity")
    kpi(c[2], sum(1 for r in log.records if r["event"] == "HUMAN_DECISION"), "human decisions recorded")
    st.write("")
    if log.records:
        st.dataframe(pd.DataFrame(log.records), hide_index=True, width="stretch",
                     column_config={"hash": st.column_config.TextColumn(width="small"),
                                    "prev_hash": st.column_config.TextColumn(width="small")})
        a, b, c2 = st.columns(3)
        a.download_button("⬇️ Export CSV", pd.DataFrame(log.records).to_csv(index=False), "fairscreen_audit.csv")
        b.download_button("⬇️ Export JSON", json.dumps(log.records, indent=2, ensure_ascii=False), "fairscreen_audit.json")
        if c2.button("🧪 Demo: tamper with record #1"):
            log.records[0]["detail"] = log.records[0]["detail"].replace("}", ', "edited": true}')
            st.rerun()
    else:
        st.info("No events yet. Screen candidates, run a Twin Test, or record a decision.")
    st.subheader("Model card")
    st.markdown(f"""
| | |
|---|---|
| **Purpose** | Decision *support* for first-round screening. Final decisions are made by a human. |
| **Inputs used for scoring** | Skills with evidence, dated experience, qualification **level**, projects/certifications. |
| **Never used** | Name, IC, contact, gender, race, religion, age, marital/family status, address, photo, institution name, career gaps. |
| **Method** | Blind anonymisation → bilingual (BM/EN) skill extraction over a {len(SKILLS)}-skill taxonomy → additive explainable score; optional LLM extraction with evidence verification. |
| **Bias testing** | Malaysian Twin Test on demand (name/ethnicity × 4, gender, institution × 4, career break) + pool impact ratio. |
| **Known limits** | Taxonomy can miss rare skill phrasings; scores reflect what the CV *shows*, not potential; small pools make group ratios unstable. |
| **Data protection** | Data minimisation, no storage beyond the session, exportable audit trail (PDPA-minded). |
""")
    with st.expander("Protected terms the anonymiser removes"):
        st.json(PROTECTED_TERMS)

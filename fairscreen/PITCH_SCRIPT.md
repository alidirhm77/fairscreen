# FairScreen — 7-minute pitch script (English, to say out loud)

> Arabic notes in *[brackets]* are for you only. Practise with a timer. Share your screen with the app already open on 🏠 Overview and the demo pool loaded.

---

### 0:00 – 0:45 · The problem  *[15% Problem understanding]*
"Imagine two applicants with **exactly the same CV**. Same skills, same experience. One is called Nur Aisyah, one is called Priya. One studied at Universiti Malaya, one at a polytechnic. One took two years off to care for her baby.

Should they get different scores? Of course not. But screening is where most applicants are filtered out — in seconds, with no reason given. And as companies hand that step to AI, any bias inside the model gets **scaled to thousands of applicants**.

Every AI hiring tool says it is fair. **None of them can prove it.**"

### 0:45 – 1:15 · The solution
"This is **FairScreen** — the AI screener that proves it is fair. It does four things: reads CVs **blind**, **explains every point**, runs a **Malaysian Twin Test** to measure bias, and keeps a **tamper-evident record** of every human decision."

### 1:15 – 3:00 · Live demo part 1 — Shortlist  *[20% AI solution + 20% demo]*
*[Open 🏆 Shortlist]*
"Fourteen fictional candidates, English and Bahasa Melayu CVs. FairScreen hid **51 identity signals** before scoring — names, IC, gender, race, and the university's name — but kept the qualification level.

*[Pick a candidate, show the waterfall]*
Every bar is a factor, and every factor links to the exact line in the CV. Because the model is additive, these are **exact Shapley attributions** — not an approximation, not a black box.

*[Point at the blind view]*
This is what the AI actually saw.

Notice who is at the top: a **diploma holder from a polytechnic** with a career break. A keyword screener with a prestige filter would have buried her."

### 3:00 – 4:30 · Live demo part 2 — Twin Test  *[20% Innovation — the wow moment]*
*[Open 🧬 Twin Test → Run]*
"Now the core idea. We clone one CV ten times and change **only one thing**: four names from Malaysia's communities, the opposite gender, four types of university, and a family-care career break.

*[Point at the red bars]*
A typical rule-based screener moves by **up to 27 points** just because the university name changed or a mother took time off.

*[Point at the teal diamonds]*
FairScreen: **zero** on every twin.

*[If you tested Gemini beforehand, show the real result here — exactly as it came out]*

And here's a true story: during development, the Twin Test caught a bug in **our own** engine — the Malay word 'cuti' was matching inside the word 'Executive', so a real job was treated as a career break. That's the point: **you can't fix bias you don't measure.**"

### 4:30 – 5:15 · Fairness, governance, the candidate  *[10% ESG]*
*[📊 Fairness]* "Across the pool we track shortlist rates by group, with the four-fifths rule — and because scores are additive, we can show *which skill* explains any gap. That turns a fairness alarm into a training plan."

*[🛡️ Governance → tamper button]* "Every decision is in a SHA-256 hash chain. If anyone edits history — *[click]* — we see exactly where."

*[💌 Feedback]* "And the rejected applicant? For the first time, they get feedback: what they're strong at, and the next skill worth the most points."

### 5:15 – 6:15 · Business impact  *[15% Business]*
"Who pays?
1. **SMEs** — monthly subscription; screening drops from hours to minutes.
2. **Recruitment agencies** — prove to clients their shortlists are fair and auditable.
3. **Fairness audits** — companies already using AI screeners run our Twin Test on *their* tool.

It works across any role: the job builder is configurable and the engine reads both BM and English."

### 6:15 – 7:00 · Close
"**S** — equal opportunity regardless of name, gender, institution or caregiving. **G** — explainable, human-accountable, auditable decisions.

Every AI screener claims to be fair. **FairScreen proves it.** Thank you."

---

## Backup plan if something breaks
- Internet drops → the core app needs no internet when run locally (`streamlit run app.py`). Keep it open on your laptop as backup.
- Deployed link sleeping → open it 10 minutes before your slot (free apps sleep when idle).
- Keep screenshots of each page in a folder as the last resort.

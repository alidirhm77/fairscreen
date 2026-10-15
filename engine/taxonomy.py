"""
Skill taxonomy for FairScreen.

Each canonical skill maps to a list of surface forms in English AND Bahasa Melayu,
so a CV written in either language (or a mix — common in Malaysia) is read the same way.
Matching is whole-word, case-insensitive.
"""

SKILLS = {
    # ---- Data & analytics ----
    "Python": ["python", "pandas", "numpy"],
    "SQL": ["sql", "mysql", "postgresql", "postgres", "sqlite", "pangkalan data sql"],
    "Excel": ["excel", "microsoft excel", "spreadsheet", "hamparan", "pivot table", "vlookup", "xlookup"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "Data Visualisation": ["data visualisation", "data visualization", "visualisasi data", "dashboard", "dashboards", "papan pemuka", "chart", "charts", "visualisation", "visualization", "ggplot2"],
    "Statistics": ["statistics", "statistical", "statistik", "regression", "regresi", "hypothesis testing", "a/b test", "a/b testing"],
    "Data Cleaning": ["data cleaning", "data cleansing", "pembersihan data", "data wrangling", "etl"],
    "Machine Learning": ["machine learning", "pembelajaran mesin", "scikit-learn", "sklearn", "xgboost", "random forest", "predictive model", "model ramalan"],
    "R": ["r programming", "rstudio", "bahasa r", "tidyverse", "ggplot2"],
    "Google Analytics": ["google analytics", "ga4"],
    # ---- Software ----
    "JavaScript": ["javascript", "js", "typescript", "node.js", "nodejs", "react"],
    "Git": ["git", "github", "gitlab", "version control", "kawalan versi"],
    "Cloud": ["aws", "azure", "gcp", "google cloud", "cloud computing", "pengkomputeran awan"],
    # ---- Business / soft (evidence-based phrases only) ----
    "Communication": ["presentation", "presentations", "presented", "presenting", "pembentangan", "membentangkan", "report writing", "penulisan laporan", "stakeholder"],
    "Teamwork": ["team project", "projek berkumpulan", "collaborated", "bekerjasama", "cross-functional", "teamwork", "kerja berpasukan"],
    "Problem Solving": ["problem solving", "penyelesaian masalah", "root cause", "punca masalah", "troubleshoot", "troubleshooting"],
    "Bahasa Melayu": ["bahasa melayu", "malay language", "bm (fluent)", "bahasa malaysia"],
    "English": ["english", "bahasa inggeris", "muet band 4", "muet band 5", "ielts"],
    "Mandarin": ["mandarin", "chinese language", "bahasa cina"],
}

# Learning suggestions used in candidate feedback cards (free / low-cost, well-known).
LEARNING = {
    "Python": "Kaggle Learn: Python + Pandas (free)",
    "SQL": "Kaggle Learn: Intro to SQL / SQLBolt (free)",
    "Excel": "Microsoft Learn: Excel data analysis modules (free)",
    "Power BI": "Microsoft Learn: Power BI Data Analyst path (free)",
    "Tableau": "Tableau Public free training videos",
    "Data Visualisation": "Build 2 dashboards on public Malaysian data (data.gov.my / OpenDOSM)",
    "Statistics": "Khan Academy: Statistics & Probability (free)",
    "Data Cleaning": "Kaggle Learn: Data Cleaning (free)",
    "Machine Learning": "Kaggle Learn: Intro to Machine Learning (free)",
    "R": "R for Data Science (free online book)",
    "Google Analytics": "Google Skillshop: GA4 certification (free)",
    "JavaScript": "freeCodeCamp JavaScript certification (free)",
    "Git": "GitHub Skills: Introduction to GitHub (free)",
    "Cloud": "AWS Cloud Practitioner Essentials (free course)",
    "Communication": "Present one project publicly (meetup, LinkedIn post, video walkthrough)",
    "Teamwork": "Contribute to a group or open-source project and document your role",
    "Problem Solving": "Write up one problem you solved: context → root cause → fix → result",
    "Bahasa Melayu": "Kursus Bahasa Melayu komunikasi (community / university language centre)",
    "English": "MUET preparation / British Council free resources",
    "Mandarin": "HSK 1–2 beginner course",
}

# Words that must NEVER influence a score (protected attributes & proxies).
# Used by the anonymiser and shown on the Governance page for transparency.
PROTECTED_TERMS = {
    "gender": ["male", "female", "lelaki", "perempuan", "man", "woman", "mr", "mrs", "ms", "miss", "encik", "puan", "cik",
               "he", "she", "his", "her", "him", "lady", "gentleman"],
    "race_religion": ["malay", "melayu", "chinese", "cina", "indian", "india", "bumiputera", "bumiputra", "kadazan", "iban",
                      "dusun", "orang asli", "muslim", "islam", "buddhist", "buddha", "hindu", "christian", "kristian",
                      "sikh", "bangsa", "agama", "race", "religion", "ethnicity", "keturunan"],
    "family": ["married", "single", "divorced", "berkahwin", "bujang", "janda", "duda", "children", "anak-anak",
               "pregnant", "mengandung", "maternity", "bersalin", "marital status", "status perkahwinan"],
    "age": ["age", "umur", "date of birth", "tarikh lahir", "dob", "born", "lahir"],
}

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
    "Tamil": ["tamil language", "bahasa tamil"],
    "Arabic": ["arabic", "bahasa arab"],
    # ---- More software & IT ----
    "Java": ["java", "spring boot"],
    "C#/.NET": ["c#", ".net", "asp.net"],
    "PHP": ["php", "laravel"],
    "Mobile Development": ["flutter", "dart", "android", "ios", "kotlin", "swift", "react native", "aplikasi mudah alih"],
    "Web Development": ["html", "css", "web development", "pembangunan web", "frontend", "front-end", "backend", "back-end"],
    "Software Testing": ["software testing", "unit test", "unit testing", "qa testing", "quality assurance testing", "pengujian perisian", "selenium"],
    "Networking": ["networking", "ccna", "tcp/ip", "rangkaian komputer", "lan/wan", "routing"],
    "Cybersecurity": ["cybersecurity", "cyber security", "keselamatan siber", "penetration testing", "siem", "firewall"],
    "IT Support": ["it support", "helpdesk", "help desk", "sokongan it", "technical support", "sokongan teknikal"],
    "UI/UX Design": ["ui/ux", "ux design", "ui design", "user experience", "figma", "wireframe", "wireframes", "prototyping"],
    "Deep Learning / NLP": ["deep learning", "tensorflow", "pytorch", "nlp", "natural language processing", "computer vision", "keras"],
    # ---- Finance & accounting ----
    "Accounting": ["accounting", "perakaunan", "bookkeeping", "simpan kira", "general ledger", "lejar am", "accounts payable", "accounts receivable", "bank reconciliation", "penyesuaian bank"],
    "Financial Reporting": ["financial reporting", "financial statements", "penyata kewangan", "mfrs", "ifrs", "month-end closing", "laporan kewangan"],
    "Taxation": ["taxation", "tax computation", "percukaian", "cukai", "sst", "lhdn", "income tax", "cukai pendapatan"],
    "Auditing": ["auditing", "audit", "pengauditan", "internal audit", "audit dalaman"],
    "Accounting Software": ["sql accounting", "autocount", "ubs accounting", "quickbooks", "xero", "sap fico", "myob"],
    "Budgeting": ["budgeting", "belanjawan", "forecasting", "ramalan kewangan", "variance analysis", "cost control", "kawalan kos"],
    # ---- Marketing & sales ----
    "Digital Marketing": ["digital marketing", "pemasaran digital", "seo", "google ads", "meta ads", "facebook ads", "email marketing"],
    "Social Media": ["social media", "media sosial", "tiktok", "instagram", "content calendar", "community management"],
    "Content Writing": ["content writing", "copywriting", "penulisan kandungan", "blog writing", "content creation", "penciptaan kandungan"],
    "Sales": ["sales", "jualan", "b2b sales", "b2c sales", "sales target", "sasaran jualan", "lead generation", "closing deals"],
    "CRM": ["crm", "salesforce", "hubspot", "zoho crm", "customer relationship management"],
    "Market Research": ["market research", "kajian pasaran", "competitor analysis", "analisis pesaing", "survey design", "consumer insights"],
    # ---- HR & admin ----
    "Recruitment": ["recruitment", "pengambilan pekerja", "talent acquisition", "sourcing candidates", "interviewing", "temu duga", "onboarding"],
    "Payroll": ["payroll", "penggajian", "kwsp", "epf", "socso", "perkeso"],
    "Employment Law": ["employment act", "akta kerja", "industrial relations", "perhubungan perusahaan", "labour law", "undang-undang buruh"],
    "Training & Development": ["training and development", "latihan dan pembangunan", "hrdf", "hrd corp", "training needs analysis", "learning and development"],
    "Administration": ["administration", "pentadbiran", "office management", "pengurusan pejabat", "filing", "document control", "kawalan dokumen", "scheduling"],
    "Microsoft Office": ["microsoft office", "ms office", "microsoft word", "powerpoint", "outlook", "google workspace"],
    # ---- Engineering & technical ----
    "AutoCAD": ["autocad", "cad drafting", "lukisan cad"],
    "3D CAD": ["solidworks", "catia", "fusion 360", "inventor", "3d modelling", "pemodelan 3d"],
    "Structural Design": ["structural design", "reka bentuk struktur", "staad pro", "etabs", "sap2000", "eurocode"],
    "Construction Management": ["construction management", "pengurusan pembinaan", "site supervision", "penyeliaan tapak", "bill of quantities", "cidb"],
    "Electrical Systems": ["electrical wiring", "pendawaian elektrik", "plc", "scada", "power distribution", "switchgear", "electrical installation"],
    "Embedded Systems / IoT": ["embedded systems", "sistem terbenam", "arduino", "esp32", "raspberry pi", "microcontroller", "mikropengawal", "iot", "internet of things"],
    "Mechanical Maintenance": ["preventive maintenance", "penyelenggaraan pencegahan", "maintenance planning", "hvac", "pumps", "turbines", "cmms"],
    "Quality Management": ["iso 9001", "quality control", "kawalan kualiti", "quality assurance", "jaminan kualiti", "six sigma", "lean manufacturing", "5s", "kaizen"],
    "Health & Safety": ["osha", "dosh", "hse", "hirarc", "keselamatan dan kesihatan pekerjaan", "safety officer", "risk assessment", "penilaian risiko"],
    "Manufacturing": ["manufacturing", "pembuatan", "production line", "barisan pengeluaran", "smt", "semiconductor", "semikonduktor", "wafer"],
    # ---- Operations, service, design, management ----
    "Customer Service": ["customer service", "khidmat pelanggan", "perkhidmatan pelanggan", "call centre", "call center", "customer support", "complaint handling", "pengendalian aduan"],
    "Logistics & Supply Chain": ["logistics", "logistik", "supply chain", "rantaian bekalan", "inventory management", "pengurusan inventori", "warehouse", "gudang", "procurement", "perolehan"],
    "Project Management": ["project management", "pengurusan projek", "pmp", "gantt", "agile", "scrum", "milestones", "project planning"],
    "Leadership": ["led a team", "team leader", "ketua pasukan", "supervised", "menyelia", "managed a team", "mentored", "membimbing"],
    "Graphic Design": ["graphic design", "reka bentuk grafik", "adobe photoshop", "photoshop", "illustrator", "indesign", "canva", "branding"],
    "Video Editing": ["video editing", "penyuntingan video", "premiere pro", "after effects", "capcut", "davinci resolve"],
    "Teaching": ["teaching", "pengajaran", "lesson planning", "rancangan pengajaran", "tutoring", "tuisyen", "curriculum", "kurikulum", "lecturer", "pensyarah"],
    "Research": ["research", "penyelidikan", "literature review", "kajian literatur", "published", "journal article", "systematic review", "data collection", "pengumpulan data"],
    "Healthcare": ["patient care", "penjagaan pesakit", "nursing", "kejururawatan", "clinical", "klinikal", "first aid", "pertolongan cemas", "bls", "cpr"],
    "Hospitality": ["hospitality", "hospitaliti", "front desk", "food and beverage", "f&b", "housekeeping", "event management", "pengurusan acara"],
}

# Which field each skill belongs to (used to group the picker in the app).
SKILL_FIELDS = {
    "Data & AI": ["Python", "SQL", "Excel", "Power BI", "Tableau", "Data Visualisation", "Statistics", "Data Cleaning",
                  "Machine Learning", "Deep Learning / NLP", "R", "Google Analytics"],
    "Software & IT": ["JavaScript", "Java", "C#/.NET", "PHP", "Mobile Development", "Web Development", "Git", "Cloud",
                      "Software Testing", "Networking", "Cybersecurity", "IT Support", "UI/UX Design"],
    "Finance & Accounting": ["Accounting", "Financial Reporting", "Taxation", "Auditing", "Accounting Software", "Budgeting"],
    "Marketing & Sales": ["Digital Marketing", "Social Media", "Content Writing", "Sales", "CRM", "Market Research"],
    "HR & Admin": ["Recruitment", "Payroll", "Employment Law", "Training & Development", "Administration", "Microsoft Office"],
    "Engineering": ["AutoCAD", "3D CAD", "Structural Design", "Construction Management", "Electrical Systems",
                    "Embedded Systems / IoT", "Mechanical Maintenance", "Quality Management", "Health & Safety", "Manufacturing"],
    "Operations & Service": ["Customer Service", "Logistics & Supply Chain", "Project Management", "Hospitality", "Healthcare"],
    "Creative & Education": ["Graphic Design", "Video Editing", "Teaching", "Research"],
    "Soft skills & Languages": ["Communication", "Teamwork", "Problem Solving", "Leadership", "Bahasa Melayu", "English",
                                "Mandarin", "Tamil", "Arabic"],
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

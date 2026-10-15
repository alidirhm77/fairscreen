"""
Synthetic demo data. ALL candidates are fictional. No real personal data.

`audit` fields simulate VOLUNTARY self-identification collected separately for
equal-opportunity monitoring. They are never passed to the scorer.
"""
from .scoring import Job

JOBS = {
    "Junior Data Analyst (Penang, hybrid)": Job(
        title="Junior Data Analyst",
        must_have=["Python", "SQL", "Excel", "Data Visualisation"],
        nice_to_have=["Power BI", "Statistics", "Communication", "Bahasa Melayu"],
        min_years=0, target_years=2, min_level=3,
        description="Analyse sales and operations data, build dashboards for managers, and present findings. "
                    "Diploma or degree in any field; skills matter more than the institution.",
    ),
    "Software Engineer Intern (KL)": Job(
        title="Software Engineer Intern",
        must_have=["JavaScript", "Git", "Problem Solving"],
        nice_to_have=["Python", "SQL", "Cloud", "Teamwork"],
        min_years=0, target_years=1, min_level=3,
        description="Build and test web features with a product team. Diploma or degree students welcome.",
    ),
    "Mobile App Developer": Job(
        title="Mobile App Developer",
        must_have=["Mobile Development", "Git", "Problem Solving"],
        nice_to_have=["UI/UX Design", "Cloud", "Software Testing", "Teamwork"],
        target_years=2, min_level=3,
        description="Build and ship Flutter / native mobile apps with a small product team.",
    ),
    "Account Executive (Accounting)": Job(
        title="Account Executive",
        must_have=["Accounting", "Financial Reporting", "Accounting Software", "Excel"],
        nice_to_have=["Taxation", "Auditing", "Budgeting", "Bahasa Melayu"],
        target_years=2, min_level=3,
        description="Full set of accounts, month-end closing, SST and tax support for an SME.",
    ),
    "Digital Marketing Executive": Job(
        title="Digital Marketing Executive",
        must_have=["Digital Marketing", "Social Media", "Content Writing"],
        nice_to_have=["Google Analytics", "Graphic Design", "Video Editing", "Market Research", "Bahasa Melayu"],
        target_years=1, min_level=3,
        description="Plan and run campaigns across Meta, TikTok and Google; create content and report results.",
    ),
    "HR Executive": Job(
        title="HR Executive",
        must_have=["Recruitment", "Payroll", "Employment Law"],
        nice_to_have=["Training & Development", "Microsoft Office", "Communication", "Bahasa Melayu"],
        target_years=2, min_level=3,
        description="End-to-end recruitment, payroll with EPF/SOCSO, and compliance with the Employment Act.",
    ),
    "Civil / Site Engineer": Job(
        title="Civil / Site Engineer",
        must_have=["AutoCAD", "Construction Management", "Health & Safety"],
        nice_to_have=["Structural Design", "Project Management", "Quality Management", "Leadership"],
        target_years=2, min_level=4,
        description="Supervise site works, coordinate contractors and ensure safety and quality compliance.",
    ),
    "Manufacturing / Process Engineer": Job(
        title="Process Engineer",
        must_have=["Manufacturing", "Quality Management", "Problem Solving"],
        nice_to_have=["Mechanical Maintenance", "Health & Safety", "3D CAD", "Statistics"],
        target_years=1, min_level=4,
        description="Improve yield and quality on a semiconductor / electronics production line in Penang.",
    ),
    "Customer Service Executive": Job(
        title="Customer Service Executive",
        must_have=["Customer Service", "Communication", "Microsoft Office"],
        nice_to_have=["CRM", "Bahasa Melayu", "English", "Mandarin", "Problem Solving"],
        target_years=1, min_level=2,
        description="Handle customer enquiries and complaints by phone, chat and email.",
    ),
    "Graphic Designer": Job(
        title="Graphic Designer",
        must_have=["Graphic Design", "Social Media"],
        nice_to_have=["Video Editing", "UI/UX Design", "Content Writing"],
        target_years=1, min_level=2,
        description="Design brand, social and print materials; portfolio required.",
    ),
    "Admin / Project Coordinator": Job(
        title="Project Coordinator",
        must_have=["Administration", "Microsoft Office", "Project Management"],
        nice_to_have=["Communication", "Leadership", "Excel", "Bahasa Melayu"],
        target_years=1, min_level=3,
        description="Coordinate schedules, documents and stakeholders for multiple projects.",
    ),
    "Research Assistant (University)": Job(
        title="Research Assistant",
        must_have=["Research", "Statistics", "Communication"],
        nice_to_have=["Python", "Machine Learning", "Data Cleaning", "English"],
        target_years=1, min_level=4,
        description="Support data collection, analysis and paper writing in a university research group.",
    ),
}

CANDIDATES = [
    {"id": "C01", "audit": {"gender": "Female", "ethnicity": "Malay", "institution": "Polytechnic / TVET"}, "cv": """Siti Nurhaliza binti Ahmad
Email: siti.n@example.my | Phone: 012-345 6789
Gender: Female

EDUCATION
Diploma in Information Technology, Politeknik Seberang Perai, 2018 - 2021

EXPERIENCE
Data Assistant, Kilang Elektronik Sdn Bhd, 2021 - 2023
- Built weekly production dashboards in Power BI used by 3 shift managers
- Wrote SQL queries (MySQL) to extract defect data; automated Excel reports with pivot table and XLOOKUP
Career break (family care), 2023 - 2024
Freelance Data Analyst, 2024 - present
- Python (pandas) data cleaning for 2 SME clients; presented findings to owners in Bahasa Melayu and English

PROJECTS
Penang rainfall vs. factory downtime analysis using Python and regression (statistics)
Interactive sales dashboard for a family kuih business (Power BI)

CERTIFICATIONS
Microsoft PL-300 Power BI Data Analyst
Google Data Analytics Certificate
"""},
    {"id": "C02", "audit": {"gender": "Male", "ethnicity": "Chinese", "institution": "Research university (public)"}, "cv": """Name: Lim Jun Hao
Email: junhao.lim@example.my
Mr Lim, age 23

EDUCATION
Bachelor of Science (Mathematics), Universiti Malaya, 2020 - 2024
Dean's List

EXPERIENCE
Intern, Bank, Jun 2023 - Aug 2023
- Updated Excel spreadsheets and prepared charts for the team

SKILLS
Excel, basic Python
"""},
    {"id": "C03", "audit": {"gender": "Female", "ethnicity": "Indian", "institution": "Regional public university"}, "cv": """Kavitha a/p Muniandy
kavitha.m@example.my | 016-222 3333

EDUCATION
Bachelor of Computer Science (Data Science), Universiti Malaysia Sabah, 2019 - 2023

EXPERIENCE
Data Analyst, Logistics company, 2023 - present
- SQL (PostgreSQL) and Python pipelines for delivery data; data cleaning and ETL
- Tableau dashboards for regional managers; monthly presentation to stakeholders
- A/B test analysis of route changes (hypothesis testing)

PROJECTS
Machine learning model (random forest) predicting late deliveries
Team project: inventory forecasting app, collaborated with 4 students

LANGUAGES
English, Tamil language, Bahasa Melayu
"""},
    {"id": "C04", "audit": {"gender": "Male", "ethnicity": "Malay", "institution": "Private university"}, "cv": """Muhammad Aiman bin Zulkifli
Telefon: 019-888 1212

PENDIDIKAN
Ijazah Sarjana Muda Sains Komputer, UCSI University, 2020 - 2024

PENGALAMAN
Latihan Industri, Syarikat Telekomunikasi, 2023 - 2024
- Membina papan pemuka Power BI untuk jualan
- Menulis pertanyaan SQL dan laporan Excel
- Pembentangan hasil kepada pengurus

PROJEK
Analisis data pelajar menggunakan Python dan statistik

KEMAHIRAN
Python, SQL, Excel, Power BI, Bahasa Melayu, English
"""},
    {"id": "C05", "audit": {"gender": "Female", "ethnicity": "Chinese", "institution": "Research university (public)"}, "cv": """Ong Pei Shan
Email: peishan@example.my
Female, 24

EDUCATION
Bachelor of Business Administration, Universiti Sains Malaysia, 2019 - 2023

EXPERIENCE
Marketing Executive, 2023 - present
- Google Analytics reports; Excel tracking of campaigns
- Presented monthly results to stakeholders

SKILLS
Excel, Canva, Communication
"""},
    {"id": "C06", "audit": {"gender": "Male", "ethnicity": "Sabah/Sarawak", "institution": "Polytechnic / TVET"}, "cv": """Jerome Anak Sali
Phone: 013-777 8899

EDUCATION
Diploma Kejuruteraan Elektrik, Politeknik Kuching Sarawak, 2017 - 2020

EXPERIENCE
Technician, 2020 - 2022
Data Technician, Solar farm operator, 2022 - present
- Python scripts to clean sensor data; SQL database of inverter faults
- Excel models for maintenance cost; built dashboards for supervisors
- Root cause analysis of downtime (problem solving)

CERTIFICATIONS
Kaggle Learn: Pandas, Data Cleaning
SKM Tahap 3
"""},
    {"id": "C07", "audit": {"gender": "Female", "ethnicity": "Malay", "institution": "Research university (public)"}, "cv": """Nurul Izzah binti Hamdan
nurul.izzah@example.my
Puan Nurul

EDUCATION
Master of Data Science, Universiti Kebangsaan Malaysia, 2021 - 2023
Bachelor of Statistics, Universiti Kebangsaan Malaysia, 2015 - 2019

EXPERIENCE
Data Analyst, Insurance company, 2019 - 2020
- SQL, Python, statistics for claims analysis; Tableau dashboards
Career break (maternity), 2020 - 2021
Research Assistant, 2021 - 2023
- Machine learning with scikit-learn; R and ggplot2 visualisation; presented at a conference

SKILLS
Python, R, SQL, Excel, Tableau, Statistics, Bahasa Melayu, English
"""},
    {"id": "C08", "audit": {"gender": "Male", "ethnicity": "Indian", "institution": "Private university"}, "cv": """Name: Ravi a/l Krishnan
ravi.k@example.my

EDUCATION
Diploma in Business, Kolej Komuniti, 2016 - 2018
Bachelor of IT, Asia Pacific University, 2019 - 2022

EXPERIENCE
Sales Executive, 2018 - 2019
Gap year, 2022 - 2024
Junior Analyst, Retail chain, 2024 - present
- Excel pivot table reports, Power BI dashboards
- Learning SQL

SKILLS
Excel, Power BI, Communication, Mandarin
"""},
    {"id": "C09", "audit": {"gender": "Female", "ethnicity": "Sabah/Sarawak", "institution": "Regional public university"}, "cv": """Cheryl Anak Ujang
cheryl.u@example.my | 014-555 0101

EDUCATION
Bachelor of Science (Statistics), Universiti Malaysia Sarawak, 2018 - 2022

EXPERIENCE
Data Analyst, Healthcare NGO, 2022 - present
- Python and R for survey analysis; SQL; data cleaning of 20,000 records
- Power BI dashboards; report writing for donors; presentation to board

PROJECTS
Dengue cases visualisation for Sarawak divisions (Python, data visualisation)
Volunteer: team project mapping rural clinics

CERTIFICATIONS
Google Data Analytics Certificate
"""},
    {"id": "C10", "audit": {"gender": "Male", "ethnicity": "Chinese", "institution": "Private university"}, "cv": """Tan Kok Leong
kokleong@example.my

EDUCATION
Bachelor of Computer Science, Monash University Malaysia, 2018 - 2021

EXPERIENCE
Software Developer, 2021 - 2024
- JavaScript, React, Git, AWS
- SQL databases

SKILLS
JavaScript, SQL, Git, AWS, Python (basic)
"""},
    {"id": "C11", "audit": {"gender": "Female", "ethnicity": "Malay", "institution": "Private university"}, "cv": """Aisyah binti Rosli
aisyah.r@example.my

EDUCATION
Bachelor of Accounting, Taylor's University, 2016 - 2020

EXPERIENCE
Audit Associate, 2020 - 2022
- Advanced Excel (XLOOKUP, pivot table)
Career break (family care), 2022 - 2024
Data Analytics Bootcamp, 2024
- Python, SQL, Tableau; statistics; capstone presented to hiring partners

PROJECTS
Bootcamp capstone: e-commerce churn analysis (Python, SQL, Tableau dashboard)
"""},
    {"id": "C12", "audit": {"gender": "Male", "ethnicity": "Malay", "institution": "Research university (public)"}, "cv": """Ahmad Faris bin Ismail
Gender: Male

EDUCATION
Bachelor of Engineering, Universiti Teknologi Malaysia, 2018 - 2022

EXPERIENCE
Engineer, 2022 - present
- Excel calculations

SKILLS
AutoCAD, Excel, Teamwork
"""},
    {"id": "C13", "audit": {"gender": "Female", "ethnicity": "Indian", "institution": "Polytechnic / TVET"}, "cv": """Deepa a/p Ramasamy
deepa.r@example.my

EDUCATION
Diploma in Statistics, Politeknik Ungku Omar, 2019 - 2022

EXPERIENCE
Data Entry & Reporting Assistant, 2022 - present
- Excel dashboards and charts; data cleaning
- Learning Python and SQL through Kaggle Learn

CERTIFICATIONS
Kaggle Learn: Intro to SQL
Kaggle Learn: Python
"""},
    {"id": "C14", "audit": {"gender": "Male", "ethnicity": "Chinese", "institution": "Regional public university"}, "cv": """Wong Jia Hui
Email: jiahui.w@example.my

EDUCATION
Bachelor of Science (Data Analytics), Universiti Utara Malaysia, 2019 - 2023

EXPERIENCE
Business Intelligence Intern, Manufacturing, 2022 - 2023
Data Analyst, E-commerce, 2023 - present
- SQL, Python, Power BI dashboards; statistics; presented weekly to stakeholders

SKILLS
Python, SQL, Excel, Power BI, Statistics, Mandarin, Bahasa Melayu, English
"""},
]

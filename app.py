import datetime
import re
from io import BytesIO

import streamlit as st
from PyPDF2 import PdfReader


st.set_page_config(page_title="CRIS", page_icon="CRIS", layout="wide")

st.markdown(
    """
<style>
:root {
    --bg-1: #0f2027;
    --bg-2: #203a43;
    --bg-3: #2c5364;
    --card: rgba(255, 255, 255, 0.07);
    --text: #f2f8ff;
    --accent: #00c6ff;
    --accent-2: #0072ff;
}
.stApp {
    background: linear-gradient(135deg, var(--bg-1), var(--bg-2), var(--bg-3));
    color: var(--text);
}
h1, h2, h3, h4, p, li, label {
    color: var(--text) !important;
}
.card {
    background: var(--card);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}
.hero {
    background: linear-gradient(120deg, #1f1c2c, #2b5876);
    border-radius: 20px;
    padding: 28px;
}
.stButton > button {
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
}
</style>
""",
    unsafe_allow_html=True,
)


CAREER_SKILLS = {
    "Data Scientist": {
        "python": 3,
        "machine learning": 3,
        "data analysis": 2,
        "sql": 2,
        "statistics": 2,
    },
    "Web Developer": {
        "html": 3,
        "css": 3,
        "javascript": 3,
        "react": 2,
        "node": 2,
    },
    "Software Engineer": {
        "c++": 2,
        "java": 2,
        "data structures": 3,
        "algorithms": 3,
        "oop": 2,
    },
}

SKILL_SYNONYMS = {
    "python": ["python", "py"],
    "machine learning": ["machine learning", "ml", "scikit", "tensorflow", "pytorch"],
    "data analysis": ["data analysis", "analytics", "eda", "pandas"],
    "sql": ["sql", "postgres", "mysql", "sqlite"],
    "statistics": ["statistics", "statistical", "probability", "hypothesis testing"],
    "html": ["html", "html5"],
    "css": ["css", "css3", "tailwind", "bootstrap"],
    "javascript": ["javascript", "js", "ecmascript"],
    "react": ["react", "next.js", "nextjs"],
    "node": ["node", "nodejs", "express"],
    "c++": ["c++", "cpp"],
    "java": ["java", "spring"],
    "data structures": ["data structures", "dsa", "hashmap", "tree", "graph"],
    "algorithms": ["algorithms", "algo", "dynamic programming", "greedy"],
    "oop": ["oop", "object oriented programming", "object-oriented"],
}

PREDEFINED_SUBJECTS = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "HTML",
    "CSS",
    "JavaScript",
    "Data Structures",
    "Machine Learning",
    "Database Systems",
    "Python",
    "SQL",
    "Statistics",
]


def init_state() -> None:
    defaults = {
        "academic_score": 0.0,
        "alignment_score": 0.0,
        "resume_score": 0.0,
        "days_left": None,
        "study_plan": [],
        "matched_resume_skills": [],
        "missing_resume_skills": [],
        "last_report": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def has_skill(text: str, skill: str) -> bool:
    variants = SKILL_SYNONYMS.get(skill, [skill])
    normalized = normalize_text(text)
    return any(variant in normalized for variant in variants)


def weighted_skill_score(source_text: str, skill_weights: dict) -> tuple[float, list[str], list[str]]:
    matched = [skill for skill in skill_weights if has_skill(source_text, skill)]
    total_weight = sum(skill_weights.values())
    matched_weight = sum(skill_weights[s] for s in matched)
    score = (matched_weight / total_weight) * 100 if total_weight else 0
    missing = [s for s in skill_weights if s not in matched]
    return score, matched, missing


def build_study_plan(
    subjects: list[str], hours: int, confidence_map: dict[str, int], days_left: int
) -> list[tuple[str, float]]:
    urgency = 1.5 if days_left <= 7 else 1.25 if days_left <= 21 else 1.0
    weighted = []
    for subject in subjects:
        confidence = confidence_map.get(subject, 3)
        weakness = 6 - confidence
        weighted.append((subject, weakness * urgency))
    total = sum(w for _, w in weighted)
    if total == 0:
        return [(s, round(hours / len(subjects), 1)) for s in subjects]
    return [(s, round((w / total) * hours, 1)) for s, w in weighted]


def unified_readiness_score(academic: float, alignment: float, resume: float) -> float:
    return 0.35 * academic + 0.30 * alignment + 0.35 * resume


def create_report(career: str) -> str:
    actions = []
    if st.session_state["alignment_score"] < 70:
        actions.append("Improve subject-career alignment in the study plan.")
    if st.session_state["resume_score"] < 70:
        actions.append("Add missing skills and project keywords to the resume.")
    if st.session_state["academic_score"] < 70:
        actions.append("Increase consistent daily study time by 1-2 hours.")
    if not actions:
        actions.append("Maintain momentum with mock interviews and projects.")

    top_actions = "\n".join(f"- {action}" for action in actions[:3])

    plan_lines = "\n".join(
        f"- {subject}: {hours} hrs/day" for subject, hours in st.session_state["study_plan"]
    )
    if not plan_lines:
        plan_lines = "- No study plan generated yet."

    report = f"""CRIS Prototype Report
Date: {datetime.date.today().isoformat()}
Target Career: {career}

Scores
- Academic Strength: {st.session_state["academic_score"]:.2f}%
- Career Alignment: {st.session_state["alignment_score"]:.2f}%
- Resume Skill Match: {st.session_state["resume_score"]:.2f}%
- Unified Career Readiness: {unified_readiness_score(st.session_state["academic_score"], st.session_state["alignment_score"], st.session_state["resume_score"]):.2f}%

Study Plan
{plan_lines}

Resume Skills Detected
- {", ".join(st.session_state["matched_resume_skills"]) if st.session_state["matched_resume_skills"] else "None"}

Skill Gaps
- {", ".join(st.session_state["missing_resume_skills"]) if st.session_state["missing_resume_skills"] else "None"}

Top 3 Next Actions
{top_actions}
"""
    return report


def extract_pdf_text(uploaded_file) -> str:
    try:
        reader = PdfReader(uploaded_file)
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        return " ".join(text)
    except Exception:
        return ""


init_state()

st.title("CRIS - Career Readiness Intelligence System")
st.caption("Bridge academics with measurable career outcomes")

st.sidebar.markdown("### Prototype Flow")
st.sidebar.markdown("1. Choose career\n2. Build study plan\n3. Analyze resume\n4. Export report")

menu = st.sidebar.radio("Navigation", ["Dashboard", "Study Planner", "Resume Analyzer"])
career = st.sidebar.selectbox("Select Target Career", list(CAREER_SKILLS.keys()))


if menu == "Dashboard":
    st.markdown(
        """
        <div class="hero">
            <h1>Welcome to CRIS</h1>
            <p>Academic planning, resume intelligence, and unified career readiness in one prototype.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            '<div class="card"><h3>Study Engine</h3><p>Priority-based daily planning from confidence and exam urgency.</p></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="card"><h3>Resume Intelligence</h3><p>Weighted skill matching with synonym-aware extraction.</p></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="card"><h3>Readiness Index</h3><p>Unified score combining academics, alignment, and resume fit.</p></div>',
            unsafe_allow_html=True,
        )

    st.subheader("Current Prototype Scores")
    overall = unified_readiness_score(
        st.session_state["academic_score"],
        st.session_state["alignment_score"],
        st.session_state["resume_score"],
    )
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Academic", f'{st.session_state["academic_score"]:.1f}%')
    p2.metric("Alignment", f'{st.session_state["alignment_score"]:.1f}%')
    p3.metric("Resume", f'{st.session_state["resume_score"]:.1f}%')
    p4.metric("Unified Readiness", f"{overall:.1f}%")

    st.caption("Scoring formula: 35% Academic + 30% Alignment + 35% Resume.")


elif menu == "Study Planner":
    st.markdown(
        """
        <div class="card">
            <h2>Smart Study Planner</h2>
            <p>Time allocation is based on your weak subjects and exam urgency.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        selected_subjects = st.multiselect("Select Subjects", PREDEFINED_SUBJECTS)
        other_subject = st.text_input("Add Other Subject")
        subjects = list(dict.fromkeys(selected_subjects + ([other_subject.strip()] if other_subject.strip() else [])))
        daily_hours = st.slider("Daily Study Hours", 1, 12, 4)

    with col2:
        exam_date = st.date_input("Exam Date", min_value=datetime.date.today() + datetime.timedelta(days=1))

    confidence_map = {}
    if subjects:
        st.markdown("#### Self-Confidence per Subject (1 low - 5 high)")
        for subject in subjects:
            confidence_map[subject] = st.slider(
                f"{subject} confidence", min_value=1, max_value=5, value=3, key=f"conf_{subject}"
            )

    if st.button("Generate Optimized Plan"):
        if not subjects:
            st.warning("Select at least one subject.")
        else:
            days_left = (exam_date - datetime.date.today()).days
            if days_left <= 0:
                st.error("Exam date must be in the future.")
            else:
                plan = build_study_plan(subjects, daily_hours, confidence_map, days_left)
                plan_text = " ".join(subjects)
                alignment, _, missing_alignment = weighted_skill_score(plan_text, CAREER_SKILLS[career])
                academic = min((daily_hours / 8) * 100, 100)

                st.session_state["days_left"] = days_left
                st.session_state["study_plan"] = plan
                st.session_state["academic_score"] = academic
                st.session_state["alignment_score"] = alignment

                st.success(f"{days_left} days remaining. Plan generated.")
                st.subheader("Daily Allocation")
                for subject, hrs in plan:
                    st.write(f"- {subject}: {hrs} hrs/day")

                s1, s2 = st.columns(2)
                with s1:
                    st.progress(int(academic))
                    st.metric("Academic Strength", f"{academic:.2f}%")
                with s2:
                    st.progress(int(alignment))
                    st.metric("Career Alignment", f"{alignment:.2f}%")

                st.subheader("Missing Career Skills From Current Study Plan")
                st.write(missing_alignment if missing_alignment else "No major gaps detected.")


elif menu == "Resume Analyzer":
    st.markdown(
        """
        <div class="card">
            <h2>Resume Intelligence Analyzer</h2>
            <p>Upload a PDF or run a demo sample to test the skill extraction pipeline.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    use_demo = st.button("Run Demo Resume")

    resume_text = ""
    if uploaded_file is not None:
        resume_text = extract_pdf_text(uploaded_file)
        if not resume_text:
            st.error("Could not parse this PDF. Please try another file.")
    elif use_demo:
        resume_text = """
        Built data pipelines with Python and SQL. Created machine learning models for churn prediction.
        Completed analytics dashboard project. Strong in statistics and experimentation.
        """
        st.info("Using built-in demo resume text.")

    if resume_text:
        resume_score, matched_skills, missing_skills = weighted_skill_score(
            resume_text, CAREER_SKILLS[career]
        )
        st.session_state["resume_score"] = resume_score
        st.session_state["matched_resume_skills"] = matched_skills
        st.session_state["missing_resume_skills"] = missing_skills

        c1, c2 = st.columns(2)
        with c1:
            st.progress(int(resume_score))
            st.metric("Skill Match", f"{resume_score:.2f}%")
        with c2:
            overall = unified_readiness_score(
                st.session_state["academic_score"],
                st.session_state["alignment_score"],
                st.session_state["resume_score"],
            )
            st.metric("Unified Readiness", f"{overall:.2f}%")

        st.subheader("Skills Detected")
        st.write(matched_skills if matched_skills else "No relevant skills found.")

        st.subheader("Skill Gaps")
        st.write(missing_skills if missing_skills else "All core skills covered.")

    st.markdown("---")
    st.subheader("Export Prototype Report")
    if st.button("Generate Report"):
        st.session_state["last_report"] = create_report(career)
        st.success("Report generated.")

    if st.session_state["last_report"]:
        data = BytesIO(st.session_state["last_report"].encode("utf-8"))
        st.download_button(
            label="Download CRIS Report",
            data=data,
            file_name="cris_prototype_report.txt",
            mime="text/plain",
        )


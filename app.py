import streamlit as st
import datetime
from PyPDF2 import PdfReader

st.set_page_config(page_title="CRIS", page_icon="🚀", layout="wide")

# ---------- BLUE UNIVERSE THEME ----------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.main {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
h1, h2, h3 {
    color: white;
}
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
}
.stMultiSelect div {
    background-color: #1f2c3c !important;
}
.stSlider > div > div {
    color: #00c6ff;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 CRIS - Career Readiness Intelligence System")
st.caption("Bridging Academics with Career Success")

menu = st.sidebar.radio("Navigation", ["Dashboard", "Study Planner", "Resume Analyzer"])

career_options = {
    "Data Scientist": ["python", "machine learning", "data analysis", "sql", "statistics"],
    "Web Developer": ["html", "css", "javascript", "react", "node"],
    "Software Engineer": ["c++", "java", "data structures", "algorithms", "oop"]
}

career = st.sidebar.selectbox("🎯 Select Target Career", list(career_options.keys()))

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":

    if menu == "Dashboard":

     st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1f1c2c, #928dab);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;">
        <h1>🌌 Welcome to CRIS</h1>
        <p style="font-size:18px;">
        Your Intelligent Academic-to-Career Optimization Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.05);
            padding: 25px;
            border-radius: 15px;
            text-align:center;">
            <h3>📚 Study Engine</h3>
            <p>Smart daily planning based on exam timeline.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.05);
            padding: 25px;
            border-radius: 15px;
            text-align:center;">
            <h3>💼 Resume Intelligence</h3>
            <p>Role-based skill analysis & gap detection.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.05);
            padding: 25px;
            border-radius: 15px;
            text-align:center;">
            <h3>🚀 Career Score</h3>
            <p>Unified readiness evaluation system.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("✨ Why CRIS is Different")

    st.markdown("""
    - 🔹 Connects Academics with Career Goals  
    - 🔹 Maps Skills to Industry Roles  
    - 🔹 Detects Career Gaps Early  
    - 🔹 Simulates Intelligent Decision Support  
    """)

    st.markdown("""
    <div style="
        margin-top:30px;
        padding:20px;
        border-radius:15px;
        background: linear-gradient(90deg,#00c6ff,#0072ff);
        text-align:center;
        color:white;">
        <h3>⚡ Built for Hackureka 2.0</h3>
        <p>Designed to empower students with data-driven clarity.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- STUDY PLANNER ----------------
elif menu == "Study Planner":

    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#141E30,#243B55);
        padding:30px;
        border-radius:20px;
        color:white;
        margin-bottom:25px;">
        <h2>📚 Smart Study Planner</h2>
        <p>Optimize your preparation with intelligent time distribution.</p>
    </div>
    """, unsafe_allow_html=True)

    predefined_subjects = [
        "Mathematics", "Physics", "Chemistry",
        "HTML", "CSS", "JavaScript",
        "Data Structures", "Machine Learning",
        "Database Systems"
    ]

    col1, col2 = st.columns(2)

    with col1:
        selected_subjects = st.multiselect("Select Subjects", predefined_subjects)
        other_subject = st.text_input("Add Other Subject")

        if other_subject:
            selected_subjects.append(other_subject)

        hours = st.slider("Daily Study Hours", 1, 12, 4)

    with col2:
        exam_date = st.date_input("Exam Date")

    if st.button("Generate Optimized Plan"):

        if len(selected_subjects) == 0:
            st.warning("Please select at least one subject.")
        else:
            today = datetime.date.today()
            days_left = (exam_date - today).days

            if days_left <= 0:
                st.error("Exam date must be in future!")
            else:
                per_subject_time = hours / len(selected_subjects)

                st.markdown(f"""
                <div style="
                    background:rgba(255,255,255,0.05);
                    padding:20px;
                    border-radius:15px;
                    margin-top:20px;">
                    <h3>🌌 {days_left} Days Remaining</h3>
                </div>
                """, unsafe_allow_html=True)

                st.subheader("📅 Daily Allocation")

                for sub in selected_subjects:
                    st.write(f"🔹 {sub} → {round(per_subject_time,1)} hrs/day")

                academic_score = min((hours / 8) * 100, 100)

                st.subheader("🎓 Academic Strength Score")
                st.progress(int(academic_score))
                st.metric("Academic Score", f"{round(academic_score,2)} %")

# ---------------- RESUME ANALYZER ----------------
elif menu == "Resume Analyzer":

    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#16222A,#3A6073);
        padding:30px;
        border-radius:20px;
        color:white;
        margin-bottom:25px;">
        <h2>💼 Resume Intelligence Analyzer</h2>
        <p>Analyze skill alignment with your target career role.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

    if uploaded_file is not None:

        reader = PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

        text = text.lower()

        required_skills = career_options[career]
        matched_skills = [skill for skill in required_skills if skill in text]

        score = (len(matched_skills) / len(required_skills)) * 100

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div style="
                background:rgba(255,255,255,0.05);
                padding:20px;
                border-radius:15px;">
                <h3>📊 Skill Match Score</h3>
            </div>
            """, unsafe_allow_html=True)

            st.progress(int(score))
            st.metric("Match Percentage", f"{round(score,2)} %")

        with col2:
            st.markdown("""
            <div style="
                background:rgba(255,255,255,0.05);
                padding:20px;
                border-radius:15px;">
                <h3>🚀 Career Readiness</h3>
            </div>
            """, unsafe_allow_html=True)

            st.metric("Readiness Level", f"{round(score,2)} %")

        st.markdown("---")

        st.subheader("✅ Skills Detected")
        st.write(matched_skills if matched_skills else "No relevant skills found")

        missing = list(set(required_skills) - set(matched_skills))

        st.subheader("❌ Skill Gaps")
        st.write(missing if missing else "All core skills covered!")
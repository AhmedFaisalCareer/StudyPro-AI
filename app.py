import streamlit as st
import requests
from google import genai
from datetime import datetime, date
import json
import re


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="StudyPro AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 18px;
    opacity: 0.7;
    margin-bottom: 25px;
}

.card {
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(128,128,128,0.25);
    margin-bottom: 15px;
}

.big-number {
    font-size: 32px;
    font-weight: 700;
}

.small-text {
    opacity: 0.7;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CONFIGURATION
# ============================================================

FIREBASE_URL = "https://ai-study-helper-69c91-default-rtdb.firebaseio.com"

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# FIREBASE HELPERS
# ============================================================

def firebase_url(path):
    return f"{FIREBASE_URL}/{path}.json"


def save_profile(student_id, profile):

    try:

        response = requests.put(
            firebase_url(f"students/{student_id}/profile"),
            json=profile,
            timeout=10
        )

        return response.status_code == 200

    except Exception:
        return False


def get_profile(student_id):

    try:

        response = requests.get(
            firebase_url(f"students/{student_id}/profile"),
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

    except Exception:
        pass

    return None


def save_history(student_id, item):

    try:

        response = requests.post(
            firebase_url(f"students/{student_id}/history"),
            json=item,
            timeout=10
        )

        return response.status_code == 200

    except Exception:
        return False


def get_history(student_id):

    try:

        response = requests.get(
            firebase_url(f"students/{student_id}/history"),
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            if not data:
                return []

            history = []

            for key, item in data.items():

                item["firebase_id"] = key

                history.append(item)

            return history

    except Exception:
        pass

    return []


def clear_history(student_id):

    try:

        response = requests.delete(
            firebase_url(f"students/{student_id}/history"),
            timeout=10
        )

        return response.status_code == 200

    except Exception:
        return False


def save_stats(student_id, stats):

    try:

        response = requests.put(
            firebase_url(f"students/{student_id}/stats"),
            json=stats,
            timeout=10
        )

        return response.status_code == 200

    except Exception:
        return False


def get_stats(student_id):

    try:

        response = requests.get(
            firebase_url(f"students/{student_id}/stats"),
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            if data:
                return data

    except Exception:
        pass

    return {
        "xp": 0,
        "level": 1,
        "quizzes": 0,
        "questions": 0,
        "correct": 0,
        "streak": 0
    }


# ============================================================
# GEMINI
# ============================================================

def ask_ai(prompt):

    try:

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        if response.text:
            return response.text

        return "The AI did not return an answer."

    except Exception as e:

        return f"AI Error: {str(e)}"


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "profile": None,
    "student_id": None,
    "page": "Dashboard",
    "stats": None,
    "generated_content": "",
    "quiz_questions": [],
    "quiz_submitted": False,
    "quiz_score": 0,
    "flashcards": []
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# LOGIN / PROFILE
# ============================================================

if st.session_state.profile is None:

    st.markdown(
        '<div class="main-title">🎓 StudyPro AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Your personal AI-powered study platform</div>',
        unsafe_allow_html=True
    )

    st.divider()

    left, right = st.columns([1, 1])

    with left:

        st.subheader("🚀 Create your student profile")

        student_id = st.text_input(
            "Student ID / Username",
            placeholder="example: ahmed123"
        )

        name = st.text_input(
            "Your Name",
            placeholder="Enter your name"
        )

        student_class = st.selectbox(
            "Class / Level",
            [
                "Class 6",
                "Class 7",
                "Class 8",
                "Class 9",
                "Class 10",
                "O Level",
                "A Level",
                "Other"
            ]
        )

        school = st.text_input(
            "School",
            placeholder="Enter school name"
        )

        subject = st.selectbox(
            "Main Subject",
            [
                "Mathematics",
                "Physics",
                "Chemistry",
                "Biology",
                "Computer Science",
                "English",
                "Geography",
                "History",
                "Islamiat",
                "Other"
            ]
        )

        goal = st.selectbox(
            "Main Study Goal",
            [
                "Exam Preparation",
                "Homework",
                "Understanding Concepts",
                "Making Notes",
                "Practice Questions",
                "Revision"
            ]
        )

        if st.button(
            "🚀 Start Studying",
            use_container_width=True
        ):

            if not student_id.strip():

                st.warning("Please enter a Student ID.")

            elif not name.strip():

                st.warning("Please enter your name.")

            elif not school.strip():

                st.warning("Please enter your school.")

            else:

                student_id = (
                    student_id
                    .strip()
                    .lower()
                    .replace(" ", "_")
                )

                old_profile = get_profile(student_id)

                if old_profile:

                    st.session_state.profile = old_profile
                    st.session_state.student_id = student_id
                    st.session_state.stats = get_stats(student_id)

                    st.success("Welcome back! 🎉")

                    st.rerun()

                else:

                    profile = {
                        "name": name.strip(),
                        "class": student_class,
                        "school": school.strip(),
                        "subject": subject,
                        "goal": goal,
                        "created": str(date.today())
                    }

                    if save_profile(student_id, profile):

                        st.session_state.profile = profile
                        st.session_state.student_id = student_id
                        st.session_state.stats = get_stats(student_id)

                        st.success("Profile created successfully!")

                        st.rerun()

                    else:

                        st.error(
                            "Could not save profile. Check your Firebase connection."
                        )

    with right:

        st.subheader("✨ What can StudyPro AI do?")

        features = [
            "📊 Track your study progress",
            "📝 Generate custom quizzes",
            "🃏 Create flashcards",
            "📚 Make smart revision notes",
            "🧠 Explain difficult concepts",
            "🗺️ Generate mind maps",
            "📅 Create study plans",
            "🏆 Earn XP and level up",
            "🔥 Build your study streak"
        ]

        for feature in features:
            st.write(feature)

    st.stop()


# ============================================================
# LOAD PROFILE
# ============================================================

profile = st.session_state.profile
student_id = st.session_state.student_id

if st.session_state.stats is None:
    st.session_state.stats = get_stats(student_id)

stats = st.session_state.stats


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎓 StudyPro AI")

    st.caption(
        f"Welcome, {profile['name']}!"
    )

    st.divider()

    pages = [
        "🏠 Dashboard",
        "🤖 AI Study Assistant",
        "📝 Quiz Generator",
        "🃏 Flashcards",
        "📚 Smart Notes",
        "🧠 Concept Explainer",
        "🗺️ Mind Map",
        "📅 Study Planner",
        "📊 Progress"
    ]

    selected_page = st.radio(
        "Navigation",
        pages
    )

    st.divider()

    st.write("### 👤 Student")

    st.write(f"**Name:** {profile['name']}")
    st.write(f"**Class:** {profile['class']}")
    st.write(f"**Subject:** {profile['subject']}")

    st.divider()

    st.metric(
        "🏆 Level",
        stats.get("level", 1)
    )

    st.metric(
        "⭐ XP",
        stats.get("xp", 0)
    )

    st.metric(
        "🔥 Streak",
        stats.get("streak", 0)
    )

    st.divider()

    if st.button(
        "🔄 Change Profile",
        use_container_width=True
    ):

        st.session_state.profile = None
        st.session_state.student_id = None
        st.session_state.stats = None

        st.rerun()

    if st.button(
        "🗑️ Clear History",
        use_container_width=True
    ):

        if clear_history(student_id):

            st.success("History cleared.")

        else:

            st.error("Could not clear history.")


# ============================================================
# DASHBOARD
# ============================================================

if selected_page == "🏠 Dashboard":

    st.title("🏠 Student Dashboard")

    st.write(
        f"Welcome back, **{profile['name']}**! "
        "Ready to learn something new?"
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🏆 Level",
            stats.get("level", 1)
        )

    with col2:

        st.metric(
            "⭐ XP",
            stats.get("xp", 0)
        )

    with col3:

        st.metric(
            "📝 Quizzes",
            stats.get("quizzes", 0)
        )

    with col4:

        st.metric(
            "🔥 Streak",
            stats.get("streak", 0)
        )

    st.divider()

    st.subheader("🚀 Quick Study")

    q1, q2, q3 = st.columns(3)

    with q1:

        if st.button(
            "📝 Generate Quiz",
            use_container_width=True
        ):

            st.info(
                "Open **Quiz Generator** from the sidebar."
            )

    with q2:

        if st.button(
            "🃏 Make Flashcards",
            use_container_width=True
        ):

            st.info(
                "Open **Flashcards** from the sidebar."
            )

    with q3:

        if st.button(
            "📚 Make Notes",
            use_container_width=True
        ):

            st.info(
                "Open **Smart Notes** from the sidebar."
            )

    st.divider()

    st.subheader("📈 Your Progress")

    quizzes = stats.get("quizzes", 0)
    correct = stats.get("correct", 0)
    questions = stats.get("questions", 0)

    if questions > 0:

        accuracy = (correct / questions) * 100

    else:

        accuracy = 0

    st.progress(
        min(accuracy / 100, 1.0)
    )

    st.write(
        f"Overall quiz accuracy: **{accuracy:.1f}%**"
    )


# ============================================================
# AI STUDY ASSISTANT
# ============================================================

elif selected_page == "🤖 AI Study Assistant":

    st.title("🤖 AI Study Assistant")

    st.write(
        "Ask questions and get explanations adapted to your level."
    )

    topic = st.text_input(
        "📚 What topic are you studying?",
        placeholder="Example: Binary numbers"
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    request_type = st.selectbox(
        "What do you want?",
        [
            "Explain the topic",
            "Give examples",
            "Give practice questions",
            "Give revision points",
            "Explain step by step"
        ]
    )

    if st.button(
        "🚀 Generate",
        use_container_width=True
    ):

        if not topic.strip():

            st.warning("Enter a topic first.")

        else:

            prompt = f"""
You are an expert educational AI.

Student:
Name: {profile['name']}
Class: {profile['class']}
Subject: {profile['subject']}
Goal: {profile['goal']}

Topic:
{topic}

Difficulty:
{difficulty}

Request:
{request_type}

Create an educational response appropriate for this student's level.

Rules:
- Use clear language.
- Explain difficult words.
- Use examples.
- Do not unnecessarily repeat information.
- Make the answer useful for examination preparation.
"""

            with st.spinner("AI is preparing your study material..."):

                answer = ask_ai(prompt)

            st.session_state.generated_content = answer

            st.markdown(answer)

            save_history(
                student_id,
                {
                    "type": "assistant",
                    "topic": topic,
                    "content": answer,
                    "date": str(datetime.now())
                }
            )

            st.download_button(
                "⬇️ Download Notes",
                answer,
                file_name=f"{topic}_study_notes.txt",
                mime="text/plain"
            )


# ============================================================
# QUIZ GENERATOR
# ============================================================

elif selected_page == "📝 Quiz Generator":

    st.title("📝 AI Quiz Generator")

    st.write(
        "Create a custom quiz based on your subject and topic."
    )

    topic = st.text_input(
        "Topic",
        placeholder="Example: Photosynthesis"
    )

    number = st.slider(
        "Number of questions",
        5,
        20,
        10
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Easy",
            "Medium",
            "Hard"
        ]
    )

    if st.button(
        "📝 Generate Quiz",
        use_container_width=True
    ):

        if not topic.strip():

            st.warning("Enter a topic.")

        else:

            prompt = f"""
Create a {number}-question multiple-choice quiz.

Subject: {profile['subject']}
Class: {profile['class']}
Topic: {topic}
Difficulty: {difficulty}

Return ONLY valid JSON.

Format:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": 0,
    "explanation": "Short explanation"
  }}
]

The answer value must be 0, 1, 2, or 3.
"""

            with st.spinner("Generating quiz..."):

                result = ask_ai(prompt)

            try:

                clean = result.strip()

                clean = re.sub(
                    r"```json|```",
                    "",
                    clean
                ).strip()

                quiz = json.loads(clean)

                st.session_state.quiz_questions = quiz
                st.session_state.quiz_submitted = False
                st.session_state.quiz_score = 0

                st.success(
                    f"{len(quiz)} questions generated!"
                )

            except Exception:

                st.error(
                    "The AI returned an invalid quiz format. Please generate again."
                )

    if st.session_state.quiz_questions:

        st.divider()

        answers = []

        for i, question in enumerate(
            st.session_state.quiz_questions
        ):

            st.markdown(
                f"### Question {i + 1}"
            )

            st.write(
                question["question"]
            )

            selected = st.radio(
                "Choose your answer:",
                question["options"],
                key=f"quiz_{i}"
            )

            answers.append(
                question["options"].index(selected)
            )

        if st.button(
            "✅ Submit Quiz",
            use_container_width=True
        ):

            score = 0

            for i, question in enumerate(
                st.session_state.quiz_questions
            ):

                if answers[i] == question["answer"]:
                    score += 1

            st.session_state.quiz_score = score
            st.session_state.quiz_submitted = True

            total = len(
                st.session_state.quiz_questions
            )

            percentage = (
                score / total
            ) * 100

            xp_earned = score * 10

            stats["quizzes"] = (
                stats.get("quizzes", 0) + 1
            )

            stats["questions"] = (
                stats.get("questions", 0) + total
            )

            stats["correct"] = (
                stats.get("correct", 0) + score
            )

            stats["xp"] = (
                stats.get("xp", 0) + xp_earned
            )

            stats["level"] = (
                stats["xp"] // 100
            ) + 1

            save_stats(
                student_id,
                stats
            )

            st.session_state.stats = stats

            st.success(
                f"🎉 You scored {score}/{total} ({percentage:.1f}%)"
            )

            st.info(
                f"⭐ You earned {xp_earned} XP!"
            )

            if percentage >= 80:

                st.balloons()

        if st.session_state.quiz_submitted:

            st.divider()

            st.subheader("📖 Answer Review")

            for i, question in enumerate(
                st.session_state.quiz_questions
            ):

                correct_index = question["answer"]

                st.write(
                    f"**Q{i + 1}:** "
                    f"{question['options'][correct_index]}"
                )

                st.caption(
                    question.get(
                        "explanation",
                        ""
                    )
                )


# ============================================================
# FLASHCARDS
# ============================================================

elif selected_page == "🃏 Flashcards":

    st.title("🃏 AI Flashcards")

    topic = st.text_input(
        "Topic",
        placeholder="Example: Electricity"
    )

    number = st.slider(
        "Number of flashcards",
        5,
        20,
        10
    )

    if st.button(
        "🃏 Generate Flashcards",
        use_container_width=True
    ):

        if not topic.strip():

            st.warning("Enter a topic.")

        else:

            prompt = f"""
Create {number} educational flashcards.

Subject: {profile['subject']}
Class: {profile['class']}
Topic: {topic}

Return ONLY JSON.

Format:

[
  {{
    "front": "Question or term",
    "back": "Answer"
  }}
]
"""

            with st.spinner("Creating flashcards..."):

                result = ask_ai(prompt)

            try:

                clean = re.sub(
                    r"```json|```",
                    "",
                    result
                ).strip()

                cards = json.loads(clean)

                st.session_state.flashcards = cards

            except Exception:

                st.error(
                    "Could not create flashcards. Try again."
                )

    if st.session_state.flashcards:

        st.divider()

        for i, card in enumerate(
            st.session_state.flashcards
        ):

            with st.expander(
                f"🃏 Card {i + 1}: {card['front']}"
            ):

                st.write(
                    card["back"]
                )


# ============================================================
# SMART NOTES
# ============================================================

elif selected_page == "📚 Smart Notes":

    st.title("📚 Smart Notes Generator")

    topic = st.text_input(
        "Topic",
        placeholder="Example: The Human Heart"
    )

    note_style = st.selectbox(
        "Notes style",
        [
            "Exam Revision",
            "Detailed",
            "Short",
            "Bullet Points",
            "O Level Notes"
        ]
    )

    if st.button(
        "📚 Generate Notes",
        use_container_width=True
    ):

        if not topic.strip():

            st.warning("Enter a topic.")

        else:

            prompt = f"""
Create high-quality study notes.

Subject: {profile['subject']}
Class: {profile['class']}
Topic: {topic}
Style: {note_style}

Include:
- Important definitions
- Key concepts
- Examples
- Important facts
- Exam tips
- Common mistakes

Use headings and bullet points.
"""

            with st.spinner("Preparing notes..."):

                notes = ask_ai(prompt)

            st.markdown(notes)

            st.download_button(
                "⬇️ Download Notes",
                notes,
                file_name=f"{topic}_notes.txt",
                mime="text/plain"
            )


# ============================================================
# CONCEPT EXPLAINER
# ============================================================

elif selected_page == "🧠 Concept Explainer":

    st.title("🧠 Concept Explainer")

    concept = st.text_input(
        "What concept do you find difficult?",
        placeholder="Example: Newton's First Law"
    )

    explanation_style = st.selectbox(
        "Explain it using",
        [
            "Simple language",
            "Real-life example",
            "Step-by-step explanation",
            "Exam-style explanation"
        ]
    )

    if st.button(
        "🧠 Explain Concept",
        use_container_width=True
    ):

        if not concept.strip():

            st.warning("Enter a concept.")

        else:

            prompt = f"""
Explain this concept to a student.

Student class: {profile['class']}
Subject: {profile['subject']}

Concept:
{concept}

Explanation style:
{explanation_style}

Use:
1. Simple definition
2. Easy explanation
3. Real-world example
4. Important points
5. Exam tip
"""

            with st.spinner("Explaining..."):

                answer = ask_ai(prompt)

            st.markdown(answer)


# ============================================================
# MIND MAP
# ============================================================

elif selected_page == "🗺️ Mind Map":

    st.title("🗺️ AI Mind Map Generator")

    topic = st.text_input(
        "Topic",
        placeholder="Example: Data Representation"
    )

    if st.button(
        "🗺️ Generate Mind Map",
        use_container_width=True
    ):

        if not topic.strip():

            st.warning("Enter a topic.")

        else:

            prompt = f"""
Create a text-based mind map for:

Subject: {profile['subject']}
Class: {profile['class']}
Topic: {topic}

Use this structure:

MAIN TOPIC
├── Branch 1
│   ├── Point
│   └── Point
├── Branch 2
│   ├── Point
│   └── Point
└── Branch 3
    ├── Point
    └── Point

Make it useful for revision.
"""

            with st.spinner("Building mind map..."):

                mindmap = ask_ai(prompt)

            st.code(
                mindmap,
                language="text"
            )

            st.download_button(
                "⬇️ Download Mind Map",
                mindmap,
                file_name=f"{topic}_mindmap.txt",
                mime="text/plain"
            )


# ============================================================
# STUDY PLANNER
# ============================================================

elif selected_page == "📅 Study Planner":

    st.title("📅 AI Study Planner")

    subjects = st.text_area(
        "Subjects",
        placeholder="Mathematics\nPhysics\nComputer Science\nGeography"
    )

    hours = st.slider(
        "Study hours per day",
        1,
        8,
        2
    )

    days = st.slider(
        "Number of days",
        3,
        30,
        7
    )

    weak_topic = st.text_input(
        "Weak topic",
        placeholder="Example: Trigonometry"
    )

    if st.button(
        "📅 Create Study Plan",
        use_container_width=True
    ):

        if not subjects.strip():

            st.warning("Enter your subjects.")

        else:

            prompt = f"""
Create a realistic study plan.

Student class: {profile['class']}

Subjects:
{subjects}

Study hours per day:
{hours}

Number of days:
{days}

Weak topic:
{weak_topic}

Include:
- Daily subjects
- Topics
- Revision
- Practice questions
- Breaks
- Review days

Make the plan realistic for a student.
"""

            with st.spinner("Creating your plan..."):

                plan = ask_ai(prompt)

            st.markdown(plan)

            st.download_button(
                "⬇️ Download Study Plan",
                plan,
                file_name="study_plan.txt",
                mime="text/plain"
            )


# ============================================================
# PROGRESS
# ============================================================

elif selected_page == "📊 Progress":

    st.title("📊 My Progress")

    quizzes = stats.get("quizzes", 0)
    questions = stats.get("questions", 0)
    correct = stats.get("correct", 0)
    xp = stats.get("xp", 0)
    level = stats.get("level", 1)
    streak = stats.get("streak", 0)

    if questions > 0:

        accuracy = (
            correct / questions
        ) * 100

    else:

        accuracy = 0

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "🏆 Level",
            level
        )

    with c2:

        st.metric(
            "⭐ XP",
            xp
        )

    with c3:

        st.metric(
            "🔥 Streak",
            streak
        )

    st.divider()

    st.subheader("📝 Quiz Performance")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Quizzes",
            quizzes
        )

    with c2:

        st.metric(
            "Questions",
            questions
        )

    with c3:

        st.metric(
            "Correct",
            correct
        )

    st.divider()

    st.subheader("🎯 Accuracy")

    st.progress(
        min(accuracy / 100, 1)
    )

    st.write(
        f"Your current accuracy is **{accuracy:.1f}%**"
    )

    st.divider()

    st.subheader("🏆 Level System")

    next_level_xp = level * 100

    st.write(
        f"XP: **{xp} / {next_level_xp}**"
    )

    progress = (
        xp % 100
    ) / 100

    st.progress(progress)

    st.caption(
        "Complete quizzes and study activities to earn XP."
    )
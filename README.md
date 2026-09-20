# 🎓 StudyPro AI

**StudyPro AI** is an AI-powered study platform made for students.

It helps students learn, practice, revise, and organize their studies using **Google Gemini AI**.

Students can create a profile, generate quizzes, make flashcards, create notes, explain difficult concepts, build mind maps, and create study plans.

The app also tracks **XP, levels, quiz scores, accuracy, and study streaks**.

---

## 🌐 Live Demo

👉 **[Open StudyPro AI](https://studypro-ai-zjnvnezjpw8usbuemegfck.streamlit.app/)**

Try the app online and explore the different study tools.

---

# ✨ Features

## 👤 Student Profile

Create a student profile with:

* Student ID
* Name
* Class / Level
* School
* Main Subject
* Study Goal

Returning students can use their Student ID to access their profile and progress.

---

## 🤖 AI Study Assistant

Ask AI about any study topic.

You can choose:

* Difficulty level
* Type of help you want
* Topic you are studying

The AI creates an explanation based on your class and subject.

---

## 📝 Quiz Generator

Create your own AI-generated quizzes.

You can choose:

* Topic
* Number of questions
* Difficulty

After completing a quiz, you get:

* Score
* Percentage
* Correct answers
* Answer explanations
* XP

---

## 🃏 Flashcards

Create AI-powered flashcards for revision.

Each flashcard contains:

**Front:** Question or term

**Back:** Answer

This can help with quick revision.

---

## 📚 Smart Notes

Generate study notes for any topic.

Choose a style such as:

* Exam Revision
* Detailed
* Short
* Bullet Points
* O Level Notes

You can also download the generated notes as a text file.

---

## 🧠 Concept Explainer

Having trouble understanding a concept?

Enter the concept and choose how you want it explained:

* Simple language
* Real-life example
* Step-by-step explanation
* Exam-style explanation

---

## 🗺️ Mind Map Generator

Generate a text-based mind map for a topic.

Example:

```text
Data Representation
├── Binary
│   ├── 0
│   └── 1
├── Decimal
│   ├── Digits
│   └── Place Value
└── Hexadecimal
    ├── Digits
    └── Letters
```

Mind maps can be downloaded for revision.

---

## 📅 Study Planner

Create a study plan using AI.

You can enter:

* Subjects
* Study hours per day
* Number of days
* Weak topic

The AI creates a study plan with:

* Daily subjects
* Topics
* Revision
* Practice questions
* Breaks
* Review days

---

## 📊 Progress Tracking

StudyPro AI tracks your learning progress.

It includes:

* 🏆 Level
* ⭐ XP
* 📝 Number of quizzes
* ❓ Questions answered
* ✅ Correct answers
* 🎯 Accuracy
* 🔥 Study streak

### XP System

Students earn XP by completing quizzes.

Every correct quiz answer gives:

**10 XP**

The student's level increases as they earn more XP.

---

# 🛠️ Technologies Used

This project uses:

* 🐍 **Python**
* 🎈 **Streamlit**
* 🤖 **Google Gemini AI**
* 🔥 **Firebase Realtime Database**
* 🌐 **Requests**

---

# 📁 Project Files

```text
StudyPro-AI/
│
├── app.py
├── requirements.txt
└── README.md
```

### `app.py`

The main Python file containing the complete StudyPro AI application.

### `requirements.txt`

Contains the Python packages needed to run the application.

### `README.md`

Contains information about the project and how to use it.

---

# 🚀 How to Run

## 1. Download the Project

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/StudyPro-AI.git
```

Open the project folder:

```bash
cd StudyPro-AI
```

---

## 2. Install Requirements

Run:

```bash
pip install -r requirements.txt
```

---

## 3. Add Gemini API Key

The application uses Streamlit Secrets for the Gemini API key.

Add:

```text
GEMINI_API_KEY
```

to your Streamlit Secrets.

The app uses the key with:

```python
st.secrets["GEMINI_API_KEY"]
```

---

## 4. Run the App

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 🔥 Firebase

StudyPro AI uses **Firebase Realtime Database** to save student information and progress.

The database structure is:

```text
students
│
├── student_id
│   │
│   ├── profile
│   │
│   ├── history
│   │
│   └── stats
```

### Profile

Stores information such as:

```text
Name
Class
School
Subject
Goal
Created Date
```

### History

Stores generated study content and previous activities.

### Stats

Stores:

```text
XP
Level
Quizzes
Questions
Correct Answers
Streak
```

---

# 💡 How StudyPro AI Works

```text
Student
   ↓
Create Profile
   ↓
Choose Study Tool
   ↓
Enter Topic
   ↓
Google Gemini AI
   ↓
Generate Study Material
   ↓
Student Learns / Practices
   ↓
Progress Saved in Firebase
```

---

# 📚 Study Tools

| Tool                  | Purpose                     |
| --------------------- | --------------------------- |
| 🤖 AI Study Assistant | Ask study questions         |
| 📝 Quiz Generator     | Create quizzes              |
| 🃏 Flashcards         | Quick revision              |
| 📚 Smart Notes        | Create study notes          |
| 🧠 Concept Explainer  | Understand difficult topics |
| 🗺️ Mind Map          | Organize topics             |
| 📅 Study Planner      | Plan study time             |
| 📊 Progress           | Track learning progress     |

---

# 🔐 Security

The Gemini API key should not be written directly into the Python code.

The project uses Streamlit Secrets:

```python
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
```

Never upload your private API key to GitHub.

---

# 🚀 Future Improvements

Some features I would like to add in future versions:

* 📄 PDF upload and analysis
* 🧾 AI-generated summaries from PDFs
* 🌐 Multiple language support
* 🇵🇰 Urdu study support
* 🏆 More achievements
* 🔥 Automatic streak tracking
* 📈 Progress charts
* 📚 Subject-specific dashboards
* 🔐 Student login system
* 👨‍🏫 Teacher dashboard
* 📱 Better mobile support
* 📝 More quiz types

---

# 🎯 Project Goal

The goal of StudyPro AI is to make studying easier by putting different AI study tools in one application.

Instead of using separate tools for notes, quizzes, flashcards, explanations, and study planning, students can use them all in one place.

---

# 👨‍💻 Author

**Ahmed Faisal**

### Skills Used

🐍 Python
🎈 Streamlit
🤖 Google Gemini AI
🔥 Firebase
📊 AI Application Development

---

## ⭐ Support the Project

If you like **StudyPro AI**, you can:

⭐ Star the GitHub repository
🍴 Fork the project
💡 Suggest new features
🐛 Report bugs

---

### 🎓 Study smarter. Practice better. Learn with AI.

**Built with Python 🐍 + Streamlit 🎈 + Gemini 🤖 + Firebase 🔥**

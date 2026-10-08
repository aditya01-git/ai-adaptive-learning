# Ada AI - Adaptive Programming Language Learning System

A BCA final-year project built with **Python, Streamlit, SQLite, Pandas, NumPy, Scikit-learn, Python AST/static analysis, and an LLM API**.

## What makes this version complete?

### 1. Multi-language learning
- Python
- Java
- JavaScript

Each language has its own learning progress.

### 2. Structured topic learning
Every topic contains:
- Concept explanation
- Example code
- Coding challenge
- Quiz
- AI coaching

Python and Java contain 7 core topics. JavaScript contains 8 topics including DOM Basics.

### 3. Real AI Tutor
The project supports:
- OpenAI API
- Anthropic API

The AI receives the selected language, current topic, and ML performance context. It can:
- Explain concepts
- Give beginner examples
- Give hints
- Explain errors
- Review submitted code
- Generate practice exercises
- Adapt explanations to the learner's performance

The app does **not** pretend a canned response is a live LLM. If no API key is connected, it clearly shows Offline Tutor Mode.

### 4. Machine Learning
A Random Forest classifier analyzes:
- Latest quiz score
- Average quiz score
- Number of attempts
- Performance trend
- Coding score

It classifies topics as:
- Needs Practice
- Improving
- Mastered
- Not Started

### 5. Adaptive learning
The recommendation engine identifies the weakest or most appropriate next topic and guides the learner through it.

### 6. Coding Lab
- Streamlit code editor
- Static code analysis
- Python AST checks
- Java and JavaScript pattern checks
- Challenge scoring
- AI code review
- Submitted code is never executed by the application

### 7. SQLite database
Stores:
- Users
- Quiz attempts
- Coding attempts
- ML predictions
- Recommendations
- AI tutor interactions

### 8. Dashboard
Includes:
- Quiz average
- Coding attempts
- Mastered topics
- Topic performance chart
- ML confidence
- Weak areas
- Strong areas
- Adaptive recommendation
- Recent activity

## Project flow

```text
Select Language
      ↓
Select Topic
      ↓
Learn Concept
      ↓
Study Example
      ↓
Coding Practice
      ↓
Quiz
      ↓
SQLite stores performance
      ↓
Random Forest analyzes performance
      ↓
Skill Classification
      ↓
Adaptive Recommendation
      ↓
AI Tutor personalizes help
      ↓
Improved Performance
```

## Folder structure

```text
ai_programming_tutor/
├── app.py
├── database.py
├── ml_model.py
├── code_analyzer.py
├── ai_tutor.py
├── learning_engine.py
├── content.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml
```

## Windows setup

Open the project folder in VS Code.

### 1. Create virtual environment

```powershell
python -m venv .venv
```

### 2. Install packages

If PowerShell activation is blocked, you do **not** need to activate the environment.

```powershell
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
```

### 3. Start Streamlit

```powershell
.\\.venv\\Scripts\\python.exe -m streamlit run app.py
```

Open the displayed local address, normally:

```text
http://localhost:8501
```

## Connecting the real AI

Inside the app sidebar:

1. Open **Connect real AI**.
2. Select OpenAI or Anthropic.
3. Enter your API key in the password field.
4. Click **Connect AI**.
5. Use **AI Tutor**, **AI Coach**, **Explain with AI**, or **AI code review**.

The API key is kept in the Streamlit session environment and is not saved in SQLite.

Never commit an API key to GitHub.

## Viva explanation

**AI:** The LLM provides personalized explanations, hints, debugging help, coding feedback, and practice questions.

**ML:** Random Forest uses learner performance features to classify each topic as Needs Practice, Improving, or Mastered.

**Adaptive learning:** The recommendation engine selects the next topic using the ML skill profile.

**Database:** SQLite stores the learner's progress, quiz attempts, coding attempts, ML predictions, recommendations, and tutor interactions.

**Code analysis:** Python code uses AST/static checks. Java and JavaScript use static pattern checks. User programs are not executed.

## Important

The project is intentionally designed as a strong BCA final-year system without React, Node.js, MongoDB, RAG, vector databases, multi-agent systems, or complicated authentication.

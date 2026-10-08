import os
import html
from datetime import datetime, timedelta

import altair as alt
import pandas as pd
import streamlit as st

import database as db
from content import LANGUAGES, CONTENT, TOPIC_META, LANGUAGE_META
from ml_model import train_model, classify, recommend
from code_analyzer import check_code, evaluate_challenge
from ai_tutor import ask, lesson, enabled

st.set_page_config(
    page_title="Ada AI | Adaptive Coding Academy",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

db.init_db()

# Train the adaptive-learning model once when the app starts.
@st.cache_resource
def get_ml_model():
    return train_model()

MODEL = get_ml_model()

# -----------------------------
# Configuration
# -----------------------------
TOPIC_SETS = {
    "Python": ["Variables", "Data Types", "Conditions", "Loops", "Functions", "Arrays/Lists", "OOP"],
    "Java": ["Variables", "Data Types", "Conditions", "Loops", "Functions", "Arrays/Lists", "OOP"],
    "JavaScript": ["Variables", "Data Types", "Conditions", "Loops", "Functions", "Arrays/Lists", "OOP", "DOM Basics"],
}

DISPLAY_TOPIC = {
    "Conditions": "If-Else / Conditions",
    "Arrays/Lists": "Arrays / Lists",
    "OOP": "Classes & OOP",
    "DOM Basics": "DOM Basics",
}

TOPIC_DESCRIPTIONS = {
    "Variables": "Store and update values",
    "Data Types": "Understand different kinds of data",
    "Conditions": "Make decisions in your program",
    "Loops": "Repeat work efficiently",
    "Functions": "Build reusable logic",
    "Arrays/Lists": "Work with collections of values",
    "OOP": "Model programs with objects and classes",
    "DOM Basics": "Control webpages with JavaScript",
}

STATUS_COLORS = {
    "Needs Practice": "#ef4444",
    "Improving": "#f59e0b",
    "Mastered": "#10b981",
    "Not Started": "#94a3b8",
}
STATUS_ICON = {
    "Needs Practice": "🟠",
    "Improving": "🟡",
    "Mastered": "🟢",
    "Not Started": "⚪",
}

# -----------------------------
# Premium UI styling
# -----------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
  --ink:#17152b; --muted:#667085; --line:#e9e7f2; --surface:#ffffff;
  --purple:#7c3aed; --pink:#ec4899; --soft:#f7f5ff;
}
html, body, [class*="css"] { font-family:'DM Sans', sans-serif; }
.block-container { max-width: 1380px; padding: 1.2rem 2rem 4rem; }
[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#100c25 0%,#17102f 52%,#24124b 100%);
  border-right:1px solid rgba(255,255,255,.08);
}
[data-testid="stSidebar"] * { color:#f8fafc; }
[data-testid="stSidebar"] .stCaption { color:#b7b2ca !important; }
[data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.10); }

.brand { display:flex; gap:12px; align-items:center; margin:4px 0 18px; }
.brand-icon { width:45px;height:45px;border-radius:14px;display:grid;place-items:center;
  background:linear-gradient(135deg,#8b5cf6,#ec4899);font-size:1.35rem;box-shadow:0 10px 28px rgba(139,92,246,.3); }
.brand-title { font-family:'Space Grotesk';font-weight:700;font-size:1.18rem;line-height:1; }
.brand-sub { color:#aaa4bf;font-size:.72rem;margin-top:4px; }

.hero { position:relative; overflow:hidden; border-radius:30px; padding:34px 36px; color:#fff;
  min-height:190px; box-shadow:0 22px 60px rgba(31,24,72,.20); margin-bottom:24px; }
.hero:after { content:''; position:absolute; width:280px;height:280px;border-radius:50%;
  right:-90px;top:-120px;background:rgba(255,255,255,.12); }
.hero h1 { font-family:'Space Grotesk'; font-size:2.35rem; margin:0; font-weight:700; position:relative;z-index:2; }
.hero p { margin:.65rem 0 0; max-width:760px; opacity:.9; font-size:1rem; position:relative;z-index:2; }
.hero .hero-chip { display:inline-block;margin-top:18px;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.2);
  padding:7px 12px;border-radius:999px;font-size:.78rem;font-weight:700;position:relative;z-index:2; }

.section-title { font-family:'Space Grotesk'; font-size:1.3rem; font-weight:700; color:var(--ink); margin:25px 0 12px; }
.muted { color:var(--muted); }
.card { background:#fff;border:1px solid var(--line);border-radius:22px;padding:21px;box-shadow:0 10px 35px rgba(31,24,72,.055); }
.metric { background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px;box-shadow:0 9px 28px rgba(31,24,72,.05);min-height:105px; }
.metric .value { font-family:'Space Grotesk';font-size:1.75rem;font-weight:700;color:var(--ink); }
.metric .label { color:var(--muted);font-size:.78rem;margin-top:3px; }

.language-card { border-radius:24px; padding:23px; color:#fff; min-height:205px; position:relative; overflow:hidden;
  box-shadow:0 18px 35px rgba(0,0,0,.10); }
.language-card:after { content:'';position:absolute;width:170px;height:170px;border-radius:50%;right:-70px;bottom:-85px;background:rgba(255,255,255,.12); }
.language-card .icon { font-size:2.15rem; }
.language-card h3 { margin:7px 0 2px;font-family:'Space Grotesk'; }
.language-card .pct { font-size:1.9rem;font-weight:800;margin-top:16px; }

.topic-shell { background:#fff;border:1px solid var(--line);border-radius:22px;padding:18px;min-height:175px;
  box-shadow:0 8px 28px rgba(31,24,72,.055); transition:.18s; }
.topic-shell:hover { transform:translateY(-3px); box-shadow:0 16px 35px rgba(31,24,72,.10); }
.topic-number { color:#9b96aa;font-size:.73rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase; }
.topic-icon { font-size:1.75rem;margin:7px 0 4px; }
.topic-name { font-family:'Space Grotesk';font-weight:700;font-size:1rem;color:var(--ink); }
.topic-desc { color:var(--muted);font-size:.78rem;min-height:34px;margin-top:4px; }
.status { display:inline-block;border-radius:999px;padding:5px 9px;font-size:.68rem;font-weight:800;margin-top:9px; }

.path-card { background:linear-gradient(135deg,#17132e,#2c1d55);border-radius:25px;padding:23px;color:#fff;box-shadow:0 16px 35px rgba(36,22,75,.18); }
.path-card h3 { font-family:'Space Grotesk';margin:0; }
.path-step { display:flex;gap:12px;align-items:flex-start;padding:11px 0;border-bottom:1px solid rgba(255,255,255,.10); }
.path-step:last-child { border-bottom:0; }
.path-dot { width:30px;height:30px;border-radius:10px;background:rgba(255,255,255,.11);display:grid;place-items:center;flex:none; }

.ai-banner { border:1px solid #ddd0ff;background:linear-gradient(135deg,#f7f3ff,#fff4fa);border-radius:22px;padding:19px 21px; }
.ai-dot { display:inline-block;width:8px;height:8px;border-radius:50%;background:#10b981;margin-right:7px; }

.stButton>button { border-radius:13px !important; border:1px solid #e5e1f0 !important; font-weight:700 !important;
  min-height:42px !important; transition:.18s !important; }
.stButton>button:hover { transform:translateY(-2px); box-shadow:0 10px 25px rgba(124,58,237,.15); }
[data-testid="stMetric"] { background:#fff;border:1px solid var(--line);border-radius:18px;padding:13px; }
.stProgress > div > div > div > div { background:linear-gradient(90deg,#7c3aed,#ec4899); }
[data-testid="stChatMessage"] { border-radius:18px; border:1px solid #eeeaf7; }
.stTextArea textarea { border-radius:16px !important; }
.stTextInput input { border-radius:12px !important; }
div[data-baseweb="tab-list"] { gap:8px; }
button[data-baseweb="tab"] { border-radius:11px !important; padding:9px 14px !important; }
.small { color:var(--muted);font-size:.82rem; }
.successbox { background:#ecfdf5;border:1px solid #a7f3d0;padding:17px;border-radius:17px; }
.warnbox { background:#fff7ed;border:1px solid #fed7aa;padding:17px;border-radius:17px; }
.info-box { background:#f5f3ff;border:1px solid #ddd6fe;padding:17px;border-radius:17px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -----------------------------
# Helpers
# -----------------------------
def display_topic(topic):
    return DISPLAY_TOPIC.get(topic, topic)


def topic_meta(topic):
    return TOPIC_META[topic]


def active_topics(language):
    return TOPIC_SETS[language]


def go(page, topic=None):
    st.session_state.page = page
    if topic is not None:
        st.session_state.topic = topic


def hero(title, subtitle, gradient, chip=None):
    chip_html = f'<div class="hero-chip">{html.escape(chip)}</div>' if chip else ''
    st.markdown(
        f'<div class="hero" style="background:{gradient}"><h1>{title}</h1><p>{subtitle}</p>{chip_html}</div>',
        unsafe_allow_html=True,
    )


def status_badge(status):
    color = STATUS_COLORS[status]
    return f'<span class="status" style="background:{color}18;color:{color}">{STATUS_ICON[status]} {status}</span>'


def get_status(user, language):
    q = db.get_quizzes(user, language)
    c = db.get_coding(user, language)
    topics = active_topics(language)
    return q, c, classify(MODEL, q, c, topics)


def streak(df):
    if df.empty:
        return 0
    days = set(pd.to_datetime(df.ts).dt.date)
    d = datetime.now().date()
    if d not in days:
        d -= timedelta(days=1)
    n = 0
    while d in days:
        n += 1
        d -= timedelta(days=1)
    return n


def xp(user):
    q = db.get_quizzes(user)
    c = db.get_coding(user)
    return int(q.score.sum() * 10 + (q.score == q.total).sum() * 20 + c[c.passed == 1].shape[0] * 25)


def configure_ai():
    provider = st.session_state.get("ai_provider", "OpenAI")
    key = st.session_state.get("ai_key", "").strip()
    if key:
        if provider == "OpenAI":
            os.environ["OPENAI_API_KEY"] = key
            os.environ.pop("ANTHROPIC_API_KEY", None)
        else:
            os.environ["ANTHROPIC_API_KEY"] = key
            os.environ.pop("OPENAI_API_KEY", None)
    return enabled()


def topic_grid(user, language, status):
    topics = active_topics(language)
    cols = st.columns(4)
    for i, topic in enumerate(topics):
        row = status[status.topic == topic].iloc[0]
        meta = topic_meta(topic)
        with cols[i % 4]:
            st.markdown(
                f'''<div class="topic-shell">
                <div class="topic-number">Topic {i+1:02d}</div>
                <div class="topic-icon">{meta["icon"]}</div>
                <div class="topic-name">{display_topic(topic)}</div>
                <div class="topic-desc">{TOPIC_DESCRIPTIONS[topic]}</div>
                {status_badge(row.status)}
                <div class="small" style="margin-top:8px">{row.avg_pct:.0f}% average · {int(row.attempts)} attempts</div>
                </div>''',
                unsafe_allow_html=True,
            )
            if st.button("Open topic →", key=f"open-{language}-{topic}", use_container_width=True):
                go("📖 Topic", topic)
                st.rerun()


def render_code_lab(user, language, topic):
    data = CONTENT[language][topic]
    st.markdown(f'<div class="card"><b>🎯 Challenge</b><p style="margin:.45rem 0 0">{html.escape(data["challenge"])}</p></div>', unsafe_allow_html=True)
    st.write("")
    code = st.text_area(
        "Code editor",
        height=300,
        key=f"editor-{language}-{topic}",
        placeholder=f"Write your {language} solution here...",
    )
    a, b, c = st.columns(3)
    if a.button("🔍 Analyze code", use_container_width=True, key=f"an-{language}-{topic}"):
        st.session_state[f"issues-{language}-{topic}"] = check_code(language, code)
    if b.button("🎯 Check challenge", use_container_width=True, key=f"ev-{language}-{topic}"):
        passed, score, msg = evaluate_challenge(language, code, data["keywords"])
        issues = check_code(language, code)
        db.save_code(user, language, topic, code, passed, len(issues), score, msg)
        st.session_state[f"result-{language}-{topic}"] = (passed, score, msg, issues)
    if c.button("🤖 AI code review", use_container_width=True, key=f"ai-{language}-{topic}"):
        if not configure_ai():
            st.warning("Connect an AI API key in the sidebar first.")
        else:
            issues = check_code(language, code)
            prompt = (
                f"Review this {language} code for the topic {topic}. Challenge: {data['challenge']}\n"
                f"Code:\n```\n{code}\n```\nStatic feedback: {issues or 'No obvious static issues.'}"
            )
            with st.spinner("Ada is reviewing your code..."):
                answer = ask(language, topic, prompt)
            db.save_tutor_message(user, language, "assistant", answer, topic)
            st.session_state[f"review-{language}-{topic}"] = answer

    issues = st.session_state.get(f"issues-{language}-{topic}")
    if issues is not None:
        if issues:
            st.warning("\n".join("• " + x for x in issues))
        else:
            st.success("No obvious static issues found. Your code was not executed.")

    result = st.session_state.get(f"result-{language}-{topic}")
    if result:
        passed, score, msg, issues = result
        box = "successbox" if passed else "warnbox"
        title = "✅ Challenge passed" if passed else "🧭 Keep practicing"
        st.markdown(
            f'<div class="{box}"><b>{title}</b><br>{html.escape(msg)}<br><br><b>Practice score: {score:.0f}%</b></div>',
            unsafe_allow_html=True,
        )

    review = st.session_state.get(f"review-{language}-{topic}")
    if review:
        st.markdown("### 🤖 Ada's AI code review")
        st.markdown(f'<div class="card">{review}</div>', unsafe_allow_html=True)


# -----------------------------
# Session + sidebar
# -----------------------------
st.session_state.setdefault("page", "🏠 Home")
st.session_state.setdefault("topic", "Variables")
st.session_state.setdefault("user", "Student")
st.session_state.setdefault("ai_provider", "OpenAI")
st.session_state.setdefault("ai_key", "")

with st.sidebar:
    st.markdown(
        '<div class="brand"><div class="brand-icon">🤖</div><div><div class="brand-title">ADA AI</div><div class="brand-sub">Adaptive Programming Academy</div></div></div>',
        unsafe_allow_html=True,
    )

    user = st.text_input("Learner name", value=st.session_state.user, key="user_input")
    user = user.strip() or "Student"
    st.session_state.user = user

    language = st.selectbox(
        "Learning language",
        LANGUAGES,
        format_func=lambda x: f'{LANGUAGE_META[x]["icon"]}  {x}',
        key="language_select",
    )

    pages = ["🏠 Home", "📚 Learn", "📖 Topic", "📝 Quiz", "💻 Practice", "🤖 AI Tutor", "📊 Dashboard"]
    st.radio("Workspace", pages, key="page")

    current_topics = active_topics(language)
    if st.session_state.topic not in current_topics:
        st.session_state.topic = current_topics[0]
    st.selectbox(
        "Current topic",
        current_topics,
        format_func=lambda x: f'{TOPIC_META[x]["icon"]}  {display_topic(x)}',
        key="topic",
    )

    q_all = db.get_quizzes(user)
    total_xp = xp(user)
    level = total_xp // 100 + 1
    st.divider()
    st.markdown(f"**⭐ Level {level}**  ·  **{total_xp} XP**")
    st.progress((total_xp % 100) / 100)
    st.caption(f"🔥 {streak(q_all)} day learning streak")

    with st.expander("🔑 Connect real AI", expanded=not enabled()):
        st.caption("Your key is used only during this session and is not stored in SQLite.")
        st.selectbox("Provider", ["OpenAI", "Anthropic"], key="ai_provider")
        st.text_input(
            "API key",
            type="password",
            key="ai_key",
            placeholder="Paste your API key here",
        )
        if st.button("Connect AI", use_container_width=True):
            if configure_ai():
                st.success("AI connected for this session.")
                st.rerun()
            else:
                st.warning("Enter an API key first.")
        if enabled():
            st.success("🟢 Live LLM connected")
        else:
            st.info("⚪ Offline tutor mode")

q, c, status = get_status(user, language)
rec_topic, rec_reason = recommend(status)
if st.session_state.topic not in active_topics(language):
    st.session_state.topic = active_topics(language)[0]
current = status[status.topic == st.session_state.topic].iloc[0]
langmeta = LANGUAGE_META[language]

# -----------------------------
# Home
# -----------------------------
if st.session_state.page == "🏠 Home":
    hero(
        f"Welcome to Ada, {html.escape(user)} 👋",
        "An adaptive coding academy that teaches concepts, measures your skills, recommends what to study next, and lets an LLM tutor you when AI is connected.",
        langmeta["gradient"],
        f'{langmeta["icon"]} {language} learning path',
    )

    avg = float(q.pct.mean()) if not q.empty else 0
    mastered = int((status.status == "Mastered").sum())
    m = st.columns(4)
    for col, value, label in zip(
        m,
        [f"{avg:.0f}%", f"{mastered}/{len(active_topics(language))}", str(len(q)), str(len(c))],
        ["Quiz average", "Topics mastered", "Quiz attempts", "Coding attempts"],
    ):
        col.markdown(f'<div class="metric"><div class="value">{value}</div><div class="label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">🧭 Your learning journey</div>', unsafe_allow_html=True)
    left, right = st.columns([1.7, 1])
    with left:
        topic_grid(user, language, status)
    with right:
        st.markdown(
            f'''<div class="path-card">
            <div class="small" style="color:#bdb4d8">ADAPTIVE NEXT STEP</div>
            <h3 style="margin-top:7px">{TOPIC_META[rec_topic]["icon"] if rec_topic else "🏆"} {display_topic(rec_topic) if rec_topic else "Path complete"}</h3>
            <p style="color:#ddd7ed">{html.escape(rec_reason)}</p>
            <div class="path-step"><div class="path-dot">1</div><div><b>Learn</b><br><span style="color:#bbb3ce">Understand the concept</span></div></div>
            <div class="path-step"><div class="path-dot">2</div><div><b>Practice</b><br><span style="color:#bbb3ce">Solve the coding challenge</span></div></div>
            <div class="path-step"><div class="path-dot">3</div><div><b>Measure</b><br><span style="color:#bbb3ce">Quiz + ML skill analysis</span></div></div>
            <div class="path-step"><div class="path-dot">4</div><div><b>Adapt</b><br><span style="color:#bbb3ce">Get your next recommendation</span></div></div>
            </div>''',
            unsafe_allow_html=True,
        )
        if rec_topic and st.button("🚀 Start recommended topic", use_container_width=True):
            go("📖 Topic", rec_topic)
            st.rerun()

    st.markdown('<div class="section-title">💻 Choose another language</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, lg in enumerate(LANGUAGES):
        lq, lc, ls = get_status(user, lg)
        pct = float(lq.pct.mean()) if not lq.empty else 0
        lm = LANGUAGE_META[lg]
        with cols[i]:
            st.markdown(
                f'<div class="language-card" style="background:{lm["gradient"]}"><div class="icon">{lm["icon"]}</div><h3>{lg}</h3><div class="small" style="color:rgba(255,255,255,.75)">Adaptive learning path</div><div class="pct">{pct:.0f}%</div><div style="opacity:.78;font-size:.78rem">average quiz performance</div></div>',
                unsafe_allow_html=True,
            )
            if st.button(f"Open {lg}", key=f"home-lang-{lg}", use_container_width=True):
                st.session_state.language_select = lg
                st.session_state.topic = active_topics(lg)[0]
                st.session_state.page = "📚 Learn"
                st.rerun()

# -----------------------------
# Learn
# -----------------------------
elif st.session_state.page == "📚 Learn":
    hero(
        f"📚 Learn {language}",
        "Pick a topic below. Every topic follows the same loop: concept → example → coding practice → quiz → adaptive recommendation.",
        langmeta["gradient"],
        f"{len(active_topics(language))} topics · beginner-friendly path",
    )
    topic_grid(user, language, status)

    st.markdown('<div class="section-title">🎯 Recommended for you</div>', unsafe_allow_html=True)
    if rec_topic:
        a, b = st.columns([3, 1])
        with a:
            st.markdown(f'<div class="ai-banner"><b>{TOPIC_META[rec_topic]["icon"]} {display_topic(rec_topic)}</b><br><span class="small">{html.escape(rec_reason)}</span></div>', unsafe_allow_html=True)
        with b:
            if st.button("Open recommendation →", use_container_width=True):
                go("📖 Topic", rec_topic)
                st.rerun()

# -----------------------------
# Topic workspace
# -----------------------------
elif st.session_state.page == "📖 Topic":
    topic = st.session_state.topic
    data = CONTENT[language][topic]
    row = status[status.topic == topic].iloc[0]
    hero(
        f'{TOPIC_META[topic]["icon"]} {display_topic(topic)}',
        f"{language} · {TOPIC_DESCRIPTIONS[topic]}. Your current ML status is {row.status}.",
        langmeta["gradient"],
        f"{STATUS_ICON[row.status]} {row.status} · {row.avg_pct:.0f}% average",
    )

    a, b, c, d = st.columns(4)
    a.metric("Skill status", row.status)
    b.metric("Average score", f"{row.avg_pct:.0f}%")
    c.metric("Attempts", int(row.attempts))
    d.metric("ML confidence", f"{row.confidence:.0%}")

    tabs = st.tabs(["📘 Concept", "💡 Example", "💻 Coding Lab", "📝 Quiz", "🤖 AI Coach"])
    with tabs[0]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"### {TOPIC_META[topic]['icon']} What you will learn")
        st.write(data["explain"])
        st.markdown("**Learning sequence**")
        st.markdown("1. Understand the core idea  \n2. Study the example  \n3. Complete the coding challenge  \n4. Take the quiz  \n5. Let the ML engine update your skill status")
        st.markdown('</div>', unsafe_allow_html=True)
    with tabs[1]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(data["example"], language={"Python":"python", "Java":"java", "JavaScript":"javascript"}[language])
        if st.button("🤖 Explain this example with AI", key=f"explain-{language}-{topic}", use_container_width=True):
            if not configure_ai():
                st.warning("Connect a live AI API key from the sidebar to use LLM explanations.")
            else:
                with st.spinner("Ada is explaining the example..."):
                    answer = ask(language, topic, f"Explain this example line by line for a BCA beginner. Use a simple analogy and then give one tiny practice question.\n\n{data['example']}")
                db.save_tutor_message(user, language, "assistant", answer, topic)
                st.markdown(answer)
        st.markdown('</div>', unsafe_allow_html=True)
    with tabs[2]:
        render_code_lab(user, language, topic)
    with tabs[3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("Complete the quiz to update your ML skill profile.")
        if st.button("Start quiz →", key=f"topic-quiz-{language}-{topic}", use_container_width=True):
            go("📝 Quiz", topic)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with tabs[4]:
        if not configure_ai():
            st.markdown('<div class="ai-banner"><b>🤖 AI Coach is ready to connect</b><br><span class="small">Add an OpenAI or Anthropic API key in the sidebar to unlock personalized LLM lessons, hints, debugging, and code reviews.</span></div>', unsafe_allow_html=True)
        else:
            prompt = st.text_area("What do you want Ada to teach you?", placeholder=f"Explain {display_topic(topic)} like I am a beginner...")
            if st.button("Ask Ada →", key=f"topic-ai-{language}-{topic}", use_container_width=True) and prompt.strip():
                with st.spinner("Ada is thinking..."):
                    answer = ask(language, topic, prompt, context=f"ML status: {row.status}; average: {row.avg_pct:.0f}%; attempts: {int(row.attempts)}")
                st.markdown(answer)

# -----------------------------
# Quiz
# -----------------------------
elif st.session_state.page == "📝 Quiz":
    topic = st.session_state.topic
    data = CONTENT[language][topic]
    hero(
        f"📝 {display_topic(topic)} Quiz",
        "Your answers are saved to SQLite and become features for the Random Forest skill classifier.",
        langmeta["gradient"],
        "3 questions · instant scoring · ML update",
    )
    qs = data["quiz"]
    with st.form(f"quiz-{language}-{topic}"):
        answers = [
            st.radio(f"**Q{i+1}.** {q}", opts, index=None, key=f"quiz-{language}-{topic}-{i}")
            for i, (q, opts, _) in enumerate(qs)
        ]
        submit = st.form_submit_button("🚀 Submit quiz", use_container_width=True)
    if submit:
        if any(x is None for x in answers):
            st.warning("Please answer every question before submitting.")
        else:
            score = sum(p == opts[correct] for (_, opts, correct), p in zip(qs, answers))
            db.save_quiz(user, language, topic, score, len(qs))
            q, c, status = get_status(user, language)
            row = status[status.topic == topic].iloc[0]
            db.save_prediction(user, language, topic, row.status, row.confidence, row.avg_pct, row.attempts)
            rec_topic, rec_reason = recommend(status)
            if rec_topic:
                db.save_recommendation(user, language, rec_topic, rec_reason)
            st.session_state.quiz_result = (score, len(qs), topic, row.status)
            if score == len(qs):
                st.balloons()
    if "quiz_result" in st.session_state:
        score, total, t, result_status = st.session_state.quiz_result
        st.markdown(
            f'<div class="card"><h2>{"🏆 Excellent work!" if score == total else "📈 Good attempt!"}</h2><div style="font-size:3rem;font-weight:800">{score}/{total}</div><p>ML skill status: <b>{result_status}</b></p></div>',
            unsafe_allow_html=True,
        )
        if score < total:
            st.info(f"Ada recommends another practice round on {display_topic(t)}.")
        else:
            st.success("Perfect score. Your performance has been fed into the adaptive engine.")

# -----------------------------
# Practice
# -----------------------------
elif st.session_state.page == "💻 Practice":
    hero(
        "💻 Coding Lab",
        "Write code, receive static feedback, check the challenge, and optionally ask the LLM to review your solution.",
        langmeta["gradient"],
        "Safe static analysis · code is never executed",
    )
    topic = st.session_state.topic
    render_code_lab(user, language, topic)

# -----------------------------
# AI Tutor
# -----------------------------
elif st.session_state.page == "🤖 AI Tutor":
    hero(
        "🤖 Ada AI Tutor",
        "Ask questions, request hints, debug errors, learn concepts, or get a personalized explanation based on your ML performance.",
        "linear-gradient(135deg,#5b21b6,#db2777)",
        "LLM-powered tutoring when connected",
    )
    weak = status[status.status == "Needs Practice"].topic.tolist()
    context = f"Weak topics: {', '.join(display_topic(x) for x in weak) or 'none'}; current topic: {display_topic(st.session_state.topic)}."

    if not configure_ai():
        st.markdown('<div class="ai-banner"><b>🔑 Connect your LLM</b><br><span class="small">Use the sidebar AI setup. The project supports OpenAI and Anthropic. Without a key, the app intentionally does not pretend that a canned response is a real LLM.</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ai-banner"><span class="ai-dot"></span><b>Live AI tutor connected</b><br><span class="small">Ada can use your selected language, topic, and ML performance context to personalize answers.</span></div>', unsafe_allow_html=True)

    history_key = f"chat-{language}"
    st.session_state.setdefault(history_key, [])
    quick = [
        f"Explain {display_topic(st.session_state.topic)} simply",
        f"Give me a hint for {display_topic(st.session_state.topic)}",
        f"Give me a beginner coding exercise in {language}",
    ]
    st.markdown('<div class="section-title">⚡ Quick prompts</div>', unsafe_allow_html=True)
    buttons = st.columns(3)
    prompt = None
    for i, text in enumerate(quick):
        if buttons[i].button(text, key=f"quick-{language}-{i}", use_container_width=True):
            prompt = text

    for m in st.session_state[history_key]:
        with st.chat_message(m["role"], avatar="🤖" if m["role"] == "assistant" else "🧑‍💻"):
            st.markdown(m["content"])

    typed = st.chat_input("Ask Ada anything about programming...") if enabled() else None
    prompt = typed or prompt
    if prompt and enabled():
        st.session_state[history_key].append({"role": "user", "content": prompt})
        db.save_tutor_message(user, language, "user", prompt, st.session_state.topic)
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Ada is thinking..."):
                answer = ask(language, st.session_state.topic, prompt, st.session_state[history_key][:-1], context)
            st.markdown(answer)
        st.session_state[history_key].append({"role": "assistant", "content": answer})
        db.save_tutor_message(user, language, "assistant", answer, st.session_state.topic)

# -----------------------------
# Dashboard
# -----------------------------
else:
    hero(
        "📊 Learning Intelligence",
        "This is the ML side of the project: quiz performance + coding performance → skill classification → adaptive recommendation.",
        "linear-gradient(135deg,#312e81,#7c3aed)",
        "Random Forest · SQLite · adaptive engine",
    )
    q, c, status = get_status(user, language)
    avg = float(q.pct.mean()) if not q.empty else 0
    weak = int((status.status == "Needs Practice").sum())
    master = int((status.status == "Mastered").sum())
    m = st.columns(4)
    for col, val, label in zip(m, [f"{avg:.0f}%", len(q), len(c), master], ["Quiz average", "Quiz attempts", "Coding attempts", "Mastered topics"]):
        col.markdown(f'<div class="metric"><div class="value">{val}</div><div class="label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">📈 Topic skill analysis</div>', unsafe_allow_html=True)
    chart_data = status.copy()
    chart_data["display"] = chart_data.topic.map(display_topic)
    chart = alt.Chart(chart_data).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x=alt.X("display:N", sort=active_topics(language), title=None, axis=alt.Axis(labelAngle=-25)),
        y=alt.Y("avg_pct:Q", scale=alt.Scale(domain=[0, 100]), title="Average performance (%)"),
        color=alt.Color("status:N", scale=alt.Scale(domain=list(STATUS_COLORS), range=list(STATUS_COLORS.values())), legend=alt.Legend(title="ML status")),
        tooltip=[alt.Tooltip("display:N", title="Topic"), "status", alt.Tooltip("avg_pct:Q", format=".1f", title="Average %"), "attempts", alt.Tooltip("confidence:Q", format=".0%")],
    ).properties(height=390)
    st.altair_chart(chart, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.markdown('<div class="section-title">🎯 Needs attention</div>', unsafe_allow_html=True)
        weak_rows = status[status.status == "Needs Practice"]
        if weak_rows.empty:
            st.success("No weak topics right now. Keep the momentum.")
        for _, r in weak_rows.iterrows():
            st.markdown(f'<div class="card"><b>{TOPIC_META[r.topic]["icon"]} {display_topic(r.topic)}</b><br>{status_badge(r.status)}<br><span class="small">{r.avg_pct:.0f}% average · {r.attempts} attempts · confidence {r.confidence:.0%}</span></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="section-title">🏆 Mastered</div>', unsafe_allow_html=True)
        master_rows = status[status.status == "Mastered"]
        if master_rows.empty:
            st.info("Complete quizzes and coding challenges to build mastered topics.")
        for _, r in master_rows.iterrows():
            st.markdown(f'<div class="card"><b>{TOPIC_META[r.topic]["icon"]} {display_topic(r.topic)}</b><br>{status_badge(r.status)}<br><span class="small">{r.avg_pct:.0f}% average · {r.attempts} attempts · confidence {r.confidence:.0%}</span></div>', unsafe_allow_html=True)

    rec_topic, rec_reason = recommend(status)
    st.markdown('<div class="section-title">🚀 Adaptive recommendation</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ai-banner"><b>{TOPIC_META[rec_topic]["icon"] if rec_topic else "🏆"} {display_topic(rec_topic) if rec_topic else "Path complete"}</b><br><span class="small">{html.escape(rec_reason)}</span></div>', unsafe_allow_html=True)
    if rec_topic and st.button(f"Practice {display_topic(rec_topic)} →", use_container_width=False):
        go("📖 Topic", rec_topic)
        st.rerun()

    st.markdown('<div class="section-title">🧾 Recent activity</div>', unsafe_allow_html=True)
    if q.empty and c.empty:
        st.info("Your activity will appear here after your first quiz or coding challenge.")
    else:
        activity = []
        if not q.empty:
            for _, r in q.tail(10).iterrows():
                activity.append({"Time": r.ts, "Type": "Quiz", "Topic": display_topic(r.topic), "Score": f"{r.pct:.0f}%"})
        if not c.empty:
            for _, r in c.tail(10).iterrows():
                activity.append({"Time": r.ts, "Type": "Coding", "Topic": display_topic(r.topic), "Score": f"{r.score:.0f}%"})
        st.dataframe(pd.DataFrame(activity).sort_values("Time", ascending=False).head(14), hide_index=True, use_container_width=True)

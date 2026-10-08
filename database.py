import sqlite3
from pathlib import Path
from datetime import datetime
import pandas as pd

DB_PATH = Path(__file__).with_name("tutor.db")

def _conn():
    c = sqlite3.connect(DB_PATH)
    c.execute("PRAGMA foreign_keys = ON")
    return c

def init_db():
    with _conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS quiz_attempts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL, language TEXT NOT NULL, topic TEXT NOT NULL,
            score INTEGER NOT NULL, total INTEGER NOT NULL,
            ts TEXT NOT NULL, duration_seconds INTEGER DEFAULT 0
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS coding_attempts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL, language TEXT NOT NULL, topic TEXT NOT NULL,
            code TEXT NOT NULL, passed INTEGER NOT NULL, issue_count INTEGER NOT NULL,
            score REAL NOT NULL, feedback TEXT, ts TEXT NOT NULL
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS ml_predictions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL, language TEXT NOT NULL, topic TEXT NOT NULL,
            status TEXT NOT NULL, confidence REAL NOT NULL, avg_score REAL NOT NULL,
            attempts INTEGER NOT NULL, ts TEXT NOT NULL
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS recommendations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL, language TEXT NOT NULL, topic TEXT NOT NULL,
            reason TEXT NOT NULL, created_at TEXT NOT NULL
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS tutor_messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL, language TEXT NOT NULL, role TEXT NOT NULL,
            message TEXT NOT NULL, topic TEXT, ts TEXT NOT NULL
        )""")

def ensure_user(name):
    with _conn() as c:
        c.execute("INSERT OR IGNORE INTO users(name, created_at) VALUES (?,?)",
                  (name, datetime.now().isoformat(timespec="seconds")))

def save_quiz(user, language, topic, score, total, duration=0):
    ensure_user(user)
    with _conn() as c:
        c.execute("""INSERT INTO quiz_attempts
            (user,language,topic,score,total,ts,duration_seconds)
            VALUES (?,?,?,?,?,?,?)""",
            (user,language,topic,score,total,datetime.now().isoformat(timespec="seconds"),duration))

def save_code(user, language, topic, code, passed, issue_count, score, feedback):
    ensure_user(user)
    with _conn() as c:
        c.execute("""INSERT INTO coding_attempts
            (user,language,topic,code,passed,issue_count,score,feedback,ts)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (user,language,topic,code,int(passed),issue_count,float(score),feedback,
             datetime.now().isoformat(timespec="seconds")))

def save_prediction(user, language, topic, status, confidence, avg_score, attempts):
    ensure_user(user)
    with _conn() as c:
        c.execute("""INSERT INTO ml_predictions
            (user,language,topic,status,confidence,avg_score,attempts,ts)
            VALUES (?,?,?,?,?,?,?,?)""",
            (user,language,topic,status,float(confidence),float(avg_score),int(attempts),
             datetime.now().isoformat(timespec="seconds")))

def save_recommendation(user, language, topic, reason):
    ensure_user(user)
    with _conn() as c:
        c.execute("""INSERT INTO recommendations(user,language,topic,reason,created_at)
                     VALUES (?,?,?,?,?)""",
                  (user,language,topic,reason,datetime.now().isoformat(timespec="seconds")))

def save_tutor_message(user, language, role, message, topic=None):
    ensure_user(user)
    with _conn() as c:
        c.execute("""INSERT INTO tutor_messages(user,language,role,message,topic,ts)
                     VALUES (?,?,?,?,?,?)""",
                  (user,language,role,message,topic,datetime.now().isoformat(timespec="seconds")))

def get_quizzes(user, language=None):
    q, p = "SELECT * FROM quiz_attempts WHERE user=?", [user]
    if language:
        q += " AND language=?"; p.append(language)
    q += " ORDER BY ts"
    with _conn() as c:
        df = pd.read_sql_query(q,c,params=p)
    if not df.empty:
        df["pct"] = df["score"] / df["total"] * 100
    return df

def get_coding(user, language=None):
    q, p = "SELECT * FROM coding_attempts WHERE user=?", [user]
    if language:
        q += " AND language=?"; p.append(language)
    q += " ORDER BY ts"
    with _conn() as c:
        return pd.read_sql_query(q,c,params=p)

def get_tutor_history(user, language, limit=20):
    with _conn() as c:
        return pd.read_sql_query(
            "SELECT role,message,topic,ts FROM tutor_messages WHERE user=? AND language=? ORDER BY id DESC LIMIT ?",
            c, params=[user,language,limit]
        ).sort_values("ts") if limit else pd.DataFrame()

def get_stats(user, language=None):
    q, p = "SELECT COUNT(*) quizzes, COALESCE(AVG(CAST(score AS REAL)/total*100),0) avg_quiz FROM quiz_attempts WHERE user=?", [user]
    if language:
        q += " AND language=?"; p.append(language)
    with _conn() as c:
        return pd.read_sql_query(q,c,params=p).iloc[0].to_dict()

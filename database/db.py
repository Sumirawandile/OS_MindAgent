import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "os_doubts.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table for logged doubts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doubts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            unit_tag TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            confidence REAL NOT NULL,
            has_diagram INTEGER DEFAULT 0
        )
    """)
    
    # Table for quiz results
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            unit_tag TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def save_doubt(unit_tag: str, question: str, answer: str, confidence: float, has_diagram: bool = False):
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO doubts (timestamp, unit_tag, question, answer, confidence, has_diagram)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (now_str, unit_tag, question, answer, confidence, 1 if has_diagram else 0))
    conn.commit()
    conn.close()

from config import TOPIC_TO_UNIT, UNIT_TO_TOPIC

def fetch_all_doubts(unit_filter: str = "All"):
    conn = get_connection()
    cursor = conn.cursor()
    if unit_filter == "All":
        cursor.execute("SELECT * FROM doubts ORDER BY id DESC")
    else:
        unit_key = TOPIC_TO_UNIT.get(unit_filter, unit_filter)
        cursor.execute("SELECT * FROM doubts WHERE unit_tag = ? OR unit_tag = ? ORDER BY id DESC", (unit_filter, unit_key))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def save_quiz_result(unit_tag: str, score: int, total: int):
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO quizzes (timestamp, unit_tag, score, total)
        VALUES (?, ?, ?, ?)
    """, (now_str, unit_tag, score, total))
    conn.commit()
    conn.close()

def fetch_quiz_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total_taken, SUM(score) as total_score, SUM(total) as total_possible FROM quizzes")
    row = cursor.fetchone()
    conn.close()
    if row and row['total_taken'] and row['total_taken'] > 0:
        return {
            "total_quizzes": row['total_taken'],
            "avg_accuracy": round((row['total_score'] / row['total_possible']) * 100, 1) if row['total_possible'] else 0
        }
    return {"total_quizzes": 0, "avg_accuracy": 0.0}

def clear_all_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM doubts")
    cursor.execute("DELETE FROM quizzes")
    conn.commit()
    conn.close()

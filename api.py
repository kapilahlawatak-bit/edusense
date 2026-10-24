"""
API Layer — FastAPI REST endpoints for the maths/reasoning engine.

Exposes the engine over HTTP:
  GET  /health
  GET  /items?rule_type=&count=          — serve items from the bank
  POST /attempts                          — record a student attempt
  GET  /attempts/{student_id}             — get a student's attempts
  GET  /qmatrix/{student_id}              — per-student error profile
  GET  /qmatrix/batch                     — batch-level aggregation
  GET  /teacher/attention                 — who needs attention
  GET  /teacher/reteach                   — what to reteach
  GET  /student/{student_id}/practice     — practice items
  GET  /student/{student_id}/progress     — mastery per topic
  GET  /spaced_repetition/{student_id}    — review queue
  POST /items/generate?count=             — generate new items

Run: uvicorn api:app --reload
"""

import sqlite3, json
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

DB = "engine.db"

app = FastAPI(title="CBSE Maths & Reasoning Engine", version="1.0")


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


class Attempt(BaseModel):
    student_id: int
    exam_id: int = 1
    items: list  # [{"item_id": int, "selected_option": str, "time_spent_seconds": int}]


# ---------------------------------------------------------------------------
# HEALTH
# ---------------------------------------------------------------------------

@app.get("/health")
def health():
    conn = get_db()
    n = conn.execute("SELECT COUNT(*) FROM item").fetchone()[0]
    conn.close()
    return {"status": "ok", "items": n}


# ---------------------------------------------------------------------------
# ITEMS
# ---------------------------------------------------------------------------

@app.get("/items")
def get_items(rule_type: Optional[str] = None, count: int = 10):
    conn = get_db()
    if rule_type:
        rows = conn.execute(
            "SELECT id, stem, option_a, option_b, option_c, option_d, correct_option, rule_type "
            "FROM item WHERE rule_type = ? ORDER BY RANDOM() LIMIT ?",
            (rule_type, count)).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, stem, option_a, option_b, option_c, option_d, correct_option, rule_type "
            "FROM item ORDER BY RANDOM() LIMIT ?", (count,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/items/{item_id}")
def get_item(item_id: int):
    conn = get_db()
    row = conn.execute(
        "SELECT id, stem, option_a, option_b, option_c, option_d, correct_option, rule_type "
        "FROM item WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")
    return dict(row)


@app.post("/items/generate")
def generate_items(rule_type: str, count: int = 10):
    """Generate new items and add them to the bank."""
    import generate_items as gi
    if rule_type not in gi.GENERATORS:
        raise HTTPException(status_code=400, detail=f"Unknown rule_type: {rule_type}")
    stored, rejected = 0, 0
    for _ in range(count):
        stem, options, correct, per_wrong = gi.GENERATORS[rule_type]()
        if not gi.verify_item(rule_type, stem, options, correct):
            rejected += 1
            continue
        conn = get_db()
        rid = conn.execute("SELECT id FROM topic WHERE subject='Reasoning'").fetchone()[0]
        conn.execute(
            "INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (rid, stem, options.get("A", ""), options.get("B", ""), options.get("C", ""), options.get("D", ""),
             correct, 1, "generated", "passed", rule_type))
        iid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        for letter, mis in per_wrong.items():
            if letter != correct and letter in options:
                conn.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                             (iid, letter, mis, mis))
        conn.commit()
        conn.close()
        stored += 1
    return {"stored": stored, "rejected": rejected}


# ---------------------------------------------------------------------------
# ATTEMPTS
# ---------------------------------------------------------------------------

@app.post("/attempts")
def record_attempt(attempt: Attempt):
    conn = get_db()
    conn.execute("INSERT INTO attempt (student_id, exam_id, started_at, submitted_at, raw_score) VALUES (?,?,?,?,?)",
                 (attempt.student_id, attempt.exam_id, 0, 0, 0))
    aid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    score = 0
    for item in attempt.items:
        iid = item["item_id"]
        sel = item["selected_option"]
        correct = conn.execute("SELECT correct_option FROM item WHERE id=?", (iid,)).fetchone()[0]
        correct_bool = 1 if sel == correct else 0
        if correct_bool:
            score += 1
        conn.execute("INSERT INTO attempt_item (attempt_id, item_id, selected_option, correct_bool, time_spent_seconds) VALUES (?,?,?,?,?)",
                     (aid, iid, sel, correct_bool, item.get("time_spent_seconds", 0)))

    conn.execute("UPDATE attempt SET raw_score=? WHERE id=?", (score, aid))
    conn.commit()
    conn.close()
    return {"attempt_id": aid, "score": score, "total": len(attempt.items)}


@app.get("/attempts/{student_id}")
def get_attempts(student_id: int):
    conn = get_db()
    rows = conn.execute(
        "SELECT id, exam_id, raw_score, started_at, submitted_at FROM attempt WHERE student_id=? ORDER BY id DESC",
        (student_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Q-MATRIX / ANALYTICS
# ---------------------------------------------------------------------------

@app.get("/qmatrix/{student_id}")
def qmatrix_student(student_id: int):
    conn = get_db()
    rows = conn.execute("""
        SELECT i.rule_type, de.error_type, de.description, COUNT(*) as n_errors
        FROM attempt_item ai
        JOIN attempt a ON a.id = ai.attempt_id
        JOIN item i ON i.id = ai.item_id
        JOIN distractor_error de ON de.item_id = ai.item_id AND de.option_letter = ai.selected_option
        WHERE ai.correct_bool = 0 AND a.student_id = ?
        GROUP BY i.rule_type, de.error_type, de.description
        ORDER BY n_errors DESC
    """, (student_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/qmatrix/batch")
def qmatrix_batch():
    conn = get_db()
    rows = conn.execute("""
        SELECT de.error_type, de.description, COUNT(DISTINCT a.student_id) as students, COUNT(*) as errors
        FROM attempt_item ai
        JOIN attempt a ON a.id = ai.attempt_id
        JOIN distractor_error de ON de.item_id = ai.item_id AND de.option_letter = ai.selected_option
        WHERE ai.correct_bool = 0
        GROUP BY de.error_type, de.description
        ORDER BY students DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# TEACHER VIEWS
# ---------------------------------------------------------------------------

@app.get("/teacher/attention")
def teacher_attention(top: int = 5):
    conn = get_db()
    rows = conn.execute("""
        SELECT a.student_id, COUNT(*) as total_errors
        FROM attempt_item ai
        JOIN attempt a ON a.id = ai.attempt_id
        WHERE ai.correct_bool = 0
        GROUP BY a.student_id
        ORDER BY total_errors DESC
        LIMIT ?
    """, (top,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/teacher/reteach")
def teacher_reteach():
    conn = get_db()
    rows = conn.execute("""
        SELECT de.error_type, de.description, COUNT(DISTINCT a.student_id) as students
        FROM attempt_item ai
        JOIN attempt a ON a.id = ai.attempt_id
        JOIN distractor_error de ON de.item_id = ai.item_id AND de.option_letter = ai.selected_option
        WHERE ai.correct_bool = 0
        GROUP BY de.error_type, de.description
        ORDER BY students DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# STUDENT VIEWS
# ---------------------------------------------------------------------------

@app.get("/student/{student_id}/practice")
def student_practice(student_id: int, count: int = 10):
    conn = get_db()
    rows = conn.execute(
        "SELECT id, stem, option_a, option_b, option_c, option_d, correct_option, rule_type "
        "FROM item ORDER BY RANDOM() LIMIT ?", (count,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/student/{student_id}/progress")
def student_progress(student_id: int):
    conn = get_db()
    rows = conn.execute("""
        SELECT i.rule_type, COUNT(*) as total,
               SUM(CASE WHEN ai.correct_bool=1 THEN 1 ELSE 0 END) as correct
        FROM attempt_item ai
        JOIN attempt a ON a.id = ai.attempt_id
        JOIN item i ON i.id = ai.item_id
        WHERE a.student_id = ?
        GROUP BY i.rule_type
    """, (student_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/spaced_repetition/{student_id}")
def spaced_repetition(student_id: int):
    conn = get_db()
    rows = conn.execute("""
        SELECT i.rule_type,
               COUNT(*) as total,
               SUM(CASE WHEN ai.correct_bool=1 THEN 1 ELSE 0 END) as correct,
               MAX(ai.rowid) as last_attempt_seq
        FROM attempt_item ai
        JOIN attempt a ON a.id = ai.attempt_id
        JOIN item i ON i.id = ai.item_id
        WHERE a.student_id = ?
        GROUP BY i.rule_type
    """, (student_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# STATS
# ---------------------------------------------------------------------------

@app.get("/stats")
def stats():
    conn = get_db()
    n_items = conn.execute("SELECT COUNT(*) FROM item").fetchone()[0]
    n_errors = conn.execute("SELECT COUNT(*) FROM distractor_error").fetchone()[0]
    n_attempts = conn.execute("SELECT COUNT(*) FROM attempt").fetchone()[0]
    n_students = conn.execute("SELECT COUNT(DISTINCT student_id) FROM attempt").fetchone()[0]
    rules = [dict(r) for r in conn.execute("SELECT rule_type, COUNT(*) as n FROM item GROUP BY rule_type")]
    conn.close()
    return {
        "items": n_items, "distractor_errors": n_errors,
        "attempts": n_attempts, "students": n_students, "rules": rules,
    }


# ---------------------------------------------------------------------------
# WEBSITE — serve the frontend at /
# ---------------------------------------------------------------------------

@app.get("/", include_in_schema=False)
def serve_site():
    return FileResponse("website/index.html")

app.mount("/static", StaticFiles(directory="website"), name="static")

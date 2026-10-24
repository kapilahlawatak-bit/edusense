"""
Phase 2 — Class 9 Number Systems seed into engine.db
Standalone (no third-party deps). Run: python bootstrap.py
"""
import sqlite3

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Wipe + rebuild cleanly
for t in ["attempt_item", "attempt", "distractor_error", "item", "exam_weightage", "exam", "topic"]:
    cur.execute(f"DROP TABLE IF EXISTS {t}")
conn.commit()

cur.executescript("""
CREATE TABLE topic (id INTEGER PRIMARY KEY, class_level INTEGER, subject TEXT,
    chapter_code TEXT, title TEXT, parent_topic_id INTEGER, difficulty_band TEXT);
CREATE TABLE exam (id INTEGER PRIMARY KEY, code TEXT UNIQUE, name TEXT, authority TEXT);
CREATE TABLE exam_weightage (exam_id INTEGER, topic_id INTEGER, marks INTEGER, question_count INTEGER);
CREATE TABLE item (id INTEGER PRIMARY KEY, topic_id INTEGER, stem TEXT,
    option_a TEXT, option_b TEXT, option_c TEXT, option_d TEXT,
    correct_option TEXT, options_key TEXT, marks INTEGER DEFAULT 1,
    generation_method TEXT, verification_state TEXT);
CREATE TABLE distractor_error (id INTEGER PRIMARY KEY, item_id INTEGER,
    option_letter TEXT, error_type TEXT, description TEXT);
CREATE TABLE attempt (id INTEGER PRIMARY KEY, student_id INTEGER, exam_id INTEGER, started_at REAL,
    submitted_at REAL, raw_score INTEGER);
CREATE TABLE attempt_item (attempt_id INTEGER, item_id INTEGER,
    selected_option TEXT, correct_bool INTEGER, time_spent_seconds INTEGER);
""")

cur.execute("INSERT INTO exam (code, name, authority) VALUES (?, ?, ?)",
            ("CBSE_09_MATHS", "Class 9 CBSE Maths", "CBSE"))
exam_id = cur.lastrowid

cur.execute("INSERT INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (?, ?, ?, ?, ?, ?)",
            (9, "Maths", "NSEC_9_1", "Number Systems", None, "easy"))
topic_id = cur.lastrowid

cur.execute("INSERT INTO exam_weightage (exam_id, topic_id, marks, question_count) VALUES (?, ?, ?, ?)",
            (exam_id, topic_id, 80, 20))

SEED = [
    ("Solve for x: 3x + 7 = 25", "C", "symbolic"),
    ("Solve for x: 5x - 4 = 21", "B", "symbolic"),
    ("Solve for x: 2x + 9 = 9", "A", "symbolic"),
    ("Solve for x: 7x - 3 = 18", "C", "symbolic"),
    ("Solve for x: 4x - 12 = -20", "A", "symbolic"),
    ("Solve for x: x/2 + 5 = 11", "D", "symbolic"),
    ("Solve for x: 3x + 4 = x + 16", "C", "symbolic"),
    ("Solve for x: 5x - 7 = 2x + 1", "C", "symbolic"),
    ("Solve for x: 2x - 9 = -x + 6", "C", "symbolic"),
    ("Solve for x: 9x - 5 = 4x + 13", "D", "symbolic"),
    ("Evaluate: 2^5 = ?", "A", "symbolic"),
    ("Evaluate: (-3)^4 = ?", "B", "symbolic"),
    ("Evaluate: 2/7 + 3/14 = ?", "A", "symbolic"),
    ("Evaluate: 0^0 = ?", "A", "symbolic"),
    ("Evaluate: (-1)^17 = ?", "B", "symbolic"),
    ("Evaluate: sqrt(81) = ?", "C", "symbolic"),
    ("Evaluate: 2 + 3*4 - 6/2 = ?", "C", "symbolic"),
    ("Evaluate: (-2)^3 * 3 = ?", "B", "symbolic"),
    ("Evaluate: 5/6 * 6/5 = ?", "D", "symbolic"),
    ("Evaluate: 100 - (15 + 28) = ?", "A", "symbolic"),
]

ALL = list("ABCD")
for i, (stem, correct, brief) in enumerate(SEED, start=1):
    correct_idx = ord(correct) - 65
    correct_letter = ALL[correct_idx]
    wrong_letters = [l for l in ALL if l != correct_letter]
    d_a, d_b, d_c = wrong_letters[0], wrong_letters[1], wrong_letters[2]
    cur.execute(
        "INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state) VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?)",
        (topic_id, stem, d_a, d_b, d_c, correct_letter, "symbolic", "checked"))
    item_id = cur.lastrowid
    if i == 1:
        cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?, ?, ?, ?)",
                    (item_id, "A", "FALSE_RATE", "x not isolated; subtracted 7 from RHS incorrectly"))
    if i == 2:
        cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?, ?, ?, ?)",
                    (item_id, "B", "FALSE_RATE", "forgot to add 4 to RHS"))
    if i == 4:
        cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?, ?, ?, ?)",
                    (item_id, "A", "SIGN_ERROR", "added 3 to RHS incorrectly"))

conn.commit()
cur.close()
conn.close()

# Read-back
conn = sqlite3.connect(DB)
c = conn.cursor()
print("=== PHASE 2 SEED COMPLETE ===")
print(f"Topic: {topic_id} | exam_id: {exam_id}")
print(f"Items: {c.execute('SELECT COUNT(*) FROM item').fetchone()[0]}")
print(f"Distractor errors: {c.execute('SELECT COUNT(*) FROM distractor_error').fetchone()[0]}")
for (stem, o, c_, gm) in c.execute("SELECT stem, option_a||option_b||option_c||option_d, correct_option, generation_method FROM item"):
    print(f"  {stem} -> {o} [{gm}]")
conn.close()
print("\nPhase 2 complete: Class 9 Number Systems seeded.")

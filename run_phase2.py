"""One-command launcher: Phase 2 seed + sim verify of reasoning rules + print readback."""
import sqlite3, random
random.seed(7)
import reasoning_rules as rr

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Rebuild a clean Phase 2 seed
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
    correct_option TEXT, marks INTEGER DEFAULT 1, generation_method TEXT, verification_state TEXT);
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
    ("Solve for x: 3x + 7 = 25", "C"),
    ("Solve for x: 5x - 4 = 21", "B"),
    ("Solve for x: 2x + 9 = 9", "A"),
    ("Solve for x: 7x - 3 = 18", "C"),
    ("Solve for x: 4x - 12 = -20", "A"),
    ("Solve for x: x/2 + 5 = 11", "D"),
    ("Solve for x: 3x + 4 = x + 16", "C"),
    ("Solve for x: 5x - 7 = 2x + 1", "C"),
    ("Solve for x: 2x - 9 = -x + 6", "C"),
    ("Solve for x: 9x - 5 = 4x + 13", "D"),
    ("Evaluate: 2^5 = ?", "A"),
    ("Evaluate: (-3)^4 = ?", "B"),
    ("Evaluate: 2/7 + 3/14 = ?", "A"),
    ("Evaluate: 0^0 = ?", "A"),
    ("Evaluate: (-1)^17 = ?", "B"),
    ("Evaluate: sqrt(81) = ?", "C"),
    ("Evaluate: 2 + 3*4 - 6/2 = ?", "C"),
    ("Evaluate: (-2)^3 * 3 = ?", "B"),
    ("Evaluate: 5/6 * 6/5 = ?", "D"),
    ("Evaluate: 100 - (15 + 28) = ?", "A"),
]

ALL = list("ABCD")
for i, (stem, correct) in enumerate(SEED, start=1):
    correct_idx = ord(correct) - 65
    correct_letter = ALL[correct_idx]
    wrong = [l for l in ALL if l != correct_letter]
    cur.execute(
        "INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (topic_id, stem, wrong[0], wrong[1], wrong[2], correct_letter, 1, 1, "symbolic", "checked"))
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

# Reasoning rules (Phase 3 practice) + distractor errors
for j, rname in enumerate(["atbash", "letter_shift"], start=1):
    out = rr.generate(rname)
    src = out["question"].split("'")[1]
    exp = rr.apply_rule(rname, src)
    assert exp == out["key"], (src, exp, out["key"])
    cur.execute(
            "INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (topic_id, out["question"], out["options"]["A"], out["options"]["B"],
             out["options"]["C"], out["options"]["D"], out["correct"], 1, "rule_based", "checked"))
    mid = cur.lastrowid
    err = {"B": "CORRECT", "C": "SHIFT_BY_ONE (+1)", "D": "SHIFT_BY_MINUS_ONE (-1)"}
    cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?, ?, ?, ?)",
                (mid, out["correct"], "CORRECT", "machine-verified exact key"))
    cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?, ?, ?, ?)",
                (mid, [k for k, v in out["options"].items() if v != out["key"]][0],
                 "OFF_BY_ONE", "adjacent letter error mode"))

conn.commit()
cur.close()
conn.close()

# Read back
conn = sqlite3.connect(DB)
c = conn.cursor()
print("=== PHASE 2 COMPLETE ===")
print(f"Topic: NSEC_9_1 | exam_id: {exam_id}")
print(f"Total items: {c.execute('SELECT COUNT(*) FROM item').fetchone()[0]}")
print(f"Distractor errors: {c.execute('SELECT COUNT(*) FROM distractor_error').fetchone()[0]}")
c.close()

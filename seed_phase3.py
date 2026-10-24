"""Phase 3a — Reasoning engine seed into engine.db."""
import sqlite3, sys
sys.path.insert(0, ".")
import reasoning_rules as rr

conn = sqlite3.connect("engine.db")
cur = conn.cursor()

for t in ["attempt_item", "attempt", "distractor_error", "item", "exam_weightage", "exam", "topic"]:
    cur.execute(f"DROP TABLE IF EXISTS {t}")
conn.commit()

cur.executescript("""
CREATE TABLE exam (id INTEGER PRIMARY KEY, code TEXT UNIQUE, name TEXT, authority TEXT);
CREATE TABLE topic (id INTEGER PRIMARY KEY, class_level INTEGER, subject TEXT, chapter_code TEXT, title TEXT, parent_topic_id INTEGER, difficulty_band TEXT);
CREATE TABLE exam_weightage (exam_id INTEGER, topic_id INTEGER, marks INTEGER, question_count INTEGER);
CREATE TABLE item (id INTEGER PRIMARY KEY, topic_id INTEGER, stem TEXT, option_a TEXT, option_b TEXT, option_c TEXT, option_d TEXT, correct_option TEXT, marks INTEGER DEFAULT 1, generation_method TEXT, verification_state TEXT, rule_type TEXT);
CREATE TABLE distractor_error (id INTEGER PRIMARY KEY, item_id INTEGER, option_letter TEXT, error_type TEXT, description TEXT);
CREATE TABLE attempt (id INTEGER PRIMARY KEY, student_id INTEGER, exam_id INTEGER, started_at REAL, submitted_at REAL, raw_score INTEGER);
CREATE TABLE attempt_item (attempt_id INTEGER, item_id INTEGER, selected_option TEXT, correct_bool INTEGER, time_spent_seconds INTEGER);
""")

cur.execute("INSERT OR IGNORE INTO exam (code, name, authority) VALUES ('CBSE_09_MATHS','Class 9 CBSE Maths','CBSE')")
exm = cur.lastrowid
cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (9,'Reasoning','RR_01','Reasoning','0','medium')")
rid = cur.lastrowid
cur.execute("INSERT OR IGNORE INTO exam_weightage (exam_id, topic_id, marks, question_count) VALUES (?, ?, ?, ?)", (exm, rid, 40, 20))

# Seed the existing maths items back in (from engine.db before wipe)
pre = sqlite3.connect("engine.db")
pre_cur = pre.cursor()
pre_cur.execute("SELECT stem, option_a, option_b, option_c, option_d, correct_option FROM item")
maths = pre_cur.fetchall()
conn.close(); pre.close()

for (stem, oa, ob, oc, od, correct) in maths:
    cur.execute("INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) VALUES (?,?,?,?,?,?,?,?, 'symbolic','passed','Maths')",
                (rid, stem, oa, ob, oc, od, correct))

# Reasoning items
rules = ([rr.gen_coding("atbash") for _ in range(4)] +
         [rr.gen_coding("caesar") for _ in range(3)] +
         [rr.gen_blood() for _ in range(3)] +
         [rr.gen_direction() for _ in range(3)] +
         [rr.gen_series() for _ in range(4)])

for r in rules:
    cur.execute("INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) VALUES (?,?,?,?,?,?,?,?, 'symbolic','passed',?)",
                (rid, r["question"], r["options"]["A"], r["options"]["B"], r["options"]["C"], r["options"]["D"],
                 r["correct"], r["rule_type"] if "rule_type" in r else r["rule"]))
    iid = cur.lastrowid
    cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                (iid, r["correct"], r["rule_type"] if "rule_type" in r else r["rule"], r["err"]))

conn.commit()
c2 = sqlite3.connect("engine.db")
print(f"Items: {c2.execute('SELECT COUNT(*) FROM item').fetchone()[0]}")
print(f"Distractor errors: {c2.execute('SELECT COUNT(*) FROM distractor_error').fetchone()[0]}")
print(f"Topics: {c2.execute('SELECT COUNT(*) FROM topic').fetchone()[0]}")
c2.close(); conn.close()

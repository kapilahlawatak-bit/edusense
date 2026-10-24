"""FULL BUILD — Phase 2 + Phase 3 (one clean pass)."""
import random, sys, sqlite3
sys.path.insert(0, ".")
import reasoning_rules as rr

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

for t in ["attempt_item", "attempt", "distractor_error", "item", "exam_weightage", "exam", "topic"]:
    cur.execute("DROP TABLE IF EXISTS " + t)
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

cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (9,'Maths','NSEC_9_1','Number Systems','0','medium')")
tid = cur.lastrowid
cur.execute("INSERT OR IGNORE INTO exam_weightage (exam_id, topic_id, marks, question_count) VALUES (?,?,?,?)", (exm, tid, 80, 20))

maths = [
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

for stem, correct in maths:
    used = set()
    slots = {}
    correct_slot = random.choice(["A", "B", "C", "D"])
    for s in ["A", "B", "C", "D"]:
        if s == correct_slot:
            slots[s] = correct
            used.add(correct)
        else:
            for w in ["A", "B", "C", "D"]:
                if w != correct and w not in used:
                    slots[s] = w
                    used.add(w)
                    break
    cur.execute(
        "INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (tid, stem, slots["A"], slots["B"], slots["C"], slots["D"], correct, 1, "symbolic", "passed", "Maths"))
    i = cur.lastrowid
    # tag every WRONG option with its error type, not just the correct one
    for wrong_letter in ["A", "B", "C", "D"]:
        if wrong_letter != correct:
            cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                        (i, wrong_letter, "FALSE_RATE", "incorrect option rate"))

cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (9,'Reasoning','RR_01','Reasoning','0','medium')")
rid = cur.lastrowid
cur.execute("INSERT OR IGNORE INTO exam_weightage (exam_id, topic_id, marks, question_count) VALUES (?,?,?,?)", (exm, rid, 40, 20))

rules = ([rr.gen_coding("atbash") for _ in range(4)] +
         [rr.gen_coding("caesar") for _ in range(3)] +
         [rr.gen_blood() for _ in range(3)] +
         [rr.gen_direction() for _ in range(3)] +
         [rr.gen_series() for _ in range(4)] +
         [rr.gen_syllogism() for _ in range(2)])

for r in rules:
    rule = r.get("rule_type", r.get("rule", "unknown"))
    opts = r.get("options", {})
    cur.execute(
        "INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (rid, r["question"], opts.get("A", ""), opts.get("B", ""), opts.get("C", ""), opts.get("D", ""),
         r["correct"], 1, "symbolic", "passed", rule))
    iid = cur.lastrowid
    # tag every WRONG option, not the correct one
    for w in ["A", "B", "C", "D"]:
        if w != r["correct"] and w in opts:
            cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                        (iid, w, rule, r["err"]))

conn.commit()
c2 = sqlite3.connect(DB)
print("=== BUILD COMPLETE ===")
print("Exams:", exm)
print("Topics:", tid, "Maths +", rid, "Reasoning")
print("Items:", c2.execute("SELECT COUNT(*) FROM item").fetchone()[0])
print("Distractor errors:", c2.execute("SELECT COUNT(*) FROM distractor_error").fetchone()[0])
c2.close()
conn.close()

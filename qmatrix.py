"""
Phase 4 — The Q-matrix.

The load-bearing question: for a batch of students, WHICH misconception or
rule-failure is causing the errors? Not just "40% wrong" — that's useless
to a teacher. This joins attempts → distractor_error → rule_type and reports
which specific error mechanism each student is exhibiting.

This is the batch-level aggregation that CENTURY Technology does, and that
no Indian product does.

Run: python qmatrix.py
"""
import sqlite3, random
from collections import defaultdict

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

# ---------------------------------------------------------------------------
# 1. Simulate 40 students taking the 39-item set, with realistic behaviour:
#    students who "make the off-by-one error" on atbash will ALSO make it on
#    caesar; students weak on series will fail arithmetic patterns. Errors
#    are grouped by misconception, not uniformly random.
# ---------------------------------------------------------------------------

random.seed(42)
STUDENTS = 40

# misconception groups: each group has students who share a failure mode
GROUPS = {
    "off_by_one":   {"share": 0.25, "rules": ["atbash", "caesar", "number_series"],
                     "description": "picks the adjacent option, not the derived answer"},
    "reversed_gen": {"share": 0.20, "rules": ["blood_relation", "direction_sense"],
                     "description": "walks the relation/turn in the wrong direction"},
    "wrong_shift":  {"share": 0.15, "rules": ["caesar"],
                     "description": "uses k+1 or k-1 instead of k"},
    "series_rate":  {"share": 0.20, "rules": ["number_series"],
                     "description": "misreads the common difference"},
    "syllogism":    {"share": 0.20, "rules": ["syllogism"],
                     "description": "accepts a conclusion that does not follow"},
}

# assign each student to a group
assignments = []
for gname, g in GROUPS.items():
    n = int(STUDENTS * g["share"])
    assignments += [gname] * n
while len(assignments) < STUDENTS:
    assignments.append("syllogism")
random.shuffle(assignments)

# build attempts
conn.execute("DELETE FROM attempt_item")
conn.execute("DELETE FROM attempt")
conn.commit()

item_rows = cur.execute(
    "SELECT id, rule_type, correct_option FROM item").fetchall()

for si in range(STUDENTS):
    gname = assignments[si]
    grp = GROUPS[gname]
    cur.execute(
        "INSERT INTO attempt (student_id, exam_id, started_at, submitted_at, raw_score) VALUES (?,?,?,?,?)",
        (si + 1, 1, 1000000 + si * 600, 1000000 + si * 600 + 900, 0))
    aid = cur.lastrowid

    score = 0
    for iid, rule_type, correct in item_rows:
        # a student fails an item if their group covers this rule AND the
        # random draw lands in their failure rate for that rule
        fail_prob = 0.65 if rule_type in grp["rules"] else 0.08
        is_wrong = random.random() < fail_prob

        # if wrong, pick a distractor (an option letter != correct)
        options = cur.execute(
            "SELECT option_a, option_b, option_c, option_d, correct_option FROM item WHERE id=?",
            (iid,)).fetchone()
        letters = ["A", "B", "C", "D"]
        if is_wrong:
            wrong_letters = [l for l, v in zip(letters, options[:4]) if v != options[4]]
            sel = random.choice(wrong_letters) if wrong_letters else correct
        else:
            sel = correct

        if sel == correct:
            score += 1
            correct_bool = 1
        else:
            correct_bool = 0

        cur.execute(
            "INSERT INTO attempt_item (attempt_id, item_id, selected_option, correct_bool, time_spent_seconds) VALUES (?,?,?,?,?)",
            (aid, iid, sel, correct_bool, random.randint(20, 80)))
    cur.execute("UPDATE attempt SET raw_score=? WHERE id=?", (score, aid))

conn.commit()

# ---------------------------------------------------------------------------
# 2. THE Q-MATRIX QUERY: for every (student, rule, error_type), count errors
#    and expose the misconception. This is the teacher's question:
#    "which 5 students need my attention, and why"
# ---------------------------------------------------------------------------

rows = cur.execute("""
SELECT
    a.student_id,
    i.rule_type,
    de.error_type,
    de.description,
    COUNT(*) as n_errors
FROM attempt_item ai
JOIN attempt a ON a.id = ai.attempt_id
JOIN item i ON i.id = ai.item_id
JOIN distractor_error de ON de.item_id = ai.item_id AND de.option_letter = ai.selected_option
WHERE ai.correct_bool = 0
GROUP BY a.student_id, i.rule_type, de.error_type, de.description
ORDER BY n_errors DESC
""").fetchall()

print("=" * 74)
print("PHASE 4 — THE Q-MATRIX")
print("=" * 74)
print()

# --- Per-student error profile (top 3 by rule) ---
by_student = defaultdict(list)
for sid, rule, etype, desc, n in rows:
    by_student[sid].append((rule, etype, desc, n))

print("PER-STUDENT ERROR PROFILE (top 3 rules each)")
print("-" * 74)
for sid in sorted(by_student)[:12]:
    top = sorted(by_student[sid], key=lambda r: -r[3])[:3]
    parts = [f"{r[0]}:{r[1]}({r[3]})" for r in top]
    print(f"  student {sid:2d}  {' | '.join(parts)}")
print()

# --- Batch-level aggregation: which error type is most common across the batch ---
print("BATCH AGGREGATION — error_type × count of students affected")
print("-" * 74)
by_error = defaultdict(set)
by_error_desc = {}
for sid, rule, etype, desc, n in rows:
    by_error[etype].add(sid)
    by_error_desc[etype] = desc

for etype in sorted(by_error, key=lambda e: -len(by_error[e])):
    students = by_error[etype]
    desc = by_error_desc.get(etype, "")
    print(f"  {etype:20s}  {len(students):2d} students  —  {desc}")
print()

# --- Per-rule breakdown ---
print("PER-RULE BREAKDOWN — which rules are failing, and why")
print("-" * 74)
by_rule = defaultdict(lambda: defaultdict(int))
by_rule_students = defaultdict(set)
for sid, rule, etype, desc, n in rows:
    by_rule[rule][etype] += n
    by_rule_students[rule].add(sid)

for rule in sorted(by_rule, key=lambda r: -len(by_rule_students[r])):
    ns = len(by_rule_students[rule])
    breakdown = ", ".join(f"{et}:{cnt}" for et, cnt in
                          sorted(by_rule[rule].items(), key=lambda x: -x[1]))
    print(f"  {rule:18s}  {ns:2d} students affected   ({breakdown})")
print()

# --- The "who needs attention this week" list ---
print("WHO NEEDS ATTENTION THIS WEEK (most errors, ranked)")
print("-" * 74)
total_by_student = defaultdict(int)
for sid, rule, etype, desc, n in rows:
    total_by_student[sid] += n

ranked = sorted(total_by_student.items(), key=lambda x: -x[1])[:5]
for sid, total in ranked:
    worst = sorted(by_student[sid], key=lambda r: -r[3])[0]
    print(f"  student {sid:2d}: {total:2d} errors — worst is {worst[0]}/{worst[1]}: \"{worst[2]}\"")
print()

# --- Honest limits ---
print("=" * 74)
print("LIMITS OF THIS METHOD (say these out loud)")
print("=" * 74)
print("  - This simulates student behaviour; real data replaces the generator.")
print("  - Error attribution works only where a distractor tag exists.")
print("  - For reasoning, the tag is the rule, not a fine-grained misconception.")
print("  - Syllogism and RC-type items: error_type is the RULE, not the trap.")
print("    A student failing syllogism gets 'syllogism' — we cannot yet tell")
print("    WHICH logical error they made. That requires human-authored items")
print("    with per-option misconception tags (Phase 5+).")
print("=" * 74)

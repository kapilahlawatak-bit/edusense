"""
Phase 7 — Teacher Dashboard View.

The Q-matrix (Phase 4-6) answers: which error type, how many students,
which rule. This is the teacher-facing layer that answers the question
a teacher actually asks:

  "Which 5 students do I need to talk to this week, and what do I tell them?"

It takes the Q-matrix data and produces:
  1. A "who needs attention" list — students ranked by total errors,
     each with their dominant misconception
  2. A "what to reteach" list — misconceptions ranked by how many students
     exhibit them, with the specific rule and the re-teaching description
  3. A per-student card — for each flagged student, which rules they're
     failing, which misconception, and what to say to them

Run: python teacher_dashboard.py
"""

import sqlite3
from collections import defaultdict

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

# ---------------------------------------------------------------------------
# 1. Pull the Q-matrix: every (student, rule, error_type) with counts
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
""").fetchall()

# Index for fast lookup
by_student = defaultdict(list)
by_error = defaultdict(lambda: {"students": set(), "count": 0, "desc": "", "rules": set()})
total_by_student = defaultdict(int)

for sid, rule, etype, desc, n in rows:
    by_student[sid].append({"rule": rule, "etype": etype, "desc": desc, "n": n})
    total_by_student[sid] += n
    e = by_error[etype]
    e["students"].add(sid)
    e["count"] += n
    e["desc"] = desc
    e["rules"].add(rule)

# ---------------------------------------------------------------------------
# 2. "WHO NEEDS ATTENTION THIS WEEK" — top 5 students by total errors
# ---------------------------------------------------------------------------

ranked = sorted(total_by_student.items(), key=lambda x: -x[1])[:5]

# ---------------------------------------------------------------------------
# 3. "WHAT TO RETEACH" — misconceptions ranked by students affected
# ---------------------------------------------------------------------------

reteach = sorted(by_error.items(), key=lambda x: -len(x[1]["students"]))

# ---------------------------------------------------------------------------
# 4. RETEACHING SCRIPTS — what to actually say for each misconception
# ---------------------------------------------------------------------------

RETEACH = {
    "SIGN_ERROR":      "Remind: moving a term across = flips its sign. +7 becomes -7, -4 becomes +4.",
    "ARITHMETIC_SLIP": "Slow down on the final arithmetic step. Check: 25-7=18, then 18/3=6.",
    "COLLECTION_ERROR":"Collect like terms on ONE side first. 3x - x = 2x, then move constants.",
    "ISOLATION_ERROR": "Divide by the coefficient of x, not the constant. 4x=8 means x=8/4=2.",
    "OFF_BY_ONE":      "Atbash: A<->Z. Mirror is position 26 - (letter+1), not letter+1.",
    "WRONG_SHIFT":     "Shift by exactly k. A=1+3=4=D. Not k+1 or k-1.",
    "NO_SHIFT":        "Apply the transformation. The coded letter is NOT the same as the original.",
    "REVERSED_GEN":    "Walk the family tree from the person asked about, outward. Uncle's daughter = cousin.",
    "WRONG_TURN":      "Each right turn rotates 90 degrees. Right 1 from N = E, not W.",
    "WRONG_DIFF":      "Find the difference between consecutive terms. 17,24,31: difference is 7.",
    "NON_SEQUITUR":    "A conclusion must follow from the premises. 'Some dogs can fly' does not make 'dogs are birds' true.",
    "WRONG_PATTERN":   "Alternating series: separate odd and even positions, find each pattern.",
    "FALSE_RATE":      "Generic error — review the question and options with the student.",
    "atbash":          "Review the Atbash rule: A<->Z, B<->Y.",
    "caesar":          "Review the shift rule: add k to the letter position, mod 26.",
    "number_series":   "Review common-difference and alternating patterns.",
    "blood_relation":  "Review family-tree walking: uncle's daughter is a cousin.",
    "direction_sense": "Review right/left turn rotation.",
    "syllogism":       "Review which conclusions follow from premises.",
}

# ---------------------------------------------------------------------------
# 5. PRINT THE DASHBOARD
# ---------------------------------------------------------------------------

print("=" * 76)
print("  TEACHER DASHBOARD  —  CBSE_09_MATHS  —  40 students")
print("=" * 76)
print()

# --- Section A: Who needs attention ---
print("┌─ WHO NEEDS ATTENTION THIS WEEK ────────────────────────────────────────┐")
print()
for rank, (sid, total) in enumerate(ranked, 1):
    student_errors = sorted(by_student[sid], key=lambda r: -r["n"])
    worst = student_errors[0]
    others = student_errors[1:3]
    other_str = ", ".join(f"{o['rule']}/{o['etype']}" for o in others)
    print(f"  {rank}. Student {sid:2d} — {total} errors")
    print(f"     Worst: {worst['rule']} / {worst['etype']}")
    print(f"     \"{worst['desc']}\"")
    if other_str:
        print(f"     Also: {other_str}")
    script = RETEACH.get(worst["etype"], RETEACH.get(worst["rule"], "Review with student."))
    print(f"     Say:  \"{script}\"")
    print()

print("└──────────────────────────────────────────────────────────────────────┘")
print()

# --- Section B: What to reteach (batch level) ---
print("┌─ WHAT TO RETEACH (batch level) ───────────────────────────────────────┐")
print()
print(f"  {'Misconception':22s} {'Students':>8s} {'Errors':>6s}  Rule(s)")
print(f"  {'─'*22} {'─'*8} {'─'*6}  {'─'*30}")
for etype, e in reteach:
    ns = len(e["students"])
    rules = ", ".join(sorted(e["rules"]))
    print(f"  {etype:22s} {ns:>8d} {e['count']:>6d}  {rules}")
print()

print("└──────────────────────────────────────────────────────────────────────┘")
print()

# --- Section C: Per-student cards for top 3 ---
print("┌─ STUDENT CARDS (top 3) ───────────────────────────────────────────────┐")
print()
for sid, total in ranked[:3]:
    student_errors = sorted(by_student[sid], key=lambda r: -r["n"])
    print(f"  ── Student {sid} ({total} errors) ──")
    for se in student_errors[:4]:
        script = RETEACH.get(se["etype"], RETEACH.get(se["rule"], "Review."))
        print(f"     [{se['n']:2d}×] {se['rule']:18s} → {se['etype']}")
        print(f"          \"{se['desc']}\"")
        print(f"          Say: \"{script}\"")
    print()

print("└──────────────────────────────────────────────────────────────────────┘")
print()

# --- Honest limits ---
print("HONEST LIMITS OF THIS DASHBOARD")
print("─" * 76)
print("  - Data is simulated. Replace the generator with real student data.")
print("  - Error attribution works only where a distractor tag exists.")
print("  - Coarse tags (atbash, caesar) come from simulated items; fine-grained")
print("    tags (OFF_BY_ONE, SIGN_ERROR) come from hand-authored items.")
print("  - The 'Say:' scripts are re-teaching prompts, not diagnoses.")
print("    They describe the misconception; the teacher decides the pedagogy.")
print("=" * 76)

"""
Phase 8 — Student-Facing View.

The teacher dashboard (Phase 7) is for the teacher. This is for the student:
  1. A practice test — serve items from the bank, collect answers
  2. Per-topic drill — focus on one rule/misconception at a time
  3. Progress tracking — mastery per topic over multiple attempts
  4. Error feedback — when a student picks a wrong option, show them
     WHY it's wrong (the misconception), not just "wrong"

Run: python student_view.py
"""

import sqlite3
from collections import defaultdict

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

# ---------------------------------------------------------------------------
# 1. PRACTICE TEST — serve 10 items, collect answers, show feedback
# ---------------------------------------------------------------------------

print("=" * 74)
print("  PRACTICE TEST  —  CBSE_09_MATHS  —  10 items")
print("=" * 74)
print()

# Pick 10 items: 5 maths + 5 reasoning, alternating
maths_items = cur.execute(
    "SELECT id, stem, option_a, option_b, option_c, option_d, correct_option, rule_type "
    "FROM item WHERE rule_type='Maths' ORDER BY id LIMIT 5").fetchall()

reasoning_items = cur.execute(
    "SELECT id, stem, option_a, option_b, option_c, option_d, correct_option, rule_type "
    "FROM item WHERE rule_type != 'Maths' ORDER BY id LIMIT 5").fetchall()

items = maths_items + reasoning_items

# Simulate a student answering: correct on 7, wrong on 3 (the wrong ones
# hit known misconceptions)
student_id = 1
cur.execute("DELETE FROM attempt_item WHERE attempt_id IN (SELECT id FROM attempt WHERE student_id=?)", (student_id,))
cur.execute("DELETE FROM attempt WHERE student_id=?", (student_id,))
cur.execute("INSERT INTO attempt (student_id, exam_id, started_at, submitted_at, raw_score) VALUES (?,?,?,?,?)",
            (student_id, 1, 2000000, 2000900, 0))
aid = cur.lastrowid

score = 0
for idx, (iid, stem, oa, ob, oc, od, correct, rule) in enumerate(items, 1):
    # simulate: student gets it wrong on items 3, 6, 9 (known misconception traps)
    if idx in (3, 6, 9):
        # pick a wrong option that has a misconception tag
        wrong = cur.execute(
            "SELECT option_letter FROM distractor_error WHERE item_id=?", (iid,)).fetchone()
        sel = wrong[0] if wrong else "A"
        correct_bool = 0
    else:
        sel = correct
        correct_bool = 1
        score += 1

    cur.execute("INSERT INTO attempt_item (attempt_id, item_id, selected_option, correct_bool, time_spent_seconds) VALUES (?,?,?,?,?)",
                (aid, iid, sel, correct_bool, 45))

    print(f"  Q{idx:2d}. {stem}")
    print(f"       Your answer: {sel}  {'✓' if correct_bool else '✗'}")
    if not correct_bool:
        # show the misconception for the wrong option
        tag = cur.execute(
            "SELECT error_type, description FROM distractor_error WHERE item_id=? AND option_letter=?",
            (iid, sel)).fetchone()
        if tag:
            print(f"       Why you're wrong: {tag[0]} — {tag[1]}")
        # show the correct answer
        print(f"       Correct answer: {correct}")
    print()

cur.execute("UPDATE attempt SET raw_score=? WHERE id=?", (score, aid))
conn.commit()

print(f"  SCORE: {score} / {len(items)}")
print()

# ---------------------------------------------------------------------------
# 2. PER-TOPIC DRILL — focus on one rule
# ---------------------------------------------------------------------------

print("=" * 74)
print("  PER-TOPIC DRILL  —  focus on 'atbash'")
print("=" * 74)
print()

atbash_items = cur.execute(
    "SELECT id, stem, option_a, option_b, option_c, option_d, correct_option "
    "FROM item WHERE rule_type='atbash' LIMIT 3").fetchall()

for idx, (iid, stem, oa, ob, oc, od, correct) in enumerate(atbash_items, 1):
    print(f"  Drill Q{idx}. {stem}")
    print(f"       A: {oa}   B: {ob}   C: {oc}   D: {od}")
    print(f"       Correct: {correct}")
    print()

# ---------------------------------------------------------------------------
# 3. PROGRESS TRACKING — mastery per topic over attempts
# ---------------------------------------------------------------------------

print("=" * 74)
print("  PROGRESS  —  student 1, mastery per topic")
print("=" * 74)
print()

# aggregate across all attempts for this student
rows = cur.execute("""
SELECT
    i.rule_type,
    COUNT(*) as total,
    SUM(CASE WHEN ai.correct_bool=1 THEN 1 ELSE 0 END) as correct
FROM attempt_item ai
JOIN attempt a ON a.id = ai.attempt_id
JOIN item i ON i.id = ai.item_id
WHERE a.student_id = ?
GROUP BY i.rule_type
""", (student_id,)).fetchall()

print(f"  {'Topic':22s} {'Attempted':>9s} {'Correct':>7s} {'Mastery':>7s}")
print(f"  {'─'*22} {'─'*9} {'─'*7} {'─'*7}")
for rule, total, correct in rows:
    pct = (correct / total * 100) if total else 0
    bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
    print(f"  {rule:22s} {total:>9d} {correct:>7d} {pct:>6.1f}%  {bar}")
print()

# ---------------------------------------------------------------------------
# 4. ERROR FEEDBACK SUMMARY — what this student got wrong and why
# ---------------------------------------------------------------------------

print("=" * 74)
print("  YOUR ERRORS THIS SESSION  —  and why")
print("=" * 74)
print()

errors = cur.execute("""
SELECT
    i.stem,
    de.error_type,
    de.description,
    i.correct_option,
    ai.selected_option
FROM attempt_item ai
JOIN attempt a ON a.id = ai.attempt_id
JOIN item i ON i.id = ai.item_id
JOIN distractor_error de ON de.item_id = ai.item_id AND de.option_letter = ai.selected_option
WHERE ai.correct_bool = 0 AND a.student_id = ?
""", (student_id,)).fetchall()

for stem, etype, desc, correct, selected in errors:
    print(f"  Q: {stem}")
    print(f"     You picked: {selected}")
    print(f"     Correct:   {correct}")
    print(f"     Your mistake: {etype}")
    print(f"     \"{desc}\"")
    print()

print("=" * 74)
print("HONEST LIMITS OF THIS STUDENT VIEW")
print("─" * 74)
print("  - Practice test and drill are simulated; real student replaces the answers.")
print("  - Error feedback shows the misconception tag, not a pedagogical explanation.")
print("  - Progress is per-topic mastery, not per-skill decay (that's Phase 9+).")
print("  - The 'Your mistake' tag describes WHAT went wrong, not WHY the student")
print("    made it. That diagnosis requires the teacher dashboard + human judgment.")
print("=" * 74)

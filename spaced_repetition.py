"""
Phase 9 — Spaced repetition / skill decay scheduling.

The mechanism that decides WHEN to retest a weak topic.

For each student × topic, we track:
  - mastery probability (p)
  - time since last correct answer
  - half-life: how fast mastery decays without practice

The scheduler then produces a daily study plan: which topics to review,
in what order, based on which are closest to being forgotten.

This is the Duolingo-style skill decay mechanism that no Indian player
applies to school maths.

Run: python spaced_repetition.py
"""

import sqlite3, math
from collections import defaultdict

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

# ---------------------------------------------------------------------------
# 1. COMPUTE SKILL STATE per (student, topic)
#    mastery_p decays exponentially with time since last practice
# ---------------------------------------------------------------------------

# Fetch all attempts with timestamps (use row order as time proxy)
rows = cur.execute("""
SELECT
    a.student_id,
    i.rule_type,
    ai.correct_bool,
    ROW_NUMBER() OVER (ORDER BY a.id, ai.rowid) as seq
FROM attempt_item ai
JOIN attempt a ON a.id = ai.attempt_id
JOIN item i ON i.id = ai.item_id
ORDER BY a.id, ai.rowid
""").fetchall()

# Build skill state: (student, topic) -> {correct, total, last_correct_seq}
# Use per-student session counting, not global row numbers.
skill = defaultdict(lambda: {"correct": 0, "total": 0, "last_correct": -1, "last_attempt": -1})

# First, find the max session per student
student_sessions = {}
for sid, rule, correct, seq in rows:
    student_sessions[sid] = max(student_sessions.get(sid, 0), seq)

# Reset seq to per-student session index
prev_student = None
session_counter = {}
for sid, rule, correct, seq in rows:
    if sid != prev_student:
        prev_student = sid
        session_counter[sid] = 0
    session_counter[sid] += 1
    local_seq = session_counter[sid]

    k = (sid, rule)
    skill[k]["total"] += 1
    skill[k]["last_attempt"] = local_seq
    if correct:
        skill[k]["correct"] += 1
        skill[k]["last_correct"] = local_seq

# ---------------------------------------------------------------------------
# 2. DECAY MODEL
#    mastery_p = base_p * exp(-decay * sessions_since_last_correct)
#    base_p = correct / total (raw accuracy)
#    decay = 0.05 (tunable — higher means faster forgetting)
# ---------------------------------------------------------------------------

DECAY = 0.05
HALF_LIFE = math.log(2) / DECAY  # sessions for mastery to halve

# current session number (max across all students, per-student)
max_seq = max((s["last_attempt"] for s in skill.values()), default=1)

# ---------------------------------------------------------------------------
# 3. COMPUTE CURRENT MASTERY + PRIORITY SCORE
#    priority = how urgently this needs review
#    higher priority = closer to being forgotten
# ---------------------------------------------------------------------------

scheduled = []
for (sid, rule), s in skill.items():
    base_p = s["correct"] / s["total"] if s["total"] > 0 else 0
    sessions_since = max_seq - s["last_correct"] if s["last_correct"] >= 0 else max_seq
    current_p = base_p * math.exp(-DECAY * sessions_since)

    # priority: low mastery + long since practice = high priority
    urgency = (1 - current_p) * (1 + sessions_since / HALF_LIFE)

    scheduled.append({
        "student": sid, "topic": rule,
        "base_p": base_p, "current_p": current_p,
        "sessions_since": sessions_since,
        "urgency": urgency,
        "correct": s["correct"], "total": s["total"],
    })

# Sort by urgency (highest first = needs review soonest)
scheduled.sort(key=lambda x: -x["urgency"])

# ---------------------------------------------------------------------------
# 4. PRINT THE SCHEDULE
# ---------------------------------------------------------------------------

print("=" * 78)
print("  SPACED REPETITION SCHEDULE  —  Duolingo-style skill decay")
print("=" * 78)
print()
print(f"  Decay rate: {DECAY} per session")
print(f"  Half-life:  {HALF_LIFE:.1f} sessions (mastery halves after this many sessions)")
print(f"  Current session: {max_seq}")
print()

print("  TODAY'S REVIEW QUEUE (sorted by urgency)")
print("  " + "─" * 74)
print(f"  {'Student':>7s}  {'Topic':22s} {'Base':>5s} {'Now':>5s} {'Since':>5s} {'Urgency':>7s}")
print(f"  {'─'*7}  {'─'*22} {'─'*5} {'─'*5} {'─'*5} {'─'*7}")

for s in scheduled[:15]:
    print(f"  {s['student']:>7d}  {s['topic']:22s} {s['base_p']:>5.2f} {s['current_p']:>5.2f} "
          f"{s['sessions_since']:>5d} {s['urgency']:>7.2f}")
print()

# ---------------------------------------------------------------------------
# 5. STUDY PLAN FOR TOP 3 STUDENTS
# ---------------------------------------------------------------------------

print("  STUDY PLANS (top 3 students by urgency)")
print("  " + "─" * 74)

student_plans = defaultdict(list)
for s in scheduled:
    student_plans[s["student"]].append(s)

for sid in sorted(student_plans, key=lambda s: -max(x["urgency"] for x in student_plans[s]))[:3]:
    plan = sorted(student_plans[sid], key=lambda x: -x["urgency"])[:5]
    print(f"\n  Student {sid} — review these {len(plan)} topics today:")
    for i, s in enumerate(plan, 1):
        # recommended action based on mastery level
        if s["current_p"] < 0.3:
            action = "RE-TEACH from scratch (mastery nearly zero)"
        elif s["current_p"] < 0.6:
            action = "Targeted drill on weak items (mastery moderate)"
        else:
            action = "Quick review, then move on (mastery high)"

        print(f"    {i}. {s['topic']:22s}  mastery={s['current_p']:.2f}  "
              f"last correct {s['sessions_since']} sessions ago")
        print(f"       → {action}")

print()

# ---------------------------------------------------------------------------
# 6. EXAM-DATE COUNTDOWN (what a student would see 30 days before exam)
# ---------------------------------------------------------------------------

print("  EXAM-DATE SIMULATION (30 days before exam)")
print("  " + "─" * 74)
print()
print("  If the exam is in 30 days, the scheduler should front-load the")
print("  topics that will decay most before then. Simulating 30 sessions")
print("  of decay (no practice):")
print()

# simulate 30 sessions of pure decay for the top student
sid = sorted(student_plans, key=lambda s: -max(x["urgency"] for x in student_plans[s]))[0]
plan = sorted(student_plans[sid], key=lambda x: -x["urgency"])[:5]

print(f"  Student {sid} — mastery 30 days out (no practice):")
for s in plan:
    p_30 = s["current_p"] * math.exp(-DECAY * 30)
    print(f"    {s['topic']:22s}  now={s['current_p']:.2f}  →  day-30={p_30:.2f}"
          f"  {'⚠ DANGER' if p_30 < 0.3 else ''}")

print()
print("  → Topics that will decay below 0.3 by exam day need practice NOW,")
print("    not 5 days before. This is the scheduler's core value.")
print()

print("=" * 78)
print("HONEST LIMITS OF SPACED REPETITION")
print("─" * 78)
print("  - Decay rate is a single global constant; real systems use per-topic rates.")
print("  - 'Sessions since last correct' is a proxy for time; real systems use")
print("    wall-clock timestamps.")
print("  - Mastery is binary accuracy, not IRT/BKT probability.")
print("    A BKT posterior would be more principled.")
print("  - The scheduler does not account for inter-topic dependencies")
print("    (e.g. you can't learn series without arithmetic).")
print("=" * 78)

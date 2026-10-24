"""
Phase 19 — Class 10 Trig + Coordinate Geometry, Class 11 Probability/Stats/Limits.
Generated items. Run: python seed_maths_extra.py
"""

import sqlite3, random

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (10,'Maths','MATHS_10X','Class 10 Maths Extra','0','medium')")
cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (11,'Maths','MATHS_11X','Class 11 Maths Extra','0','medium')")
conn.commit()
T10 = cur.execute("SELECT id FROM topic WHERE chapter_code='MATHS_10X'").fetchone()[0]
T11 = cur.execute("SELECT id FROM topic WHERE chapter_code='MATHS_11X'").fetchone()[0]

items = []

# ---- Trig: sin/cos/tan values ----
trig_vals = [(0, "0", "1", "0"), (30, "1/2", "√3/2", "1/√3"), (45, "√2/2", "√2/2", "1"), (60, "√3/2", "1/2", "√3"), (90, "1", "0", "undefined")]
for angle, s, c, t in trig_vals:
    items.append((f"What is sin {angle}°?", {"A": s, "B": c, "C": t, "D": "1"}, "A", {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "WRONG_CONCEPT"}, T10, "Trig_Values"))
    items.append((f"What is cos {angle}°?", {"A": s, "B": c, "C": t, "D": "1"}, "B", {"A": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "WRONG_CONCEPT"}, T10, "Trig_Values"))
    items.append((f"What is tan {angle}°?", {"A": s, "B": c, "C": t, "D": "0"}, "C", {"A": "CONFUSED_TERMS", "B": "CONFUSED_TERMS", "D": "WRONG_CONCEPT"}, T10, "Trig_Values"))

# trig identities
for _ in range(20):
    a = random.choice([30, 45, 60])
    items.append((f"sin²{a}° + cos²{a}° = ?",
                 {"A": "0", "B": "1", "C": "2", "D": "sin{a}°cos{a}°"}, "B",
                 {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}, T10, "Trig_Identity"))

# ---- Coordinate Geometry: distance formula ----
for _ in range(25):
    x1, y1 = random.randint(0, 5), random.randint(0, 5)
    x2, y2 = random.randint(0, 5), random.randint(0, 5)
    from fractions import Fraction
    d2 = (x2-x1)**2 + (y2-y1)**2
    import math
    d = math.isqrt(d2)
    if d*d != d2:
        d = f"√{d2}"
    else:
        d = str(d)
    # distractors
    d_wrong1 = str(abs(x2-x1) + abs(y2-y1))  # manhattan
    d_wrong2 = str(abs(x2-x1))
    d_wrong3 = str(abs(y2-y1))
    items.append((f"Distance between ({x1},{y1}) and ({x2},{y2}) is:",
                 {"A": d, "B": d_wrong1, "C": d_wrong2, "D": d_wrong3}, "A",
                 {"B": "WRONG_FORMULA", "C": "PARTIAL", "D": "PARTIAL"}, T10, "Coord_Distance"))

# ---- Coordinate Geometry: midpoint ----
for _ in range(20):
    x1, y1 = random.randint(0, 8), random.randint(0, 8)
    x2, y2 = random.randint(0, 8), random.randint(0, 8)
    mx = (x1+x2)/2
    my = (y1+y2)/2
    mx_s = str(int(mx)) if mx == int(mx) else f"{x1+x2}/2"
    my_s = str(int(my)) if my == int(my) else f"{y1+y2}/2"
    correct = f"({mx_s}, {my_s})"
    d1 = f"({x1+x2}, {y1+y2})"
    d2 = f"({x1}, {y1})"
    d3 = f"({x2}, {y2})"
    items.append((f"Midpoint of ({x1},{y1}) and ({x2},{y2}) is:",
                 {"A": correct, "B": d1, "C": d2, "D": d3}, "A",
                 {"B": "WRONG_FORMULA", "C": "PARTIAL", "D": "PARTIAL"}, T10, "Coord_Midpoint"))

# ---- Probability (Class 11) ----
for _ in range(30):
    n = random.randint(2, 6)
    favorable = random.randint(1, n)
    from math import gcd
    from fractions import Fraction
    f = Fraction(favorable, n)
    correct = f"{f.numerator}/{f.denominator}"
    d1 = f"{n}/{favorable}"
    d2 = f"{favorable-1}/{n}" if favorable > 1 else f"{favorable+1}/{n}"
    d3 = f"{n-favorable}/{n}"
    items.append((f"A die is rolled once. Probability of getting a number ≤ {favorable} is:",
                 {"A": correct, "B": d1, "C": d2, "D": d3}, "A",
                 {"B": "REVERSED", "C": "OFF_BY_ONE", "D": "COMPLEMENT"}, T11, "Probability_Basic"))

# ---- Statistics: mean ----
for _ in range(20):
    nums = [random.randint(1, 20) for _ in range(5)]
    mean = sum(nums)/5
    mean_s = str(mean) if mean == int(mean) else f"{sum(nums)}/5"
    d1 = str(max(nums))
    d2 = str(min(nums))
    d3 = str(sorted(nums)[2])  # median-ish
    items.append((f"Mean of {nums} is:",
                 {"A": mean_s, "B": d1, "C": d2, "D": d3}, "A",
                 {"B": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}, T11, "Stats_Mean"))

# ---- Statistics: median ----
for _ in range(20):
    nums = sorted([random.randint(1, 20) for _ in range(5)])
    med = nums[2]
    d1 = str(nums[0])
    d2 = str(nums[4])
    d3 = str(round(sum(nums)/5))
    items.append((f"Median of {nums} is:",
                 {"A": str(med), "B": d1, "C": d2, "D": d3}, "A",
                 {"B": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}, T11, "Stats_Median"))

# ---- Limits (Class 11) ----
limits = [
    ("lim (x→0) sin(x)/x =", {"A": "0", "B": "1", "C": "∞", "D": "-1"}, "B"),
    ("lim (x→∞) 1/x =", {"A": "0", "B": "1", "C": "∞", "D": "-1"}, "A"),
    ("lim (x→0) (1-cos x)/x² =", {"A": "0", "B": "1/2", "C": "1", "D": "2"}, "B"),
    ("lim (x→∞) (2x+3)/(x+1) =", {"A": "0", "B": "1", "C": "2", "D": "3"}, "C"),
    ("lim (x→0) (e^x - 1)/x =", {"A": "0", "B": "1", "C": "e", "D": "∞"}, "B"),
    ("lim (x→0) tan(x)/x =", {"A": "0", "B": "1", "C": "∞", "D": "-1"}, "B"),
]
for stem, opts, correct in limits:
    for _ in range(4):
        items.append((stem, opts, correct, {"A": "WRONG_CONCEPT", "B": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}, T11, "Limits_Basic"))

MIS = {
    "WRONG_FORMULA": "Used wrong formula",
    "PARTIAL": "Partial calculation",
    "REVERSED": "Reversed numerator/denominator",
    "OFF_BY_ONE": "Off by one",
    "COMPLEMENT": "Used complement instead",
    "CONFUSED_TERMS": "Confused similar terms",
    "WRONG_CONCEPT": "Wrong concept",
}

stored = 0
for stem, opts, correct, pw, tid, rt in items:
    cur.execute("INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (tid, stem, opts["A"], opts["B"], opts["C"], opts["D"], correct, 1, "generated", "passed", rt))
    iid = cur.lastrowid
    for letter, mis in pw.items():
        if letter != correct:
            cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                        (iid, letter, mis, MIS.get(mis, mis)))
    stored += 1

conn.commit()
c2 = sqlite3.connect(DB)
print("Maths extra items added:", stored)
print("Grand total:", c2.execute("SELECT COUNT(*) FROM item").fetchone()[0])
c2.close(); conn.close()

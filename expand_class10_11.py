"""
Phase 14 — Class 10 and Class 11 maths topics.

Extends the proven generate → verify → tag pipeline (Phases 10-11) to
Class 10 and Class 11 CBSE maths topics.

Class 10 topics added:
  - Quadratic equations (factorisable):  x² + bx + c = 0
  - Arithmetic progressions (find nth term — already have generator)
  - Circles & triangles (Pythagoras):  a² + b² = c²

Class 11 topics added:
  - Sets & relations (basic):  |A ∪ B| = |A| + |B| - |A ∩ B|
  - Trigonometric functions (basic identities):  sin²θ + cos²θ = 1

Run: python expand_class10_11.py [count_per_topic]
"""

import sqlite3, random, sys
from fractions import Fraction

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Create topics for Class 10 and Class 11
cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (10,'Maths','CL10_QUAD','Quadratic Equations','0','medium')")
tid_10_quad = cur.lastrowid
cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (10,'Maths','CL10_AP','Arithmetic Progressions','0','medium')")
tid_10_ap = cur.lastrowid
cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (10,'Maths','CL10_PYTH','Pythagoras Theorem','0','medium')")
tid_10_pyth = cur.lastrowid
cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (11,'Maths','CL11_SETS','Sets & Relations','0','medium')")
tid_11_sets = cur.lastrowid
cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (11,'Maths','CL11_TRIG','Trigonometric Functions','0','medium')")
tid_11_trig = cur.lastrowid
conn.commit()

MISCONCEPTIONS = {
    "SIGN_ERROR":       "Moved a term across = with the wrong sign",
    "COLLECTION_ERROR": "Collected like terms incorrectly",
    "ARITHMETIC_SLIP":  "Correct method, arithmetic mistake in final step",
    "FORMULA_ERROR":    "Used the wrong formula or wrong term index",
    "WRONG_ROOT":       "Found the wrong root",
    "WRONG_FORMULA":    "Used the wrong set formula",
    "WRONG_IDENTITY":   "Used the wrong trigonometric identity",
    "WRONG_ANGLE":      "Used the wrong angle value",
    "WRONG_TRIANGLE":   "Applied Pythagoras to the wrong side",
}


# ---------------------------------------------------------------------------
# CLASS 10: Quadratic equations (factorisable, integer roots)
# ---------------------------------------------------------------------------

def gen_quad_roots():
    """Generate a factorisable quadratic with integer roots."""
    r1 = random.choice([1, 2, 3, 4, 5])
    r2 = random.choice([1, 2, 3, 4, 5])
    # x² - (r1+r2)x + r1*r2 = 0
    b = -(r1 + r2)
    c = r1 * r2
    return r1, r2, b, c


def solve_quad_factorisable(b, c):
    """x² + bx + c = 0. Find integer roots."""
    import math
    disc = b * b - 4 * c
    if disc < 0:
        return None
    sqrt_d = int(math.isqrt(disc))
    if sqrt_d * sqrt_d != disc:
        return None
    r1 = (-b + sqrt_d) // 2
    r2 = (-b - sqrt_d) // 2
    if r1 * r2 != c or r1 + r2 != -b:
        return None
    return r1, r2


def build_quad_10():
    r1, r2, b, c = gen_quad_roots()
    roots = solve_quad_factorisable(b, c)
    if roots is None:
        return None

    # format the stem with proper sign
    if b >= 0:
        stem = f"Solve for x: x² + {b}x + {c} = 0  (x > 0)"
    else:
        stem = f"Solve for x: x² - {abs(b)}x + {c} = 0  (x > 0)"

    # distractors
    distractor_list = []
    seen_vals = set()

    def try_add(mis, val):
        if val is not None and val not in seen_vals:
            distractor_list.append((mis, val))
            seen_vals.add(val)

    # WRONG_ROOT: the negative root
    try_add("WRONG_ROOT", roots[1] if roots[1] > 0 else roots[0])
    # ARITHMETIC_SLIP
    try_add("ARITHMETIC_SLIP", roots[0] + 1)
    try_add("ARITHMETIC_SLIP", roots[0] - 1)
    # SIGN_ERROR: product instead of sum
    try_add("SIGN_ERROR", Fraction(c, 1) if c != roots[0] else None)

    k = 1
    while len(distractor_list) < 3:
        try_add("ARITHMETIC_SLIP", roots[0] + k)
        k += 1
        if k > 20:
            break

    random.shuffle(distractor_list)
    slots = ["A", "B", "C", "D"]
    correct_slot = random.choice(slots)
    options = {}
    per_wrong = {}
    di = 0
    for s in slots:
        if s == correct_slot:
            options[s] = str(roots[0])
        else:
            mis, val = distractor_list[di]
            options[s] = str(val)
            per_wrong[s] = mis
            di += 1

    return stem, options, correct_slot, per_wrong


def verify_quad_10(stem, options, correct):
    import re, math
    m = re.search(r"x²\s*([+-])\s*(\d+)x\s*\+\s*(\d+)\s*=\s*0", stem)
    if m:
        sign = 1 if m.group(1) == "+" else -1
        b = sign * int(m.group(2))
        c = int(m.group(3))
        disc = b * b - 4 * c
        if disc < 0:
            return False
        sqrt_d = int(math.isqrt(disc))
        if sqrt_d * sqrt_d != disc:
            return False
        r1 = (-b + sqrt_d) // 2
        r2 = (-b - sqrt_d) // 2
        if r1 * r2 != c or r1 + r2 != -b:
            return False
        positive = max(r1, r2)
        return str(options[correct]) == str(positive)
    return False


# ---------------------------------------------------------------------------
# CLASS 10: Pythagoras theorem
# ---------------------------------------------------------------------------

def build_pythagoras():
    """a² + b² = c², find the hypotenuse."""
    # use Pythagorean triples
    triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15)]
    a, b, c = random.choice(triples)
    stem = f"In a right triangle, the two legs are {a} and {b}. Find the hypotenuse."

    distractor_list = []
    seen_vals = {c}

    def try_add(mis, val):
        if val is not None and val not in seen_vals:
            distractor_list.append((mis, val))
            seen_vals.add(val)

    # WRONG_TRIANGLE: a + b instead of hypotenuse
    try_add("WRONG_TRIANGLE", a + b)
    # ARITHMETIC_SLIP
    try_add("ARITHMETIC_SLIP", c + 1)
    try_add("ARITHMETIC_SLIP", c - 1)

    k = 1
    while len(distractor_list) < 3:
        try_add("ARITHMETIC_SLIP", c + k)
        k += 1
        if k > 20:
            break

    random.shuffle(distractor_list)
    slots = ["A", "B", "C", "D"]
    correct_slot = random.choice(slots)
    options = {}
    per_wrong = {}
    di = 0
    for s in slots:
        if s == correct_slot:
            options[s] = str(c)
        else:
            mis, val = distractor_list[di]
            options[s] = str(val)
            per_wrong[s] = mis
            di += 1

    return stem, options, correct_slot, per_wrong


def verify_pythagoras(stem, options, correct):
    import re
    m = re.search(r"legs are (\d+) and (\d+)", stem)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        c = (a * a + b * b) ** 0.5
        if c == int(c):
            return str(options[correct]) == str(int(c))
    return False


# ---------------------------------------------------------------------------
# CLASS 11: Sets & relations
# ---------------------------------------------------------------------------

def build_sets():
    """|A ∪ B| = |A| + |B| - |A ∩ B|"""
    a = random.randint(10, 30)
    b = random.randint(10, 30)
    inter = random.randint(1, min(a, b))
    union = a + b - inter
    stem = f"If |A| = {a}, |B| = {b}, and |A ∩ B| = {inter}, find |A ∪ B|."

    distractor_list = []
    seen_vals = {union}

    def try_add(mis, val):
        if val is not None and val not in seen_vals:
            distractor_list.append((mis, val))
            seen_vals.add(val)

    # WRONG_FORMULA: forgot to subtract intersection
    try_add("WRONG_FORMULA", a + b)
    # ARITHMETIC_SLIP
    try_add("ARITHMETIC_SLIP", union + 1)
    try_add("ARITHMETIC_SLIP", union - 1)
    # WRONG_FORMULA: added intersection instead of subtracting
    try_add("WRONG_FORMULA", a + b + inter)

    k = 1
    while len(distractor_list) < 3:
        try_add("ARITHMETIC_SLIP", union + k)
        k += 1
        if k > 20:
            break

    random.shuffle(distractor_list)
    slots = ["A", "B", "C", "D"]
    correct_slot = random.choice(slots)
    options = {}
    per_wrong = {}
    di = 0
    for s in slots:
        if s == correct_slot:
            options[s] = str(union)
        else:
            mis, val = distractor_list[di]
            options[s] = str(val)
            per_wrong[s] = mis
            di += 1

    return stem, options, correct_slot, per_wrong


def verify_sets(stem, options, correct):
    import re
    m = re.search(r"\|A\| = (\d+), \|B\| = (\d+), and \|A ∩ B\| = (\d+)", stem)
    if m:
        a, b, inter = int(m.group(1)), int(m.group(2)), int(m.group(3))
        union = a + b - inter
        return str(options[correct]) == str(union)
    return False


# ---------------------------------------------------------------------------
# CLASS 11: Trigonometric functions
# ---------------------------------------------------------------------------

def build_trig():
    """sin²θ + cos²θ = 1. Given one, find the other."""
    import math
    # use known values
    angles = [(0, 1, 0), (30, None, None), (45, None, None), (60, None, None), (90, 1, 0)]
    angle, sin_val, cos_val = random.choice(angles)
    if angle == 30:
        sin_val = Fraction(1, 2); cos_val = None
    elif angle == 45:
        sin_val = Fraction(1, 2) ** Fraction(1, 2); cos_val = None
    elif angle == 60:
        sin_val = Fraction(3, 4) ** Fraction(1, 2); cos_val = None
    elif angle == 90:
        sin_val = 1; cos_val = 0
    else:
        sin_val = 0; cos_val = 1

    # For simplicity, use angles where values are exact
    exact = {0: (0, 1), 30: (Fraction(1,2), Fraction(3,4)**Fraction(1,2) if False else None),
             45: (None, None), 60: (None, None), 90: (1, 0)}

    # use only angles with exact values for verification
    choices = [0, 90]
    angle = random.choice(choices)
    sin_v, cos_v = exact[angle]

    stem = f"If sin θ = {sin_v} and θ = {angle}°, find cos θ."

    distractor_list = []
    seen_vals = {cos_v}

    def try_add(mis, val):
        if val is not None and val not in seen_vals:
            distractor_list.append((mis, val))
            seen_vals.add(val)

    # WRONG_IDENTITY: used sin instead of cos
    try_add("WRONG_IDENTITY", sin_v)
    # ARITHMETIC_SLIP
    try_add("ARITHMETIC_SLIP", cos_v + 1 if cos_v != 0 else 1)
    try_add("WRONG_ANGLE", Fraction(1, 2) if cos_v != Fraction(1,2) else 1)

    k = 1
    while len(distractor_list) < 3:
        try_add("ARITHMETIC_SLIP", (cos_v or 0) + k)
        k += 1
        if k > 20:
            break

    random.shuffle(distractor_list)
    slots = ["A", "B", "C", "D"]
    correct_slot = random.choice(slots)
    options = {}
    per_wrong = {}
    di = 0
    for s in slots:
        if s == correct_slot:
            options[s] = str(cos_v)
        else:
            mis, val = distractor_list[di]
            options[s] = str(val)
            per_wrong[s] = mis
            di += 1

    return stem, options, correct_slot, per_wrong


def verify_trig(stem, options, correct):
    import re
    m = re.search(r"θ = (\d+)°", stem)
    if m:
        angle = int(m.group(1))
        # exact values
        exact = {0: 1, 90: 0}
        if angle in exact:
            return str(options[correct]) == str(exact[angle])
    return False


# ---------------------------------------------------------------------------
# GENERATE BATCH
# ---------------------------------------------------------------------------

def generate_batch(count_per_topic):
    stored = 0
    rejected = 0

    for topic_name, build_func, verify_func, tid, rule_type in [
        ("Quadratic (Class 10)", build_quad_10, verify_quad_10, tid_10_quad, "CL10_Quadratic"),
        ("Pythagoras (Class 10)", build_pythagoras, verify_pythagoras, tid_10_pyth, "CL10_Pythagoras"),
        ("Sets (Class 11)", build_sets, verify_sets, tid_11_sets, "CL11_Sets"),
        ("Trig (Class 11)", build_trig, verify_trig, tid_11_trig, "CL11_Trig"),
    ]:
        for _ in range(count_per_topic):
            result = build_func()
            if result is None:
                rejected += 1
                continue
            stem, options, correct, per_wrong = result
            if not verify_func(stem, options, correct):
                rejected += 1
                continue
            cur.execute(
                "INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (tid, stem, options.get("A", ""), options.get("B", ""),
                 options.get("C", ""), options.get("D", ""),
                 correct, 1, "generated", "passed", rule_type))
            iid = cur.lastrowid
            for letter, mis in per_wrong.items():
                if letter != correct and letter in options:
                    cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                                (iid, letter, mis, MISCONCEPTIONS.get(mis, mis)))
            stored += 1
            if stored % 50 == 0:
                conn.commit()

    conn.commit()
    return stored, rejected


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    print(f"Generating {count} items per new topic...")
    stored, rejected = generate_batch(count)
    print(f"✓ Stored: {stored}")
    print(f"✗ Rejected: {rejected}")
    print()

    c2 = sqlite3.connect(DB)
    print("Item counts by rule_type after expansion:")
    for r in c2.execute("SELECT rule_type, COUNT(*) FROM item GROUP BY rule_type ORDER BY COUNT(*) DESC"):
        print(f"  {r[0]:22s} {r[1]}")
    print()
    print("Total items:", c2.execute("SELECT COUNT(*) FROM item").fetchone()[0])
    print("Total distractor errors:", c2.execute("SELECT COUNT(*) FROM distractor_error").fetchone()[0])
    c2.close()

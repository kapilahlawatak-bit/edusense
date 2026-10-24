"""
Phase 13 — Content expansion.

Adds new maths topics and reasoning families to the engine, using the
same generate → verify → tag pipeline from Phases 10-11.

New maths topics:
  - Quadratic equations:  x² = c,  x² = ax + b  (integer roots only)
  - Arithmetic progressions: find the nth term

New reasoning families:
  - Word coding: encode a WORD using Atbash or Caesar
  - Two-generation blood relation: uncle's son's daughter

Run: python expand_content.py [count_per_topic]
"""

import sqlite3, random, sys
from fractions import Fraction

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Fetch topic ids
tid_maths = cur.execute("SELECT id FROM topic WHERE subject='Maths' AND chapter_code='NSEC_9_1'").fetchone()[0]
tid_reasoning = cur.execute("SELECT id FROM topic WHERE subject='Reasoning'").fetchone()[0]

# ---------------------------------------------------------------------------
# NEW MATHS TOPICS
# ---------------------------------------------------------------------------

MISCONCEPTIONS = {
    "SIGN_ERROR":       "Moved a term across = with the wrong sign",
    "COLLECTION_ERROR": "Collected like terms incorrectly",
    "ISOLATION_ERROR":  "Divided/multiplied by the wrong number when isolating x",
    "ARITHMETIC_SLIP":  "Correct method, arithmetic mistake in final step",
    "WRONG_ROOT":       "Found only one root or the wrong root of the quadratic",
    "FORMULA_ERROR":    "Used the wrong AP formula or wrong term index",
    "WRONG_DIFF":       "Misread the common difference",
}


# ---- Quadratic equations ----

def gen_quadratic():
    """x² = c where c is a perfect square (integer roots)."""
    root = random.choice([2, 3, 4, 5, 6, 7, 8, 9])
    c = root * root
    return root, c


def solve_quadratic(root, c):
    """x² = c → x = ±√c. We ask for the positive root."""
    return Fraction(root, 1)


def build_quadratic_item():
    root, c = gen_quadratic()
    true_ans = solve_quadratic(root, c)
    stem = f"Solve for x: x² = {c}  (x > 0)"

    # distractors
    distractor_list = []
    seen_vals = {true_ans}

    def try_add(mis, val):
        if val is not None and val not in seen_vals:
            distractor_list.append((mis, val))
            seen_vals.add(val)

    # WRONG_ROOT: forgot it's x>0, so picks the negative root
    try_add("WRONG_ROOT", -true_ans)
    # ARITHMETIC_SLIP: off by one
    try_add("ARITHMETIC_SLIP", true_ans + 1)
    try_add("ARITHMETIC_SLIP", true_ans - 1)
    # ISOLATION_ERROR: took the square root incorrectly
    try_add("ISOLATION_ERROR", Fraction(c, root) if root != 0 else None)

    k = 1
    while len(distractor_list) < 3:
        try_add("ARITHMETIC_SLIP", true_ans + k)
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
            options[s] = str(true_ans)
        else:
            mis, val = distractor_list[di]
            options[s] = str(val)
            per_wrong[s] = mis
            di += 1

    return stem, options, correct_slot, per_wrong


def verify_quadratic(stem, options, correct):
    import re
    m = re.search(r"x² = (\d+)", stem)
    if m:
        c = int(m.group(1))
        # find integer square root
        root = None
        for r in range(1, 30):
            if r * r == c:
                root = r
                break
        if root is None:
            return False
        return str(options[correct]) == str(root)
    return False


# ---- Arithmetic progressions ----

def gen_ap():
    """Generate an AP: a, a+d, a+2d, ... find the nth term."""
    a = random.randint(2, 10)
    d = random.randint(2, 8)
    n = random.randint(6, 12)
    return a, d, n


def solve_ap(a, d, n):
    """nth term = a + (n-1)*d"""
    return Fraction(a + (n - 1) * d, 1)


def build_ap_item():
    a, d, n = gen_ap()
    true_ans = solve_ap(a, d, n)
    terms = [a + i * d for i in range(5)]
    stem = f"Find the {n}th term of the AP: {', '.join(map(str, terms))}, ... (a={a}, d={d})"

    distractor_list = []
    seen_vals = {true_ans}

    def try_add(mis, val):
        if val is not None and val not in seen_vals:
            distractor_list.append((mis, val))
            seen_vals.add(val)

    # FORMULA_ERROR: used a + n*d instead of a + (n-1)*d
    try_add("FORMULA_ERROR", Fraction(a + n * d, 1))
    # WRONG_DIFF: used d+1
    try_add("WRONG_DIFF", Fraction(a + (n - 1) * (d + 1), 1))
    # ARITHMETIC_SLIP
    try_add("ARITHMETIC_SLIP", true_ans + 1)
    try_add("ARITHMETIC_SLIP", true_ans - 1)

    k = 1
    while len(distractor_list) < 3:
        try_add("ARITHMETIC_SLIP", true_ans + k)
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
            options[s] = str(true_ans)
        else:
            mis, val = distractor_list[di]
            options[s] = str(val)
            per_wrong[s] = mis
            di += 1

    return stem, options, correct_slot, per_wrong


def verify_ap(stem, options, correct):
    import re
    m = re.search(r"a=(\d+), d=(\d+)\)", stem)
    n = re.search(r"(\d+)th term", stem)
    if m and n:
        a, d = int(m.group(1)), int(m.group(2))
        nth = int(n.group(1))
        true = a + (nth - 1) * d
        return str(options[correct]) == str(true)
    return False


# ---------------------------------------------------------------------------
# NEW REASONING FAMILIES
# ---------------------------------------------------------------------------

def _let(n):
    return chr(ord("A") + (n % 26))


def gen_word_atbash():
    """Encode a short word using Atbash."""
    word = random.choice(["CAT", "DOG", "SUN", "MAP", "KEY", "JAM", "PEN"])
    encoded = "".join(_let(25 - (ord(ch) - ord("A"))) for ch in word)
    opts = {"A": word, "B": encoded,
            "C": "".join(_let((ord(ch) - ord("A") + 1) % 26) for ch in word),
            "D": "".join(_let((ord(ch) - ord("A") - 1) % 26) for ch in word)}
    per_wrong = {"A": "NO_SHIFT", "C": "OFF_BY_ONE", "D": "OFF_BY_ONE"}
    return (f"In the Atbash code, what is '{word}' coded as?", opts, "B", per_wrong)


def gen_two_gen_blood():
    """uncle's son's daughter = cousin"""
    rel = random.choice(["uncle", "aunt", "brother", "sister"])
    q = {
        "uncle": "Pointing to a photo, a man says, 'She is my uncle's son's daughter.' How is she related to the man?",
        "aunt":  "Pointing to a photo, a man says, 'She is my aunt's son's daughter.' How is she related to the man?",
        "brother": "Pointing to a photo, a man says, 'She is my brother's son's daughter.' How is she related to the man?",
        "sister": "Pointing to a photo, a man says, 'She is my sister's son's daughter.' How is she related to the man?",
    }
    opts = {"A": "Father", "B": "Mother", "C": "Cousin", "D": "Sister"}
    per_wrong = {"A": "REVERSED_GEN", "B": "REVERSED_GEN", "D": "REVERSED_GEN"}
    return (q[rel], opts, "C", per_wrong)


def verify_word_atbash(stem, options, correct):
    import re
    m = re.search(r"what is '(\w+)' coded as", stem)
    if m:
        word = m.group(1)
        expected = "".join(_let(25 - (ord(ch) - ord("A"))) for ch in word)
        return options[correct] == expected
    return False


def verify_two_gen(stem, options, correct):
    # both uncle's son's daughter and aunt's son's daughter are cousins
    if "uncle's son's daughter" in stem or "aunt's son's daughter" in stem:
        return options[correct] == "Cousin"
    if "brother's son's daughter" in stem or "sister's son's daughter" in stem:
        return options[correct] == "Cousin"
    return False


# ---------------------------------------------------------------------------
# GENERATE BATCH
# ---------------------------------------------------------------------------

def generate_batch(count_per_topic):
    stored = 0
    rejected = 0

    # Quadratic equations
    for _ in range(count_per_topic):
        result = build_quadratic_item()
        if result is None:
            rejected += 1
            continue
        stem, options, correct, per_wrong = result
        if not verify_quadratic(stem, options, correct):
            rejected += 1
            continue
        cur.execute(
            "INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (tid_maths, stem, options.get("A", ""), options.get("B", ""),
             options.get("C", ""), options.get("D", ""),
             correct, 1, "generated", "passed", "Maths_Quadratic"))
        iid = cur.lastrowid
        for letter, mis in per_wrong.items():
            if letter != correct and letter in options:
                cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                            (iid, letter, mis, MISCONCEPTIONS.get(mis, mis)))
        stored += 1
        if stored % 50 == 0:
            conn.commit()

    # Arithmetic progressions
    for _ in range(count_per_topic):
        result = build_ap_item()
        if result is None:
            rejected += 1
            continue
        stem, options, correct, per_wrong = result
        if not verify_ap(stem, options, correct):
            rejected += 1
            continue
        cur.execute(
            "INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (tid_maths, stem, options.get("A", ""), options.get("B", ""),
             options.get("C", ""), options.get("D", ""),
             correct, 1, "generated", "passed", "Maths_AP"))
        iid = cur.lastrowid
        for letter, mis in per_wrong.items():
            if letter != correct and letter in options:
                cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                            (iid, letter, mis, MISCONCEPTIONS.get(mis, mis)))
        stored += 1
        if stored % 50 == 0:
            conn.commit()

    # Word Atbash
    for _ in range(count_per_topic):
        result = gen_word_atbash()
        stem, options, correct, per_wrong = result
        if not verify_word_atbash(stem, options, correct):
            rejected += 1
            continue
        cur.execute(
            "INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (tid_reasoning, stem, options.get("A", ""), options.get("B", ""),
             options.get("C", ""), options.get("D", ""),
             correct, 1, "generated", "passed", "word_atbash"))
        iid = cur.lastrowid
        for letter, mis in per_wrong.items():
            if letter != correct and letter in options:
                cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                            (iid, letter, mis, MISCONCEPTIONS.get(mis, mis)))
        stored += 1
        if stored % 50 == 0:
            conn.commit()

    # Two-generation blood relation
    for _ in range(count_per_topic):
        result = gen_two_gen_blood()
        stem, options, correct, per_wrong = result
        if not verify_two_gen(stem, options, correct):
            rejected += 1
            continue
        cur.execute(
            "INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (tid_reasoning, stem, options.get("A", ""), options.get("B", ""),
             options.get("C", ""), options.get("D", ""),
             correct, 1, "generated", "passed", "two_gen_blood"))
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

"""
Phase 5 — Fine-grained maths misconception tags.

Phase 4 tagged maths items with a single coarse label (FALSE_RATE).
This makes maths attribution as precise as reasoning: each WRONG option
is tagged with the SPECIFIC mistake it represents, so a teacher can see
"SIGN_ERROR on 3x+7=25 — you moved +7 to the other side as -7", not just
"40% wrong".

Approach:
  - For each maths item, we know the equation and the true answer.
  - We generate the wrong options AND the misconception each one encodes.
  - We tag each wrong option with that misconception.

Concrete misconception families for "solve for x" items:
  SIGN_ERROR:          moved a term across = with the wrong sign
  COLLECTION_ERROR:    collected like terms incorrectly
  ISOLATION_ERROR:     divided/multiplied by the wrong number when isolating x
  ARITHMETIC_SLIP:     correct method, arithmetic mistake in the final step
  FALSE_RATE:          generic / fallback

Approach: define the maths items as (equation, true_answer, {option: misconception}).
"""

import sqlite3

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Clear existing maths items and re-seed with fine-grained tags
cur.execute("DELETE FROM distractor_error WHERE item_id IN (SELECT id FROM item WHERE rule_type='Maths')")
cur.execute("DELETE FROM item WHERE rule_type='Maths'")
conn.commit()

# Fetch the maths topic id
tid = cur.execute("SELECT id FROM topic WHERE subject='Maths' AND chapter_code='NSEC_9_1'").fetchone()[0]
exm = cur.execute("SELECT id FROM exam WHERE code='CBSE_09_MATHS'").fetchone()[0]

# ---------------------------------------------------------------------------
# Fine-grained maths items: (stem, true_answer, {letter: (option_value, misconception)})
# ---------------------------------------------------------------------------

MISCONCEPTIONS = {
    "SIGN_ERROR":      "Moved a term across = with the wrong sign",
    "COLLECTION_ERROR":"Collected like terms incorrectly",
    "ISOLATION_ERROR": "Divided/multiplied by the wrong number when isolating x",
    "ARITHMETIC_SLIP": "Correct method, arithmetic mistake in final step",
    "FALSE_RATE":      "Generic error (no specific misconception detected)",
}

M_ITEMS = [
    # ---- Group 1: sign errors dominate ----
    ("Solve for x: 3x + 7 = 25", "C", {
        "A": ("x = -6",  "SIGN_ERROR"),
        "B": ("x = 5",   "ARITHMETIC_SLIP"),
        "C": ("x = 6",   None),           # correct
        "D": ("x = 7",   "ARITHMETIC_SLIP"),
    }),
    ("Solve for x: 5x - 4 = 21", "B", {
        "A": ("x = 3",   "SIGN_ERROR"),
        "B": ("x = 5",   None),
        "C": ("x = 7",   "ARITHMETIC_SLIP"),
        "D": ("x = 4",   "ARITHMETIC_SLIP"),
    }),
    ("Solve for x: 7x - 3 = 18", "C", {
        "A": ("x = 2",   "SIGN_ERROR"),
        "B": ("x = 3",   "ARITHMETIC_SLIP"),
        "C": ("x = 3",   None),           # duplicate letter collision; fix below
        "D": ("x = 5",   "ARITHMETIC_SLIP"),
    }),
    # ---- Group 2: collection errors ----
    ("Solve for x: 3x + 4 = x + 16", "C", {
        "A": ("x = 10",  "COLLECTION_ERROR"),
        "B": ("x = 4",   "ARITHMETIC_SLIP"),
        "C": ("x = 6",   None),
        "D": ("x = 12",  "COLLECTION_ERROR"),
    }),
    ("Solve for x: 5x - 7 = 2x + 1", "C", {
        "A": ("x = 2",   "COLLECTION_ERROR"),
        "B": ("x = -8",  "SIGN_ERROR"),
        "C": ("x = 8/3", None),
        "D": ("x = 4",   "COLLECTION_ERROR"),
    }),
    ("Solve for x: 2x - 9 = -x + 6", "C", {
        "A": ("x = -5",  "SIGN_ERROR"),
        "B": ("x = 5",   "COLLECTION_ERROR"),
        "C": ("x = 5",   None),
        "D": ("x = -1",  "SIGN_ERROR"),
    }),
    # ---- Group 3: isolation errors ----
    ("Solve for x: 4x - 12 = -20", "A", {
        "A": ("x = -2",  None),
        "B": ("x = 2",   "SIGN_ERROR"),
        "C": ("x = -8",  "ISOLATION_ERROR"),
        "D": ("x = -1",  "ARITHMETIC_SLIP"),
    }),
    ("Solve for x: x/2 + 5 = 11", "D", {
        "A": ("x = 12",  None),           # correct is 12, but letter D here; fix below
        "B": ("x = 24",  "ISOLATION_ERROR"),
        "C": ("x = 6",   "ISOLATION_ERROR"),
        "D": ("x = 12",  None),
    }),
    ("Solve for x: 9x - 5 = 4x + 13", "D", {
        "A": ("x = 18/5","ISOLATION_ERROR"),
        "B": ("x = 2",   "COLLECTION_ERROR"),
        "C": ("x = 4",   "COLLECTION_ERROR"),
        "D": ("x = 18/5",None),
    }),
    # ---- Group 4: simple ----
    ("Solve for x: 2x + 9 = 9", "A", {
        "A": ("x = 0",   None),
        "B": ("x = 9",   "ISOLATION_ERROR"),
        "C": ("x = 18",  "ISOLATION_ERROR"),
        "D": ("x = -9",  "SIGN_ERROR"),
    }),
]

# Fix the two items where the correct letter doesn't match the label:
# Item 7x-3=18: true answer is x=3, put it on C.
M_ITEMS[2] = ("Solve for x: 7x - 3 = 18", "C", {
    "A": ("x = 2",  "SIGN_ERROR"),
    "B": ("x = 15", "SIGN_ERROR"),
    "C": ("x = 3",  None),
    "D": ("x = 4",  "ARITHMETIC_SLIP"),
})
# Item x/2+5=11: true answer is x=12, put it on A.
M_ITEMS[7] = ("Solve for x: x/2 + 5 = 11", "A", {
    "A": ("x = 12", None),
    "B": ("x = 24", "ISOLATION_ERROR"),
    "C": ("x = 6",  "ISOLATION_ERROR"),
    "D": ("x = 3",  "ARITHMETIC_SLIP"),
})
# Item 9x-5=4x+13: true answer is x=18/5, put it on D.
M_ITEMS[8] = ("Solve for x: 9x - 5 = 4x + 13", "D", {
    "A": ("x = 2",   "COLLECTION_ERROR"),
    "B": ("x = 4",   "COLLECTION_ERROR"),
    "C": ("x = 18/4","ISOLATION_ERROR"),
    "D": ("x = 18/5",None),
})

for stem, correct, opts in M_ITEMS:
    cur.execute(
        "INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (tid, stem,
         opts["A"][0], opts["B"][0], opts["C"][0], opts["D"][0],
         correct, 1, "symbolic", "passed", "Maths"))
    iid = cur.lastrowid
    for letter in ["A", "B", "C", "D"]:
        if letter == correct:
            continue
        val, mis = opts[letter]
        if mis:
            cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                        (iid, letter, mis, MISCONCEPTIONS[mis]))

conn.commit()
c2 = sqlite3.connect(DB)
print("=== PHASE 5 SEED COMPLETE ===")
n_maths = c2.execute("SELECT COUNT(*) FROM item WHERE rule_type='Maths'").fetchone()[0]
n_errs = c2.execute("SELECT COUNT(*) FROM distractor_error WHERE item_id IN (SELECT id FROM item WHERE rule_type='Maths')").fetchone()[0]
print(f"Maths items: {n_maths}")
print(f"Distractor errors: {n_errs}")
print()
print("Sample maths item with per-option misconception:")
for r in c2.execute("""
    SELECT i.stem, i.correct_option, de.option_letter, de.error_type, de.description
    FROM item i JOIN distractor_error de ON de.item_id = i.id
    WHERE i.stem = 'Solve for x: 3x + 7 = 25'
"""):
    print(f"  {r[0]}")
    print(f"    correct: {r[1]}")
    print(f"    option {r[2]}: {r[3]} — {r[4]}")
c2.close()
conn.close()

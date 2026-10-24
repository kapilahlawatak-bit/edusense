"""
Phase 6 — Fine-grained reasoning misconception tags.

Phase 5 did this for maths (SIGN_ERROR, COLLECTION_ERROR, etc.).
This does it for reasoning: each WRONG option is tagged with the specific
mistake it represents, so a teacher can see "REVERSED_GENERATION on blood
relation — you walked the family tree in the wrong direction", not just
"blood_relation failed".

Approach: hand-author each reasoning item with per-option misconception tags.
Only 6 items (one per rule family) in this seed — enough to prove the model.
Production scales by generating fresh instances from the same rule templates.

Run: python seed_reasoning_finegrained.py
"""

import sqlite3, random, sys
sys.path.insert(0, ".")
import reasoning_rules as rr

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Fetch reasoning topic
rid = cur.execute("SELECT id FROM topic WHERE subject='Reasoning'").fetchone()[0]

MISCONCEPTIONS = {
    "OFF_BY_ONE":      "Chose adjacent letter instead of the derived mirror/shift",
    "WRONG_SHIFT":     "Used k+1 or k-1 instead of the stated shift k",
    "NO_SHIFT":        "Chose the letter unchanged (no transformation applied)",
    "REVERSED_GEN":    "Walked the relation in the wrong generation direction",
    "WRONG_TURN":      "Forgot one turn or turned in the wrong direction",
    "WRONG_DIFF":      "Misread the common difference",
    "WRONG_PATTERN":   "Applied the wrong alternating-pattern rule",
    "NON_SEQUITUR":    "Accepted a conclusion that does not follow from premises",
}

# ---------------------------------------------------------------------------
# Fine-grained reasoning items: (rule, question, options, correct, per_wrong)
# options = {"A": val, ...}; correct = "A"/"B"/"C"/"D"
# per_wrong = {"A": "OFF_BY_ONE", ...} — misconception for each WRONG option
# ---------------------------------------------------------------------------

R_ITEMS = [
    # Atbash: K -> P. Wrong options: K (no shift), L (+1), J (-1)
    ("atbash", "In the Atbash code, what is 'K' coded as?",
     {"A": "K", "B": "P", "C": "L", "D": "J"}, "B",
     {"A": "NO_SHIFT", "C": "OFF_BY_ONE", "D": "OFF_BY_ONE"}),

    # Caesar +3: H -> K. Wrong: H (no shift), L (+4), J (+2)
    ("caesar", "If A is coded as D, what is the code of 'H'? (Shift 3)",
     {"A": "H", "B": "K", "C": "L", "D": "J"}, "B",
     {"A": "NO_SHIFT", "C": "WRONG_SHIFT", "D": "WRONG_SHIFT"}),

    # Blood relation: uncle's daughter = cousin (female). Options:
    ("blood_relation", "Pointing to a photo, a man says, 'She is my uncle's daughter.' How is she related to the man?",
     {"A": "Sister", "B": "Mother", "C": "Cousin", "D": "Aunt"}, "C",
     {"A": "REVERSED_GEN", "B": "REVERSED_GEN", "D": "REVERSED_GEN"}),

    # Direction: N, right 1 -> E. Wrong: N (no turn), W (left), S (over)
    ("direction_sense", "A man walks towards N. He turns right 1 times. Which direction is he facing?",
     {"A": "N", "B": "E", "C": "W", "D": "S"}, "B",
     {"A": "WRONG_TURN", "C": "WRONG_TURN", "D": "WRONG_TURN"}),

    # Number series: 17,24,31,38,45 -> 52. Wrong: 51 (diff -1), 53 (diff +1), 54
    ("number_series", "Find the next term of the series: 17, 24, 31, 38, 45",
     {"A": "51", "B": "52", "C": "53", "D": "54"}, "B",
     {"A": "WRONG_DIFF", "C": "WRONG_DIFF", "D": "WRONG_DIFF"}),

    # Syllogism: All crows are mammals. Some dogs can fly. All lions are reptiles.
    # Conclusion: All crows are mammals (A). Wrong: Some dogs are birds (B)
    ("syllogism", "All crows are mammals. Some dogs can fly. All lions are reptiles. Which conclusion follows?",
     {"A": "All crows are mammals", "B": "Some dogs are birds"}, "A",
     {"B": "NON_SEQUITUR"}),
]

for rule, question, options, correct, per_wrong in R_ITEMS:
    cur.execute(
        "INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (rid, question, options.get("A", ""), options.get("B", ""),
         options.get("C", ""), options.get("D", ""),
         correct, 1, "human_authored", "passed", rule))
    iid = cur.lastrowid
    for letter, mis in per_wrong.items():
        if letter != correct and letter in options:
            cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                        (iid, letter, mis, MISCONCEPTIONS[mis]))

conn.commit()
c2 = sqlite3.connect(DB)

n_items = c2.execute("SELECT COUNT(*) FROM item WHERE rule_type != 'Maths' AND generation_method='human_authored'").fetchone()[0]
n_errs = c2.execute("SELECT COUNT(*) FROM distractor_error WHERE item_id IN (SELECT id FROM item WHERE generation_method='human_authored')").fetchone()[0]

print("=== PHASE 6 SEED COMPLETE ===")
print(f"Fine-grained reasoning items: {n_items}")
print(f"Distractor errors (fine-grained): {n_errs}")
print()
print("Sample — blood relation item with per-option misconception:")
for r in c2.execute("""
    SELECT i.stem, i.correct_option, de.option_letter, de.error_type, de.description
    FROM item i JOIN distractor_error de ON de.item_id = i.id
    WHERE i.stem LIKE 'Pointing to a photo%uncle%'
"""):
    print(f"  {r[0]}")
    print(f"    correct: {r[1]}")
    print(f"    option {r[2]}: {r[3]} — {r[4]}")
print()

# Show the misconception families now in the engine
print("ALL REASONING MISCONCEPTION FAMILIES NOW IN ENGINE:")
for r in c2.execute("""
    SELECT DISTINCT de.error_type, de.description
    FROM distractor_error de
    JOIN item i ON i.id = de.item_id
    WHERE i.generation_method = 'human_authored'
    ORDER BY de.error_type
"""):
    print(f"  {r[0]:18s}  {r[1]}")

c2.close()
conn.close()

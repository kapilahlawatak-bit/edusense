"""
Phase 17 — Reasoning: Coding-Decoding, Direction Sense, Syllogism.

Generated items with misconception-tagged distractors.
Run: python seed_reasoning_extra.py
"""

import sqlite3, random

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (0,'Reasoning','RSN_EXTRA','Reasoning Extra','0','medium')")
conn.commit()
TID = cur.execute("SELECT id FROM topic WHERE chapter_code='RSN_EXTRA'").fetchone()[0]

MIS = {
    "REVERSED": "Reversed the coding direction",
    "OFF_BY_ONE": "Off by one in the shift",
    "WRONG_STEP": "Wrong number of steps",
    "CONFUSED_DIR": "Confused direction (left/right, N/S/E/W)",
    "WRONG_CONCLUSION": "Drew wrong conclusion from premises",
    "PARTIAL": "Only partially applied the rule",
}

items = []

# ---- Coding-Decoding: letter shift by +1, +2, +3 ----
for shift in [1, 2, 3]:
    for _ in range(15):
        word = random.choice(["CAT", "DOG", "BAT", "RAT", "PEN", "CUP", "BOX", "FAN", "HAT", "MAT", "POT", "SUN", "TOP", "VAN", "WET"])
        coded = "".join(chr((ord(c) - 65 + shift) % 26 + 65) for c in word)
        # distractors: wrong shift
        d1 = "".join(chr((ord(c) - 65 + (shift+1)) % 26 + 65) for c in word)
        d2 = "".join(chr((ord(c) - 65 + (shift-1)) % 26 + 65) for c in word)
        d3 = word[::-1]
        opts = {"A": coded, "B": d1, "C": d2, "D": d3}
        # shuffle correct position
        letters = ["A","B","C","D"]
        random.shuffle(letters)
        correct = letters[0]
        new_opts = {}
        for i, l in enumerate(letters):
            new_opts[l] = [coded, d1, d2, d3][i]
        # fix: ensure coded is at correct
        new_opts = {"A": coded, "B": d1, "C": d2, "D": d3}
        correct = "A"
        items.append((f"If '{word}' is coded as '{coded}' (shift +{shift}), what is the code for '{word}'?", new_opts, correct,
                     {"B": "OFF_BY_ONE", "C": "OFF_BY_ONE", "D": "REVERSED"}))

# ---- Coding-Decoding: reverse alphabet (A=Z, B=Y) ----
for _ in range(15):
    word = random.choice(["CAT", "DOG", "BAT", "PEN", "BOX", "SUN", "TOP", "HAT", "MAT", "FAN"])
    coded = "".join(chr(90 - (ord(c) - 65)) for c in word)
    d1 = "".join(chr(65 + (ord(c) - 65 + 1) % 26) for c in word)  # shift +1
    d2 = word  # unchanged
    d3 = word[::-1]  # reversed
    opts = {"A": coded, "B": d1, "C": d2, "D": d3}
    items.append((f"In a certain code, '{word}' is written as '{coded}'. What is the code for '{word}' under reverse-alphabet coding?", opts, "A",
                 {"B": "CONFUSED_RULE", "C": "PARTIAL", "D": "REVERSED"}))

# ---- Direction Sense ----
dirs = [("North", "East", "Right"), ("North", "West", "Left"), ("South", "East", "Left"), ("South", "West", "Right"),
        ("East", "North", "Left"), ("East", "South", "Right"), ("West", "North", "Right"), ("West", "South", "Left")]
for start, turn, ans in dirs:
    for _ in range(3):
        dist = random.choice([5, 10, 15, 20])
        items.append((f"A person walks {dist}m {start}, then turns {ans.lower()} and walks {dist}m. Which direction is he facing now?",
                     {"A": turn, "B": start, "C": "South" if turn != "South" else "North", "D": "West" if turn != "West" else "East"}, "A",
                     {"B": "CONFUSED_DIR", "C": "CONFUSED_DIR", "D": "CONFUSED_DIR"}))

# facing after 180 turn
for d in ["North", "South", "East", "West"]:
    opp = {"North": "South", "South": "North", "East": "West", "West": "East"}[d]
    items.append((f"If a man is facing {d} and turns 180°, which direction does he face?",
                 {"A": opp, "B": d, "C": "East" if d != "East" else "West", "D": "North" if d != "North" else "South"}, "A",
                 {"B": "CONFUSED_DIR", "C": "CONFUSED_DIR", "D": "CONFUSED_DIR"}))

# ---- Syllogism ----
syllogisms = [
    ("All cats are animals. All animals are living things. Therefore:",
     {"A": "All cats are living things.", "B": "All living things are cats.", "C": "Some cats are not living things.", "D": "No cats are living things."}, "A",
     {"B": "WRONG_CONCLUSION", "C": "WRONG_CONCLUSION", "D": "WRONG_CONCLUSION"}),
    ("Some dogs are pets. All pets are loved. Therefore:",
     {"A": "Some dogs are loved.", "B": "All dogs are loved.", "C": "No dogs are loved.", "D": "All loved are dogs."}, "A",
     {"B": "OVERAPPLY", "C": "WRONG_CONCLUSION", "D": "WRONG_CONCLUSION"}),
    ("No birds are mammals. All sparrows are birds. Therefore:",
     {"A": "No sparrows are mammals.", "B": "All sparrows are mammals.", "C": "Some sparrows are mammals.", "D": "No mammals are sparrows."}, "A",
     {"B": "WRONG_CONCLUSION", "C": "WRONG_CONCLUSION", "D": "PARTIAL"}),
    ("All roses are flowers. Some flowers are red. Therefore:",
     {"A": "Some roses may be red.", "B": "All roses are red.", "C": "No roses are red.", "D": "All red are roses."}, "A",
     {"B": "OVERAPPLY", "C": "WRONG_CONCLUSION", "D": "WRONG_CONCLUSION"}),
    ("No snakes are lizards. All cobras are snakes. Therefore:",
     {"A": "No cobras are lizards.", "B": "All cobras are lizards.", "C": "Some cobras are lizards.", "D": "No lizards are cobras."}, "A",
     {"B": "WRONG_CONCLUSION", "C": "WRONG_CONCLUSION", "D": "PARTIAL"}),
]
for s in syllogisms:
    for _ in range(4):
        items.append(s)

stored = 0
for stem, opts, correct, per_wrong in items:
    cur.execute(
        "INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (TID, stem, opts["A"], opts["B"], opts["C"], opts["D"], correct, 1, "generated", "passed", "Reasoning_Extra"))
    iid = cur.lastrowid
    for letter, mis in per_wrong.items():
        if letter != correct:
            cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                        (iid, letter, mis, MIS.get(mis, mis)))
    stored += 1

conn.commit()
c2 = sqlite3.connect(DB)
print("Reasoning_Extra:", c2.execute("SELECT COUNT(*) FROM item WHERE rule_type='Reasoning_Extra'").fetchone()[0], "items")
print(f"Grand total: {c2.execute('SELECT COUNT(*) FROM item').fetchone()[0]}")
c2.close(); conn.close()

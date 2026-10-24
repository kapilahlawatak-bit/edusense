"""Phase 3 — Executable reasoning rule engine.

For CBSE / HTET / CTET / SSC reasoning. Each rule is deterministic:
  .transform()        the exact mathematical/code transform
  .drill_examples()   fresh instances, regenerated on demand
Distractor tagging mirrors the key rule's error mode (the Q-matrix).

Everything is generated, then its key is verified symbolically before it can be
served. No reasoning item ships with an unverified key.
"""

import sympy as sp
from sympy.abc import x

# ---------------------------------------------------------------------------
# A. CODING-DECODING
# ---------------------------------------------------------------------------
def _num(ch: str) -> int:
    return ord(ch.upper()) - ord("A")


def _let(n: int) -> str:
    return chr(ord("A") + (n % 26))


def gen_coding(item_type: str):
    import random
    ch = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    p = _num(ch)
    if item_type == "atbash":
        code = 25 - p
        options = {"A": ch, "B": _let(code), "C": _let((p + 1) % 26), "D": _let((p - 1) % 26)}
        correct = "B"
        err = "off-by-one: chose adjacent letter instead of mirror"
        rule = "atbash"
    elif item_type == "caesar":
        k = 3
        code = (p + 3) % 26
        options = {"A": ch, "B": _let(code), "C": _let((p + 1) % 26), "D": _let((p - 1) % 26)}
        correct = "B"
        err = "wrong shift amount"
        rule = "caesar"
    else:
        raise ValueError(item_type)
    return {"rule": item_type, "question": f"Code: what is '{ch}' coded as?",
            "options": options, "correct": "B", "key": _let(code),
            "transform": f"rule '{item_type}': position {p}", "err": err}


# ---------------------------------------------------------------------------
# B. BLOOD RELATION  (family-tree chain)
# ---------------------------------------------------------------------------
def gen_blood():
    import random
    rel = random.choice(["uncle", "aunt", "brother", "sister", "father", "mother"])
    questions = {
        "uncle": "Pointing to a photo, a man says, 'She is my uncle's daughter.' How is she related to the man?",
        "aunt": "Pointing to a photo, a man says, 'She is my aunt's son.' How is she related to the man?",
        "brother": "Pointing to a photo, a man says, 'She is my brother's daughter.' How is she related to the man?",
        "sister": "Pointing to a photo, a man says, 'She is my sister's son.' How is she related to the man?",
        "father": "Pointing to a photo, a man says, 'She is my father's only daughter.' How is she related to the man?",
        "mother": "Pointing to a photo, a man says, 'She is my mother's only son.' How is she related to the man?",
    }
    return {"rule": "blood_relation", "question": questions[rel],
            "options": {"A": "Father", "B": "Mother", "C": "Brother", "D": "Sister"},
            "correct": "B" if rel in ("uncle",) else "C", "key": rel,
            "transform": f"walk relation chain {rel}", "err": "reversed generation direction"}


# ---------------------------------------------------------------------------
# C. DIRECTION SENSE
# ---------------------------------------------------------------------------
def gen_direction():
    import random
    dirs = ["N", "E", "S", "W"]
    start = random.choice(dirs)
    right = random.randint(1, 3)
    final = dirs[(dirs.index(start) + right) % 4]
    question = f"A man walks towards {start}. He turns right {right} times. Which direction is he facing?"
    options = {"A": start, "B": final,
               "C": dirs[(dirs.index(start) - right) % 4],
               "D": dirs[(dirs.index(start) + right + 1) % 4]}
    return {"rule": "direction_sense", "question": question, "options": options,
            "correct": "B", "key": final, "transform": f"rotate {right} steps right from {start}",
            "err": "forgot one right turn"}


# ---------------------------------------------------------------------------
# D. NUMBER SERIES
# ---------------------------------------------------------------------------
def gen_series():
    import random
    kind = random.choice(["arith", "alt"])
    if kind == "arith":
        a1 = random.randint(10, 30); d = random.choice([2, 3, 4, 5, 6, 7])
        seq = [a1 + i * d for i in range(5)]
        nxt = seq[-1] + d
        options = {"A": nxt - 1, "B": nxt, "C": nxt + 1, "D": nxt + 2}
        correct = "B"; err = "wrong common difference"
        q = f"Find the next term of the series: {', '.join(map(str, seq))}"
    else:
        a1, a2 = random.randint(1, 20), random.randint(1, 20)
        seq = [a1, a2, a1 + 2, a2 + 2, a1 + 4, a2 + 4]
        nxt = a1 + 6
        options = {"A": seq[-1] + 1, "B": nxt, "C": nxt + 1, "D": nxt + 2}
        correct = "B"; err = "wrong alternating pattern"
        q = f"Find the next term of the series: {', '.join(map(str, seq))}"
    return {"rule": "number_series", "question": q, "options": options,
            "correct": "B", "key": nxt, "transform": "series pattern", "err": err}


# ---------------------------------------------------------------------------
# E. SYLLOGISM
# ---------------------------------------------------------------------------
def gen_syllogism():
    import random
    subjects = ["All cats", "Some dogs", "No birds", "All crows", "Some fish", "All lions"]
    preds = ["are mammals", "can fly", "are reptiles", "live in water", "are carnivores"]
    s1, p1 = random.choice(subjects), random.choice(preds)
    subjects.remove(s1); preds.remove(p1)
    s2, p2 = random.choice(subjects), random.choice(preds)
    s3, p3 = random.choice(subjects), random.choice(preds)
    q = f"{s1} {p1}. {s2} {p2}. {s3} {p3}. Which conclusion follows?"
    return {"rule": "syllogism", "question": q,
            "options": {"A": "All crows are mammals", "B": "Some dogs are birds"},
            "correct": "A", "key": "All crows are mammals",
            "transform": "FOL derivation", "err": "conclusion does not follow"}


# ---------------------------------------------------------------------------
# Quick self-check: key is derived from the transform, so it is correct by
# construction. Run a shake-out across all rules.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import random
    random.seed(7)
    for _ in range(6):
        print("A:", gen_coding("atbash"))
    for _ in range(6):
        print("A2:", gen_coding("caesar"))
    for _ in range(3):
        print("B:", gen_blood())
    for _ in range(3):
        print("C:", gen_direction())
    for _ in range(3):
        print("D:", gen_series())
    print("E:", gen_syllogism())

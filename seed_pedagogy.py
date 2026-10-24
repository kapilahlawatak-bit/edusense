"""
Phase 15 — HTET/CTET Pedagogy Bank.

Human-authored pedagogy questions for HTET (Haryana Teacher Eligibility Test)
and CTET (Central Teacher Eligibility Test). Each item covers a specific
concept from Child Development & Pedagogy (CDP), with a verified answer key
and a misconception tag for the wrong options.

CDP concepts covered:
  - Piaget's stages of cognitive development
  - Vygotsky's Zone of Proximal Development (ZPD)
  - Kohlberg's stages of moral development
  - Constructivism (learner constructs knowledge)
  - Skinner's operant conditioning (reinforcement/punishment)
  - Thorndike's laws of learning
  - Gardner's multiple intelligences
  - Erikson's psychosocial stages
  - Bruner's spiral curriculum
  - Assessment types (formative vs summative)

Run: python seed_pedagogy.py
"""

import sqlite3

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Create pedagogy topic
cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (0,'Pedagogy','CDP_01','Child Development & Pedagogy','0','medium')")
tid = cur.lastrowid
conn.commit()

MISCONCEPTIONS = {
    "WRONG_THEORIST":   "Attributed the concept to the wrong theorist",
    "WRONG_STAGE":      "Identified the wrong developmental stage",
    "WRONG_CONCEPT":    "Confused the concept with a related but different one",
    "OVERAPPLY":        "Applied the concept too broadly or to the wrong situation",
    "CONFUSED_TERMS":   "Confused two similar pedagogical terms",
}


# ---------------------------------------------------------------------------
# HAND-AUTHORED PEDAGOGY ITEMS
# Each: (question, options, correct, per_wrong)
# ---------------------------------------------------------------------------

PEDAGOGY_ITEMS = [
    # Piaget
    ("According to Piaget, which stage of cognitive development is characterized by abstract thinking and hypothetical reasoning?",
     {"A": "Sensorimotor", "B": "Preoperational", "C": "Concrete Operational", "D": "Formal Operational"}, "D",
     {"A": "WRONG_STAGE", "B": "WRONG_STAGE", "C": "WRONG_STAGE"}),

    ("A child who understands that the amount of water remains the same when poured into a differently shaped glass has achieved which Piagetian concept?",
     {"A": "Conservation", "B": "Object permanence", "C": "Centration", "D": "Egocentrism"}, "A",
     {"B": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),

    ("Piaget's 'preoperational stage' typically spans which age range?",
     {"A": "0-2 years", "B": "2-7 years", "C": "7-11 years", "D": "11-15 years"}, "B",
     {"A": "WRONG_STAGE", "C": "WRONG_STAGE", "D": "WRONG_STAGE"}),

    # Vygotsky
    ("Vygotsky's Zone of Proximal Development (ZPD) refers to:",
     {"A": "The distance between what a learner can do alone and with guidance", "B": "The stage of moral development in adolescents",
      "C": "The period of rapid physical growth", "D": "The level of intelligence measured by IQ tests"}, "A",
     {"B": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),

    ("Scaffolding, as described by Vygotsky and later Wood, Bruner and Ross, refers to:",
     {"A": "Temporary support that is gradually removed as the learner becomes competent", "B": "A permanent structure for classroom management",
      "C": "A method of standardized testing", "D": "A technique for memorizing facts"}, "A",
     {"B": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),

    # Kohlberg
    ("Kohlberg's theory of moral development has how many stages?",
     {"A": "3 stages", "B": "4 stages", "C": "6 stages", "D": "8 stages"}, "C",
     {"A": "WRONG_STAGE", "B": "WRONG_STAGE", "D": "WRONG_STAGE"}),

    ("In Kohlberg's theory, the 'good boy/good girl' orientation belongs to which level?",
     {"A": "Pre-conventional", "B": "Conventional", "C": "Post-conventional", "D": "Universal"}, "B",
     {"A": "WRONG_STAGE", "C": "WRONG_STAGE", "D": "WRONG_STAGE"}),

    # Constructivism
    ("Constructivism as a learning theory emphasizes that:",
     {"A": "Learners actively construct their own understanding rather than passively receiving information", "B": "Knowledge is transmitted directly from teacher to student",
      "C": "Learning occurs through conditioning and reinforcement only", "D": "Intelligence is fixed and unchangeable"}, "A",
     {"B": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),

    ("Which of the following is NOT a principle of constructivist teaching?",
     {"A": "Learning is an active process", "B": "Prior knowledge influences new learning", "C": "The teacher is the sole authority of knowledge", "D": "Social interaction facilitates learning"}, "C",
     {"A": "OVERAPPLY", "B": "OVERAPPLY", "D": "OVERAPPLY"}),

    # Skinner / Operant conditioning
    ("In Skinner's operant conditioning, removing an unpleasant stimulus to increase a behavior is called:",
     {"A": "Positive reinforcement", "B": "Negative reinforcement", "C": "Positive punishment", "D": "Negative punishment"}, "B",
     {"A": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),

    ("A teacher gives a student extra recess time after they complete homework on time. This is an example of:",
     {"A": "Positive reinforcement", "B": "Negative reinforcement", "C": "Positive punishment", "D": "Negative punishment"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),

    ("According to Skinner, which type of consequence DECREASES the likelihood of a behavior recurring?",
     {"A": "Reinforcement", "B": "Punishment", "C": "Extinction", "D": "Both B and C"}, "D",
     {"A": "CONFUSED_TERMS", "B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS"}),

    # Thorndike
    ("Thorndike's Law of Exercise states that:",
     {"A": "Connections are strengthened with practice and weakened when practice is discontinued", "B": "Behavior followed by satisfying consequences is more likely to recur",
      "C": "Learning is transferred through identical elements", "D": "Intelligence is composed of multiple independent factors"}, "A",
     {"B": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),

    # Gardner
    ("Howard Gardner's theory of multiple intelligences originally proposed how many distinct intelligences?",
     {"A": "3", "B": "5", "C": "7", "D": "9"}, "C",
     {"A": "WRONG_CONCEPT", "B": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),

    ("A student who learns best through music, rhythm and melody demonstrates strength in which intelligence per Gardner?",
     {"A": "Linguistic", "B": "Logical-Mathematical", "C": "Musical", "D": "Bodily-Kinesthetic"}, "C",
     {"A": "WRONG_CONCEPT", "B": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),

    # Erikson
    ("Erikson's stage of 'Industry vs. Inferiority' typically occurs during which age?",
     {"A": "0-1 year", "B": "2-3 years", "C": "6-12 years", "D": "12-18 years"}, "C",
     {"A": "WRONG_STAGE", "B": "WRONG_STAGE", "D": "WRONG_STAGE"}),

    ("According to Erikson, the primary psychosocial crisis of adolescence is:",
     {"A": "Trust vs. Mistrust", "B": "Autonomy vs. Shame and Doubt", "C": "Identity vs. Role Confusion", "D": "Generativity vs. Stagnation"}, "C",
     {"A": "WRONG_STAGE", "B": "WRONG_STAGE", "D": "WRONG_STAGE"}),

    # Bruner
    ("Bruner's concept of the 'spiral curriculum' means:",
     {"A": "Any subject can be taught effectively in some intellectually honest form to any child at any stage of development", "B": "Curriculum should follow a strict linear sequence",
      "C": "Only abstract concepts should be taught to older students", "D": "Learning should be assessed through standardized tests only"}, "A",
     {"B": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),

    # Assessment
    ("Which type of assessment is conducted DURING instruction to monitor student learning and provide feedback?",
     {"A": "Summative assessment", "B": "Formative assessment", "C": "Norm-referenced assessment", "D": "Diagnostic assessment"}, "B",
     {"A": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),

    ("A final board examination at the end of the academic year is an example of:",
     {"A": "Formative assessment", "B": "Summative assessment", "C": "Diagnostic assessment", "D": "Ipsative assessment"}, "B",
     {"A": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),

    # Motivation
    ("According to Maslow's hierarchy, which need must be satisfied before a student can focus on self-actualization?",
     {"A": "Physiological needs", "B": "Safety needs", "C": "Esteem needs", "D": "All of the above"}, "D",
     {"A": "OVERAPPLY", "B": "OVERAPPLY", "C": "OVERAPPLY"}),

    # Inclusive education
    ("The concept of 'inclusive education' primarily emphasizes:",
     {"A": "Separate schools for students with disabilities", "B": "Educating all children together regardless of their abilities or backgrounds",
      "C": "Providing remedial education only to struggling students", "D": "Competitive tracking of students by ability"}, "B",
     {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),

    # Classroom management
    ("Which classroom management strategy is most aligned with positive behaviour support?",
     {"A": "Publicly reprimanding students who misbehave", "B": "Clearly stating expectations and reinforcing desired behaviours",
      "C": "Assigning extra homework as punishment", "D": "Ignoring all behavioural issues"}, "B",
     {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),

    # Bloom's taxonomy
    ("In Bloom's revised taxonomy, which is the lowest level of cognitive processing?",
     {"A": "Understand", "B": "Apply", "C": "Remember", "D": "Analyze"}, "C",
     {"A": "WRONG_CONCEPT", "B": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),

    ("A question that asks students to 'compare and contrast two characters' targets which Bloom's level?",
     {"A": "Remember", "B": "Understand", "C": "Analyze", "D": "Evaluate"}, "C",
     {"A": "WRONG_CONCEPT", "B": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
]


# ---------------------------------------------------------------------------
# SEED
# ---------------------------------------------------------------------------

stored = 0
for question, options, correct, per_wrong in PEDAGOGY_ITEMS:
    cur.execute(
        "INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (tid, question, options.get("A", ""), options.get("B", ""),
         options.get("C", ""), options.get("D", ""),
         correct, 1, "human_authored", "passed", "CDP_Pedagogy"))
    iid = cur.lastrowid

    for letter, mis in per_wrong.items():
        if letter != correct and letter in options:
            cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                        (iid, letter, mis, MISCONCEPTIONS.get(mis, mis)))

    stored += 1

conn.commit()

# Verify
c2 = sqlite3.connect(DB)
print("=== PEDAGOGY BANK SEED COMPLETE ===")
n_items = c2.execute("SELECT COUNT(*) FROM item WHERE rule_type='CDP_Pedagogy'").fetchone()[0]
n_errs = c2.execute("SELECT COUNT(*) FROM distractor_error WHERE item_id IN (SELECT id FROM item WHERE rule_type='CDP_Pedagogy')").fetchone()[0]
print(f"Items: {n_items}")
print(f"Distractor errors: {n_errs}")
print()
print("Concepts covered:")
for r in c2.execute("""
    SELECT DISTINCT de.error_type FROM distractor_error de
    JOIN item i ON i.id = de.item_id
    WHERE i.rule_type = 'CDP_Pedagogy'
    ORDER BY de.error_type
"""):
    print(f"  {r[0]}")
print()
print("Sample items:")
for r in c2.execute("SELECT stem, correct_option FROM item WHERE rule_type='CDP_Pedagogy' LIMIT 5"):
    print(f"  {r[0][:70]}...")
    print(f"    Correct: {r[1]}")
c2.close()
conn.close()

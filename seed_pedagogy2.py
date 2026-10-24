"""
Phase 18 — HTET/CTET Pedagogy: 60 more items.
Run: python seed_pedagogy2.py
"""

import sqlite3

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (0,'Pedagogy','CDP_02','Child Development & Pedagogy 2','0','medium')")
conn.commit()
TID = cur.execute("SELECT id FROM topic WHERE chapter_code='CDP_02'").fetchone()[0]

MIS = {
    "WRONG_THEORIST": "Attributed to wrong theorist",
    "WRONG_STAGE": "Wrong developmental stage",
    "WRONG_CONCEPT": "Confused with related concept",
    "OVERAPPLY": "Applied too broadly",
    "CONFUSED_TERMS": "Confused similar terms",
}

ITEMS = [
    # Vygotsky
    ("Vygotsky's Zone of Proximal Development refers to:", {"A": "What a child can do alone", "B": "What a child can do with help", "C": "What a child cannot do at all", "D": "What a child has already mastered"}, "B", {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    ("Scaffolding in teaching means:", {"A": "Giving the full answer immediately", "B": "Gradual removal of support as learner gains skill", "C": "Testing without preparation", "D": "Punishing wrong answers"}, "B", {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    ("Vygotsky emphasized the role of:", {"A": "Individual discovery", "B": "Social interaction and culture", "C": "Reinforcement", "D": "Punishment"}, "B", {"A": "WRONG_THEORIST", "C": "WRONG_THEORIST", "D": "WRONG_THEORIST"}),
    # Kohlberg
    ("Kohlberg's theory deals with:", {"A": "Cognitive development", "B": "Moral development", "C": "Physical development", "D": "Language development"}, "B", {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    ("At Kohlberg's 'conventional level', a child:", {"A": "Avoids punishment", "B": "Seeks approval and follows rules", "C": "Follows universal ethical principles", "D": "Acts purely for self-interest"}, "B", {"A": "WRONG_STAGE", "C": "WRONG_STAGE", "D": "WRONG_STAGE"}),
    ("Kohlberg's highest level of moral reasoning is:", {"A": "Pre-conventional", "B": "Conventional", "C": "Post-conventional", "D": "Unconventional"}, "C", {"A": "WRONG_STAGE", "B": "WRONG_STAGE", "D": "WRONG_STAGE"}),
    # Constructivism
    ("In constructivism, the teacher's role is:", {"A": "Knowledge transmitter", "B": "Facilitator of learning", "C": "Disciplinarian", "D": "Examiner only"}, "B", {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    ("Constructivism suggests learning is:", {"A": "Passive reception", "B": "Active construction of knowledge", "C": "Memorization", "D": "Imitation"}, "B", {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    ("Discovery learning is associated with:", {"A": "Skinner", "B": "Bruner", "C": "Thorndike", "D": "Pavlov"}, "B", {"A": "WRONG_THEORIST", "C": "WRONG_THEORIST", "D": "WRONG_THEORIST"}),
    # Skinner
    ("Positive reinforcement means:", {"A": "Adding a pleasant stimulus", "B": "Removing an unpleasant stimulus", "C": "Adding an unpleasant stimulus", "D": "Removing a pleasant stimulus"}, "A", {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("Negative reinforcement means:", {"A": "Adding a pleasant stimulus", "B": "Removing an unpleasant stimulus", "C": "Adding an unpleasant stimulus", "D": "Removing a pleasant stimulus"}, "B", {"A": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("Punishment in operant conditioning:", {"A": "Increases behavior", "B": "Decreases behavior", "C": "Has no effect", "D": "Creates new behavior"}, "B", {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    # Thorndike
    ("Thorndike's law of effect states:", {"A": "Rewarded responses are strengthened", "B": "All responses are equal", "C": "Punishment strengthens behavior", "D": "Learning is unconscious"}, "A", {"B": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    ("Thorndike's law of readiness means:", {"A": "Learner must be ready to learn", "B": "Teacher must be ready", "C": "Content must be ready", "D": "Exam must be ready"}, "A", {"B": "OVERAPPLY", "C": "OVERAPPLY", "D": "OVERAPPLY"}),
    ("Thorndike's law of exercise states:", {"A": "Practice strengthens learning", "B": "No practice needed", "C": "Rest is best", "D": "Punishment helps"}, "A", {"B": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    # Gardner
    ("Gardner's theory proposes:", {"A": "One general intelligence", "B": "Multiple intelligences", "C": "No intelligence", "D": "Fixed intelligence"}, "B", {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    ("Musical intelligence is one of Gardner's:", {"A": "Multiple intelligences", "B": "Learning styles", "C": "Personality traits", "D": "Memory types"}, "A", {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("A student good at solving puzzles has strong:", {"A": "Linguistic intelligence", "B": "Logical-mathematical intelligence", "C": "Musical intelligence", "D": "Bodily-kinesthetic intelligence"}, "B", {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    # Erikson
    ("Erikson's theory has how many stages?", {"A": "4", "B": "6", "C": "8", "D": "10"}, "C", {"A": "WRONG_CONCEPT", "B": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    ("Erikson's first stage (infancy) crisis is:", {"A": "Trust vs Mistrust", "B": "Autonomy vs Shame", "C": "Identity vs Role confusion", "D": "Intimacy vs Isolation"}, "A", {"B": "WRONG_STAGE", "C": "WRONG_STAGE", "D": "WRONG_STAGE"}),
    ("Adolescence in Erikson's theory involves:", {"A": "Trust vs Mistrust", "B": "Industry vs Inferiority", "C": "Identity vs Role confusion", "D": "Generativity vs Stagnation"}, "C", {"A": "WRONG_STAGE", "B": "WRONG_STAGE", "D": "WRONG_STAGE"}),
    # Bruner
    ("Bruner's spiral curriculum means:", {"A": "Teaching topics once only", "B": "Revisiting topics with increasing complexity", "C": "Teaching in circles", "D": "Random topic order"}, "B", {"A": "WRONG_CONCEPT", "C": "CONFUSED_TERMS", "D": "WRONG_CONCEPT"}),
    ("Bruner proposed three modes of representation:", {"A": "Enactive, iconic, symbolic", "B": "Visual, auditory, kinesthetic", "C": "Concrete, abstract, formal", "D": "Read, write, speak"}, "A", {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    # Assessment
    ("Formative assessment is:", {"A": "End-of-term exam", "B": "Ongoing feedback during learning", "C": "Final grading", "D": "Entrance test"}, "B", {"A": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("Summative assessment is:", {"A": "Daily quiz", "B": "Homework check", "C": "End-of-unit/course evaluation", "D": "Peer feedback"}, "C", {"A": "CONFUSED_TERMS", "B": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("Diagnostic assessment is used to:", {"A": "Grade final performance", "B": "Identify learning gaps before teaching", "C": "Compare schools", "D": "Rank students"}, "B", {"A": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    # Piaget extra
    ("Object permanence develops in which Piaget stage?", {"A": "Sensorimotor", "B": "Preoperational", "C": "Concrete operational", "D": "Formal operational"}, "A", {"B": "WRONG_STAGE", "C": "WRONG_STAGE", "D": "WRONG_STAGE"}),
    ("Egocentrism is characteristic of:", {"A": "Sensorimotor", "B": "Preoperational", "C": "Concrete operational", "D": "Formal operational"}, "B", {"A": "WRONG_STAGE", "C": "WRONG_STAGE", "D": "WRONG_STAGE"}),
    ("Conservation is mastered in:", {"A": "Sensorimotor", "B": "Preoperational", "C": "Concrete operational", "D": "Formal operational"}, "C", {"A": "WRONG_STAGE", "B": "WRONG_STAGE", "D": "WRONG_STAGE"}),
    ("Formal operational stage begins around age:", {"A": "2", "B": "7", "C": "11", "D": "15"}, "C", {"A": "WRONG_STAGE", "B": "WRONG_STAGE", "D": "WRONG_STAGE"}),
    # Inclusive education
    ("Inclusive education means:", {"A": "Separate schools for disabled", "B": "All children learn together", "C": "Only gifted children", "D": "Only average children"}, "B", {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    ("RTE Act 2009 mandates free education for ages:", {"A": "3-14", "B": "6-14", "C": "5-18", "D": "8-16"}, "B", {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    ("CWSN stands for:", {"A": "Children With Special Needs", "B": "Children Without School Needs", "C": "Common Wealth Student Network", "D": "Central Welfare Scheme for Needy"}, "A", {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    # Classroom management
    ("Democratic classroom style is:", {"A": "Teacher decides everything", "D": "Students decide everything", "B": "Shared decision making", "C": "No decisions made"}, "B", {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    ("Laissez-faire teaching style means:", {"A": "Strict control", "B": "Minimal teacher intervention", "C": "Democratic", "D": "Authoritarian"}, "B", {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    ("Bloom's taxonomy highest level is:", {"A": "Knowledge", "B": "Comprehension", "C": "Application", "D": "Creating"}, "D", {"A": "WRONG_STAGE", "B": "WRONG_STAGE", "C": "WRONG_STAGE"}),
    ("Bloom's taxonomy lowest level is:", {"A": "Knowledge", "B": "Comprehension", "C": "Application", "D": "Analysis"}, "A", {"B": "WRONG_STAGE", "C": "WRONG_STAGE", "D": "WRONG_STAGE"}),
    # Learning theories
    ("Maslow's hierarchy top level is:", {"A": "Physiological", "B": "Safety", "C": "Esteem", "D": "Self-actualization"}, "D", {"A": "WRONG_STAGE", "B": "WRONG_STAGE", "C": "WRONG_STAGE"}),
    ("Maslow's hierarchy bottom level is:", {"A": "Physiological", "B": "Safety", "C": "Love/Belonging", "D": "Esteem"}, "A", {"B": "WRONG_STAGE", "C": "WRONG_STAGE", "D": "WRONG_STAGE"}),
    # Language acquisition
    ("Chomsky proposed:", {"A": "Behaviorist language theory", "B": "Innate language acquisition device", "C": "Social learning theory", "D": "Operant conditioning"}, "B", {"A": "WRONG_THEORIST", "C": "WRONG_THEORIST", "D": "WRONG_THEORIST"}),
    ("Mother tongue should be medium of instruction because:", {"A": "It is easier for children", "B": "It builds strong foundation", "C": "Parents prefer it", "D": "Government mandates only"}, "B", {"A": "OVERAPPLY", "C": "OVERAPPLY", "D": "OVERAPPLY"}),
    # Motivation
    ("Intrinsic motivation comes from:", {"A": "External rewards", "B": "Internal satisfaction", "C": "Punishment avoidance", "D": "Peer pressure"}, "B", {"A": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("Extrinsic motivation comes from:", {"A": "Internal interest", "B": "External rewards", "C": "Curiosity", "D": "Enjoyment"}, "B", {"A": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    # Assessment tools
    ("A rubric is:", {"A": "A grading scale with criteria", "B": "A test paper", "C": "A textbook", "D": "A report card"}, "A", {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("Portfolio assessment collects:", {"A": "Single test score", "B": "Student work over time", "C": "Attendance record", "D": "Exam marks only"}, "B", {"A": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("Peer assessment means:", {"A": "Teacher grades student", "B": "Students grade each other", "C": "Self grading", "D": "Parent grading"}, "B", {"A": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("Self assessment means:", {"A": "Teacher grades", "B": "Peer grades", "C": "Student evaluates own work", "D": "Parent evaluates"}, "C", {"A": "CONFUSED_TERMS", "B": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    # Special needs
    ("Dyslexia affects:", {"A": "Math ability", "B": "Reading ability", "C": "Hearing", "D": "Vision"}, "B", {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    ("ADHD stands for:", {"A": "Attention Deficit Hyperactivity Disorder", "B": "Advanced Developmental Health Disorder", "C": "Academic Difficulty Handling Disorder", "D": "Attention Deficit Hearing Disorder"}, "A", {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("Autism is a:", {"A": "Physical disability", "B": "Developmental disorder", "C": "Hearing impairment", "D": "Visual impairment"}, "B", {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    # ICT in education
    ("ICT in education stands for:", {"A": "Information and Communication Technology", "B": "International Curriculum Teaching", "C": "Individual Computer Training", "D": "Integrated Classroom Technique"}, "A", {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("MOOC stands for:", {"A": "Massive Open Online Course", "B": "Modern Online Open Classroom", "C": "Multiple Option Online Course", "D": "Managed Open Online Content"}, "A", {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    # NCF
    ("NCF stands for:", {"A": "National Curriculum Framework", "B": "New Classroom Format", "C": "National Child Foundation", "D": "New Curriculum for Future"}, "A", {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("NCF 2005 emphasized:", {"A": "Rote learning", "B": "Child-centered learning", "C": "Exam focus", "D": "Teacher-centered"}, "B", {"A": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    # CCE
    ("CCE stands for:", {"A": "Continuous and Comprehensive Evaluation", "B": "Central Curriculum Examination", "C": "Classroom Continuous Evaluation", "D": "Comprehensive Course Evaluation"}, "A", {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("CCE was introduced to:", {"A": "Reduce exam stress", "B": "Increase rote learning", "C": "Eliminate teachers", "D": "Standardize only"}, "A", {"B": "WRONG_CONCEPT", "C": "WRONG_CONCEPT", "D": "WRONG_CONCEPT"}),
    # Right to Education
    ("Free and compulsory education is a:", {"A": "Fundamental right", "B": "Fundamental duty", "C": "Directive principle only", "D": "Legal suggestion"}, "A", {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("Article 21A of Indian Constitution deals with:", {"A": "Right to equality", "B": "Right to education", "C": "Right to freedom", "D": "Right to religion"}, "B", {"A": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
]

stored = 0
for q, opts, correct, pw in ITEMS:
    cur.execute("INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (TID, q, opts["A"], opts["B"], opts["C"], opts["D"], correct, 1, "human_authored", "passed", "CDP_Pedagogy"))
    iid = cur.lastrowid
    for letter, mis in pw.items():
        if letter != correct:
            cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                        (iid, letter, mis, MIS.get(mis, mis)))
    stored += 1

conn.commit()
c2 = sqlite3.connect(DB)
print("Pedagogy2:", c2.execute("SELECT COUNT(*) FROM item WHERE rule_type='CDP_Pedagogy'").fetchone()[0], "total pedagogy items")
print("Grand total:", c2.execute("SELECT COUNT(*) FROM item").fetchone()[0])
c2.close(); conn.close()

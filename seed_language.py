"""
Phase 16 — Hindi & English Grammar + Comprehension Bank.

Hand-authored language items for Haryana/CBSE Class 9-10 students.
Hindi: sandhi, samas, alankar, vibhakti, ling, vachan, kriya, muhavare
English: tenses, subject-verb agreement, voice, speech, articles, prepositions

Run: python seed_language.py
"""

import sqlite3

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Create topics
cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (9,'Hindi','HIN_01','Hindi Grammar & Comprehension','0','medium')")
cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (9,'English','ENG_01','English Grammar & Comprehension','0','medium')")
conn.commit()

HINDI_TID = cur.execute("SELECT id FROM topic WHERE chapter_code='HIN_01'").fetchone()[0]
ENG_TID = cur.execute("SELECT id FROM topic WHERE chapter_code='ENG_01'").fetchone()[0]

MISCONCEPTIONS = {
    "CONFUSED_RULE":   "Confused a similar grammar rule",
    "WRONG_FORM":      "Selected the wrong grammatical form",
    "SPELLING_ERROR":  "Spelling mistake in the answer",
    "MEANING_ERROR":   "Misunderstood the meaning",
    "OVERAPPLY":       "Applied the rule too broadly",
    "CONFUSED_TERMS":  "Confused two similar terms",
}

HINDI_ITEMS = [
    ("'राम + ईश्वर' ka sandhi kya hoga?",
     {"A": "रामेश्वर", "B": "रामईश्वर", "C": "रामिश्वर", "D": "रामोश्वर"}, "A",
     {"B": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),
    ("'सत्य + आग्रह' ka sandhi kya hoga?",
     {"A": "सत्याग्रह", "B": "सत्यआग्रह", "C": "सत्यग्रह", "D": "सत्याग्रहा"}, "A",
     {"B": "WRONG_FORM", "C": "CONFUSED_TERMS", "D": "SPELLING_ERROR"}),
    ("'विद्या + आलय' ka sandhi kya hoga?",
     {"A": "विद्यालय", "B": "विद्याआलय", "C": "विद्यालया", "D": "विद्यालयम"}, "A",
     {"B": "WRONG_FORM", "C": "SPELLING_ERROR", "D": "WRONG_FORM"}),
    ("'प्रति + उत्तर' ka sandhi kya hoga?",
     {"A": "प्रत्युत्तर", "B": "प्रतिउत्तर", "C": "प्रत्यूत्तर", "D": "प्रतिउत्तरम"}, "A",
     {"B": "WRONG_FORM", "C": "SPELLING_ERROR", "D": "WRONG_FORM"}),
    ("'सु + अग्र' ka sandhi kya hoga?",
     {"A": "स्वाग्र", "B": "सौअग्र", "C": "सुअग्र", "D": "स्वाग्रम"}, "A",
     {"B": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),
    ("'अति + उत्तम' ka sandhi kya hoga?",
     {"A": "अत्युत्तम", "B": "अतिउत्तम", "C": "अत्युत्तमा", "D": "अतिउत्तमम"}, "A",
     {"B": "WRONG_FORM", "C": "SPELLING_ERROR", "D": "WRONG_FORM"}),
    ("'परि + उपकार' ka sandhi kya hoga?",
     {"A": "पर्युपकार", "B": "परिउपकार", "C": "पर्यूपकार", "D": "परिउपकारम"}, "A",
     {"B": "WRONG_FORM", "C": "SPELLING_ERROR", "D": "WRONG_FORM"}),
    ("'निर + ईश' ka sandhi kya hoga?",
     {"A": "निरीश", "B": "निरिश", "C": "निरीशा", "D": "निरेश"}, "A",
     {"B": "WRONG_FORM", "C": "SPELLING_ERROR", "D": "CONFUSED_TERMS"}),

    ("'Rajdhani' shabd ka samas kya hai?",
     {"A": "Tatpurush", "B": "Dvandva", "C": "Bahuvrihi", "D": "Avyayibhav"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("'Panchtatva' shabd ka samas kya hai?",
     {"A": "Dvandva", "B": "Tatpurush", "C": "Bahuvrihi", "D": "Avyayibhav"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("'Neelkanth' shabd ka samas kya hai?",
     {"A": "Bahuvrihi", "B": "Tatpurush", "C": "Dvandva", "D": "Avyayibhav"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("'Pratidin' shabd ka samas kya hai?",
     {"A": "Avyayibhav", "B": "Tatpurush", "C": "Dvandva", "D": "Bahuvrihi"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),

    ("'Chandrama' shabd ka ling kya hai?",
     {"A": "Pulling", "B": "Striling", "C": "Ubhayling", "D": "Napumsakling"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("'Ladki' shabd ka ling kya hai?",
     {"A": "Striling", "B": "Pulling", "C": "Ubhayling", "D": "Napumsakling"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("'Phool' shabd ka ling kya hai?",
     {"A": "Napumsakling", "B": "Pulling", "C": "Striling", "D": "Ubhayling"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("'Bachcha' shabd ka vachan kya hai (plural)?",
     {"A": "Bachche", "B": "Bachcha", "C": "Bachchon", "D": "Bachchi"}, "A",
     {"B": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),

    ("'Kamal' shabd ka vachan (plural) kya hai?",
     {"A": "Kamal", "B": "Kamalon", "C": "Kamale", "D": "Kamali"}, "A",
     {"B": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),
    ("'Ladka' (plural) ka sahi rup kya hai?",
     {"A": "Ladke", "B": "Ladka", "C": "Ladki", "D": "Ladkon"}, "A",
     {"B": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),

    ("'Main school jaata hoon' — yeh kis kaal mein hai?",
     {"A": "Vartaman kaal", "B": "Bhoot kaal", "C": "Bhavishya kaal", "D": "Sanyukt kaal"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("'Main school gaya tha' — yeh kis kaal mein hai?",
     {"A": "Bhoot kaal", "B": "Vartaman kaal", "C": "Bhavishya kaal", "D": "Sanyukt kaal"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("'Main school jaunga' — yeh kis kaal mein hai?",
     {"A": "Bhavishya kaal", "B": "Vartaman kaal", "C": "Bhoot kaal", "D": "Sanyukt kaal"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),

    ("'Rama ne phal khaya' — is vakya mein kriya kya hai?",
     {"A": "khaya", "B": "Rama", "C": "phal", "D": "ne"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("'Ladka park mein khel raha hai' — is vakya ka karta kaun hai?",
     {"A": "Ladka", "B": "park", "C": "khel", "D": "raha"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),

    ("'Bhaag do (run away)' ka sahi prayog kya hai?",
     {"A": "Bhaag jana", "B": "Bhaag dena", "C": "Bhaag karna", "D": "Bhaag lena"}, "A",
     {"B": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),
    ("'Nazar aana' ka sahi arth kya hai?",
     {"A": "Dikhai dena", "B": "Chhup jana", "C": "Bhaag jana", "D": "Khona"}, "A",
     {"B": "MEANING_ERROR", "C": "MEANING_ERROR", "D": "MEANING_ERROR"}),
    ("'Aankh khulna' ka sahi arth kya hai?",
     {"A": "Jag jaana", "B": "So jaana", "C": "Rona", "D": "Hasna"}, "A",
     {"B": "MEANING_ERROR", "C": "MEANING_ERROR", "D": "MEANING_ERROR"}),

    ("Hindi mein 'upma' alankar kya hota hai?",
     {"A": "Do vastuon ka tulna", "B": "Atishayokti", "C": "Rupak", "D": "Anupras"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("'Chandramukhi' mein kaunsa alankar hai?",
     {"A": "Rupak", "B": "Upma", "C": "Atishayokti", "D": "Anupras"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("'Gagan talai' mein kaunsa alankar hai?",
     {"A": "Rupak", "B": "Upma", "C": "Atishayokti", "D": "Anupras"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("'Ghata ghata mein ram hai' mein kaunsa alankar hai?",
     {"A": "Anupras", "B": "Upma", "C": "Rupak", "D": "Atishayokti"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
]

ENGLISH_ITEMS = [
    ("Choose the correct form: 'She ___ to school every day.'",
     {"A": "go", "B": "goes", "C": "gone", "D": "going"}, "B",
     {"A": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),
    ("Choose the correct form: 'They ___ playing cricket now.'",
     {"A": "is", "B": "are", "C": "was", "D": "were"}, "B",
     {"A": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),
    ("Choose the correct form: 'I ___ this book since morning.'",
     {"A": "read", "B": "have read", "C": "am reading", "D": "was reading"}, "B",
     {"A": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),
    ("Choose the correct form: 'He ___ in Delhi for 5 years.'",
     {"A": "lives", "B": "has lived", "C": "is living", "D": "lived"}, "B",
     {"A": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),
    ("Choose the correct form: 'By next year, she ___ her degree.'",
     {"A": "will complete", "B": "will have completed", "C": "completes", "D": "completed"}, "B",
     {"A": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),
    ("Choose the correct form: 'The train ___ before we reached the station.'",
     {"A": "left", "B": "had left", "C": "has left", "D": "leaves"}, "B",
     {"A": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),
    ("Choose the correct form: 'If I ___ rich, I would buy a car.'",
     {"A": "am", "B": "was", "C": "were", "D": "will be"}, "C",
     {"A": "WRONG_FORM", "B": "WRONG_FORM", "D": "WRONG_FORM"}),

    ("Convert to passive: 'Rama writes a letter.'",
     {"A": "A letter is written by Rama.", "B": "A letter was written by Rama.", "C": "A letter is wrote by Rama.", "D": "A letter written by Rama."}, "A",
     {"B": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),
    ("Convert to passive: 'The teacher punished the boy.'",
     {"A": "The boy was punished by the teacher.", "B": "The boy is punished by the teacher.", "C": "The boy punished by the teacher.", "D": "The teacher was punished by the boy."}, "A",
     {"B": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),
    ("Convert to active: 'The cake was eaten by the children.'",
     {"A": "The children ate the cake.", "B": "The children eat the cake.", "C": "The cake ate the children.", "D": "The children were eating the cake."}, "A",
     {"B": "WRONG_FORM", "C": "MEANING_ERROR", "D": "WRONG_FORM"}),

    ("Convert to indirect speech: He said, 'I am happy.'",
     {"A": "He said that he was happy.", "B": "He said that I am happy.", "C": "He said that he is happy.", "D": "He said that he had been happy."}, "A",
     {"B": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),
    ("Convert to indirect speech: She said, 'I will come tomorrow.'",
     {"A": "She said that she would come the next day.", "B": "She said that she will come tomorrow.", "C": "She said that she would come tomorrow.", "D": "She said that I would come the next day."}, "A",
     {"B": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),

    ("Fill in the blank: 'He is ___ honest man.'",
     {"A": "a", "B": "an", "C": "the", "D": "no article"}, "B",
     {"A": "CONFUSED_RULE", "C": "CONFUSED_RULE", "D": "CONFUSED_RULE"}),
    ("Fill in the blank: '___ sun rises in the east.'",
     {"A": "A", "B": "An", "C": "The", "D": "No article"}, "C",
     {"A": "CONFUSED_RULE", "B": "CONFUSED_RULE", "D": "CONFUSED_RULE"}),
    ("Fill in the blank: 'I have ___ umbrella.'",
     {"A": "a", "B": "an", "C": "the", "D": "no article"}, "B",
     {"A": "CONFUSED_RULE", "C": "CONFUSED_RULE", "D": "CONFUSED_RULE"}),

    ("Fill in the blank: 'She is good ___ mathematics.'",
     {"A": "in", "B": "at", "C": "on", "D": "for"}, "B",
     {"A": "CONFUSED_RULE", "C": "CONFUSED_RULE", "D": "CONFUSED_RULE"}),
    ("Fill in the blank: 'He is afraid ___ dogs.'",
     {"A": "of", "B": "from", "C": "with", "D": "to"}, "A",
     {"B": "CONFUSED_RULE", "C": "CONFUSED_RULE", "D": "CONFUSED_RULE"}),
    ("Fill in the blank: 'The book is ___ the table.'",
     {"A": "on", "B": "in", "C": "at", "D": "over"}, "A",
     {"B": "CONFUSED_RULE", "C": "CONFUSED_RULE", "D": "CONFUSED_RULE"}),

    ("Choose the correct sentence:",
     {"A": "She don't like apples.", "B": "She doesn't likes apples.", "C": "She doesn't like apples.", "D": "She not like apples."}, "C",
     {"A": "WRONG_FORM", "B": "WRONG_FORM", "D": "WRONG_FORM"}),
    ("Choose the correct sentence:",
     {"A": "Each of the boys have a book.", "B": "Each of the boys has a book.", "C": "Each of the boys had a book.", "D": "Each of the boys having a book."}, "B",
     {"A": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),
    ("Choose the correct sentence:",
     {"A": "Neither Ram nor Shyam are present.", "B": "Neither Ram nor Shyam is present.", "C": "Neither Ram nor Shyam were present.", "D": "Neither Ram nor Shyam be present."}, "B",
     {"A": "WRONG_FORM", "C": "WRONG_FORM", "D": "WRONG_FORM"}),

    ("Identify the figure of speech: 'The wind whispered through the trees.'",
     {"A": "Personification", "B": "Simile", "C": "Metaphor", "D": "Hyperbole"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("Identify the figure of speech: 'He is as brave as a lion.'",
     {"A": "Simile", "B": "Metaphor", "C": "Personification", "D": "Hyperbole"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("Identify the figure of speech: 'The classroom was a zoo.'",
     {"A": "Metaphor", "B": "Simile", "C": "Personification", "D": "Hyperbole"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),

    ("Synonym of 'Abundant' is:",
     {"A": "Scarce", "B": "Plentiful", "C": "Rare", "D": "Limited"}, "B",
     {"A": "MEANING_ERROR", "C": "MEANING_ERROR", "D": "MEANING_ERROR"}),
    ("Antonym of 'Brave' is:",
     {"A": "Courageous", "B": "Fearless", "C": "Cowardly", "D": "Bold"}, "C",
     {"A": "MEANING_ERROR", "B": "MEANING_ERROR", "D": "MEANING_ERROR"}),
    ("One-word substitution for 'A person who loves books' is:",
     {"A": "Bibliophile", "B": "Philatelist", "C": "Ornithologist", "D": "Somnambulist"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("One-word substitution for 'Fear of water' is:",
     {"A": "Hydrophobia", "B": "Claustrophobia", "C": "Arachnophobia", "D": "Acrophobia"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),

    ("In the sentence 'The boy ran quickly', 'quickly' is a:",
     {"A": "Noun", "B": "Verb", "C": "Adjective", "D": "Adverb"}, "D",
     {"A": "CONFUSED_TERMS", "B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS"}),
    ("In the sentence 'She is beautiful', 'beautiful' is a:",
     {"A": "Noun", "B": "Verb", "C": "Adjective", "D": "Adverb"}, "C",
     {"A": "CONFUSED_TERMS", "B": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
    ("'Honesty is the best policy' — 'Honesty' is a:",
     {"A": "Noun", "B": "Verb", "C": "Adjective", "D": "Adverb"}, "A",
     {"B": "CONFUSED_TERMS", "C": "CONFUSED_TERMS", "D": "CONFUSED_TERMS"}),
]

# Comprehension passages
HINDI_COMP = [
    ("Passage: 'Bharat ek kisaan pradhan desh hai. Yahan ki 70% janta kheti se judi hai. Lekin ab bhi anek kisaan purane tarike se kheti karte hain, jisse utpadan kam hota hai.'\n\nQuestion: Bharat mein kitne % janta kheti se judi hai?",
     {"A": "50%", "B": "60%", "C": "70%", "D": "80%"}, "C",
     {"A": "MEANING_ERROR", "B": "MEANING_ERROR", "D": "MEANING_ERROR"}),
    ("Passage: 'Bharat ek kisaan pradhan desh hai. Yahan ki 70% janta kheti se judi hai. Lekin ab bhi anek kisaan purane tarike se kheti karte hain, jisse utpadan kam hota hai.'\n\nQuestion: Kisaanon ka kaunsa kaam utpadan kam kar raha hai?",
     {"A": "Naye tarike", "B": "Purane tarike", "C": "Machine ka use", "D": "Sarkari yojana"}, "B",
     {"A": "MEANING_ERROR", "C": "MEANING_ERROR", "D": "MEANING_ERROR"}),
]

ENGLISH_COMP = [
    ("Passage: 'Reading is a habit that develops over time. It improves vocabulary, concentration, and imagination. A good reader reads not just for information but for pleasure.'\n\nQuestion: What does reading improve?",
     {"A": "Only vocabulary", "B": "Vocabulary, concentration, and imagination", "C": "Only concentration", "D": "Only imagination"}, "B",
     {"A": "MEANING_ERROR", "C": "MEANING_ERROR", "D": "MEANING_ERROR"}),
    ("Passage: 'Reading is a habit that develops over time. It improves vocabulary, concentration, and imagination. A good reader reads not just for information but for pleasure.'\n\nQuestion: Why does a good reader read?",
     {"A": "Only for information", "B": "Only for pleasure", "C": "For information and pleasure", "D": "For exams"}, "C",
     {"A": "MEANING_ERROR", "B": "MEANING_ERROR", "D": "MEANING_ERROR"}),
]

ALL_ITEMS = [(HINDI_TID, HINDI_ITEMS + HINDI_COMP, "Hindi_Grammar")] + \
             [(ENG_TID, ENGLISH_ITEMS + ENGLISH_COMP, "English_Grammar")]

stored = 0
for tid, items, rule_type in ALL_ITEMS:
    for question, options, correct, per_wrong in items:
        cur.execute(
            "INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (tid, question, options.get("A", ""), options.get("B", ""),
             options.get("C", ""), options.get("D", ""),
             correct, 1, "human_authored", "passed", rule_type))
        iid = cur.lastrowid
        for letter, mis in per_wrong.items():
            if letter != correct and letter in options:
                cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                            (iid, letter, mis, MISCONCEPTIONS.get(mis, mis)))
        stored += 1

conn.commit()

# Verify
c2 = sqlite3.connect(DB)
print("=== LANGUAGE BANK SEED COMPLETE ===")
for rt in ["Hindi_Grammar", "English_Grammar"]:
    n = c2.execute("SELECT COUNT(*) FROM item WHERE rule_type=?", (rt,)).fetchone()[0]
    e = c2.execute("SELECT COUNT(*) FROM distractor_error WHERE item_id IN (SELECT id FROM item WHERE rule_type=?)", (rt,)).fetchone()[0]
    print(f"  {rt}: {n} items, {e} distractor tags")
print(f"  Total new: {stored}")
print(f"  Grand total items: {c2.execute('SELECT COUNT(*) FROM item').fetchone()[0]}")
c2.close()
conn.close()

"""
Phase 20 — Hindi & English: 120 more grammar + comprehension items.
Run: python seed_language2.py
"""

import sqlite3

DB = "engine.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (9,'Hindi','HIN_02','Hindi Grammar 2','0','medium')")
cur.execute("INSERT OR IGNORE INTO topic (class_level, subject, chapter_code, title, parent_topic_id, difficulty_band) VALUES (9,'English','ENG_02','English Grammar 2','0','medium')")
conn.commit()
HIN = cur.execute("SELECT id FROM topic WHERE chapter_code='HIN_02'").fetchone()[0]
ENG = cur.execute("SELECT id FROM topic WHERE chapter_code='ENG_02'").fetchone()[0]

MIS = {"CONFUSED_RULE": "Confused rule", "WRONG_FORM": "Wrong form", "MEANING_ERROR": "Meaning error",
       "CONFUSED_TERMS": "Confused terms", "SPELLING_ERROR": "Spelling error", "OVERAPPLY": "Over-applied"}

H = []
E = []

# ===== HINDI (60 items) =====
# Sandhi more
for w, ans, opts in [("prati+uttar", "pratyuttar", ["pratiuttar","pratyuttar","pratiuttr","pratyuttr"]),
                      ("su+agam", "svagam", ["suagam","svagam","sugam","swagam"]),
                      ("nir+is", "niris", ["niris","nirish","nirish","nires"]),
                      ("ati+uttam", "atyuttam", ["atiuttam","atyuttam","atyuttam","atiuttm"]),
                      ("pari+upakar", "paryupakar", ["pariupakar","paryupakar","parupakar","paryupkar"]),
                      ("dur+aachar", "duraachar", ["duraachar","durachar","durachar","duraachr"]),
                      ("sam+gam", "sangam", ["samgam","sangam","sangm","samgm"]),
                      ("ut+pat", "utpat", ["utpat","utpaat","utpt","utpaat"])]:
    H.append((f"'{w}' ka sandhi kya hoga?", {"A": opts[0], "B": opts[1], "C": opts[2], "D": opts[3]}, "B" if ans == opts[1] else "A",
              {"C": "WRONG_FORM", "D": "WRONG_FORM"}))

# Muhavare
muh = [("Aankh ka tara", "Bahut pyara", ["Bahut pyara", "Bahut bada", "Bahut chota", "Bahut kala"]),
       ("Aankh uthana", "Izzat badhana", ["Izzat badhana", "Izzat ghatana", "Aankh band karna", "So jana"]),
       ("Hath uthana", "Marne ka sanket", ["Marne ka sanket", "Hath milana", "Hath jodna", "Hath hilana"]),
       ("Paani pila dena", "Marna", ["Marna", "Jinda rakhna", "Pani dena", "Bhagana"]),
       ("Naak katna", "Apmaan hona", ["Apmaan hona", "Naak badhna", "Sardi hona", "Khush hona"]),
       ("Gardan uthana", "Ghamand karna", ["Ghamand karna", "Gardan jhukana", "Rona", "Hasna"]),
       ("Dil tootna", "Dukhi hona", ["Dukhi hona", "Khush hona", "Gussa aana", "So jana"]),
       ("Sir chadna", "Ghamand karna", ["Ghamand karna", "Sir jhukana", "Sir dard", "Sir kaatna"]),
       ("Kaan kholna", "Dhyan dena", ["Dhyan dena", "Kaan band karna", "Sunna band", "So jana"]),
       ("Muuh uthana", "Ghamand karna", ["Ghamand karna", "Muuh band karna", "Bolna", "Khana"])]
for phrase, meaning, opts in muh:
    H.append((f"'{phrase}' muhavare ka arth kya hai?", {"A": opts[0], "B": opts[1], "C": opts[2], "D": opts[3]}, "A",
              {"B": "MEANING_ERROR", "C": "MEANING_ERROR", "D": "MEANING_ERROR"}))

# Ling
ling = [("Ladka", "Pulling"), ("Ladki", "Striling"), ("Guru", "Pulling"), ("Guruwani", "Striling"),
        ("Sher", "Pulling"), ("Sherani", "Striling"), ("Ghorha", "Pulling"), ("Ghodi", "Striling"),
        ("Mor", "Pulling"), ("Morani", "Striling"), ("Naukar", "Pulling"), ("Naukrani", "Striling"),
        ("Raja", "Pulling"), ("Rani", "Striling"), ("Beta", "Pulling"), ("Beti", "Striling")]
for word, gender in ling:
    opts = ["Pulling", "Striling", "Ubhayling", "Napumsakling"]
    correct = opts.index(gender) + 1
    letter = chr(64 + correct)
    H.append((f"'{word}' shabd ka ling kya hai?", {"A": opts[0], "B": opts[1], "C": opts[2], "D": opts[3]}, letter,
              {"A": "CONFUSED_TERMS" if letter != "A" else "WRONG_FORM",
               "B": "CONFUSED_TERMS" if letter != "B" else "WRONG_FORM",
               "C": "CONFUSED_TERMS" if letter != "C" else "WRONG_FORM",
               "D": "CONFUSED_TERMS" if letter != "D" else "WRONG_FORM"}))

# Kaal
kaal = [("Main khata hoon", "Vartaman"), ("Main khaya", "Bhoot"), ("Main khunga", "Bhavishya"),
        ("Woh padhti hai", "Vartaman"), ("Woh padha tha", "Bhoot"), ("Woh padhegi", "Bhavishya"),
        ("Hum khelte hain", "Vartaman"), ("Hum khel chuke the", "Bhoot"), ("Hum khelenge", "Bhavishya")]
for s, k in kaal:
    opts = ["Vartaman kaal", "Bhoot kaal", "Bhavishya kaal", "Sanyukt kaal"]
    idx = opts.index(k + " kaal") + 1
    letter = chr(64 + idx)
    H.append((f"'{s}' — yeh kis kaal mein hai?", {"A": opts[0], "B": opts[1], "C": opts[2], "D": opts[3]}, letter,
              {"A": "CONFUSED_TERMS" if letter != "A" else "WRONG_FORM",
               "B": "CONFUSED_TERMS" if letter != "B" else "WRONG_FORM",
               "C": "CONFUSED_TERMS" if letter != "C" else "WRONG_FORM",
               "D": "CONFUSED_TERMS" if letter != "D" else "WRONG_FORM"}))

# Samas
samas = [("Rajdhani", "Tatpurush"), ("Panchtatva", "Dvandva"), ("Neelkanth", "Bahuvrihi"),
         ("Pratidin", "Avyayibhav"), ("Himachal", "Tatpurush"),
         ("Dwarikapati", "Tatpurush"), ("Chandramukhi", "Bahuvrihi"), ("Gaganvani", "Tatpurush")]
for w, s in samas:
    opts = ["Tatpurush", "Dvandva", "Bahuvrihi", "Avyayibhav"]
    idx = opts.index(s) + 1
    letter = chr(64 + idx)
    H.append((f"'{w}' shabd ka samas kya hai?", {"A": opts[0], "B": opts[1], "C": opts[2], "D": opts[3]}, letter,
              {"A": "CONFUSED_TERMS" if letter != "A" else "WRONG_FORM",
               "B": "CONFUSED_TERMS" if letter != "B" else "WRONG_FORM",
               "C": "CONFUSED_TERMS" if letter != "C" else "WRONG_FORM",
               "D": "CONFUSED_TERMS" if letter != "D" else "WRONG_FORM"}))

# Alankar
alankar = [("Chandramukhi", "Rupak"), ("Gagan talai", "Rupak"), ("Ghata ghata mein ram", "Anupras"),
            ("Hari anant hari katha ananta", "Anupras"),
            ("Pawan chali to chali", "Anupras"), ("Kamal nayan", "Rupak"), ("Chandni raat", "Rupak")]
for w, a in alankar:
    opts = ["Rupak", "Upma", "Anupras", "Atishayokti"]
    idx = opts.index(a) + 1
    letter = chr(64 + idx)
    H.append((f"'{w}' mein kaunsa alankar hai?", {"A": opts[0], "B": opts[1], "C": opts[2], "D": opts[3]}, letter,
              {"A": "CONFUSED_TERMS" if letter != "A" else "WRONG_FORM",
               "B": "CONFUSED_TERMS" if letter != "B" else "WRONG_FORM",
               "C": "CONFUSED_TERMS" if letter != "C" else "WRONG_FORM",
               "D": "CONFUSED_TERMS" if letter != "D" else "WRONG_FORM"}))

# Comprehension (Hindi)
H.append(("Passage: 'Bharat ek kisaan pradhan desh hai. 70% janta kheti se judi hai. Purane tarike se kheti karne se utpadan kam hota hai.'\n\nPrashn: Bharat mein kitne % janta kheti se judi hai?",
         {"A": "50%", "B": "60%", "C": "70%", "D": "80%"}, "C",
         {"A": "MEANING_ERROR", "B": "MEANING_ERROR", "D": "MEANING_ERROR"}))
H.append(("Passage: 'Bharat ek kisaan pradhan desh hai. 70% janta kheti se judi hai. Purane tarike se kheti karne se utpadan kam hota hai.'\n\nPrashn: Ut padan kam karne ka kaaran kya hai?",
         {"A": "Naye tarike", "B": "Purane tarike", "C": "Machine", "D": "Sarkari yojana"}, "B",
         {"A": "MEANING_ERROR", "C": "MEANING_ERROR", "D": "MEANING_ERROR"}))

# ===== ENGLISH (60 items) =====
# Tenses more
tenses = [("She ___ (play) piano every day.", "plays", ["play", "plays", "played", "playing"]),
          ("They ___ (study) now.", "are studying", ["study", "studies", "are studying", "studied"]),
          ("I ___ (finish) my homework.", "have finished", ["finish", "finishes", "have finished", "finished"]),
          ("He ___ (live) here since 2010.", "has lived", ["lives", "has lived", "is living", "lived"]),
          ("By 2025, she ___ (graduate).", "will have graduated", ["will graduate", "will have graduated", "graduates", "graduated"]),
          ("The train ___ (leave) before we arrived.", "had left", ["left", "had left", "has left", "leaves"]),
          ("If I were rich, I ___ (buy) a car.", "would buy", ["will buy", "would buy", "buy", "bought"]),
          ("She ___ (not/like) apples.", "doesn't like", ["don't like", "doesn't likes", "doesn't like", "not like"]),
          ("Each of the boys ___ a book.", "has", ["have", "has", "had", "having"]),
          ("Neither Ram nor Shyam ___ present.", "is", ["are", "is", "were", "be"])]
for s, ans, opts in tenses:
    idx = opts.index(ans) + 1
    letter = chr(64 + idx)
    E.append((s, {"A": opts[0], "B": opts[1], "C": opts[2], "D": opts[3]}, letter,
              {"A": "WRONG_FORM" if letter != "A" else "CONFUSED_RULE",
               "B": "WRONG_FORM" if letter != "B" else "CONFUSED_RULE",
               "C": "WRONG_FORM" if letter != "C" else "CONFUSED_RULE",
               "D": "WRONG_FORM" if letter != "D" else "CONFUSED_RULE"}))

# Voice
voice = [("Rama writes a letter.", "A letter is written by Rama.", ["A letter is written by Rama.", "A letter was written by Rama.", "A letter is wrote by Rama.", "A letter written by Rama."]),
         ("The teacher punished the boy.", "The boy was punished by the teacher.", ["The boy was punished by the teacher.", "The boy is punished by the teacher.", "The boy punished by the teacher.", "The teacher was punished by the boy."]),
         ("She sings a song.", "A song is sung by her.", ["A song is sung by her.", "A song was sung by her.", "A song is sang by her.", "A song sung by her."]),
         ("They built a house.", "A house was built by them.", ["A house was built by them.", "A house is built by them.", "A house built by them.", "A house is build by them."]),
         ("The children ate the cake.", "The cake was eaten by the children.", ["The cake was eaten by the children.", "The cake is eaten by the children.", "The cake ate the children.", "The children were eating the cake."])]
for s, ans, opts in voice:
    idx = opts.index(ans) + 1
    letter = chr(64 + idx)
    E.append((f"Convert to passive: '{s}'", {"A": opts[0], "B": opts[1], "C": opts[2], "D": opts[3]}, letter,
              {"A": "WRONG_FORM" if letter != "A" else "CONFUSED_RULE",
               "B": "WRONG_FORM" if letter != "B" else "CONFUSED_RULE",
               "C": "WRONG_FORM" if letter != "C" else "CONFUSED_RULE",
               "D": "WRONG_FORM" if letter != "D" else "CONFUSED_RULE"}))

# Speech
speech = [("He said, 'I am happy.'", "He said that he was happy.", ["He said that he was happy.", "He said that I am happy.", "He said that he is happy.", "He said that he had been happy."]),
          ("She said, 'I will come tomorrow.'", "She said that she would come the next day.", ["She said that she would come the next day.", "She said that she will come tomorrow.", "She said that she would come tomorrow.", "She said that I would come the next day."]),
          ("He said, 'I have finished my work.'", "He said that he had finished his work.", ["He said that he had finished his work.", "He said that he has finished his work.", "He said that I have finished my work.", "He said that he finished his work."]),
          ("She said to me, 'You are late.'", "She told me that I was late.", ["She told me that I was late.", "She said to me that you are late.", "She told me that you were late.", "She said that I am late."])]
for s, ans, opts in speech:
    idx = opts.index(ans) + 1
    letter = chr(64 + idx)
    E.append((f"Convert to indirect speech: {s}", {"A": opts[0], "B": opts[1], "C": opts[2], "D": opts[3]}, letter,
              {"A": "WRONG_FORM" if letter != "A" else "CONFUSED_RULE",
               "B": "WRONG_FORM" if letter != "B" else "CONFUSED_RULE",
               "C": "WRONG_FORM" if letter != "C" else "CONFUSED_RULE",
               "D": "WRONG_FORM" if letter != "D" else "CONFUSED_RULE"}))

# Articles
articles = [("He is ___ honest man.", "an", ["a", "an", "the", "no article"]),
            ("___ sun rises in the east.", "The", ["A", "An", "The", "No article"]),
            ("I have ___ umbrella.", "an", ["a", "an", "the", "no article"]),
            ("She is ___ university student.", "a", ["a", "an", "the", "no article"]),
            ("___ Ganges is a holy river.", "The", ["A", "An", "The", "No article"]),
            ("He plays ___ piano well.", "the", ["a", "an", "the", "no article"]),
            ("___ Mount Everest is the highest peak.", "No article", ["A", "An", "The", "No article"])]
for s, ans, opts in articles:
    idx = opts.index(ans) + 1
    letter = chr(64 + idx)
    E.append((f"Fill in the blank: '{s}'", {"A": opts[0], "B": opts[1], "C": opts[2], "D": opts[3]}, letter,
              {"A": "CONFUSED_RULE" if letter != "A" else "WRONG_FORM",
               "B": "CONFUSED_RULE" if letter != "B" else "WRONG_FORM",
               "C": "CONFUSED_RULE" if letter != "C" else "WRONG_FORM",
               "D": "CONFUSED_RULE" if letter != "D" else "WRONG_FORM"}))

# Prepositions
preps = [("She is good ___ mathematics.", "at", ["in", "at", "on", "for"]),
         ("He is afraid ___ dogs.", "of", ["of", "from", "with", "to"]),
         ("The book is ___ the table.", "on", ["on", "in", "at", "over"]),
         ("He is interested ___ music.", "in", ["in", "at", "on", "for"]),
         ("She is married ___ a doctor.", "to", ["to", "with", "by", "for"]),
         ("The train arrived ___ time.", "on", ["on", "in", "at", "by"]),
         ("He is suffering ___ fever.", "from", ["from", "with", "of", "by"]),
         ("She is fond ___ reading.", "of", ["of", "in", "at", "for"])]
for s, ans, opts in preps:
    idx = opts.index(ans) + 1
    letter = chr(64 + idx)
    E.append((f"Fill in the blank: '{s}'", {"A": opts[0], "B": opts[1], "C": opts[2], "D": opts[3]}, letter,
              {"A": "CONFUSED_RULE" if letter != "A" else "WRONG_FORM",
               "B": "CONFUSED_RULE" if letter != "B" else "WRONG_FORM",
               "C": "CONFUSED_RULE" if letter != "C" else "WRONG_FORM",
               "D": "CONFUSED_RULE" if letter != "D" else "WRONG_FORM"}))

# Figures of speech
figs = [("The wind whispered through the trees.", "Personification", ["Personification", "Simile", "Metaphor", "Hyperbole"]),
        ("He is as brave as a lion.", "Simile", ["Simile", "Metaphor", "Personification", "Hyperbole"]),
        ("The classroom was a zoo.", "Metaphor", ["Metaphor", "Simile", "Personification", "Hyperbole"]),
        ("I have told you a thousand times.", "Hyperbole", ["Hyperbole", "Simile", "Metaphor", "Personification"]),
        ("The leaves danced in the wind.", "Personification", ["Personification", "Simile", "Metaphor", "Hyperbole"]),
        ("Her smile is like sunshine.", "Simile", ["Simile", "Metaphor", "Personification", "Hyperbole"])]
for s, ans, opts in figs:
    idx = opts.index(ans) + 1
    letter = chr(64 + idx)
    E.append((f"Identify the figure of speech: '{s}'", {"A": opts[0], "B": opts[1], "C": opts[2], "D": opts[3]}, letter,
              {"A": "CONFUSED_TERMS" if letter != "A" else "WRONG_FORM",
               "B": "CONFUSED_TERMS" if letter != "B" else "WRONG_FORM",
               "C": "CONFUSED_TERMS" if letter != "C" else "WRONG_FORM",
               "D": "CONFUSED_TERMS" if letter != "D" else "WRONG_FORM"}))

# Synonyms/Antonyms/One-word
vocab = [("Synonym of 'Abundant' is:", "Plentiful", ["Scarce", "Plentiful", "Rare", "Limited"]),
         ("Antonym of 'Brave' is:", "Cowardly", ["Courageous", "Fearless", "Cowardly", "Bold"]),
         ("One-word for 'A person who loves books' is:", "Bibliophile", ["Bibliophile", "Philatelist", "Ornithologist", "Somnambulist"]),
         ("One-word for 'Fear of water' is:", "Hydrophobia", ["Hydrophobia", "Claustrophobia", "Arachnophobia", "Acrophobia"]),
         ("Synonym of 'Eloquent' is:", "Articulate", ["Articulate", "Silent", "Confused", "Dull"]),
         ("Antonym of 'Generous' is:", "Stingy", ["Kind", "Stingy", "Giving", "Noble"]),
         ("One-word for 'A person who walks in sleep' is:", "Somnambulist", ["Somnambulist", "Bibliophile", "Insomniac", "Narcissist"]),
         ("One-word for 'Study of birds' is:", "Ornithology", ["Ornithology", "Entomology", "Zoology", "Botany"])]
for s, ans, opts in vocab:
    idx = opts.index(ans) + 1
    letter = chr(64 + idx)
    E.append((s, {"A": opts[0], "B": opts[1], "C": opts[2], "D": opts[3]}, letter,
              {"A": "MEANING_ERROR" if letter != "A" else "CONFUSED_TERMS",
               "B": "MEANING_ERROR" if letter != "B" else "CONFUSED_TERMS",
               "C": "MEANING_ERROR" if letter != "C" else "CONFUSED_TERMS",
               "D": "MEANING_ERROR" if letter != "D" else "CONFUSED_TERMS"}))

# Parts of speech
pos = [("In 'The boy ran quickly', 'quickly' is a:", "Adverb", ["Noun", "Verb", "Adjective", "Adverb"]),
       ("In 'She is beautiful', 'beautiful' is a:", "Adjective", ["Noun", "Verb", "Adjective", "Adverb"]),
       ("'Honesty is the best policy' — 'Honesty' is a:", "Noun", ["Noun", "Verb", "Adjective", "Adverb"]),
       ("In 'He runs fast', 'fast' is a:", "Adverb", ["Noun", "Verb", "Adjective", "Adverb"]),
       ("In 'The red apple', 'red' is a:", "Adjective", ["Noun", "Verb", "Adjective", "Adverb"])]
for s, ans, opts in pos:
    idx = opts.index(ans) + 1
    letter = chr(64 + idx)
    E.append((s, {"A": opts[0], "B": opts[1], "C": opts[2], "D": opts[3]}, letter,
              {"A": "CONFUSED_TERMS" if letter != "A" else "WRONG_FORM",
               "B": "CONFUSED_TERMS" if letter != "B" else "WRONG_FORM",
               "C": "CONFUSED_TERMS" if letter != "C" else "WRONG_FORM",
               "D": "CONFUSED_TERMS" if letter != "D" else "WRONG_FORM"}))

# Comprehension (English)
E.append(("Passage: 'Reading is a habit that develops over time. It improves vocabulary, concentration, and imagination. A good reader reads not just for information but for pleasure.'\n\nQuestion: What does reading improve?",
         {"A": "Only vocabulary", "B": "Vocabulary, concentration, and imagination", "C": "Only concentration", "D": "Only imagination"}, "B",
         {"A": "MEANING_ERROR", "C": "MEANING_ERROR", "D": "MEANING_ERROR"}))
E.append(("Passage: 'Reading is a habit that develops over time. It improves vocabulary, concentration, and imagination. A good reader reads not just for information but for pleasure.'\n\nQuestion: Why does a good reader read?",
         {"A": "Only for information", "B": "Only for pleasure", "C": "For information and pleasure", "D": "For exams"}, "C",
         {"A": "MEANING_ERROR", "B": "MEANING_ERROR", "D": "MEANING_ERROR"}))
E.append(("Passage: 'The Taj Mahal is one of the Seven Wonders of the World. It was built by Emperor Shah Jahan in memory of his wife Mumtaz Mahal. It is made of white marble and stands on the banks of the Yamuna river.'\n\nQuestion: Who built the Taj Mahal?",
         {"A": "Akbar", "B": "Shah Jahan", "C": "Aurangzeb", "D": "Jahangir"}, "B",
         {"A": "MEANING_ERROR", "C": "MEANING_ERROR", "D": "MEANING_ERROR"}))
E.append(("Passage: 'The Taj Mahal is one of the Seven Wonders of the World. It was built by Emperor Shah Jahan in memory of his wife Mumtaz Mahal. It is made of white marble and stands on the banks of the Yamuna river.'\n\nQuestion: The Taj Mahal is made of:",
         {"A": "Red sandstone", "B": "White marble", "C": "Granite", "D": "Limestone"}, "B",
         {"A": "MEANING_ERROR", "C": "MEANING_ERROR", "D": "MEANING_ERROR"}))

stored = 0
for stem, opts, correct, pw in H:
    cur.execute("INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (HIN, stem, opts["A"], opts["B"], opts["C"], opts["D"], correct, 1, "human_authored", "passed", "Hindi_Grammar"))
    iid = cur.lastrowid
    for letter, mis in pw.items():
        if letter != correct:
            cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                        (iid, letter, mis, MIS.get(mis, mis)))
    stored += 1

for stem, opts, correct, pw in E:
    cur.execute("INSERT INTO item (topic_id, stem, option_a, option_b, option_c, option_d, correct_option, marks, generation_method, verification_state, rule_type) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (ENG, stem, opts["A"], opts["B"], opts["C"], opts["D"], correct, 1, "human_authored", "passed", "English_Grammar"))
    iid = cur.lastrowid
    for letter, mis in pw.items():
        if letter != correct:
            cur.execute("INSERT INTO distractor_error (item_id, option_letter, error_type, description) VALUES (?,?,?,?)",
                        (iid, letter, mis, MIS.get(mis, mis)))
    stored += 1

conn.commit()
c2 = sqlite3.connect(DB)
print("Language2 added:", stored)
print("Grand total:", c2.execute("SELECT COUNT(*) FROM item").fetchone()[0])
c2.close(); conn.close()

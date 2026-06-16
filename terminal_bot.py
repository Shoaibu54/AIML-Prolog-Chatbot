# -*- coding: utf-8 -*-
"""
Family Relationship Chatbot - Terminal Version
Uses AIML for natural language processing and Pytholog for Prolog-based knowledge base queries.
"""

from aiml import Kernel
import pytholog as pl
from glob import glob
import os



import pytholog.search_util as _su, pytholog.querizer as _qz
from pytholog.goal import Goal as _G; from pytholog.fact import Fact as _F
def _neq_fix(rule, cg, Q):
    t0,t1=rule.terms[0],rule.terms[1]; v0=cg.domain.get(t0,t0); v1=cg.domain.get(t1,t1)
    if v0!=v1: Q.push(_G(_F(rule.to_string()),parent=cg,domain=cg.domain))
_su.filter_eq=_neq_fix; _qz.filter_eq=_neq_fix
# ─────────────────────────────────────────────
#  PATHS  →  adjust if your files move
# ─────────────────────────────────────────────
BASE_DIR  = r"D:\Pycharm\ChatBot\Repo"
PL_FILE   = os.path.join(BASE_DIR, "FamilyKB.pl")
AIML_GLOB = os.path.join(BASE_DIR, "*.aiml")

# ─────────────────────────────────────────────
#  INITIALISE BOT & KNOWLEDGE BASE
# ─────────────────────────────────────────────
print("Loading knowledge base and AIML files, please wait...")

bot = Kernel()
kb  = pl.KnowledgeBase("familyKb")

kb.from_file(PL_FILE)

aiml_files = glob(AIML_GLOB)
if not aiml_files:
    print(f"[WARNING] No AIML files found at: {AIML_GLOB}")
else:
    for file in aiml_files:
        bot.learn(file)
    print(f"[INFO] Loaded {len(aiml_files)} AIML file(s).")

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────

def is_valid(result, *exclude):
    """Return True if result is a real answer dict and not a self-match."""
    if not isinstance(result, dict):
        return False
    x = result.get('X')
    return x not in exclude


def getPerson(person, relation):
    """Who is the <relation> of <person>?  e.g. who is the father of ali"""
    query    = relation + "(X," + person + ")"
    response = kb.query(pl.Expr(query))
    if response is None or response == ['No']:
        return "No One"
    names = set(r['X'] for r in response if is_valid(r, person))
    return ", ".join(list(names)) if names else "No One"


def getP1(person, relation):
    """Whose <relation> is <person>?  e.g. whose child is ali"""
    query    = relation + "(" + person + ",X)"
    response = kb.query(pl.Expr(query))
    if response is None or response == ['No']:
        return "No One"
    names = set(r['X'] for r in response if is_valid(r, person))
    return ", ".join(list(names)) if names else "No One"


def isthe_Relation(person1, relation, person2):
    """Is <person1> the <relation> of <person2>?  e.g. is ali the son of ahmed"""
    if person1 == person2:
        return "No"
    query   = relation + "(X" + "," + person2 + ")"
    results = kb.query(pl.Expr(query))
    if results is None or results == ['No']:
        return "No"
    for r in results:
        if isinstance(r, dict) and r.get('X') == person1:
            return "Yes"
    return "No"


def checkRelation(person, relation):
    """Does <person> have a <relation>?  e.g. does ali have a brother"""
    query   = relation + "(X," + person + ")"
    results = kb.query(pl.Expr(query))
    if results is None or results == ['No']:
        return "No"
    valid = [r for r in results if is_valid(r, person)]
    return "Yes" if valid else "No"


def countRelation(person, relation):
    """How many <relation>s does <person> have?  e.g. how many children does ahmed have"""
    query   = relation + "(X," + person + ")"
    results = kb.query(pl.Expr(query))
    if results is None or results == ['No']:
        return "0"
    unique = set(r['X'] for r in results if is_valid(r, person))
    return str(len(unique))


def getage(person):
    """What is the age of <person>?"""
    query   = "age(" + person + ",X)"
    results = kb.query(pl.Expr(query))
    if results is None or results == ['No']:
        return "unknown"
    return str(results[0]['X'])

# ─────────────────────────────────────────────
#  MAIN CHAT LOOP
# ─────────────────────────────────────────────

print("\n" + "=" * 50)
print("      Family Relationship Chatbot")
print("      Type 'quit' or 'exit' to stop")
print("=" * 50 + "\n")

while True:
    try:
        question = input("You : ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nBot : Goodbye!")
        break

    # ── quit condition ──────────────────────────
    if question.lower() in ("quit", "exit", "bye", "q"):
        print("Bot : Goodbye! Have a great day.")
        break

    # ── skip empty input ────────────────────────
    if not question:
        continue

    # ── first pass: let AIML parse and set predicates ──
    bot.respond(question)

    relation = bot.getPredicate("rel").lower().strip()
    if relation and relation[-1] == 's':
        relation = relation[:-1]

    person1 = bot.getPredicate("p1").lower().strip()
    person2 = bot.getPredicate("p2").lower().strip()
    qtype   = bot.getPredicate("type").strip()

    # ── knowledge base lookup based on question type ──
    if qtype == "whois":
        person2 = getPerson(person1, relation)
        bot.setPredicate("p2", person2)

    elif qtype == "isthe":
        answer = isthe_Relation(person1, relation, person2)
        bot.setPredicate("answer", answer)

    elif qtype == "does":
        answer = checkRelation(person1, relation)
        bot.setPredicate("answer", answer)

    elif qtype == "howmany":
        count = countRelation(person1, relation)
        bot.setPredicate("count", count)

    elif qtype == "whose":
        p1 = getP1(person2, relation)
        bot.setPredicate("p1", p1)

    elif qtype == "age":
        age = getage(person1)
        bot.setPredicate("age", age)

    # ── second pass: get the final formatted reply ──
    reply = bot.respond(question)
    print(f"Bot : {reply}\n")

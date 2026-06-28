"""
Family Relationship Chatbot - Terminal Version
Uses AIML for natural language processing and Pytholog for Prolog-based knowledge base queries.
"""
from aiml import Kernel
import pytholog as pl
from glob import glob
import os
import time
time.clock = time.perf_counter

import pytholog.search_util as _su, pytholog.querizer as _qz
from pytholog.goal import Goal as _G; from pytholog.fact import Fact as _F
from pytholog.search_util import prob_parser as _pp

def _neq_fix(rule, cg, Q):
    try:
        t0, t1 = rule.terms[0], rule.terms[1]
        v0 = cg.domain.get(t0, t0)
        v1 = cg.domain.get(t1, t1)
        if v0 == v1 and (isinstance(v0, str) and v0[0].isupper()):
            pass
        elif v0 == v1:
            return
        Q.push(_G(_F(rule.to_string()), parent=cg, domain=cg.domain))
    except Exception:
        pass

def _prob_fix(cg, rl, Q):
    key, value = _pp(cg.domain, rl.to_string(), rl.terms)
    value = eval(value)
    if value == True:
        value = cg.domain.get(key)
        if value is None:
            value = "Yes"
    elif value == False:
        return
    cg.domain[key] = value
    Q.push(_G(_F(rl.to_string()), parent=cg, domain=cg.domain))
_su.filter_eq = _neq_fix;  _qz.filter_eq = _neq_fix
_su.prob_calc = _prob_fix;  _qz.prob_calc = _prob_fix

BASE_DIR  = r"D:\Projects\AIML-Prolog-Chatbot/Retreive-Facts"
PL_FILE   = os.path.join(BASE_DIR, "FamilyKB.pl")
AIML_GLOB = os.path.join(BASE_DIR, "*.aiml")

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

def is_valid(result, *exclude):
    if not isinstance(result, dict):
        return False
    x = result.get('X')
    return x not in exclude

def getPerson(person, relation):
    query    = relation + "(X," + person + ")"
    response = kb.query(pl.Expr(query))
    if response is None or response == ['No']:
        return "No One"
    names = set(r['X'] for r in response if is_valid(r, person))
    return ", ".join(list(names)) if names else "No One"

def getP1(person, relation):
    query    = relation + "(" + person + ",X)"
    response = kb.query(pl.Expr(query))
    if response is None or response == ['No']:
        return "No One"
    names = set(r['X'] for r in response if is_valid(r, person))
    return ", ".join(list(names)) if names else "No One"

def isthe_Relation(person1, relation, person2):
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
    query   = relation + "(X," + person + ")"
    results = kb.query(pl.Expr(query))
    if results is None or results == ['No']:
        return "No"
    valid = [r for r in results if is_valid(r, person)]
    return "Yes" if valid else "No"

def countRelation(person, relation):
    query   = relation + "(X," + person + ")"
    results = kb.query(pl.Expr(query))
    if results is None or results == ['No']:
        return "0"
    unique = set(r['X'] for r in results if is_valid(r, person))
    return str(len(unique))

def getage(person):
    query   = "age(" + person + ",X)"
    results = kb.query(pl.Expr(query))
    if results is None or results == ['No']:
        return "unknown"
    return str(results[0]['X'])

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

    if question.lower() in ("quit", "exit", "bye", "q"):
        print("Bot : Goodbye! Have a great day.")
        break

    if not question:
        continue

    bot.respond(question)

    relation = bot.getPredicate("rel").lower().strip()
    if relation and relation[-1] == 's':
        relation = relation[:-1]

    person1 = bot.getPredicate("p1").lower().strip()
    person2 = bot.getPredicate("p2").lower().strip()
    qtype   = bot.getPredicate("type").strip()

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

    reply = bot.respond(question)
    print(f"Bot : {reply}\n")

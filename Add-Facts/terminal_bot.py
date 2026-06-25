# -*- coding: utf-8 -*-
from aiml import Kernel
import pytholog as pl
from glob import glob
import os
import pytholog.search_util as _su, pytholog.querizer as _qz
from pytholog.goal import Goal as _G;
from pytholog.fact import Fact as _F


def _neq_fix(rule, cg, Q):
    t0, t1 = rule.terms[0], rule.terms[1]
    v0 = cg.domain.get(t0, t0)
    v1 = cg.domain.get(t1, t1)
    if v0 != v1:
        Q.push(_G(_F(rule.to_string()), parent=cg, domain=cg.domain))
_su.filter_eq = _neq_fix
_qz.filter_eq = _neq_fix

BASE_DIR = r"D:\Pycharm\ChatBot\Assignment 02"
PL_FILE = os.path.join(BASE_DIR, "FamilyKB.pl")
AIML_GLOB = os.path.join(BASE_DIR, "*.aiml")

def reload_kb():
    fresh_kb = pl.KnowledgeBase("familyKb")
    fresh_kb.from_file(PL_FILE)
    return fresh_kb

bot = Kernel()
kb = reload_kb()

aiml_files = glob(AIML_GLOB)
if not aiml_files:
    print(f"[WARNING] No AIML files found at: {AIML_GLOB}")
else:
    for file in aiml_files:
        bot.learn(file)
    print(f"[INFO] Loaded {len(aiml_files)} AIML file(s).")

def fact_already_exists(fact_line):
    with open(PL_FILE, "r") as f:
        return fact_line in f.read()

def add_fact_to_file(fact_line):
    if fact_already_exists(fact_line):
        return False
    with open(PL_FILE, "r") as f:
        content = f.read()
    with open(PL_FILE, "w") as f:
        f.write(fact_line + "\n" + content)
    return True

def build_facts(fact_type, p1, p2):
    facts = []
    if fact_type == "male":
        facts.append("male(" + p1 + ").")
    elif fact_type == "female":
        facts.append("female(" + p1 + ").")
    elif fact_type == "dateofbirth":
        facts.append("dateofbirth(" + p1 + "," + p2 + ").")
    elif fact_type == "parent":
        facts.append("parent(" + p1 + "," + p2 + ").")
    elif fact_type == "married":
        facts.append("marriedto(" + p1 + "," + p2 + ").")
        facts.append("marriedto(" + p2 + "," + p1 + ").")
    return facts

def is_valid(result, *exclude):
    if not isinstance(result, dict):
        return False
    x = result.get('X')
    return x not in exclude

def getPerson(person, relation):
    query = relation + "(X," + person + ")"
    response = kb.query(pl.Expr(query))
    if response is None or response == ['No']:
        return "No One"
    names = set(r['X'] for r in response if is_valid(r, person))
    return ", ".join(list(names)) if names else "No One"

def getP1(person, relation):
    query = relation + "(" + person + ",X)"
    response = kb.query(pl.Expr(query))
    if response is None or response == ['No']:
        return "No One"
    names = set(r['X'] for r in response if is_valid(r, person))
    return ", ".join(list(names)) if names else "No One"

def isthe_Relation(person1, relation, person2):
    if person1 == person2:
        return "No"
    query = relation + "(X" + "," + person2 + ")"
    results = kb.query(pl.Expr(query))
    if results is None or results == ['No']:
        return "No"
    for r in results:
        if isinstance(r, dict) and r.get('X') == person1:
            return "Yes"
    return "No"

def checkRelation(person, relation):
    query = relation + "(X," + person + ")"
    results = kb.query(pl.Expr(query))
    if results is None or results == ['No']:
        return "No"
    valid = [r for r in results if is_valid(r, person)]
    return "Yes" if valid else "No"

def countRelation(person, relation):
    query = relation + "(X," + person + ")"
    results = kb.query(pl.Expr(query))
    if results is None or results == ['No']:
        return "0"
    unique = set(r['X'] for r in results if is_valid(r, person))
    return str(len(unique))

def getage(person):
    query = "age(" + person + ",X)"
    results = kb.query(pl.Expr(query))
    if results is None or results == ['No']:
        return "unknown"
    return str(results[0]['X'])

def show_facts():
    print("\n── Current Facts in FamilyKB.pl ──")
    with open(PL_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("%") and ":-" not in line:
                print("  " + line)

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
    qtype = bot.getPredicate("type").strip()

    if qtype == "addfact":
        fact_type = bot.getPredicate("fact").lower().strip()
        p1 = bot.getPredicate("p1").lower().strip()
        p2 = bot.getPredicate("p2").lower().strip()

        facts_to_add = build_facts(fact_type, person1, person2)

        added_any = False
        for fact_line in facts_to_add:
            success = add_fact_to_file(fact_line)
            if success:
                added_any = True
            else:
                print(f"[KB] Already exists → {fact_line}")

        if added_any:
            kb = reload_kb()
            print("Bot : Fact(s) added and knowledge base updated!\n")
        else:
            print("Bot : That fact already exists in the knowledge base.\n")

        bot.setPredicate("type", "")
        bot.setPredicate("fact", "")
        bot.setPredicate("p1", "")
        bot.setPredicate("p2", "")
        continue

    elif qtype == "showfacts":
        show_facts()
        bot.setPredicate("type", "")
        continue

    elif qtype == "whois":
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

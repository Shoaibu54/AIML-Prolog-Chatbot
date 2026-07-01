
from aiml import Kernel
from glob import glob
import os
import neo4j_kb as kb
import time
time.clock = time.perf_counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AIML_GLOB = os.path.join(BASE_DIR, "*.aiml")

bot = Kernel()

aiml_files = glob(AIML_GLOB)
if not aiml_files:
    print(f"[WARNING] No AIML files found at: {AIML_GLOB}")
else:
    for file in aiml_files:
        bot.learn(file)
    print(f"[INFO] Loaded {len(aiml_files)} AIML file(s).")


def build_facts_message(fact_type, p1, p2):
    if fact_type == "male":
        return f"male({p1})"
    if fact_type == "female":
        return f"female({p1})"
    if fact_type == "dateofbirth":
        return f"dateofbirth({p1},{p2})"
    if fact_type == "parent":
        return f"parent({p1},{p2})"
    if fact_type == "married":
        return f"married({p1},{p2})"
    return f"{fact_type}({p1},{p2})"


print("\n" + "=" * 50)
print("      Family Relationship Chatbot (Neo4j-backed)")
print("      Type 'quit' or 'exit' to stop")
print("      Type 'discover' to run inference/discovery demo")
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

    # ---- extra: demo hook for functional requirement 5 (inference/discovery) ----
    if question.lower() == "discover":
        print("\n-- Inferred cousin pairs (not explicitly stated) --")
        for row in kb.discover_cousins_not_marked():
            print(f"  {row['person1']} <-> {row['person2']}")
        print("\n-- Materializing GRANDPARENT_OF edges from 2-hop PARENT_OF chains --")
        for row in kb.infer_and_materialize_grandparents():
            print(f"  {row['grandparent']} -> {row['grandchild']}")
        print()
        continue

    bot.respond(question)

    relation = bot.getPredicate("rel").lower().strip()
    if relation and relation[-1] == "s":
        relation = relation[:-1]

    person1 = bot.getPredicate("p1").lower().strip()
    person2 = bot.getPredicate("p2").lower().strip()
    qtype = bot.getPredicate("type").strip()

    if qtype == "addfact":
        fact_type = bot.getPredicate("fact").lower().strip()
        p1 = bot.getPredicate("p1").lower().strip()
        p2 = bot.getPredicate("p2").lower().strip()

        added = kb.add_fact(fact_type, p1, p2)
        fact_line = build_facts_message(fact_type, p1, p2)

        if added:
            print(f"Bot : Fact stored in graph -> {fact_line}\n")
        else:
            print(f"Bot : That fact already exists in the graph -> {fact_line}\n")

        bot.setPredicate("type", "")
        bot.setPredicate("fact", "")
        bot.setPredicate("p1", "")
        bot.setPredicate("p2", "")
        continue

    elif qtype == "showfacts":
        kb.show_facts()
        bot.setPredicate("type", "")
        continue

    elif qtype == "whois":
        person2 = kb.getPerson(person1, relation)
        bot.setPredicate("p2", person2)

    elif qtype == "isthe":
        answer = kb.isthe_Relation(person1, relation, person2)
        bot.setPredicate("answer", answer)

    elif qtype == "does":
        answer = kb.checkRelation(person1, relation)
        bot.setPredicate("answer", answer)

    elif qtype == "howmany":
        count = kb.countRelation(person1, relation)
        bot.setPredicate("count", count)

    elif qtype == "whose":
        p1 = kb.getP1(person2, relation)
        bot.setPredicate("p1", p1)

    elif qtype == "age":
        age = kb.getage(person1)
        bot.setPredicate("age", age)

    reply = bot.respond(question)
    print(f"Bot : {reply}\n")

kb.close()

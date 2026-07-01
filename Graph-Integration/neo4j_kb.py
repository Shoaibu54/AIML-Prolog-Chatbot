from neo4j import GraphDatabase

URI = "neo4j+s://0389fd03.databases.neo4j.io"
AUTH = ("0389fd03", "XZWx3B7LnJ5CoAmVnVkK0TBWJ50hP0bKhxPyETDmyw8")
CURRENT_YEAR = 2026

driver = GraphDatabase.driver(URI, auth=AUTH)

def close():
    driver.close()

def _run(cypher, **params):
    with driver.session() as session:
        return [dict(r) for r in session.run(cypher, **params)]

REL_PATTERNS = {
    "father":       "(x:Person {gender:'male'})-[:PARENT_OF]->(y:Person {name:$p})",
    "mother":       "(x:Person {gender:'female'})-[:PARENT_OF]->(y:Person {name:$p})",
    "parent":       "(x:Person)-[:PARENT_OF]->(y:Person {name:$p})",
    "child":        "(y:Person {name:$p})-[:PARENT_OF]->(x:Person)",
    "son":          "(y:Person {name:$p})-[:PARENT_OF]->(x:Person {gender:'male'})",
    "daughter":     "(y:Person {name:$p})-[:PARENT_OF]->(x:Person {gender:'female'})",
    "husband":      "(y:Person {name:$p})-[:MARRIED_TO]->(x:Person {gender:'male'})",
    "wife":         "(y:Person {name:$p})-[:MARRIED_TO]->(x:Person {gender:'female'})",
    "spouse":       "(y:Person {name:$p})-[:MARRIED_TO]->(x:Person)",
    "married":      "(y:Person {name:$p})-[:MARRIED_TO]->(x:Person)",
    "sibling":      "(x:Person)<-[:PARENT_OF]-(:Person)-[:PARENT_OF]->(y:Person {name:$p}) WHERE x.name <> y.name WITH DISTINCT x, y",
    "brother":      "(x:Person {gender:'male'})<-[:PARENT_OF]-(:Person)-[:PARENT_OF]->(y:Person {name:$p}) WHERE x.name <> y.name WITH DISTINCT x, y",
    "sister":       "(x:Person {gender:'female'})<-[:PARENT_OF]-(:Person)-[:PARENT_OF]->(y:Person {name:$p}) WHERE x.name <> y.name WITH DISTINCT x, y",
    "grandfather":  "(x:Person {gender:'male'})-[:PARENT_OF]->(:Person)-[:PARENT_OF]->(y:Person {name:$p})",
    "grandmother":  "(x:Person {gender:'female'})-[:PARENT_OF]->(:Person)-[:PARENT_OF]->(y:Person {name:$p})",
    "grandparent":  "(x:Person)-[:PARENT_OF]->(:Person)-[:PARENT_OF]->(y:Person {name:$p})",
    "grandson":     "(y:Person {name:$p})-[:PARENT_OF]->(:Person)-[:PARENT_OF]->(x:Person {gender:'male'})",
    "granddaughter":"(y:Person {name:$p})-[:PARENT_OF]->(:Person)-[:PARENT_OF]->(x:Person {gender:'female'})",
    "grandchild":   "(y:Person {name:$p})-[:PARENT_OF]->(:Person)-[:PARENT_OF]->(x:Person)",
    "ancestor":     "(x:Person)-[:PARENT_OF*1..6]->(y:Person {name:$p})",
    "descendant":   "(y:Person {name:$p})-[:PARENT_OF*1..6]->(x:Person)",
    "cousin":       "(x:Person)<-[:PARENT_OF]-(:Person)<-[:PARENT_OF]-(:Person)-[:PARENT_OF]->(:Person)-[:PARENT_OF]->(y:Person {name:$p}) WHERE x.name <> y.name WITH DISTINCT x, y",
    "uncle":        "(x:Person {gender:'male'})<-[:PARENT_OF]-(:Person)-[:PARENT_OF]->(:Person)-[:PARENT_OF]->(y:Person {name:$p}) WHERE x.name <> y.name WITH DISTINCT x, y",
    "aunt":         "(x:Person {gender:'female'})<-[:PARENT_OF]-(:Person)-[:PARENT_OF]->(:Person)-[:PARENT_OF]->(y:Person {name:$p}) WHERE x.name <> y.name WITH DISTINCT x, y",
}

def add_fact(fact_type, p1, p2):
    """Stores a fact in the graph. Returns True if something new was created."""
    with driver.session() as session:
        if fact_type == "male":
            rec = session.run(
                "MERGE (p:Person {name:$p1}) "
                "ON CREATE SET p.gender='male', p._created=true "
                "ON MATCH SET p._created=(p.gender <> 'male') "
                "SET p.gender='male' "
                "RETURN p._created AS is_new",
                p1=p1,
            ).single()
        elif fact_type == "female":
            rec = session.run(
                "MERGE (p:Person {name:$p1}) "
                "ON CREATE SET p.gender='female', p._created=true "
                "ON MATCH SET p._created=(p.gender <> 'female') "
                "SET p.gender='female' "
                "RETURN p._created AS is_new",
                p1=p1,
            ).single()
        elif fact_type == "dateofbirth":
            try:
                year = int(p2)
            except ValueError:
                return False
            rec = session.run(
                "MERGE (p:Person {name:$p1}) "
                "ON CREATE SET p._created=true "
                "ON MATCH SET p._created=(p.dob <> $p2 OR p.dob IS NULL) "
                "SET p.dob=$p2 "
                "RETURN p._created AS is_new",
                p1=p1, p2=year,
            ).single()
        elif fact_type == "parent":
            rec = session.run(
                "MERGE (a:Person {name:$p1}) "
                "MERGE (b:Person {name:$p2}) "
                "MERGE (a)-[r:PARENT_OF]->(b) "
                "RETURN r IS NOT NULL AS is_new",
                p1=p1, p2=p2,
            ).single()
        elif fact_type == "married":
            rec = session.run(
                "MERGE (a:Person {name:$p1}) "
                "MERGE (b:Person {name:$p2}) "
                "MERGE (a)-[:MARRIED_TO]->(b) "
                "MERGE (b)-[:MARRIED_TO]->(a) "
                "RETURN true AS is_new",
                p1=p1, p2=p2,
            ).single()
        else:
            return False

        session.run("MATCH (p:Person) REMOVE p._created")
        return bool(rec["is_new"]) if rec else False

def getPerson(person, relation):
    pattern = REL_PATTERNS.get(relation)
    if not pattern:
        return "No One"
    rows = _run(f"MATCH {pattern} RETURN DISTINCT x.name AS name", p=person)
    names = [r["name"] for r in rows if r["name"] != person]
    return ", ".join(names) if names else "No One"

def getP1(person, relation):
    pattern = REL_PATTERNS.get(relation)
    if not pattern:
        return "No One"
    rows = _run(f"MATCH {pattern} RETURN DISTINCT y.name AS name", p=person)
    names = [r["name"] for r in rows if r["name"] != person]
    return ", ".join(names) if names else "No One"

def isthe_Relation(person1, relation, person2):
    if person1 == person2:
        return "No"
    pattern = REL_PATTERNS.get(relation)
    if not pattern:
        return "No"
    rows = _run(f"MATCH {pattern} WHERE x.name = $p1 RETURN x", p=person2, p1=person1)
    return "Yes" if rows else "No"

def checkRelation(person, relation):
    return "Yes" if getPerson(person, relation) != "No One" else "No"

def countRelation(person, relation):
    pattern = REL_PATTERNS.get(relation)
    if not pattern:
        return "0"
    rows = _run(f"MATCH {pattern} RETURN DISTINCT x.name AS name", p=person)
    return str(len([r for r in rows if r["name"] != person]))

def getage(person):
    rows = _run("MATCH (p:Person {name:$p}) RETURN p.dob AS dob", p=person)
    if not rows or rows[0]["dob"] is None:
        return "unknown"
    return str(CURRENT_YEAR - rows[0]["dob"])

def show_facts():
    print("\n-- Current Facts in Neo4j --")
    for r in _run("MATCH (p:Person) RETURN p.name AS name, p.gender AS gender, p.dob AS dob ORDER BY p.name"):
        print(f"  Person({r['name']}, gender={r['gender']}, dob={r['dob']})")
    for r in _run(
        "MATCH (a:Person)-[rel]->(b:Person) "
        "RETURN a.name AS a, type(rel) AS t, b.name AS b ORDER BY t, a"
    ):
        print(f"  {r['t']}({r['a']}, {r['b']})")

def discover_cousins_not_marked():
    return _run(
        "MATCH (x:Person)<-[:PARENT_OF]-(px)<-[:PARENT_OF]-(gp)-[:PARENT_OF]->(py)-[:PARENT_OF]->(y:Person) "
        "WHERE px.name <> py.name AND x.name <> y.name AND x.name < y.name "
        "RETURN DISTINCT x.name AS person1, y.name AS person2"
    )

def mutual_connections(p1, p2):
    return _run(
        "MATCH (a:Person {name:$p1})--(m:Person)--(b:Person {name:$p2}) "
        "WHERE a.name <> b.name AND m.name <> a.name AND m.name <> b.name "
        "RETURN DISTINCT m.name AS mutual",
        p1=p1, p2=p2,
    )

def infer_and_materialize_grandparents():
    _run(
        "MATCH (x:Person)-[:PARENT_OF]->()-[:PARENT_OF]->(y:Person) "
        "MERGE (x)-[:GRANDPARENT_OF]->(y)"
    )
    return _run("MATCH (x)-[:GRANDPARENT_OF]->(y) RETURN x.name AS grandparent, y.name AS grandchild")

def clear_all():
    _run("MATCH (n) DETACH DELETE n")

# Family Relations Expert System & Chatbot

A hybrid Artificial Intelligence conversational agent that combines **AIML (Artificial Intelligence Markup Language)** for natural language pattern matching with a **Prolog-based knowledge base** for symbolic reasoning. 

This CLI-based chatbot allows users to query complex family trees, deduce relationships dynamically, and retrieve biographical data through natural conversation.

## 🧠 Architecture
This project leverages a dual-layer architecture:
* **Natural Language Interface:** Uses Python's `aiml` library to parse user inputs, handle greetings, and extract relationship variables/predicates. 
* **Symbolic Reasoning Engine:** Uses `pytholog` to parse a Prolog file (`FamilyKB.pl`). It computes generational logic, dynamically resolving queries like "Who is the uncle of X?" or "How many siblings does Y have?" rather than relying on hardcoded responses.
* **Robust Variable Mapping:** Features carefully structured AIML star index assignments to accurately handle relationship tracking, including strict edge-case handling for "No" or empty responses.

## 🚀 Features
* **Relationship Deduction:** Query direct and indirect relationships (e.g., grandfather, cousin, uncle, niece, brother-in-law).
* **Quantity Queries:** Ask how many relatives a specific person has (e.g., "How many children does Bashir have?").
* **Age Calculation:** Dynamically calculates ages based on birth years stored in the knowledge base.
* **Conversational Parsing:** Understands various sentence structures (e.g., "Who is X of Y?", "Whose X is Y?", "Does X have a Y?").

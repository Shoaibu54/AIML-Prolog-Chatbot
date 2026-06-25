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

## 📁 Project Structure
- `README.md` - Project overview and usage information.
- `terminal_bot.py` - Main Python CLI bot that loads AIML files and the Prolog knowledge base.
- `FamilyKB.pl` - Prolog file storing family facts, predicates, and relationships.
- `Chatbot-Greetings.aiml` - AIML patterns for greetings, help, and basic chatbot replies.
- `Chatbot-retreive.aiml` - AIML patterns for querying relationships, age, and yes/no family questions.
- `Chatbot-Greetings.aiml` - AIML patterns for greeting messages and introductory conversation.

- `Add-Facts/` - Contains an extended example of the chatbot with add-facts support and its own terminal interface.

## 🔧 How It Works
1. `terminal_bot.py` initializes an AIML `Kernel` and loads AIML scripts.
2. It also loads `FamilyKB.pl` through `pytholog` to create a Prolog knowledge base.
3. User input is passed to AIML, which sets control predicates such as `type`, `fact`, `rel`, `p1`, and `p2`.
4. Based on the extracted type, the bot performs one of the following actions:
   * `addfact` — builds a Prolog fact and appends it to `FamilyKB.pl`, then reloads the knowledge base.
   * `showfacts` — prints current facts from `FamilyKB.pl`.
   * `whois`, `isthe`, `does`, `howmany`, `age`, `whose` — queries the knowledge base and generates a response.
5. The AIML reply and Prolog query result are combined to respond naturally in the terminal.

## Add-Facts Folder Description
The `Add-Facts` folder contains a working example designed to demonstrate adding facts interactively:
* `terminal_bot.py` — A Python terminal bot that integrates the AIML files and Prolog KB, enabling users to enter new family facts or ask queries.
* `Chatbot-addfacts.aiml` — AIML patterns for adding new facts such as gender, parent relationships, birthdates, and marriages.
* `Chatbot-greetings.aiml` — AIML greeting templates for conversation starters and help responses.
* `Chatbot-retreive.aiml` — AIML patterns for retrieving facts, checking relationships, and asking age or count-based questions.
* `FamilyKB.pl` — The Prolog fact database used by the bot to answer queries and store added facts.
* `Defect.txt` — Notes about known issues or current limitations of the implementation.

## ▶️ Running the Bot
From the project root or `Add-Facts` folder, run:

```bash
python terminal_bot.py
```

Then try examples such as:
* `hello`
* `Ali is male`
* `Ali is parent of Zaid`
* `Who is the parent of Zaid?`
* `Show facts`
* `What is the age of Ali?`
* `Does Ali have a parent?`

# Add-Facts Folder

This folder contains files used for the AIML/Prolog chatbot example that demonstrates adding facts, greeting users, and retrieving information.

## Files

- `Chatbot-addfacts.aiml`
  - AIML script used for handling user interactions related to adding new facts to the knowledge base.

- `Chatbot-greetings.aiml`
  - AIML script that manages greeting messages and conversational openings for the chatbot.

- `Chatbot-retreive.aiml`
  - AIML script responsible for retrieving and responding with stored information from the knowledge base.

- `Defect.txt`
  - Notes or known issues related to this version of the chatbot implementation.

- `FamilyKB.pl`
  - Prolog knowledge base file used by the chatbot to store and query family relationship facts.

- `terminal_bot.py`
  - Python terminal chatbot interface that integrates with the AIML scripts and Prolog knowledge base.

## Usage

To run the chatbot from this folder:

```bash
cd Add-Facts
python terminal_bot.py
```

Example terminal interactions after starting the bot:

- `hello`
  - Bot: `Hello! Ask me about family relations!`
- `Ali is a male`
  - Bot: `Got it! Ali is male.`
- `Ali is parent of Zaid`
  - Bot: `Got it! Ali is the parent of Zaid.`
- `Who is the parent of Zaid?`
  - Bot: `Zaid is parent of Ali.` 
- `Show facts`
  - Bot: `Okay, let me show you the current facts in the knowledge base.`
  - Then the bot prints current facts from `FamilyKB.pl`.

These commands demonstrate greetings, fact addition, and fact retrieval via the integrated AIML and Prolog files.

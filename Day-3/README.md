# Day 3 - Your First Agent: Secure Password Assistant

## Task

Rebuild the Secure Password Assistant using LangChain, add conversation memory, and test it with a CSV file.

## What `task.py` does

1. **LangChain chain**: `ChatPromptTemplate | ChatGroq | StrOutputParser`.
2. **Memory**: `MessagesPlaceholder("history")` and an `ask()` function to remember previous conversations.
3. **Password Security Guidance**: Explains strong passwords, password length, phishing, and password safety.
4. **Tests**: `run_tests()` reads `test.csv` (`question`, `must_include`), checks responses, and prints the pass rate.
5. **Agent sneak peek**: `create_agent(model, tools=[], system_prompt=SYSTEM)` creates a basic AI agent without tools.

## Run

```bash
pip install langchain langchain-groq
export GROQ_API_KEY="your_key"
python task.py
```

## Results

| Run | Prompt change | Temperature | Pass rate |
|---|---|---|---|
| 1 | Baseline | 0.3 | *Fill in* |
| 2 | Improved security instructions | 0.3 | *Fill in* |
| 3 | Baseline | 1.0 | *Fill in* |
| 4 | Baseline | 1.0 | *Fill in* |

## Agent or not? (My Use Case)

| Job | Type |
|---|---|
| Explain strong password rules | One LLM call |
| Recommend password length | One LLM call |
| Explain phishing attacks | One LLM call |
| Generate a password using secure random code | Plain code |
| Check password strength using predefined rules | Plain code |
| Generate, evaluate and explain a password using tools | Agent |

## Key Learnings

- A chatbot answers questions, while an agent can decide steps and use tools.
- LangChain connects prompts, LLMs and output parsers.
- Memory helps the assistant remember previous conversations.
- CSV testing helps measure response quality.
- Temperature affects the creativity and consistency of responses.

## Before Day 4

Prepare two Python functions with type hints and docstrings:

1. `generate_password()` – Generates a random password using Python's secure random module.
2. `check_password_strength()` – Checks password length, uppercase, lowercase, numbers and special characters.

These functions can become tools for the Secure Password Assistant on Day 4.

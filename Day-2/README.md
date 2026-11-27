# Day 2 - Prompts, Memory and the Python Agent

## Project: Secure Password Assistant

### Task

Turn the Day-1 single API call into a real **Secure Password Assistant chatbot** that understands cybersecurity questions, remembers the conversation context, provides password safety guidance, and handles errors without crashing.

## What `task.py` does

- **Structured system prompt:** Uses ROLE, FACTS, RULES and FORMAT to define the assistant's behaviour.
- **Dictionary:** `PASSWORD_GUIDE` stores password security rules, such as minimum length, recommended length, requirements and common passwords to avoid. The dictionary is injected into the system prompt using `json.dumps`.
- **Function with type hints and docstring:** `analyze_password(password: str) -> dict` checks password characteristics locally and returns a strength assessment with suggestions.
- **Decorator:** `@log_call` logs function calls without displaying password arguments.
- **Memory by hand:** A `history` list stores system, user and assistant messages. It is trimmed to the last `MAX_TURNS` messages before sending the conversation to the model.
- **Few-shot examples:** Provides sample cybersecurity questions and answers to guide the assistant's responses.
- **Error handling:** Uses `try/except` to handle `RateLimitError`, `AuthenticationError`, `APIConnectionError` and other API errors.
- **JSON output:** `extract_request()` asks the AI model to return structured JSON containing the user's intent, topic, summary and whether a local password check is required. The response is parsed using `json.loads`.
- **Password checking:** The `/check` command performs a basic local password-strength check without sending the entered password to the AI model.

## Run
```
pip install openai
export GROQ_API_KEY="your_key"
$env:GROQ_API_KEY="your_key"
python task.py
```
## Key Learnings

- **Messages and roles:** Understand system, user and assistant messages.
- **Structured prompts:** Use ROLE, FACTS, RULES and FORMAT to control AI behaviour.
- **Few-shot prompting:** Give examples so the model understands the expected response.
- **Memory:** Store previous messages in a Python list to maintain conversation context.
- **Dictionaries and JSON:** Store password security guidelines in a dictionary and convert structured data using `json.dumps` and `json.loads`.
- **Functions and type hints:** Create reusable Python functions with clear input and output types.
- **Decorators:** Use decorators to log function calls.
- **Error handling:** Handle API errors and invalid responses using `try/except`.
- **Password security:** Perform basic password checks locally instead of sending real passwords to an AI model.

## Before Day 3

Prepare the following:

1. **10 cybersecurity customer questions** that users may ask the Secure Password Assistant.
2. **Password security catalogue** as a Python dictionary containing password rules, recommended length, security requirements and common password patterns to avoid.








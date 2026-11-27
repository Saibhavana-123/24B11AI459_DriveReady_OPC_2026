# Day 4 - Building Tools for Secure Password Assistant

## Task

Extend the Secure Password Assistant using LangChain custom tools. Enable the AI agent to generate secure passwords, check password strength, and provide cybersecurity tips.

## What `task.py` does

1. **Groq LLM**: Connects the Secure Password Assistant to the Groq API.
2. **Password Generation**: `generate_password()` creates random passwords using Python's `secrets` module.
3. **Password Strength Checker**: `check_password_strength()` evaluates password length, uppercase, lowercase, numbers, and special characters.
4. **Security Tips**: `get_security_tips()` provides password safety recommendations.
5. **AI Agent**: `create_agent()` allows the LLM to select and execute the appropriate tools.
6. **Memory**: The `chat()` function maintains conversation history.

## Run

Install dependencies:

```bash
pip install langchain langchain-groq
```
## Results

| Test | Expected Result |
|---|---|
| Generate password | Random secure password |
| Check password | Weak / Medium / Strong |
| Get security tips | Password safety recommendations |
| Memory demo | Remembers conversation context |

## Agent or not? (My Use Case)

| Job | Type |
|---|---|
| Generate a random password | Plain code |
| Check password strength | Plain code |
| Explain password security | One LLM call |
| Select and execute the required security tool | Agent |

## Key Learnings

- Custom Python functions can be converted into LangChain tools.
- AI agents select tools based on user requests.
- Python's `secrets` module generates cryptographically secure random values.
- Password strength checking helps identify weak passwords.
- Conversation memory maintains previous interactions.

## Before Day 5
Improve the Secure Password Assistant by adding more cybersecurity tools and testing the agent with different user requests.

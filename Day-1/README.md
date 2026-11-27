# Day 1 - How LLMs Work and Your First API Call

## Task

Build a first API call to an LLM through Groq and explore how it behaves using the **SecurePass AI – Password Security Assistant** use case.

## What `Task-1.py` does

| # | Experiment | What to observe |
|---|---|---|
| 1 | System prompt (role, facts, rules) | The assistant follows password security rules |
| 2 | Temperature 0.2 vs 1.2 | Low = consistent, high = varied responses |
| 3 | Remove security facts | The assistant should avoid inventing unknown college policies |
| 4 | Separate calls vs conversation history | The model has no built-in memory; code must resend history |

## Run

```bash
pip install langchain-groq
```

Set your Groq API key in Windows PowerShell:

```powershell
$env:GROQ_API_KEY="your_key"
```

Run the Python file:

```bash
py Task-1.py
```

## Key Learnings

- An LLM generates responses based on the input and context.
- System prompts guide the assistant's behaviour.
- Facts and rules help reduce hallucinations.
- Temperature controls creativity and consistency.
- Memory is not built in; previous messages must be sent again.

## Before Day 2

Write down 10 common password security questions users may ask SecurePass AI.








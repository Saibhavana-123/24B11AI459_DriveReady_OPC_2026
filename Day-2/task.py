"""Day 2 - Prompts, memory and the Python agents need.

Builds the Secure Password Assistant chatbot: structured system prompt,
password security dictionary, documented function, hand-made memory
with trimming, error handling, and JSON request extraction.

Setup:
    pip install openai
    export GROQ_API_KEY="your_key"
"""

import functools
import json
import os

from openai import (APIConnectionError,APIError,AuthenticationError,OpenAI,RateLimitError,
)
# Groq API connection
client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)

MODEL = "openai/gpt-oss-120b"
MAX_TURNS = 8  

# Dictionary: Password security guidelines
PASSWORD_GUIDE = {
    "minimum_length": 12,
    "recommended_length": 16,
    "requirements": [
        "Use a combination of uppercase and lowercase letters",
        "Include numbers and special characters",
        "Use a unique password for every account",
        "Avoid personal information",
        "Enable multi-factor authentication",
    ],
    "avoid": [
        "123456",
        "password",
        "qwerty",
        "admin",
        "your name",
        "date of birth",
    ],
}

# Structured system prompt
SYSTEM = f"""
ROLE:
You are a friendly and helpful Secure Password Assistant.
You provide basic cybersecurity and password safety guidance.

FACTS:
Password security guidelines:
{json.dumps(PASSWORD_GUIDE, indent=2)}

RULES:
1. Never ask users to share their real account passwords.
2. Never encourage users to reuse passwords.
3. Recommend unique passwords for every account.
4. Explain cybersecurity concepts in simple English.
5. Recommend multi-factor authentication.
6. Do not claim that a password is completely secure.
7. Password strength checking must be performed locally.
8. If a question is outside your knowledge, say so honestly.

FORMAT:
Give clear, short and beginner-friendly answers.
Use bullet points when necessary.
Match the user's language where possible.
"""

# Decorator: Logs function calls without printing password arguments
def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"   [log] {func.__name__} called successfully")
        return result
    return wrapper

# Function: Check password characteristics locally
@log_call
def analyze_password(password: str) -> dict:
    """
    Analyze basic password characteristics locally.

    Args:
        password: A sample password entered by the user.

    Returns:
        A dictionary containing score, strength and suggestions.
    """

    score = 0
    suggestions = []

    if len(password) >= PASSWORD_GUIDE["minimum_length"]:
        score += 1
    else:
        suggestions.append("Use at least 12 characters.")

    if len(password) >= PASSWORD_GUIDE["recommended_length"]:
        score += 1
    else:
        suggestions.append("Consider using 16 or more characters.")

    if any(char.isupper() for char in password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    if any(char.islower() for char in password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    if any(char.isdigit() for char in password):
        score += 1
    else:
        suggestions.append("Add numbers.")

    if any(not char.isalnum() for char in password):
        score += 1
    else:
        suggestions.append("Add special characters.")

    common_passwords = {
        "123456",
        "password",
        "qwerty",
        "admin",
        "12345678",
    }

    if password.lower() in common_passwords:
        score = 0
        suggestions.append("Avoid common passwords.")

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return {
        "score": score,
        "maximum_score": 6,
        "strength": strength,
        "suggestions": suggestions,
    }

# Few-shot examples: guide the assistant's responses
FEW_SHOT_EXAMPLES = [
    {
        "role": "user",
        "content": "How can I create a strong password?"
    },
    {
        "role": "assistant",
        "content": (
            "Use a unique password with at least 12 characters. "
            "A longer passphrase is a good option. Avoid personal information."
        )
    },
    {
        "role": "user",
        "content": "Should I use the same password everywhere?"
    },
    {
        "role": "assistant",
        "content": (
            "No. Use a different password for every account. "
            "A password manager can help you manage them."
        )
    },
    {
        "role": "user",
        "content": "What is MFA?"
    },
    {
        "role": "assistant",
        "content": (
            "MFA means Multi-Factor Authentication. "
            "It adds another verification step when you log in."
        )
    },
]

# Memory by hand: store previous messages
history = [
    {"role": "system", "content": SYSTEM}
]

def chat(user_text: str) -> str:
    """
    Send a user message to the AI and maintain conversation memory.
    """

    history.append({
        "role": "user",
        "content": user_text
    })

    # Keep system prompt, few-shot examples and recent conversation
    recent = [history[0]] + history[1:][-MAX_TURNS:]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=FEW_SHOT_EXAMPLES + recent,
            temperature=0.3,
        )

        reply = response.choices[0].message.content or (
            "Sorry, I could not generate a response."
        )

    except RateLimitError:
        reply = "The service is busy. Please try again later."

    except AuthenticationError:
        reply = "API authentication failed. Please check your Groq API key."

    except APIConnectionError:
        reply = "I cannot connect to the server. Check your internet connection."

    except APIError:
        reply = "An API error occurred. Please try again."

    history.append({
        "role": "assistant",
        "content": reply
    })

    return reply

# JSON output: Extract structured information from a cybersecurity request
def extract_request(text: str) -> dict | None:
    """
    Ask the AI to classify a cybersecurity request and return JSON.
    """

    prompt = f"""
Analyze this cybersecurity request.

Return ONLY valid JSON with these keys:
intent, topic, summary, requires_local_password_check.

Use a boolean (true or false) for requires_local_password_check.

User request: {text}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            temperature=0,
            messages=[
                {"role": "system", "content": (
                    "You are a cybersecurity request classifier. "
                    "Return only valid JSON."
                )},
                {"role": "user", "content": prompt},
            ],
        )

        raw = (response.choices[0].message.content or "").strip()

        raw = (
            raw.removeprefix("```json")
               .removeprefix("```")
               .removesuffix("```")
               .strip()
        )

        return json.loads(raw)

    except json.JSONDecodeError:
        print("Model did not return valid JSON.")
        return None

    except (RateLimitError, AuthenticationError, APIConnectionError, APIError):
        print("Could not extract the request because of an API error.")
        return None

# Demo function
def demo():
    print("\n--- Password Analysis Demo ---")

    # Use only a fictional sample password, never a real account password
    sample = "DemoPass@12345"

    result = analyze_password(sample)
    print("Password analysis:", result)

    print("\n--- JSON Request Demo ---")

    request = "How can I protect my email account from hackers?"

    print("User request:", request)
    print("Extracted JSON:", extract_request(request))

# Main chatbot
if __name__ == "__main__":

    demo()

    print("\n====================================")
    print("   SECURE PASSWORD ASSISTANT")
    print("====================================")

    print("Ask me cybersecurity questions.")
    print("Type 'bye' to quit.")
    print("Type '/reset' to clear conversation memory.")
    print("Type '/json <message>' to extract request information.")

    while True:

        text = input("\nYou: ").strip()

        if text.lower() in ("bye", "exit", "quit"):
            print("Bot: Stay safe online. Goodbye!")
            break
          
        elif text == "/reset":
            history.clear()
            history.append({
                "role": "system",
                "content": SYSTEM
            })
            print("Bot: Conversation memory has been reset.")

        elif text.startswith("/json "):
            request_text = text[6:]
            print("Bot:", extract_request(request_text))

        elif not text:
            print("Bot: Please enter a question.")
            
        else:
            print("Bot:", chat(text))

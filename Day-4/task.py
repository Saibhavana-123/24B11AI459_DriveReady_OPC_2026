# ============================================================
# DAY 4 - SECURE PASSWORD ASSISTANT
# AI Agent with LangChain and Custom Cybersecurity Tools
# ============================================================

!pip install -q langchain langchain-groq

import os
import secrets
import string

from google.colab import userdata
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent

# 1. GROQ API SETUP
api_key = userdata.get("GROQ_API_KEY")

if not api_key:
    raise ValueError("Please add GROQ_API_KEY in Colab Secrets.")

os.environ["GROQ_API_KEY"] = api_key

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.2,
    max_retries=3
)

# 2. PASSWORD GENERATION TOOL

@tool
def generate_password(length: int = 16) -> str:
    """Generate a secure random password.

    Args:
        length: Password length between 12 and 64 characters.
    """
    if not 12 <= length <= 64:
        return "Password length must be between 12 and 64."

    # Use Python's cryptographically secure random generator
    chars = (
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits +
        "!@#$%^&*"
    )

    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*")
    ]

    password += [
        secrets.choice(chars) for _ in range(length - 4)
    ]

    secrets.SystemRandom().shuffle(password)

    return "Generated secure password: " + "".join(password)

# 3. PASSWORD STRENGTH CHECKER TOOL

@tool
def check_password_strength(password: str) -> str:
    """Evaluate password strength using basic security rules.

    Args:
        password: A sample or test password to evaluate.
    """
    score = 0
    suggestions = []

    if len(password) >= 12:
        score += 1
    else:
        suggestions.append("Use at least 12 characters.")

    if any(c.isupper() for c in password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    if any(c.islower() for c in password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        suggestions.append("Add numbers.")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        suggestions.append("Add special characters.")

    if score == 5:
        strength = "Strong"
    elif score >= 3:
        strength = "Medium"
    else:
        strength = "Weak"

    result = f"Password strength: {strength} ({score}/5)"

    if suggestions:
        result += "\nSuggestions:\n" + "\n".join(suggestions)

    return result

# 4. PASSWORD SECURITY TIPS TOOL

@tool
def get_security_tips() -> str:
    """Provide important password security recommendations."""

    return """
    1. Use at least 12 characters.
    2. Use uppercase and lowercase letters.
    3. Include numbers and special characters.
    4. Never reuse passwords across websites.
    5. Enable Two-Factor Authentication (2FA).
    6. Never share passwords with others.
    7. Use a trusted password manager.
    """

# 5. CREATE AI AGENT

SYSTEM = """
ROLE:
You are a friendly Secure Password Assistant.

PURPOSE:
Help users create strong passwords and understand cybersecurity.

TOOLS:
- generate_password: Generate secure random passwords.
- check_password_strength: Evaluate password strength.
- get_security_tips: Provide password security advice.

RULES:
1. Use generate_password when users request a new password.
2. Use check_password_strength for sample password evaluation.
3. Use get_security_tips for password security guidance.
4. Never store or log passwords.
5. Never ask users to share their real passwords.
6. Tell users to use sample passwords for strength testing.
7. Explain security concepts in simple English.

FORMAT:
Give short, clear and beginner-friendly answers.
"""

agent = create_agent(
    model=llm,
    tools=[
        generate_password,
        check_password_strength,
        get_security_tips
    ],
    system_prompt=SYSTEM
)

# 6. CONVERSATION MEMORY

history = []

def chat(text: str) -> str:
    global history

    try:
        result = agent.invoke({
            "messages": history + [
                {"role": "user", "content": text}
            ]
        })

        history = result["messages"]

        return history[-1].content

    except Exception as e:
        print("Agent error:", e)
        return "Sorry, something went wrong. Please try again."

# 7. TEST THE SECURE PASSWORD ASSISTANT

print("--- Password Generation ---")
print(chat("Generate a secure password of 16 characters."))

print("\n--- Password Strength ---")
print(chat("Check this sample password: Test@123"))

print("\n--- Security Tips ---")
print(chat("Give me important password security tips."))

print("\n--- Memory Demo ---")
print(chat("What can you help me with?"))

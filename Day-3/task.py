"""Day 3 - Your First Agent: Secure Password Assistant

Features:
1. LangChain Prompt Template
2. Groq LLM Integration
3. Conversation Memory
4. CSV Test Suite
5. First Agent using create_agent

Setup:
    pip install langchain langchain-groq

Set GROQ_API_KEY in your environment.
"""

import csv
import os

from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq

if "GROQ_API_KEY" not in os.environ:
    raise SystemExit("Please set your GROQ_API_KEY first.")

TEMPERATURE = 0.3

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=TEMPERATURE
)

SYSTEM = """
ROLE: You are a friendly Secure Password Assistant.

PURPOSE:
Help users understand password security and create strong passwords.

RULES:
1. Explain how to create strong passwords.
2. Recommend at least 12 characters.
3. Suggest uppercase, lowercase, numbers and symbols.
4. Never ask users to share their real passwords.
5. Explain common password attacks and prevention.
6. Never claim that a password is 100% secure.
7. Keep answers short, simple and beginner-friendly.

FORMAT:
Answer in simple English using clear security tips.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    MessagesPlaceholder("history"),
    ("human", "{question}")
])

chain = prompt | llm | StrOutputParser()


# Conversation Memory
history = []


def ask(question: str) -> str:
    """Ask cybersecurity questions with conversation memory."""

    answer = chain.invoke({
        "history": history,
        "question": question
    })

    history.extend([
        ("human", question),
        ("ai", answer)
    ])

    return answer


# CSV Testing
def run_tests(path="test.csv"):
    """Test password security knowledge using CSV questions."""

    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    passed = 0

    for row in rows:
        answer = chain.invoke({
            "history": [],
            "question": row["question"]
        })

        ok = row["must_include"].lower() in answer.lower()
        passed += ok

        print(
            "PASS" if ok else "FAIL",
            "|", row["question"],
            "->", answer[:70]
        )

    rate = passed / len(rows) if rows else 0

    print(f"\n{passed}/{len(rows)} passed ({rate:.0%})")

    return rate

# First Agent Demo
def agent_demo():
    """Create a basic agent without tools."""

    agent = create_agent(
        model=llm,
        tools=[],
        system_prompt=SYSTEM
    )

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "What are the characteristics of a strong password?"
            }
        ]
    })

    print(result["messages"][-1].content)

if __name__ == "__main__":

    print("--- Memory Demo ---")

    print(ask("What is a strong password?"))

    print(ask("How many characters should it contain?"))

    print("\n--- CSV Tests ---")

    run_tests()

    print("\n--- Agent Demo ---")

    agent_demo()

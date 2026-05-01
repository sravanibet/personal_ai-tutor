from src.model.ollama_client import OllamaClient
from src.utils.config import CONFIG

client = OllamaClient(CONFIG.ollama_base_url)


def evaluate_answer(question, student_answer):
    prompt = f"""
You are a tutor evaluating a student's answer.

Question:
{question}

Student Answer:
{student_answer}

Evaluate it:

- Say if it's correct, partially correct, or incorrect
- Explain why in simple terms
- Be encouraging
"""

    response = client.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return response


def evaluate_quiz_answer(quiz_text, student_answer):
    prompt = f"""
You are a tutor checking a student's answers to a multiple-choice quiz.

Quiz:
{quiz_text}

Student Answers:
{student_answer}

Evaluate the answers using this format:

Overall: Correct, Partially Correct, or Incorrect
Question 1: Correct or Wrong - short reason
Question 2: Correct or Wrong - short reason
Correct Answers: list the correct options only at the end

Rules:
- Be concise
- Explicitly use the word "Wrong" for wrong answers
- Do not restate the full quiz
- If the student's format is unclear, say that first and ask them to answer like 1:A, 2:C
"""

    response = client.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response
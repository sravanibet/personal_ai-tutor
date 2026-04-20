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
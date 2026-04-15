from typing import List, Dict, Optional


def build_system_prompt(difficulty: str, mode: str) -> str:
    difficulty_map = {
        "Beginner": "Use very simple language, define terms clearly, and avoid unnecessary jargon.",
        "Intermediate": "Use moderate technical detail, explain the intuition, and connect concepts clearly.",
        "Advanced": "Use precise ML terminology, deeper reasoning, and mathematical intuition where useful.",
    }

    mode_map = {
        "Explain": "Teach the concept step by step and give an example when useful.",
        "Quiz": "Teach briefly, then ask one short quiz question and provide the answer at the end.",
        "Hint": "Do not give the full answer immediately. Give a useful hint first.",
    }

    difficulty_text = difficulty_map.get(difficulty, difficulty_map["Beginner"])
    mode_text = mode_map.get(mode, mode_map["Explain"])

    return f"""
You are an AI tutor specialized in Machine Learning.

Your job is to help students understand machine learning concepts from simple to complex.
Be patient, accurate, and educational.

Guidelines:
- Focus on Machine Learning topics unless supporting math or programming concepts are needed.
- Prefer teaching over giving short generic answers.
- Be clear and structured.
- Break answers into simple steps when helpful.
- If the question is ambiguous, ask one short clarifying question.

Difficulty mode:
{difficulty_text}

Tutor mode:
{mode_text}
""".strip()


def build_messages(
    user_question: str,
    difficulty: str,
    mode: str,
    chat_history: Optional[List[Dict[str, str]]] = None,
) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": build_system_prompt(difficulty, mode)}
    ]

    if chat_history:
        messages.extend(chat_history)

    messages.append({"role": "user", "content": user_question})
    return messages

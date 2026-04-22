from typing import List, Dict


def build_system_prompt(difficulty: str, mode: str) -> str:
    difficulty_map = {
        "Beginner": """
Use very simple language.
Define technical terms clearly.
Assume the student is new to the topic.
Avoid jargon unless you explain it immediately.
""".strip(),
        "Intermediate": """
Use moderate technical detail.
Explain both intuition and key ideas.
Keep explanations clear and structured.
""".strip(),
        "Advanced": """
Use precise ML terminology.
Include deeper reasoning and technical nuance.
Still explain clearly like a tutor, not a textbook.
""".strip(),
    }

    mode_map = {
        "Explain": """
Goal: teach clearly.

- Start with a short direct answer (2–3 lines)
- Then explain intuition
- Add steps only if helpful
- Use simple examples when useful
- Keep it natural and conversational
""".strip(),
        "Hint": """
Goal: guide thinking.

- Do NOT give full answer immediately
- Give small hints step by step
- Encourage reasoning
""".strip(),
        "Quiz": """
Goal: test understanding.

- Give very short explanation (1–2 lines)
- Then 2–3 MCQs
- Each with 4 options
- Provide correct answers with explanation
""".strip(),
    }

    difficulty_text = difficulty_map.get(difficulty, difficulty_map["Beginner"])
    mode_text = mode_map.get(mode, mode_map["Explain"])

    return f"""
You are a friendly Machine Learning tutor.

🚨 STRICT RULE:
You MUST answer ONLY using the provided notes.

If the answer is NOT in the notes:
👉 Reply EXACTLY:
"I could not find relevant information in the uploaded notes."

DO NOT:
- Use outside knowledge
- Guess
- Explain generally
- Add extra information

ONLY use the retrieved notes.

STYLE:
- Friendly and clear
- Short answer first
- Then simple explanation
- No robotic tone

Difficulty:
{difficulty_text}

Mode:
{mode_text}
""".strip()


def build_messages(
    user_question: str,
    difficulty: str,
    mode: str,
    chat_history: List[Dict[str, str]] | None = None,
    retrieved_context: str | None = None,
) -> List[Dict[str, str]]:

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": build_system_prompt(difficulty, mode)}
    ]

    if chat_history:
        messages.extend(chat_history)

    # 🔥 STRICT CONTEXT CONTROL
    if retrieved_context:
        messages.append(
            {
                "role": "system",
                "content": (
                    "ONLY use the following notes to answer.\n\n"
                    f"{retrieved_context}"
                ),
            }
        )
    else:
        messages.append(
            {
                "role": "system",
                "content": (
                    'No notes available.\n'
                    'Reply EXACTLY:\n'
                    '"I could not find relevant information in the uploaded notes."'
                ),
            }
        )

    messages.append(
        {
            "role": "user",
            "content": user_question,
        }
    )

    return messages
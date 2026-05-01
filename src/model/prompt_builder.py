from typing import List, Dict, Optional


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

    - Do NOT give the final answer
    - Give 1 to 3 short hints only
    - Start broad, then get slightly more specific
    - Encourage the student to try answering after the hints
""".strip(),
        "Quiz": """
Goal: test understanding.

- Output only the quiz
- Write exactly 2 multiple-choice questions
- Use this format exactly:
    1. question text
    A) option text
    B) option text
    C) option text
    D) option text
    2. question text
    A) option text
    B) option text
    C) option text
    D) option text
- Do NOT include answers
- Do NOT include explanations
- Do NOT include intro text before the questions
""".strip(),
    }

    difficulty_text = difficulty_map.get(difficulty, difficulty_map["Beginner"])
    mode_text = mode_map.get(mode, mode_map["Explain"])

    return f"""
You are a friendly Machine Learning tutor.

Answer ONLY using the provided notes from the student's document.
If notes are provided, base your entire answer on them.
If no notes are provided, say: "Please upload your notes first so I can answer from your material."

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
    chat_history: Optional[List[Dict[str, str]]] = None,
    retrieved_context: Optional[str] = None,
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
                "content": "No notes have been uploaded. Ask the student to upload their document first.",
            }
        )

    messages.append(
        {
            "role": "user",
            "content": user_question,
        }
    )

    return messages
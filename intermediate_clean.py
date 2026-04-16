import json
import re
from pathlib import Path

INPUT_FILE = r"C:\Users\rashm\Downloads\ml_tutor_chatbot\project_ai_tutor_dataset\project_ai_tutor_full.jsonl"
OUTPUT_FILE = r"C:\Users\rashm\Downloads\ml_tutor_chatbot\project_ai_tutor_dataset\intermediate_clean_v2.jsonl"

INTERMEDIATE_PATTERNS = [
    r"\bcompare\b",
    r"\bdifference between\b",
    r"\bhow does\b",
    r"\bwhy does\b",
    r"\bwhy is\b",
    r"\bwhen should i use\b",
    r"\bwhen to use\b",
    r"\btrade[- ]?off\b",
    r"\bintuition\b",
    r"\bworkflow\b",
    r"\bprocess\b",
    r"\bpractical example\b",
    r"\bexample with\b",
    r"\bclassification\b",
    r"\bregression\b",
    r"\boverfitting\b",
    r"\bunderfitting\b",
    r"\bcross[- ]validation\b",
    r"\bfeature engineering\b",
    r"\bconfusion matrix\b",
    r"\bprecision\b",
    r"\brecall\b",
    r"\bf1\b",
    r"\bgradient descent\b",
    r"\bloss function\b",
    r"\bhow to\b",
    r"\bsteps\b",
    r"\buse case\b",
    r"\bapplications\b",
    r"\badvantages\b",
    r"\bdisadvantages\b",
]

BAD_PHRASES = [
    "a related machine learning concept",
    "it is unrelated to learning from data",
]

def is_intermediate_prompt(user_text: str) -> bool:
    text = user_text.lower()
    return any(re.search(pattern, text) for pattern in INTERMEDIATE_PATTERNS)

def is_bad_response(text: str) -> bool:
    lower = text.lower().strip()

    if any(bad in lower for bad in BAD_PHRASES):
        return True

    # relaxed threshold to keep more useful intermediate answers
    if len(text.split()) < 12:
        return True

    if lower in {"ok", "yes", "no", "sure", "fine"}:
        return True

    return False

def extract_roles(messages):
    system_msg = ""
    user_msg = ""
    assistant_msg = ""

    for msg in messages:
        role = msg.get("role", "").strip().lower()
        content = msg.get("content", "").strip()

        if role == "system":
            system_msg = content
        elif role == "user":
            user_msg = content
        elif role == "assistant":
            assistant_msg = content

    return system_msg, user_msg, assistant_msg

def main():
    input_path = Path(INPUT_FILE)
    output_path = Path(OUTPUT_FILE)

    kept = []
    seen_users = set()

    total = 0
    candidates = 0
    removed_duplicates = 0
    removed_bad = 0
    skipped_incomplete = 0

    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            total += 1

            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                skipped_incomplete += 1
                continue

            messages = record.get("messages", [])
            if not messages:
                skipped_incomplete += 1
                continue

            system_msg, user_msg, assistant_msg = extract_roles(messages)

            if not user_msg or not assistant_msg:
                skipped_incomplete += 1
                continue

            if not is_intermediate_prompt(user_msg):
                continue

            candidates += 1

            user_key = re.sub(r"\s+", " ", user_msg.strip().lower())
            if user_key in seen_users:
                removed_duplicates += 1
                continue

            if is_bad_response(assistant_msg):
                removed_bad += 1
                continue

            seen_users.add(user_key)

            cleaned_record = {
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                    {"role": "assistant", "content": assistant_msg},
                ]
            }

            kept.append(cleaned_record)

    with output_path.open("w", encoding="utf-8") as f:
        for item in kept:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print("===== Intermediate Dataset Summary =====")
    print(f"Total records scanned       : {total}")
    print(f"Intermediate candidates     : {candidates}")
    print(f"Removed duplicates          : {removed_duplicates}")
    print(f"Removed bad-quality samples : {removed_bad}")
    print(f"Skipped incomplete/bad JSON : {skipped_incomplete}")
    print(f"Final intermediate set      : {len(kept)}")
    print(f"Saved to                    : {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
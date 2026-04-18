import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

INPUT_FILE = "data/project_ai_tutor_full.jsonl"
OUTPUT_FILE = "data/beginner_clean_v2.jsonl"

BEGINNER_PATTERNS = [
    r"\bwhat is\b",
    r"\bexplain\b",
    r"\bbeginner\b",
    r"\bbasic\b",
    r"\bsimple\b",
    r"\bconfused\b",
    r"\bhint\b",
    r"\bstep[- ]by[- ]step\b",
    r"\bi am new to\b",
    r"\beasy example\b",
    r"\bteach me\b",
    r"\bhelp me understand\b",
]

BAD_PHRASES = [
    "a related machine learning concept",
    "it is unrelated to learning from data",
]

def is_beginner_prompt(user_text: str) -> bool:
    text = user_text.lower()
    return any(re.search(pattern, text) for pattern in BEGINNER_PATTERNS)

def is_bad_response(text: str) -> bool:
    lower = text.lower().strip()

    if any(bad in lower for bad in BAD_PHRASES):
        return True

    # less strict than before
    if len(text.split()) < 10:
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
    beginner_candidates = 0
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

            if not is_beginner_prompt(user_msg):
                continue

            beginner_candidates += 1

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

    print("===== Beginner Dataset Cleaning Summary =====")
    print(f"Total records scanned       : {total}")
    print(f"Beginner candidates found   : {beginner_candidates}")
    print(f"Removed duplicates          : {removed_duplicates}")
    print(f"Removed bad-quality samples : {removed_bad}")
    print(f"Skipped incomplete/bad JSON : {skipped_incomplete}")
    print(f"Final cleaned beginner set  : {len(kept)}")
    print(f"Saved to                    : {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

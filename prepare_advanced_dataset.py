import json
import re
from pathlib import Path

INPUT_FILE = r"C:\Users\rashm\Downloads\ml_tutor_chatbot\project_ai_tutor_dataset\project_ai_tutor_full.jsonl"
OUTPUT_FILE = r"C:\Users\rashm\Downloads\ml_tutor_chatbot\project_ai_tutor_dataset\advanced_clean.jsonl"

ADVANCED_PATTERNS = [
    r"\bderive\b",
    r"\bmathematical\b",
    r"\bproof\b",
    r"\bformal\b",
    r"\bgradient\b",
    r"\bbackpropagation\b",
    r"\bderivative\b",
    r"\boptimization\b",
    r"\bregularization\b",
    r"\bl1\b",
    r"\bl2\b",
    r"\bbias[- ]variance\b",
    r"\bhyperparameter tuning\b",
    r"\btransformer\b",
    r"\battention\b",
    r"\bself[- ]attention\b",
    r"\bembedding\b",
    r"\btokenization\b",
    r"\bfine[- ]tuning\b",
    r"\blora\b",
    r"\bquantization\b",
    r"\bcnn\b",
    r"\brnn\b",
    r"\blstm\b",
    r"\bgan\b",
    r"\bvae\b",
    r"\bcomplexity\b",
    r"\bbig[- ]o\b",
    r"\bmemory\b",
    r"\bperformance\b",
    r"\bscalability\b",
    r"\bdistributed\b",
    r"\bdebug\b",
    r"\bimplementation\b",
    r"\barchitecture\b",
    r"\bresearch\b",
]

BAD_PHRASES = [
    "a related machine learning concept",
    "it is unrelated to learning from data",
]

def is_advanced_prompt(user_text: str) -> bool:
    text = user_text.lower()
    return any(re.search(pattern, text) for pattern in ADVANCED_PATTERNS)

def is_bad_response(text: str) -> bool:
    lower = text.lower().strip()

    if any(bad in lower for bad in BAD_PHRASES):
        return True

    # slightly strict but not too strict
    if len(text.split()) < 15:
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

            if not is_advanced_prompt(user_msg):
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

            kept.append({
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                    {"role": "assistant", "content": assistant_msg},
                ]
            })

    with output_path.open("w", encoding="utf-8") as f:
        for item in kept:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print("===== Advanced Dataset Summary =====")
    print(f"Total records scanned       : {total}")
    print(f"Advanced candidates         : {candidates}")
    print(f"Removed duplicates          : {removed_duplicates}")
    print(f"Removed bad-quality samples : {removed_bad}")
    print(f"Skipped incomplete/bad JSON : {skipped_incomplete}")
    print(f"Final advanced set          : {len(kept)}")
    print(f"Saved to                    : {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
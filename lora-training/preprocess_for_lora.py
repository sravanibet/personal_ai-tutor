import json
from datasets import load_dataset
from transformers import AutoTokenizer

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

DATA_FILE = r"C:\Users\rashm\Downloads\ml_tutor_chatbot\project_ai_tutor_dataset\final_training_dataset.jsonl"

OUTPUT_PATH = r"C:\Users\rashm\Downloads\ml_tutor_chatbot\project_ai_tutor_dataset\processed_dataset"

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Load dataset
dataset = load_dataset("json", data_files={"train": DATA_FILE})

# Step 1: Convert to prompt-response format
def format_chat(example):
    messages = example["messages"]

    prompt = ""
    response = ""

    for msg in messages:
        if msg["role"] == "system":
            prompt += f"<|system|>\n{msg['content']}\n"
        elif msg["role"] == "user":
            prompt += f"<|user|>\n{msg['content']}\n"
        elif msg["role"] == "assistant":
            response = f"<|assistant|>\n{msg['content']}\n"

    full_text = prompt + response

    return {
        "prompt": prompt,
        "response": response,
        "full_text": full_text
    }

dataset = dataset.map(format_chat)

# Step 2: Tokenize and mask prompt
def tokenize(example):
    full = tokenizer(
        example["full_text"],
        truncation=True,
        padding="max_length",
        max_length=512,
    )

    prompt_tokens = tokenizer(example["prompt"], truncation=True, max_length=512)

    labels = full["input_ids"].copy()

    prompt_len = len(prompt_tokens["input_ids"])

    # Mask prompt tokens
    for i in range(prompt_len):
        labels[i] = -100

    full["labels"] = labels

    return full

dataset = dataset.map(tokenize)

# Step 3: Save to correct folder
dataset.save_to_disk(OUTPUT_PATH)

print(f"Preprocessing complete. Saved to {OUTPUT_PATH}")

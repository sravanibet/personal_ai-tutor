import torch
from pathlib import Path
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

BASE_DIR = Path(__file__).resolve().parent
TRAIN_FILE = BASE_DIR / "train.jsonl"
VAL_FILE = BASE_DIR / "val.jsonl"
OUTPUT_DIR = BASE_DIR / "lora_final_output"

# Load JSONL files directly
dataset = load_dataset(
    "json",
    data_files={
        "train": str(TRAIN_FILE),
        "validation": str(VAL_FILE)
    }
)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


def format_chat(example):
    messages = example["messages"]

    prompt = ""
    response = ""

    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        if role == "system":
            prompt += f"<|system|>\n{content}\n"
        elif role == "user":
            prompt += f"<|user|>\n{content}\n"
        elif role == "assistant":
            response = f"<|assistant|>\n{content}\n"

    full_text = prompt + response
    return {
        "prompt": prompt,
        "response": response,
        "full_text": full_text
    }


dataset = dataset.map(format_chat)


def tokenize(example):
    full = tokenizer(
        example["full_text"],
        truncation=True,
        padding="max_length",
        max_length=512,
    )

    prompt_tokens = tokenizer(
        example["prompt"],
        truncation=True,
        max_length=512
    )

    labels = full["input_ids"].copy()
    prompt_len = len(prompt_tokens["input_ids"])

    for i in range(prompt_len):
        if i < len(labels):
            labels[i] = -100

    full["labels"] = labels
    return full


dataset = dataset.map(tokenize, remove_columns=dataset["train"].column_names)

# Load model
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Apply LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

# Training arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    logging_steps=10,
    save_steps=200,
    save_total_limit=2,
    evaluation_strategy="steps",
    eval_steps=50,
    fp16=True,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"],
)

trainer.train()

model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("Training complete. Model saved to:", OUTPUT_DIR)

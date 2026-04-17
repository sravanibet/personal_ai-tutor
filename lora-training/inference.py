# Import required libraries
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

# Base model used for LoRA fine-tuning
BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"

# Path to your trained LoRA adapter (update if needed)
LORA_PATH = "./lora_final_output"

# Use GPU if available, otherwise CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load tokenizer from base model
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)

# Load LoRA adapter on top of base model
model = PeftModel.from_pretrained(base_model, LORA_PATH)

# Move model to device
model = model.to(device)

# Set model to evaluation mode
model.eval()


# Function to build prompt in chat format (important for model performance)
def build_prompt(question: str, context: str = "") -> str:
    return f"""<|system|>
You are a helpful AI tutor.

<|user|>
Context:
{context}

Question:
{question}

<|assistant|>
"""


# Main function used by tutor module to generate answers
def generate_answer(question: str, context: str = "", max_new_tokens: int = 200) -> str:
    
    # Build structured prompt
    prompt = build_prompt(question, context)

    # Convert text to model input tokens
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # Disable gradient calculation (faster inference)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    # Decode model output into readable text
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Clean unnecessary parts from output
    if "Question:" in decoded:
        decoded = decoded.split("Question:")[-1]

    if "<|assistant|>" in decoded:
        decoded = decoded.split("<|assistant|>")[-1]

    # Return final clean answer
    return decoded.strip()


# Example test (for verification)
if __name__ == "__main__":
    sample_question = "What is overfitting?"
    sample_context = "Overfitting happens when a model learns training data too closely and fails on new data."

    answer = generate_answer(sample_question, sample_context)
    print("Answer:\n", answer)

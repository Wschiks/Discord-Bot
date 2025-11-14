import os
from transformers import AutoTokenizer, AutoModelForCausalLM

# Local save path
model_path = "./models/gpt-neo-125m"

# Make sure folder exists
os.makedirs("./models", exist_ok=True)

print("Downloading GPT-Neo 125M from Hugging Face...")

# Download smaller + faster model
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-125M")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M")

print(f"Saving model to {model_path}...")
tokenizer.save_pretrained(model_path)
model.save_pretrained(model_path)

print("Download complete")

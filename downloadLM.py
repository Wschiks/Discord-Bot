import os
from transformers import AutoTokenizer, AutoModelForCausalLM


model_path = "./models/gpt-neo-350M"


os.makedirs("./models", exist_ok=True)


print("Downloading GPT-Neo 350M from Hugging Face...")

# of 125m
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")



print(f"Saving model to {model_path}...")
tokenizer.save_pretrained(model_path)
model.save_pretrained(model_path)

print("Download complete! You can now use GPT-Neo 350M in your bot.")

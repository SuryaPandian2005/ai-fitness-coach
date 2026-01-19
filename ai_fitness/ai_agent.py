from groq import Groq
from dotenv import load_dotenv
import os
from prompts import fitness_prompt

# Load .env file
load_dotenv()

# Create Groq client using ENV variable
client = Groq(api_key=os.getenv("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"))

def generate_fitness_plan(user_data):
    prompt = fitness_prompt(user_data)

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",  # ✅ CURRENT & SUPPORTED
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_completion_tokens=1024,  # ✅ correct param
        top_p=1
    )

    return response.choices[0].message.content

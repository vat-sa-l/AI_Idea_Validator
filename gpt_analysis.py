import google.generativeai as genai
import json
import re
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-1.5-flash")  

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f" Error: {e}"

def get_market_size(idea):
    return ask_gemini(f"What is the estimated market size for the startup idea: {idea}?")

def get_competitors(idea):
    return ask_gemini(f"List some competitors already working on the startup idea: {idea}")

def get_pain_points(idea):
    return ask_gemini(f"What are the pain points that the idea '{idea}' is solving?")

def get_monetization(idea):
    return ask_gemini(f"Suggest monetization strategies for the idea: {idea}")

def get_improvements(idea):
    return ask_gemini(f"Suggest 3 improvements or tweaks to make the startup idea '{idea}' more unique and competitive")

def get_customer_personas(idea):
    prompt = f"""
Based on this startup idea:

{idea}

Generate 3 detailed customer personas that would be ideal users of this product. 
Each persona should have:
- Name (fictional)
- Age
- Occupation
- Location
- Goals & motivations
- Pain points / challenges
- How this product helps them

Format as bullet points for each persona.
"""
    return ask_gemini(prompt)

def get_validation_scores(idea: str) -> dict:
    prompt = f"""
Given this startup idea:

\"\"\"
{idea}
\"\"\"

Evaluate it on the following criteria and give scores out of 10:

1. Market Size
2. Competition Level
3. Pain Point Clarity
4. Monetization Potential
5. Uniqueness / Improvement Possibilities

Respond ONLY in JSON format like:
{{
  "Market Size": 8,
  "Competitors": 5,
  "Pain Points": 7,
  "Monetization": 6,
  "Tweaks": 4
}}
"""
    response = ask_gemini(prompt)
    cleaned = re.sub(r"```(?:json)?", "", response).strip("`\n ")
    
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON from LLM:\n{response}")


import google.generativeai as genai
import json
import re
from dotenv import load_dotenv
import os
import requests

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-2.0-flash")  

def fetch_realtime_snippets(query: str) -> str:
    serp_api_key = os.getenv("SERPAPI_KEY")  # Add this in your .env
    params = {
        "engine": "google",
        "q": query,
        "api_key": serp_api_key
    }
    try:
        res = requests.get("https://serpapi.com/search", params=params).json()
        results = res.get("organic_results", [])[:3]
        snippets = "\n".join([f"{r['title']}: {r['snippet']}" for r in results])
        return snippets
    except Exception as e:
        return f"Error fetching real-time data: {e}"

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f" Error: {e}"

def get_market_size(idea):
    realtime = fetch_realtime_snippets(f"{idea} market size 2025 India")
    prompt = f"""
Use this real-time context to answer accurately:

{realtime}

Now tell me: What is the estimated market size for the startup idea: {idea}?
"""
    return ask_gemini(prompt)

def get_competitors(idea):
    web_data = fetch_realtime_snippets(f"{idea} startup competitors 2024 site:techcrunch.com OR site:crunchbase.com")
    prompt = f"""
Based on the following recent web search results, list 4–5 direct or indirect competitors for the startup idea: "{idea}".

Results:
{web_data}

Only include those that are relevant and briefly describe them.
"""
    return ask_gemini(prompt)

def get_pain_points(idea):
    web_data = fetch_realtime_snippets(f"{idea} user problems OR pain points site:reddit.com OR site:quora.com")
    prompt = f"""
Using these public discussions and recent search results, identify the key pain points that the startup idea '{idea}' is addressing.

Results:
{web_data}

Return them as a bullet-point list with short explanations.
"""
    return ask_gemini(prompt)


def get_monetization(idea):
    web_data = fetch_realtime_snippets(f"{idea} monetization strategies site:medium.com OR site:techcrunch.com")
    prompt = f"""
Based on the following recent strategies found online, suggest 3–4 monetization models for the startup idea: "{idea}".

Results:
{web_data}

List them with 1-line explanation each.
"""
    return ask_gemini(prompt)


def get_improvements(idea):
    web_data = fetch_realtime_snippets(f"{idea} similar ideas and USP site:producthunt.com OR site:techcrunch.com")
    prompt = f"""
Analyze the idea: "{idea}" and the following competitor information:

{web_data}

Now suggest 3 smart improvements or differentiators to make it more unique and competitive.
"""
    return ask_gemini(prompt)

def get_pitch(idea):
    web_data = fetch_realtime_snippets(f"{idea} startup funding news site:techcrunch.com")
    prompt = f"""
Use this recent context to craft a compelling 30-second investor pitch for the AI startup idea: "{idea}".

Results:
{web_data}

Keep it exciting and founder-style, with a closing hook.
"""
    return ask_gemini(prompt)

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


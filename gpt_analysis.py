import google.generativeai as genai


genai.configure(api_key="AIzaSyDcAJ9wr997y7sFBmQY3AG8TpWBc6s63Ek")


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

import openai
import os
import json
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

def summarize_job(title, company, location, link):
    prompt = f"""
You are a career assistant. Summarize this job in 2 lines and suggest 1 must-have skill.

Job Title: {title}
Company: {company}
Location: {location}
Job Link: {link}

Respond strictly in this format:
Summary: ...
Skill: ...
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or your available proxy model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()
        lines = content.split("\n")
        summary = lines[0].replace("Summary:", "").strip()
        skill = lines[1].replace("Skill:", "").strip()
        return summary, skill

    except Exception as e:
        print("❌ GPT Summary Error:", e)
        return "Summary not available.", "Skill not available."

import os 
import openai
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
api_base = os.getenv('OPENAI_API_BASE')

client = openai.OpenAI(api_key=api_key, base_url=api_base)



def extract_job_title_location_gpt(user_input):
    prompt = f""" You are an intelligent assistant. Extract the job title and location from this user query: "{user_input}". 
     Respond in this JSON format exactly:
     {{
        "job_title": "...",
        "location": "..."
     }}
     """
    try:
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [{"role": "user",  "content" : prompt}],
            temperature = 0
        )

        message = response.choices[0].message.content.strip()


        import json

        result = json.loads(message)

        return(result.get("job_title", "").strip(), result.get("location", "").strip())

    
    
    except Exception as e:
        print(f"GPT NLP ERROR : {e}")
        return None, None



if __name__ == "__main__":
    title, loc = extract_job_title_location_gpt(user_input="I want a data analyst internship in Bangalore")
    print(f"title : {title}, location : {loc}")
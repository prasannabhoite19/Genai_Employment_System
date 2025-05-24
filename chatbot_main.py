from src.chatbot_nlp import extract_job_inputs
from src.linkedin_scraper import scrape_linkedin_jobs
from src.linkedin_cleaner import clean_jobs_from_links
import os

def chatbot():
    print("🤖 Welcome! I can help you find real-time jobs on LinkedIn.")
    print("Type something like: 'Looking for data analyst jobs in Mumbai'")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("🤖 Goodbye!")
            break

        job_title, location = extract_job_inputs(user_input)

        # NLP fallback handling
        if "please specify" in job_title.lower():
            print(f"🤖 {job_title}")
            continue

        print(f"\n🔎 Searching LinkedIn for '{job_title}' jobs in '{location}'...\n")

        # Step 1: Get job links
        scraper_df = scrape_linkedin_jobs(job_title, location, max_jobs=10)

        if scraper_df.empty or scraper_df["link"].isnull().all():
            print("⚠️ No job links found. Try a different keyword or location.\n")
            continue

        # Step 2: Clean each link by visiting job post
        cleaned_df = clean_jobs_from_links(csv_path="data/raw/jobs.csv", limit=10)

        if cleaned_df.empty:
            print("⚠️ No clean job data available. Try again later.\n")
            continue

        print("✅ Found the following job openings:\n")
        for i, row in cleaned_df.iterrows():
            print(f"{i+1}. {row['title']} at {row['company']} ({row['location']})")
            print(f"🔗 {row['link']}\n")

if __name__ == "__main__":
    chatbot()

import streamlit as st
from src.chatbot_nlp import extract_job_inputs
from src.linkedin_scraper import scrape_linkedin_jobs
from src.linkedin_cleaner import clean_jobs_from_links
import pandas as pd

st.set_page_config(page_title="JobBot 💼", layout="centered")

st.title("💼 JobBot - Real-time LinkedIn Job Finder")

user_input = st.text_input("🔍 What kind of job are you looking for?", placeholder="e.g., Data analyst in Mumbai")

if st.button("Find Jobs") and user_input:
    job_title, location = extract_job_inputs(user_input)

    if "please specify" in job_title.lower():
        st.warning(job_title)
    else:
        st.info(f"Searching for **{job_title}** jobs in **{location}**...")

        # Step 1: Scrape LinkedIn for job links
        scraped_df = scrape_linkedin_jobs(job_title, location, max_jobs=10)

        if scraped_df.empty or scraped_df["link"].isnull().all():
            st.error("No job links found. Try a different query.")
        else:
            # Step 2: Clean job metadata from individual pages
            cleaned_df = clean_jobs_from_links("data/raw/jobs.csv", limit=10)

            if cleaned_df.empty:
                st.error("Could not extract job details. Try again later.")
            else:
                st.success(f"Found {len(cleaned_df)} job(s)! 👇")
                for _, row in cleaned_df.iterrows():
                    st.markdown(f"### {row['title']}")
                    st.markdown(f"**Company:** {row['company']}")
                    st.markdown(f"**Location:** {row['location']}")
                    st.markdown(f"[🔗 View Job Posting]({row['link']})", unsafe_allow_html=True)
                    st.markdown("---")



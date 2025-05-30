import streamlit as st
import pandas as pd
from src.gpt_nlp import extract_job_title_location_gpt
from src.linkedin_scraper import scrape_linkedin_jobs
from src.linkedin_cleaner import clean_jobs_from_links
from src.course_scraper import search_coursera_courses
from src.gpt_helper import summarize_job

# ---------------------------- PAGE CONFIG ---------------------------- #
st.set_page_config(
    page_title="Employment & Skill Development Platform",
    layout="centered",
    page_icon="💼"
)

# ---------------------------- CUSTOM STYLING ---------------------------- #
custom_css = """
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stTextInput>div>div>input {
        border: 2px solid #4CAF50;
        border-radius: 10px;
    }
    .job-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------- HEADER ---------------------------- #
st.markdown("<h1 style='text-align: center;'>💼 Employment & Skill Development</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Find jobs and boost your skills with personalized course recommendations.</p>", unsafe_allow_html=True)

# ---------------------------- INPUT FIELD ---------------------------- #
user_input = st.text_input("🔍 What kind of job are you looking for?", placeholder="e.g., Data analyst in Mumbai")

# ---------------------------- MAIN PROCESS ---------------------------- #
if st.button("🚀 Find Jobs") and user_input:
    with st.spinner("Thinking... ✨"):
        job_title, location = extract_job_title_location_gpt(user_input)

    if not job_title or not location or "please specify" in job_title.lower():
        st.warning("⚠️ Please specify both job title and location.")
        st.stop()

    st.info(f"🔎 Searching for **{job_title}** jobs in **{location}**...")

    with st.spinner("Getting LinkedIn jobs..."):
        scraped_df = scrape_linkedin_jobs(job_title, location, max_jobs=10)

    if scraped_df.empty or scraped_df["link"].isnull().all():
        st.error("❌ No job links found. Try a different query.")
    else:
        with st.spinner("Processing job descriptions..."):
            cleaned_df = clean_jobs_from_links("data/raw/jobs.csv", limit=15)

        if cleaned_df.empty:
            st.error("❌ Could not extract job details. Try again later.")
        else:
            st.success(f"✅ Found {len(cleaned_df)} job(s)!")

            for _, row in cleaned_df.iterrows():
                summary, skill = summarize_job(row['title'], row['company'], row['location'], row['link'])

                with st.container():
                    st.markdown(f"""<div class="job-card" style="color: black;">
                        <h3 style="color: black;">{row['title']}</h3>
                        <p><strong>🏢 Company:</strong> {row['company']}</p>
                        <p><strong>📍 Location:</strong> {row['location']}</p>
                        <p><em>{summary}</em></p>
                        <p><strong>🛠 Must-have Skill:</strong> {skill}</p>
                        <a href="{row['link']}" target="_blank">🔗 View Job Posting</a>
                    </div>""", unsafe_allow_html=True)

            if not cleaned_df.empty:
                # Download button
                csv = cleaned_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Jobs as CSV",
                    data=csv,
                    file_name="job_listings.csv",
                    mime="text/csv"
                )

            # ---------------------------- COURSE RECOMMENDATIONS ---------------------------- #
            st.subheader("🎓 Recommended Courses")

            with st.spinner("Finding courses on Coursera..."):
                course_df = search_coursera_courses(job_title)

            if not course_df.empty:
                for _, row in course_df.iterrows():
                    st.markdown(f"""
                    <div style="background-color: white; padding: 1rem; border-radius: 10px; 
                                box-shadow: 0 2px 6px rgba(0,0,0,0.1); margin-bottom: 1rem; color: black;">
                        <p style="font-weight: bold; font-size: 16px;">🎓 {row['title']}</p>
                        <a href="{row['link']}" target="_blank" style="text-decoration: none; color: #1a73e8;">
                            🔗 View on Coursera
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                course_csv = course_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Recommended Courses as CSV",
                    data=course_csv,
                    file_name="recommended_courses.csv",
                    mime="text/csv"
                )
                
            else:
                st.markdown("❌ No relevant courses found.")


# ---------------------------- SIDEBAR ---------------------------- #
st.sidebar.title("🛠 Options")
st.sidebar.markdown("Use this app to find jobs and improve your skills.")
if st.sidebar.button("❌ Exit App"):
    st.sidebar.warning("App stopped. You can close the browser tab.")
    st.stop()

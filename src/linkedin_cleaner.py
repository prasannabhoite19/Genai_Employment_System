import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os

def clean_jobs_from_links(csv_path="data/raw/jobs.csv", limit=10):
    df = pd.read_csv(csv_path)
    links = df["link"].dropna().unique().tolist()[:limit]

    print(f" Cleaning {len(links)} job listings...")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()

    titles = []
    companies = []
    locations = []
    job_links = []

    for link in links:
        try:
            driver.get(link)
            time.sleep(3)

            title = driver.find_element(By.CLASS_NAME, "topcard__title").text.strip()
            company = driver.find_element(By.CLASS_NAME, "topcard__org-name-link").text.strip()
            location = driver.find_element(By.CLASS_NAME, "topcard__flavor--bullet").text.strip()

            titles.append(title)
            companies.append(company)
            locations.append(location)
            job_links.append(link)

        except Exception as e:
            print(f" Error processing link: {link}\n{e}")
            continue

    driver.quit()

    cleaned_df = pd.DataFrame({
        "title": titles,
        "company": companies,
        "location": locations,
        "link": job_links
    })

    os.makedirs("data/processed", exist_ok=True)
    cleaned_df.to_csv("data/processed/cleaned_jobs.csv", index=False)
    print("Cleaned data saved to data/processed/cleaned_jobs.csv")

    return cleaned_df

if __name__ == "__main__":
    df = clean_jobs_from_links(limit=10)
    print(df.head())

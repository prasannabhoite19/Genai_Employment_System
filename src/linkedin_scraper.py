from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os

def scrape_linkedin_jobs(job_title, location, max_jobs=10):
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()

    job_title = job_title.replace(" ", "%20")
    location = location.replace(" ", "%20")
    url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}&f_TPR=r2592000"


    print(f" Searching for '{job_title}' jobs in '{location}'")
    driver.get(url)
    time.sleep(5)

    # Scroll to load more jobs
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    job_titles = []
    companies = []
    locations = []
    links = []

    try:
        job_cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="jobs-search__results-list"]/li'))
        )
    except:
        print(" No job cards found.")
        driver.quit()
        return pd.DataFrame()

    for index, card in enumerate(job_cards[:max_jobs]):
        try:
            title = card.find_element(By.XPATH, './/h3[contains(@class, "base-search-card__title")]').text.strip()
            company = card.find_element(By.XPATH, './/h4[contains(@class, "base-search-card__subtitle")]').text.strip()
            location = card.find_element(By.XPATH, './/span[contains(@class, "job-search-card__location")]').text.strip()
            link = card.find_element(By.TAG_NAME, 'a').get_attribute("href")

            job_titles.append(title)
            companies.append(company)
            locations.append(location)
            links.append(link)
        except Exception as e:
            print(f" Error parsing job {index + 1}: {e}")
            continue

    driver.quit()

    df = pd.DataFrame({
        "title": job_titles,
        "company": companies,
        "location": locations,
        "link": links
    })

    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/jobs.csv", index=False)
    print(" Job data saved to data/raw/jobs.csv")

    return df

if __name__ == "__main__":
    df = scrape_linkedin_jobs("data science", "Pune", max_jobs=10)
    print(df.head())
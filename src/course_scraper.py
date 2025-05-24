import requests 
import pandas as pd
from bs4 import BeautifulSoup

def search_coursera_courses(query, limit = 10 ):
    """
    Scrape Coursera's search results for the given query.
    Returns a list of course titles and links.

    """

    query = query.replace(" ", "+")
    url = f"https://www.coursera.org/search?query={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url,headers=headers)
        response.raise_for_status()

    except Exception as e:
        print("Failed to fetch Coursera results:", e)
        return pd.DataFrame()
    
    soup = BeautifulSoup(response.text, "html.parser")
    coursera_cards = soup.find_all("a", class_="cds-CommonCard-titleLink")

    titles = []
    links = []

    for card in coursera_cards[:limit]:
        title = card.get_text(strip=True)
        link = "https://www.coursera.org" + card.get("href")
        titles.append(title)
        links.append(link)

    return pd.DataFrame({"title": titles, "link": links})


if __name__ == "__main__":
    df = search_coursera_courses("data science")
    print(df)
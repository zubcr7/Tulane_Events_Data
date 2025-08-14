import time
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver

# Mapping of URLs to categories
CATEGORY_MAP = {
    "tulane.campuslabs.com/engage/events": "Student-life / Clubs / Social Mixers",
    "events.tulane.edu": "University-wide (Academic, Cultural, Wellness, etc.)",
    "apply.tulane.edu/portal/tulanecomestoyou": "Admissions / Info Sessions",
    "freeman.tulane.edu/events": "Academic & Professional Development",
    "medicine.tulane.edu/events-calendar": "Medical Academic & Professional",
    "tmedweb.tulane.edu/clubs": "Medical Student Clubs / Org Events",
    "campusrecreation.tulane.edu/event-listings": "Fitness, Wellness & Recreation"
}

class GenericEventScraper:
    def __init__(self, urls):
        self.urls = urls
        self.driver = self._init_driver()
        self.results = []

    def _init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        return webdriver.Chrome(options=options)

    def scrape_site(self, url):
        print(f"🌐 Scraping {url}")
        self.driver.get(url)
        time.sleep(2)

        # Infinite scroll until stable
        last_height = 0
        same_count = 0
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                same_count += 1
                if same_count >= 2:
                    break
            else:
                same_count = 0
            last_height = new_height

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        events = soup.find_all("li", class_="views-row")  # may vary per site

        category = self.get_category(url)
        for e in events:
            title_tag = e.find("a", href=True)
            title = title_tag.get_text(strip=True) if title_tag else "No Title"
            link = urljoin(url, title_tag['href']) if title_tag else None
            self.results.append({
                "Source": url,
                "Category": category,
                "Title": title,
                "Link": link
            })

        print(f"✅ {len(events)} events found from {url}")

    def get_category(self, url):
        for key, cat in CATEGORY_MAP.items():
            if key in url:
                return cat
        return "Uncategorized"

    def run(self):
        try:
            for url in self.urls:
                self.scrape_site(url)
        finally:
            self.driver.quit()

    def save_results(self, filename="scraping_results.csv"):
        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False)
        print(f"💾 Results saved to {filename}")


if __name__ == "__main__":
    urls_to_scrape = [
        "https://tulane.campuslabs.com/engage/events",
        "https://events.tulane.edu/",
        "https://apply.tulane.edu/portal/tulanecomestoyou",
        "https://freeman.tulane.edu/events",
        "https://medicine.tulane.edu/events-calendar",
        "https://tmedweb.tulane.edu/clubs/",
        "https://campusrecreation.tulane.edu/event-listings"
    ]

    scraper = GenericEventScraper(urls_to_scrape)
    scraper.run()
    scraper.save_results()

import time
import pandas as pd
from bs4 import BeautifulSoup, NavigableString
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException


class FsbEventsScrapper:
    def __init__(self, url="https://freeman.tulane.edu/events"):
        self.url = url
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.events = []

    def scraper(self):
        print(f"🌐 Scraping {self.url}")
        self.driver.get(self.url)

        # Click "Load More" until all events are loaded
        while True:
            try:
                load_more_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Load More')]") )
                )
                self.driver.execute_script("arguments[0].click();", load_more_btn)
                time.sleep(2)
            except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                break

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        event_cards = soup.find_all("div", class_="views-row")
        for card in event_cards:
            title_tag = card.find("a", href=True)
            title = title_tag.get_text(strip=True) if title_tag else "No Title"
            link = urljoin(self.url, title_tag["href"]) if title_tag else None

            date_time_tag = card.find("time", class_="block font-bold tuf-mb-3")
            date_time = date_time_tag.get_text(strip=True) if date_time_tag else None

            if date_time:
                parts = date_time.split(',', 1)
                weekday = parts[0].strip() if len(parts) > 1 else "No Weekday"
                rest = parts[1].strip() if len(parts) > 1 else ''
                date_time_parts = rest.rsplit(' ', 3)
                date = ' '.join(date_time_parts[:-2]) if len(date_time_parts) > 2 else rest
                time_str = ' '.join(date_time_parts[-2:]) if len(date_time_parts) > 2 else ''
            else:
                weekday = "No Weekday"
                date = "No Date"
                time_str = "No Time"

            desc_div = date_time_tag.find_next_sibling("div") if date_time_tag else None
            description = desc_div.get_text(strip=True) if desc_div else ""

            event = {
                "Title": title,
                "Weekday": weekday,
                "Date": date,
                "Time": time_str,
                "Link": link,
                "Description": description
            }
            self.events.append(event)

    def save_to_csv(self, filename="fsb_events.csv"):
        df = pd.DataFrame(self.events)
        df.to_csv(filename, index=False)
        print(f"💾 Saved to {filename}")

    def run(self):
        try:
            self.scraper()
            self.save_to_csv()
            print(f"Total events saved: {len(self.events)}")
        finally:
            self.driver.quit()
            print("✅ Browser closed.")
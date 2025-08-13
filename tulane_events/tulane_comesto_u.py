csv_filename = "tulaneComestoYou.csv"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv

class TulaneComesToYouScraper:
    def __init__(self, url="https://apply.tulane.edu/portal/tulanecomestoyou"):
        self.url = url
        self.data = []

    def run(self, csv_filename="tulaneComestoYou.csv"):
        chrome_options = Options()
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(self.url)

        # Click "Browse All"
        browse_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Browse All']"))
        )
        browse_btn.click()

        # Scroll to load all events
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Parse HTML
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        container = soup.find("div", class_="event_list_display")

        data = []
        current_state = None

        # Loop through in order
        for div in container.find_all("div", recursive=True):
            classes = div.get("class", [])
            if "item_header" in classes:
                current_state = div.get_text(strip=True)
            elif "item" in classes:
                event_div = div.find("div", class_="event")
                if event_div:
                    date_time = event_div.get("data-date")
                    location = event_div.get("data-location")
                    title_tag = event_div.find("a")
                    title = title_tag.get_text(strip=True) if title_tag else None
                    link = title_tag["href"] if title_tag else None

                    # Split date and time
                    date_part, time_part = None, None
                    if date_time:
                        if "T" in date_time:
                            date_part, time_part = date_time.split("T", 1)
                        else:
                            date_part = date_time

                    # Extract only the state name (before the first ' - ')
                    state_name = current_state.split(' - ')[-1] if current_state and ' - ' in current_state else current_state
                    data.append([state_name, title, date_part, time_part, location, link])

        # Save to CSV
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["State", "Title", "Date", "Time", "Location", "Link"])
            writer.writerows(data)

        print(f"✅ Saved {len(data)} events to {csv_filename}")
        self.data = data

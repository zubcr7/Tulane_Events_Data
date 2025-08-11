import csv
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

class Event:
    """Data model for a single event."""
    def __init__(self, title, weekday, month, day, time_str, location, link):
        self.title = title
        self.weekday = weekday
        self.month = month
        self.day = day
        self.time_str = time_str
        self.location = location
        self.link = link

    def to_list(self):
        """Convert event data to list format for CSV."""
        return [
            self.title, self.weekday, self.month, self.day,
            self.time_str, self.location, self.link
        ]

class CampusEventScraper:
    BASE_URL = "https://tulane.campuslabs.com"
    EVENTS_URL = "https://tulane.campuslabs.com/engage/events"

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.events = []

    def load_all_events(self):
        """Click 'Load More' until all events are loaded."""
        self.driver.get(self.EVENTS_URL)
        while True:
            try:
                load_more_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Load More')]") )
                )
                self.driver.execute_script("arguments[0].click();", load_more_btn)
                time.sleep(2)
            except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                break

    def parse_events(self):
        """Parse events from the page."""
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        event_cards = soup.select("#event-discovery-list a")

        for card in event_cards:
            link = urljoin(self.BASE_URL, card.get("href", ""))
            title_tag = card.select_one("h3")
            title = title_tag.get_text(strip=True) if title_tag else "No Title"

            # Date/time
            date_tag = card.find("div", style="margin: 0px 0px 0.125rem;")
            date_time = date_tag.get_text(strip=True) if date_tag else "No Date"

            weekday, month, day, time_str = ("", "", "", "")
            if date_time:
                parts = date_time.split()
                if len(parts) >= 4:
                    weekday, month, day, time_str = parts[0], parts[1], parts[2], " ".join(parts[3:])

            # Location
            location_tag = date_tag.find_next("div") if date_tag else None
            location = location_tag.get_text(strip=True) if location_tag else "No Location"

            self.events.append(Event(title, weekday, month, day, time_str, location, link))

    def save_to_csv(self, filename="eventsCampus.csv"):
        """Save scraped events to CSV."""
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "Weekday", "Month", "Day", "Time", "Location", "Link"])
            for event in self.events:
                writer.writerow(event.to_list())

    def run(self):
        try:
            self.load_all_events()
            self.parse_events()
            self.save_to_csv()
            print(f"Total events saved: {len(self.events)}")
        finally:
            self.driver.quit()

import time
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

# URL to scrape
url = "https://freeman.tulane.edu/events"

# Setup Selenium
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

events = []

try:
    print(f"🌐 Scraping {url}")
    driver.get(url)

    # Click "Load More" until all events are loaded
    while True:
        try:
            load_more_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Load More')]"))
            )
            driver.execute_script("arguments[0].click();", load_more_btn)
            time.sleep(2)
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
            break

    # Parse page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    event_cards = soup.find_all("div", class_="views-row")
    for card in event_cards:
        title_tag = card.find("a", href=True)
        title = title_tag.get_text(strip=True) if title_tag else "No Title"
        link = urljoin(url, title_tag["href"]) if title_tag else None

        date_time = card.find("time", class_="block font-bold tuf-mb-3" )
        date_time = date_time.get_text(strip=True) if date_time else None

        if date_time:
            parts = date_time.split(',', 1)
            weekday = parts[0].strip()  # 'Friday'
            rest = parts[1].strip() if len(parts) > 1 else ''
            date_time_parts = rest.rsplit(' ', 3)
            date = ' '.join(date_time_parts[:-2])  # 'April 17, 2026'
            time = ' '.join(date_time_parts[-2:])  # '2:00 pm'
            date_time = f"{date}, {time}"
        else:
            time = "No Time"
        desc_div = card.find("time", class_="block font-bold tuf-mb-3").find_next_sibling("div")
        description = desc_div.get_text(strip=True) if desc_div else ""

        event = {
            "Title": title,
            "Weekday": weekday if 'weekday' in locals() else "No Weekday",
            "Date": date if 'dat'
            'e' in locals() else "No Date",
            "Time": time,
            "Link": link,
            "Description": description
        }
        events.append(event)
        print(events)
    print(f"Total events saved: {len(events)}")

finally:
    driver.quit()
    print("✅ Browser closed.")

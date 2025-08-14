import time
import pandas as pd
from bs4 import BeautifulSoup, NavigableString
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class TulaneEventScraper:
    def __init__(self, base_url="https://events.tulane.edu/"):
        self.base_url = base_url
        self.driver = self._init_driver()
        self.events = []

    def _init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        return webdriver.Chrome(options=options)

    def load_all_events(self):
        print("📜 Scrolling to load all events...")
        last_event_count = 0
        same_count_repeats = 0

        while True:
            # Scroll to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new events to load

            # Count events loaded so far
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            events = soup.find_all("li", class_="views-row")
            current_event_count = len(events)
            print(f"Found {current_event_count} events so far...")

            # If new events loaded, reset repeat counter
            if current_event_count > last_event_count:
                last_event_count = current_event_count
                same_count_repeats = 0
            else:
                same_count_repeats += 1

            # Stop after 3 scrolls with no change
            if same_count_repeats >= 3:
                print("✅ All events loaded.")
                break

    def extract_event_data(self, event):
        title_tag = event.find("a", href=True)
        title = title_tag.get_text(strip=True) if title_tag else "No title"
        link = urljoin(self.base_url, title_tag["href"]) if title_tag else None

        img_tag = event.find("img")
        image = urljoin(self.base_url, img_tag["src"]) if img_tag else None

        venue = None
        strong_tag = event.find("div", class_="col-span-7 second p-10")
        contents = strong_tag.contents if strong_tag else []
        found_strong = False
        for item in contents:
            if getattr(item, 'name', None) == 'strong':
                found_strong = True
            elif found_strong and isinstance(item, NavigableString):
                text = item.strip()
                if text:
                    venue = text
                    break

        calendar_div = event.select_one("div.col-span-2.bg-tu-green-official.text-white.text-center.first")
        if calendar_div:
            card_month = calendar_div.find("div", class_="card-month")
            card_date = calendar_div.find("div", class_="card-date")
            card_day = calendar_div.find("div", class_="card-day")
            month = card_month.get_text(strip=True) if card_month else None
            date = card_date.get_text(strip=True) if card_date else None
            day = card_day.get_text(strip=True) if card_day else None
        else:
            month = date = day = None

        full_datetime = None
        times = event.find_all("time")
        if times:
            first_time_tag = times[0]
            datetime_attr = first_time_tag.get("datetime")
            date_span = first_time_tag.find("span", class_="smart-date--date")
            time_span = first_time_tag.find("span", class_="smart-date--time")
            readable_date = date_span.get_text(strip=True) if date_span else None
            readable_time = time_span.get_text(strip=True) if time_span else None
            full_datetime = f"{readable_date} at {readable_time}" if readable_date and readable_time else datetime_attr

        return {
            "Title": title,
            "Link": link,
            "Image": image,
            "Location": venue,
            "DateTime": full_datetime,
            "Month": month,
            "Date": date,
            "Day": day
        }

    def parse_events(self):
        print("🔍 Parsing all events...")
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        events = soup.find_all("li", class_="views-row")
        print(f"✅ Found {len(events)} events.")
        for event in events:
            data = self.extract_event_data(event)
            self.events.append(data)

    def save_to_csv(self, filename="eventsTulaneedu.csv"):
        df = pd.DataFrame(self.events)
        df.to_csv(filename, index=False)
        print(f"💾 Saved to {filename}")

    def save_to_txt(self, filename="eventsTulaneedu.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            for i, event in enumerate(self.events, 1):
                f.write(f"Event {i}:\n")
                for key, value in event.items():
                    f.write(f"{key}: {value}\n")
                f.write("=" * 80 + "\n")
        print(f"💾 Saved to {filename}")

    def run(self):
        try:
            self.driver.get(self.base_url)
            print("🌐 Page loaded.")
            self.load_all_events()
            self.parse_events()
            self.save_to_csv()
            self.save_to_txt()
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self.driver.quit()
            print("✅ Browser closed.")



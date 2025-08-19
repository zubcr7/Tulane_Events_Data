import requests
from bs4 import BeautifulSoup
import pandas as pd
from dateutil import parser

class RecEventsScraper:
    def __init__(self, url=None, output_file=None):
        self.url = url or "https://campusrecreation.tulane.edu/event-listings"
        self.output_file = output_file or "rec.csv"

    def scrape(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        events = []
        for row in soup.select("div.mb-5.views-row"):
            # Title & Link
            title_tag = row.select_one("div.text-xl a")
            title = title_tag.get_text(strip=True) if title_tag else ""
            link = self.url + title_tag["href"] if title_tag else ""
            # Date
            date_tag = row.find("em")
            date_text = date_tag.get_text(strip=True) if date_tag else ""
            try:
                dt = parser.parse(date_text)
                weekday = dt.strftime("%A")
                day = dt.day
                month = dt.strftime("%B")
                year = dt.year
            except:
                weekday, day, month, year = "", "", "", ""
            # Details section (time, location, description)
            details_tag = row.select_one("div.views-field-value-2 span.field-content")
            time, location, description = "", "", ""
            if details_tag:
                ps = details_tag.find_all("p")
                for p in ps:
                    txt = p.get_text(strip=True)
                    if "am" in txt or "pm" in txt:
                        time = txt
                    elif "Center" in txt or "Room" in txt or "Hall" in txt:
                        location = txt
                    else:
                        description += txt + " "
            events.append({
                "Title": title,
                "Weekday": weekday,
                "Day": day,
                "Month": month,
                "Year": year,
                "Time": time,
                "Location": location,
                "Description": description.strip(),
                "Link": link
            })
        df = pd.DataFrame(events)
        df.to_csv(self.output_file, index=False)
        print(f"✅ Saved events to {self.output_file}")

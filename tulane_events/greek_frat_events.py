import requests
from bs4 import BeautifulSoup
import csv
import html

class GreekFratEventsScraper:
    def __init__(self, url='https://greek.tulane.edu/event-listings', output_file=None):
        self.url = url or 'https://greek.tulane.edu/event-listings'
        self.output_file = output_file or 'tulane_greek_events.csv'

    def scrape(self):
        response = requests.get(self.url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        event_rows = soup.find_all('div', class_='mb-10 views-row')
        events = []

        for event_row in event_rows:
            # --- Event name and link ---
            name_tag = event_row.find('div', class_='text-xl font-bold')
            event_name, event_link = '', ''
            if name_tag:
                a_tag = name_tag.find('a')
                if a_tag:
                    event_name = html.unescape(a_tag.get_text(strip=True))
                    event_link = a_tag['href']
                    if not event_link.startswith('http'):
                        event_link = 'https://greek.tulane.edu' + event_link
                else:
                    event_name = html.unescape(name_tag.get_text(strip=True))

            # --- Date & Time ---
            weekday, date_str, time_str = '', '', ''
            # find the div that has span with "Date:"
            date_container = event_row.find('span', string=lambda t: t and "Date:" in t)
            if date_container and date_container.find_next('em'):
                date_time_text = date_container.find_next('em').get_text(strip=True)
                parts = [p.strip() for p in date_time_text.split(',')]

                if len(parts) == 2:
                    weekday_date = parts[0]   # "Tuesday August 19th"
                    time_str = parts[1]       # "5:00 PM"
                    if ' ' in weekday_date:
                        weekday, date_str = weekday_date.split(' ', 1)
                    else:
                        weekday = weekday_date
                else:
                    weekday = date_time_text

            # --- Description ---
            desc_div = event_row.find('div', class_='views-field-value-4')
            description = ''
            if desc_div:
                desc_span = desc_div.find('span', class_='field-content')
                if desc_span:
                    description = html.unescape(desc_span.get_text(strip=True))

            events.append({
                'Event Name': event_name,
                'Weekday': weekday,
                'Date': date_str,
                'Time': time_str,
                'Description': description,
                'Link': event_link
            })

        # --- Save to CSV ---
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Event Name', 'Weekday', 'Date', 'Time', 'Description', 'Link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for event in events:
                writer.writerow(event)

        print(f"Saved {len(events)} events to {self.output_file}.")

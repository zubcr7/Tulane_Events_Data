import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# URL to scrape
url = 'https://greek.tulane.edu/event-listings'

response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

# Find all event blocks directly
event_rows = soup.find_all('div', class_='mb-10 views-row')
events = []
for event_row in event_rows:
    # Event Name and Link
    name_tag = event_row.find('div', class_='text-xl font-bold')
    event_name = ''
    event_link = ''
    if name_tag:
        a_tag = name_tag.find('a')
        if a_tag:
            event_name = a_tag.get_text(strip=True)
            event_link = a_tag['href']
            if not event_link.startswith('http'):
                event_link = 'https://greek.tulane.edu' + event_link
        else:
            event_name = name_tag.get_text(strip=True)
    # Date, Weekday, Time
    date_div = event_row.find('div', class_='views-field-value-2')
    weekday = ''
    date_str = ''
    time_str = ''
    if date_div:
        date_span = date_div.find('span')
        em_tag = date_div.find('em')
        if em_tag:
            date_time_text = em_tag.get_text(strip=True)
            parts = date_time_text.split(',')
            if len(parts) == 2:
                weekday_date = parts[0].strip().split(' ', 1)
                if len(weekday_date) == 2:
                    weekday = weekday_date[0]
                    date_str = weekday_date[1]
                time_str = parts[1].strip()
            else:
                time_str = date_time_text
    # Description
    desc_div = event_row.find('div', class_='views-field-value-4')
    description = ''
    if desc_div:
        desc_span = desc_div.find('span', class_='field-content')
        if desc_span:
            description = desc_span.get_text(strip=True)
    events.append({
        'Event Name': event_name,
        'Weekday': weekday,
        'Date': date_str,
        'Time': time_str,
        'Description': description,
        'Link': event_link
    })

with open('tulane_greek_events.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Event Name', 'Weekday', 'Date', 'Time', 'Description', 'Link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for event in events:
        writer.writerow(event)

print(f"Saved {len(events)} events to tulane_greek_events.csv.")
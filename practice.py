from icalendar import Calendar
import pandas as pd

# Path to your downloaded .ics file
ics_file = r"D:\Downloads\calendar.ics"

events = []
with open(ics_file, 'rb') as f:
    cal = Calendar.from_ical(f.read())
    for e in cal.walk('VEVENT'):
        title = str(e.get('SUMMARY', ''))
        start = e.get('DTSTART').dt if e.get('DTSTART') else ''
        end = e.get('DTEND').dt if e.get('DTEND') else ''
        location = str(e.get('LOCATION', ''))
        description_full = str(e.get('DESCRIPTION', ''))
        # Extract only the main event description (line starting with 'Description:')
        description = ''
        for line in description_full.splitlines():
            if line.strip().startswith('Description:'):
                description = line.replace('Description:', '').strip()
                break
        # Extract date and time
        def get_date(dt):
            if hasattr(dt, 'date'):
                return dt.date().isoformat()
            elif isinstance(dt, str) and len(dt) >= 10:
                return dt[:10]
            return ''
        def get_time(dt):
            if hasattr(dt, 'strftime'):
                return dt.strftime('%H:%M')
            elif isinstance(dt, str) and len(dt) >= 16:
                return dt[11:16]
            return ''
        date = get_date(start)
        start_time = get_time(start)
        end_time = get_time(end)
        events.append({
            "Title": title,
            "Date": date,
            "Start": start_time,
            "End": end_time,
            "Location": location,
            "Description": description
        })

df = pd.DataFrame(events, columns=["Title", "Date", "Start", "End", "Location", "Description"])
df.to_csv("tulane_events.csv", index=False)
print("✅ Saved events to tulane_events.csv")

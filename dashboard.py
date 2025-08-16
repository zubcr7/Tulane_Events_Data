import pandas as pd
import matplotlib.pyplot as plt
import os

# ---- SCRAPING PROGRESS DATA ----
def count_events(csv_path):
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            return len(df)
        except Exception:
            return 0
    return 0

websites = [
    {"Website": "https://tulane.campuslabs.com/engage/events", "Scraped": True,  "Events": count_events("eventsCampus.csv")},
    {"Website": "https://events.tulane.edu/", "Scraped": True,  "Events": count_events("eventsTulaneedu.csv")},
    {"Website": "https://apply.tulane.edu/portal/tulanecomestoyou", "Scraped": True,  "Events": count_events("tulaneComestoYou.csv")},
    {"Website": "https://freeman.tulane.edu/events", "Scraped": True,  "Events": count_events("fsb_events.csv")},
    {"Website": "https://medicine.tulane.edu/events-calendar", "Scraped": True, "Events": count_events("medicalSchool_events.csv")},
    {"Website": "https://greek.tulane.edu/event-listings", "Scraped": True, "Events": count_events("tulane_greek_events.csv")},
    {"Website": "https://tmedweb.tulane.edu/clubs/", "Scraped": False, "Events": 0},
    {"Website": "https://campusrecreation.tulane.edu/event-listings", "Scraped": False, "Events": 0},
]

df = pd.DataFrame(websites)

# ---- SUMMARY ----
total_sites = len(df)
scraped_sites = df["Scraped"].sum()
total_events = df["Events"].sum()

print("=== Summary ===")
print(f"Total Websites: {total_sites}")
print(f"Websites Scraped: {scraped_sites}")
print(f"Total Events: {total_events}")

# ---- PLOTS ----
plt.figure(figsize=(14, 5))

# 1. Pie chart for scraping progress
plt.subplot(1, 2, 1)
plt.pie(
    [scraped_sites, total_sites - scraped_sites],
    labels=["Scraped", "Not Scraped"],
    autopct="%1.1f%%",
    colors=["#4CAF50", "#FF5722"]
)
plt.title("Scraping Progress")

# 2. Bar chart for events per website
plt.subplot(1, 2, 2)
plt.barh(df["Website"], df["Events"], color=["#4CAF50" if s else "#FF5722" for s in df["Scraped"]])
plt.title("Events per Website")
plt.xlabel("Events Count")

plt.tight_layout()
plt.show()

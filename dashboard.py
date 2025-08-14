import pandas as pd
import matplotlib.pyplot as plt

# ---- SCRAPING PROGRESS DATA ----
websites = [
    {"Website": "https://tulane.campuslabs.com/engage/events", "Scraped": True,  "Events": 50, "Academic": 20, "Sports": 10, "Others": 20},
    {"Website": "https://events.tulane.edu/", "Scraped": True,  "Events": 40, "Academic": 15, "Sports": 5, "Others": 20},
    {"Website": "https://apply.tulane.edu/portal/tulanecomestoyou", "Scraped": True,  "Events": 30, "Academic": 25, "Sports": 0, "Others": 5},
    {"Website": "https://freeman.tulane.edu/events", "Scraped": True,  "Events": 35, "Academic": 30, "Sports": 0, "Others": 5},
    {"Website": "https://medicine.tulane.edu/events-calendar", "Scraped": False, "Events": 0, "Academic": 0, "Sports": 0, "Others": 0},
    {"Website": "https://tmedweb.tulane.edu/clubs/", "Scraped": False, "Events": 0, "Academic": 0, "Sports": 0, "Others": 0},
    {"Website": "https://campusrecreation.tulane.edu/event-listings", "Scraped": False, "Events": 0, "Academic": 0, "Sports": 0, "Others": 0},
]

df = pd.DataFrame(websites)

# ---- SUMMARY ----
total_sites = len(df)
scraped_sites = df["Scraped"].sum()
total_events = df["Events"].sum()
category_totals = {
    "Academic": df["Academic"].sum(),
    "Sports": df["Sports"].sum(),
    "Others": df["Others"].sum()
}

print("=== Summary ===")
print(f"Total Websites: {total_sites}")
print(f"Websites Scraped: {scraped_sites}")
print(f"Total Events: {total_events}")
print("Category Breakdown:", category_totals)

# ---- PLOTS ----
plt.figure(figsize=(14, 5))

# 1. Pie chart for scraping progress
plt.subplot(1, 3, 1)
plt.pie(
    [scraped_sites, total_sites - scraped_sites],
    labels=["Scraped", "Not Scraped"],
    autopct="%1.1f%%",
    colors=["#4CAF50", "#FF5722"]
)
plt.title("Scraping Progress")

# 2. Bar chart for event categories
plt.subplot(1, 3, 2)
plt.bar(category_totals.keys(), category_totals.values(), color=["#2196F3", "#FFC107", "#9C27B0"])
plt.title("Events by Category")
plt.ylabel("Number of Events")

# 3. Bar chart for events per website
plt.subplot(1, 3, 3)
plt.barh(df["Website"], df["Events"], color=["#4CAF50" if s else "#FF5722" for s in df["Scraped"]])
plt.title("Events per Website")
plt.xlabel("Events Count")

plt.tight_layout()
plt.show()

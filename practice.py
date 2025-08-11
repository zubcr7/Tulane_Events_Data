from bs4 import BeautifulSoup
from bs4.element import NavigableString

html = '''
<li class="views-row">
  <div class="views-field views-field-title">
    <span class="field-content">
      <div class="grid grid-cols-1 md:grid-cols-12">
        <div class="col-span-2 bg-tu-green-official text-white text-center first">
          <div class="card-month">Aug - Oct</div>
          <div class="card-date">4 - 10</div>
          <div class="card-day">Mon - Fri</div>
        </div>
        <div class="col-span-7 second p-10">
          <span class="field-title">
            <a href="/content/rodgers-hammersteins-carousel-2" hreflang="en">
              Rodgers & Hammerstein's CAROUSEL
            </a>
          </span>
          <br><br>
          <strong>
            <span class="smart-date--date">
              <time datetime="2025-08-02T19:30:00-05:00">Sat, Aug 2 2025</time>
            </span>
            ,
            <span class="smart-date--time">
              <time datetime="2025-08-02T19:30:00-05:00">7:30</time>
              -
              <time datetime="2025-08-02T23:00:00-05:00">11pm</time>
            </span>
          </strong>
          <br><br>
          Dixon Hall
        </div>
        <div class="col-span-3 third flex">
          <a href="/content/rodgers-hammersteins-carousel-2" hreflang="en">
            <img loading="lazy" src="/sites/default/files/styles/scale and crop/public/events/carousel.jpg" alt="Event Image">
          </a>
        </div>
      </div>
    </span>
  </div>
</li>'''  # (insert the full HTML string here)

soup = BeautifulSoup(html, 'html.parser')

# Step 1: Find the container div that holds the event info
event_div = soup.find('div', class_='col-span-7 second p-10')

# Step 2: Get all contents (including text) of this div
contents = event_div.contents

# Step 3: After the <strong> tag, look for the next NavigableString (plain text)
venue = None
found_strong = False

for item in contents:
    if item.name == 'strong':
        found_strong = True
    elif found_strong and isinstance(item, NavigableString):
        text = item.strip()
        if text:
            venue = text
            break

print("Venue:", venue)
month = soup.find(class_="card-month").get_text(strip=True)
date = soup.find(class_="card-date").get_text(strip=True)
day = soup.find(class_="card-day").get_text(strip=True)

print("Month:", month)
print("Date:", date)
print("Day:", day)
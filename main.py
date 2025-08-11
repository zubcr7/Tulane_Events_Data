from tulane_events.tulane_scraper import TulaneEventScraper
from tulane_events.campus_scraper import CampusEventScraper

if __name__ == "__main__":
    # Example: run TulaneEventScraper
    scraper = TulaneEventScraper()
    scraper.run()
    # To run CampusEventScraper, uncomment below:
    scraper1 = CampusEventScraper()
    scraper1.run()

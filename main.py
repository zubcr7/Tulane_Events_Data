
from tulane_events.tulane_scraper import TulaneEventScraper
from tulane_events.campus_scraper import CampusEventScraper
from tulane_events.tulane_comesto_u import TulaneComesToYouScraper

if __name__ == "__main__":
    # Run TulaneEventScraper
    scraper = TulaneEventScraper()
    scraper.run()

    # Run CampusEventScraper
    scraper1 = CampusEventScraper()
    scraper1.run()

    # Run TulaneComesToYouScraper
    scraper2 = TulaneComesToYouScraper()
    scraper2.run()

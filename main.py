
from tulane_events.tulane_scraper import TulaneEventScraper
from tulane_events.campus_scraper import CampusEventScraper
from tulane_events.tulane_comesto_u import TulaneComesToYouScraper
from tulane_events.fsb_events import FsbEventsScrapper

if __name__ == "__main__":
    # Run TulaneEventScraper
    scraper = TulaneEventScraper()
    scraper.run()

    # Run CampusEventScraper
    scraper1 = CampusEventScraper()
    scraper1.run()

    # Run Tula    neComesToYouScraper
    scraper2 = TulaneComesToYouScraper()
    scraper2.run()

    scraper3 = FsbEventsScrapper()
    scraper3.run()

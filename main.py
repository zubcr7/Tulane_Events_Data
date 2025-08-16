from tulane_events.tulane_scraper import TulaneEventScraper
from tulane_events.campus_scraper import CampusEventScraper
from tulane_events.tulane_comesto_u import TulaneComesToYouScraper
from tulane_events.fsb_events import FsbEventsScrapper
from tulane_events.medical_school_scraper import MedicalSchoolEventScraper
from tulane_events.greek_frat_events import GreekFratEventsScraper

if __name__ == "__main__":
    # Run TulaneEventScraper
    scraper = TulaneEventScraper()
    scraper.run()

    # Run CampusEventScraper
    scraper1 = CampusEventScraper()
    scraper1.run()

    # Run TulaneComesToYouScraper1
    scraper2 = TulaneComesToYouScraper()
    scraper2.run()

    scraper3 = FsbEventsScrapper()
    scraper3.run()

    # Run MedicalSchoolEventScraper
    medical_scraper = MedicalSchoolEventScraper()
    medical_scraper.scrape()

    # Run GreekFratEventsScraper
    greek_scraper = GreekFratEventsScraper()
    greek_scraper.scrape()

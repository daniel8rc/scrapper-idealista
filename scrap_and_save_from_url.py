from scraper.scraper_selenium_idealista import ScraperSeleniumIdealista
from scraper.scraper_selenium_fotocasa import ScraperSeleniumFotocasa

from mongodb_dao.mongodb_data_recorder import MongoDBDataRecorder
from mongodb_dao.mongodb_config_grabber import MongoConfigGrabber
from mongodb_dao.mongodb_summary_recorder import MongoDBSummaryRecorder

import json

class ScrapAndSaveFromURL():
    def __init__(self):
        self.conf = self.load_conf()
        self.urls = self.conf['idealista_scraper']

    def load_conf(self):
        with open('conf.json', 'r') as myfile:
            data = myfile.read()
        return json.loads(data)

    def main(self):

        scraper_idealista = ScraperSeleniumIdealista(self.urls)

        scraper_idealista.get_data()
        data_idealista = scraper_idealista.data
        summary_dictionary_idealista = scraper_idealista.summaries

        mongodb_data_recorder = MongoDBDataRecorder(data_idealista)
        mongodb_data_recorder.post_data()
        mongodb_summary_recorder_idealista = MongoDBSummaryRecorder(summary_dictionary_idealista)
        mongodb_summary_recorder_idealista.post_data()

if __name__ == '__main__':
    ScrapAndSaveFromURL().main()

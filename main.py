from scraper.scraper_selenium_idealista import ScraperSeleniumIdealista
from scraper.scraper_selenium_fotocasa import ScraperSeleniumFotocasa

from mongodb_dao.mongodb_data_recorder import MongoDBDataRecorder
from mongodb_dao.mongodb_config_grabber import MongoConfigGrabber
from mongodb_dao.mongodb_summary_recorder import MongoDBSummaryRecorder

def main():
    #urls=['https://www.idealista.com/venta-viviendas/galapagar-madrid/con-precio-hasta_300000,chalets,casas-de-pueblo/']
    print("aaaaaaaaaaaaaaa")
    config_grabber = MongoConfigGrabber()
    print("Mongo...")
    config_grabber.get_scrapping_urls()
    print("get...")
    urls_idealista=config_grabber.scrapping_urls_idealista
    # urls_fotocasa = config_grabber.scrapping_urls_fotocasa
    print("1")
    # scraper_fotocasa = ScraperSeleniumFotocasa(urls_fotocasa)
    # scraper_fotocasa.get_data()
    # data_fotocasa = scraper_fotocasa.data
    # summary_dictionary_fotocasa = scraper_fotocasa.summaries
    print("2")
    print(urls_idealista)
    scraper_idealista = ScraperSeleniumIdealista(urls_idealista)
    scraper_idealista.get_data()
    data_idealista = scraper_idealista.data
    summary_dictionary_idealista = scraper_idealista.summaries

    data = data_idealista.copy()
    print(data)
    print("------")
    # data.update(data_fotocasa)

    mongodb_data_recorder = MongoDBDataRecorder(data)
    mongodb_data_recorder.post_data()

    mongodb_summary_recorder_idealista= MongoDBSummaryRecorder(summary_dictionary_idealista)
    mongodb_summary_recorder_idealista.post_data()

    mongodb_summary_recorder_fotocasa= MongoDBSummaryRecorder(summary_dictionary_fotocasa)
    mongodb_summary_recorder_fotocasa.post_data()


if __name__ == '__main__':
	main()

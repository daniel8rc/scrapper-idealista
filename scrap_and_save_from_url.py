from scraper.scraper_selenium_idealista import ScraperSeleniumIdealista
from scraper.scraper_selenium_fotocasa import ScraperSeleniumFotocasa

from mongodb_dao.mongodb_data_recorder import MongoDBDataRecorder
from mongodb_dao.mongodb_config_grabber import MongoConfigGrabber
from mongodb_dao.mongodb_summary_recorder import MongoDBSummaryRecorder

class ScrapAndSaveFromURL():
    def main(self):
        urls=[
            'https://www.idealista.com/point/venta-viviendas/12/con-precio-hasta_200000,precio-desde_120000,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas,ascensor,terraza,publicado_ultimas-48-horas/?shape=%28%28ghzuF%60hxT%3Fbz%60Apjb%40%3F%3Fcz%60Aqjb%40%3F%29%29&ordenado-por=fecha-publicacion-desc',
            'https://www.idealista.com/point/venta-viviendas/12/con-precio-hasta_200000,precio-desde_120000,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas,ascensor,piscina,publicado_ultimas-48-horas/?shape=%28%28ghzuF%60hxT%3Fbz%60Apjb%40%3F%3Fcz%60Aqjb%40%3F%29%29&ordenado-por=fecha-publicacion-desc'
        ]

        scraper_idealista = ScraperSeleniumIdealista(urls)

        scraper_idealista.get_data()
        data_idealista = scraper_idealista.data
        summary_dictionary_idealista = scraper_idealista.summaries

        mongodb_data_recorder = MongoDBDataRecorder(data_idealista)
        mongodb_data_recorder.post_data()
        mongodb_summary_recorder_idealista = MongoDBSummaryRecorder(summary_dictionary_idealista)
        mongodb_summary_recorder_idealista.post_data()

if __name__ == '__main__':
    ScrapAndSaveFromURL().main()

from selenium import webdriver
import sys

from utils_app.util_summary_builder import UtilsSummaryBuilder
from dto.real_state_entry_dto import RealStateEntryDTO
from dto.summary_scrapped_dto import SummaryScrappedDTO

import time 
import random

#https://www.seleniumhq.org/download/
#14393
#https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

class ScraperSeleniumIdealista:

    def __init__(self, urls):
        self.urls = urls
        #self.driver = webdriver.Edge()
        #self.driver = webdriver.Chrome()
        
        # self.driver = webdriver.PhantomJS()
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')

        self.driver = webdriver.Firefox(firefox_options=options)
        self.data ={}
        self.summaries = {}
    
    def get_data(self):
        for url_from_db in self.urls:
            driver = self.driver
            driver.get(url_from_db) 
            #driver.set_window_position(-4000,0)

            self.get_data_from_page(driver,url_from_db) 
        driver.close()
       

    def get_data_from_page(self,driver,url_from_db):
        print("obtaining data from " + driver.current_url)
        item_info_container = self.driver.find_elements_by_class_name("item-info-container")
        mask = self.driver.find_elements_by_class_name("item-multimedia")

        
        random_int =8573 + random.randint(-3, 3)
        driver.execute_script("window.scrollTo(0, "+str(random_int) +");")
        time.sleep(random.uniform(0.5,0.9))
        self.parse_info_container_and_update_data(item_info_container,url_from_db, mask)

        print("obtained " + str(len(self.data[url_from_db])) + " entries")


        time.sleep(random.uniform(0.5,1))
        if (self.is_next_page()):
            url=driver.find_elements_by_class_name("icon-arrow-right-after")[0].get_attribute("href")
            driver.get(url)
            self.get_data_from_page(driver,url_from_db)
        else: 
            self.get_summary(driver,url_from_db)
            

    def is_next_page(self):
        next_button=self.driver.find_elements_by_class_name("icon-arrow-right-after")
        return not next_button == []

    def parse_info_container_and_update_data(self,info_container_array,url_from_db, item_multimedia):
            if(self.data==None): self.data = {}
            if(not url_from_db in self.data.keys()): self.data[url_from_db]=[]
            print("Mismo n??mero de elementos %s" % str(len(info_container_array) == len(item_multimedia)))
            for idx, home in enumerate(info_container_array):
                links = home.find_elements_by_tag_name('a')

                real_estate_title = ''
                real_estate_link = ''
                if len(links) == 2:
                    title = links[0].get_attribute("title").strip()
                    url_element = links[0].get_attribute("href").strip()
                elif len(links) == 3:
                    real_estate_title = links[0].get_attribute("title").strip()
                    real_estate_link = links[0].get_attribute("href").strip()
                    title = links[1].get_attribute("title").strip()
                    url_element = links[1].get_attribute("href").strip()

                images = item_multimedia[idx].find_elements_by_tag_name('img')
                if len(images) > 0:
                    image = images[0].get_attribute("src").strip()
                else:
                    image = ''
                prize=home.find_elements_by_class_name('item-price')[0].text.replace(" ???","").replace("\u20ac","").strip()
                rooms=home.find_elements_by_class_name('item-detail')[0].text.replace(" hab.","").strip()
                meters=home.find_elements_by_class_name('item-detail')[1].text.replace(" m??","").strip()
                floor=home.find_elements_by_class_name('item-detail')[2].text.strip()
                description=home.find_elements_by_class_name('item-description')[0].text

                dto=RealStateEntryDTO(
                    title,prize,meters,rooms,self.driver.current_url,url_element,url_from_db,
                    floor,
                    real_estate_link, real_estate_title, image,
                    description
                )
                self.data[url_from_db]=self.data[url_from_db] + [dto]

    def get_summary(self,driver,url_from_db):
        average_prize=self.driver.find_elements_by_class_name("items-average-price")[0].text.replace("Precio medio","").replace("eur/m??","").strip()
        util_summary_builder=UtilsSummaryBuilder(self.data[url_from_db],url_from_db,average_prize)
        util_summary_builder.obtain_summary()
        summary = util_summary_builder.summary
        self.summaries[url_from_db] = summary
        
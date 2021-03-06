import unittest
import sys
from pymongo import MongoClient
import hashlib
sys.path.append("..")
from scraper.scraper_selenium_fotocasa import ScraperSeleniumFotocasa


class ChangeIdsMongodb(unittest.TestCase):  

    def testFotocasa(self):
        self.client = MongoClient('mongodb://root:rootpassword@localhost:27017')
        self.db = self.client['real-state-db']

        scraped_collection=self.db.scrapped
        for scraped_data in scraped_collection.find({}):
            if(scraped_data["title"]=="" or scraped_data["title"]==None):
                print("cleaning " + scraped_data["_id"])
                if "url_first_page" in scraped_data.keys():
                    hash_object = hashlib.sha1(scraped_data["url_first_page"].encode('utf-8'))
                else: 
                    if ("url_scrapped" in scraped_data.keys()):
                        hash_object = hashlib.sha1(scraped_data["url_scrapped"].encode('utf-8'))
                    
                hex_dig = hash_object.hexdigest() 
                scraped_data["_id"]=hex_dig+scraped_data["_id"]
                scraped_data["title"] = hex_dig
                print("saving " + scraped_data["_id"])

                scraped_collection.save(scraped_data)
        self.assertTrue(True)
if __name__ == '__main__':
	    unittest.main()

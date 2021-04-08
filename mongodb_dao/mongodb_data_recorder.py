import requests
import sys
from pymongo import MongoClient
from dto.real_state_entry_dto import RealStateEntryDTO

from send_email import Mail

class MongoDBDataRecorder:

    def __init__(self, dto_dictionary):
        self.dto_dictionary = dto_dictionary
        self.client = MongoClient('mongodb://root:rootpassword@localhost:27017')
        self.db = self.client['real-state-db']
    
    def post_data(self):
        scrapped_data_collection=self.db.scrapped
        for key, dto_list in self.dto_dictionary.items():
            # print("------- saving data from url " + key)
            for dto in dto_list:
                if scrapped_data_collection.find({'_id': dto._id}).count() == 0:
                    print("saving " + dto._id)
                    dto_mongodb=dto.__dict__
                    scrapped_data_collection.save(dto_mongodb)
                    mail = Mail(dto.__dict__, 'terraza o piscina')
                    mail.send()

                # Test
                # print("saving " + dto._id)

                # print(dto.__dict__)
                # print('-------')
                # break
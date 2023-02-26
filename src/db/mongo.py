import datetime
import os
from contextlib import contextmanager
from typing import Optional

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(".env")

CONNECTION_STRING = "mongodb://{}:{}@{}/".format(
    os.getenv("MONGO_USER"),
    os.getenv("MONGO_PASSWORD"),
    os.getenv("MONGO_HOST"),
    # os.getenv("MONGO_PORT"),
)
# set db
db = MongoClient(CONNECTION_STRING).athome


class MongoDatabase():
    def __init__(self):
        pass

    def add_row(self, row: dict) -> int:
        unique_id = db[self.collection_name].insert_one(row).inserted_id
        return unique_id

    def get_list_of_collections(self) -> list:
        return db.list_collection_names()
    
    def find_by_sort(self, by_sort: list):
        return db[self.collection_name].find_one(sort=by_sort)
    
    def get_all_rows(self, row):
        return [x for x in db[self.collection_name].find(row)]

    def get_all_admins(self, row):
        out = []
        for x in db[self.collection_name].find(row):
            out.append(x["adminID"])
        return out
    
    def drop_collection(self):
        db[self.collection_name].drop()

    def change_data(self, query: dict, update: dict):
        new_update = {"$srt" : update}
        db[self.collection_name].update_one(query, new_update)


class db_collection(MongoDatabase):
    def __init__(self, name_of_collection):
        self.collection_name = name_of_collection




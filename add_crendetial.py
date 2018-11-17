import os
import sys
import time
import json
import calendar
import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId

from config import (MONGO_DB_URL, MONGO_DB_NAME, TABLES)

from collections import Counter 



### Setup database ####

mongo_client = MongoClient(MONGO_DB_URL)
mongo_db = mongo_client[MONGO_DB_NAME]



data = {}

data["ig_username"] = "finallyarbaaz"
data["ig_password"] = "TrashIt420"
data["can_mine"] = True
data["proxy"] = "173.234.232.164:3128"



cred_coll = mongo_db[TABLES["IG_CRED"]]

cred_coll.insert_one(data)
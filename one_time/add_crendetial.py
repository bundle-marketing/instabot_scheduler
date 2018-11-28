import os
import sys
import time
import json
import calendar
import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId

sys.path.append(os.path.join(sys.path[0], '../'))
from db_config.config import (MONGO_DB_URL, MONGO_DB_NAME, TABLES)

from collections import Counter 



### Setup database ####

mongo_client = MongoClient(MONGO_DB_URL)
mongo_db = mongo_client[MONGO_DB_NAME]

cred_coll = mongo_db[TABLES["IG_CRED"]]


with open('credential.json') as f:
	cred_data = json.load(f)

	for username, details in cred_data.items():


		data = {}

		data["ig_username"] = username
		data["ig_password"] = details[0]
		data["proxy"] = details[1]

		data["can_mine"] = details[2]
		

		key = {}
		key["ig_username"] = username

		cred_coll.replace_one(key, data, upsert=True)
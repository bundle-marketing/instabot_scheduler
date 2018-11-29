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

DELAY_MINS = 6 * 60

with open('to_track.json') as f:
	data = json.load(f)

	#Temp fix
	data = data[:50] + data[90:100]

def get_current_time():
	return calendar.timegm(time.gmtime())

client = MongoClient(MONGO_DB_URL)
db = client[MONGO_DB_NAME]

update_follow_coll = db[TABLES["INFLUENCER_CONFIG"]] 

for row in data:

	record = {}

	record["ig_username"] = row[1]
	record["user_id"] = row[2]

	record["active"] = True

	record["delay_mins"] = DELAY_MINS
	record["next_run_ts"] = get_current_time()

	record["media"] = {}

	record["media"]["count"] = 10
	record["media"]["likers"] = True
	record["media"]["comment"] = True


	key = {}
	key["user_id"] = record["user_id"]
	key["ig_username"] = record["ig_username"]

	update_follow_coll.replace_one(key, record, upsert=True)



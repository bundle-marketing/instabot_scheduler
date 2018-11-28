import os
import sys
import time
import json
import calendar
import datetime


from pymongo import MongoClient

sys.path.append(os.path.join(sys.path[0], '../'))
from db_config.config import (MONGO_DB_URL, MONGO_DB_NAME, TABLES)

mongo_client = MongoClient(MONGO_DB_URL)
mongo_db = mongo_client[MONGO_DB_NAME]

config_coll = mongo_db[TABLES["USER_ACTIVITY"]]


def get_current_time():
	return calendar.timegm(time.gmtime())




ts = get_current_time()

data = {}

data["user_name"] = "melrose"
data["ig_username"] = "melrosethriftco"

data["like_delay"] = 20
data["next_like_ts"] = ts

data["follow_delay"] = 15
data["next_follow_ts"] = ts

data["unfollow_delay"] = 15
data["next_unfollow_ts"] = ts


key = {}
key["user_name"] = data["user_name"]
key["ig_username"] = data["ig_username"]



# config_coll.remove({})
config_coll.replace_one(key, data, upsert=True)


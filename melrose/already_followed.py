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


def get_current_time():
	return calendar.timegm(time.gmtime())


### Setup database ####

mongo_client = MongoClient(MONGO_DB_URL)
mongo_db = mongo_client[MONGO_DB_NAME]

activity_coll = mongo_db[TABLES["USER_FOLLOW"]]
# USER_ACTIVITY

user_id = []

with open('already_followed.txt', 'r') as f:
	for line in f.readlines():
		user_id.append(line.strip())

with open('whitelist.txt', 'r') as f:
	for line in f.readlines():
		user_id.append(line.strip())


already_present, new_added = 0, 0
ts = -1

print("Actual len of read lines: ", len(user_id))
print("Set len of read lines: ", len(set(user_id)))


for user in user_id:

	key = { 
		"user_name": "melrose", 
		"ig_username": "melrosethriftco", 
		"target_user_id" : user 
	}

	data = {}

	data["user_name"] = "melrose"
	data["ig_username"] = "melrosethriftco"
	data["target_user_id"] = user
	data["weight"] = -1

	data["followed_time"] = ts
	data["unfollowed_time"] = ts
	data["status"] = 1

	activity_coll.replace_one(key, data, upsert=True)


# 	data = list(activity_coll.find(key))

	

# 	if len(data) == 1:

# 		already_present += 1

# 		data = data[0]
		
# 		data["followed_time"] = ts
# 		data["unfollowed_time"] = ts
# 		data["status"] = 1

# 		activity_coll.update(key, data)

# 	elif len(data) == 0:

# 		new_added += 1

# 		data = {}

# 		data["user_name"] = "melrose"
# 		data["ig_username"] = "melrosethriftco"
# 		data["target_user_id"] = user
# 		data["weight"] = -1

# 		data["followed_time"] = ts
# 		data["unfollowed_time"] = ts
# 		data["status"] = 1

# 		activity_coll.insert_one(data)

# 	print(new_added, "	", already_present)


# print("New added: ", new_added)
# print("Alredy found: ", already_present)


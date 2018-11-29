import os
import sys
import time
import json
import calendar
import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId

from collections import Counter 

sys.path.append(os.path.join(sys.path[0], '../'))
from db_config.config import (MONGO_DB_URL, MONGO_DB_NAME, TABLES)



### Setup database ####

mongo_client = MongoClient(MONGO_DB_URL)
mongo_db = mongo_client[MONGO_DB_NAME]

def get_current_time():
	return calendar.timegm(time.gmtime())

FOLLOW_DOWNLOAD_BUFFER = 7*24*60*60



def get_active_influencer_config():

	config_coll = mongo_db[TABLES["INFLUENCER_CONFIG"]]

	key = {"active" : True, "next_run_ts" : {"$lt": get_current_time()}  }
	sort_key = [ ("next_run_ts" , 1) ]

	return list(config_coll.find(key).sort(sort_key))

def update_active_influencer_config(data):
	config_coll = mongo_db[TABLES["INFLUENCER_CONFIG"]]

	key = {"_id" : data["_id"]}
	config_coll.replace_one(key, data)


def get_user_data(ig_username):

	infl_data_coll = mongo_db[TABLES["INFLUENCER_DATA"]]

	key = {"ig_username" : ig_username}
	sort_key = [ ("timestamp" , -1) ]

	return list(infl_data_coll.find(key).sort(sort_key).limit(1))



def get_active_follow_config():

	config_coll = mongo_db[TABLES["UPDATE_FOLLOW_CONFIG"]]

	key = {"active" : True}

	return list(config_coll.find(key))

def update_active_follow_config(data):
	config_coll = mongo_db[TABLES["UPDATE_FOLLOW_CONFIG"]]

	key = {"_id" : data["_id"]}
	config_coll.replace_one(key, data)



def get_user_follow(user_name, ig_username, target_user_id):

	user_follow_coll = mongo_db[TABLES["USER_FOLLOW"]]

	key = {
		"user_name":user_name,
		"ig_username":ig_username,
		"target_user_id":target_user_id
	}

	records = list(user_follow_coll.find(key))

	if len(records) == 0:
		return None

	else:
		return records[0]

def add_user_follow(data):

	user_follow_coll = mongo_db[TABLES["USER_FOLLOW"]]

	user_follow_coll.insert_one(data)

def update_user_follow(data):

	user_follow_coll = mongo_db[TABLES["USER_FOLLOW"]]

	key = {"_id" : data["_id"]}
	user_follow_coll.replace_one(key, data)




def refresh_user_follow(follow_config_record, user_record):

	print("Going to refresh users")

	if "weight" not in follow_config_record:
		return None
	
	user_list = []

	user_list.extend( user_record["follower"] * follow_config_record["weight"]["follower"]  )
	user_list.extend( user_record["following"] * follow_config_record["weight"]["following"]  )

	if "media" in user_record and "media" in follow_config_record:
		for media in user_record["media"]:

			if "likers" in media and ("likers" in follow_config_record["media"] and follow_config_record["media"]["likers"] == True):
				if "media" in follow_config_record["weight"]:
					user_list.extend( media["likers"] * follow_config_record["weight"]["media"]  )


	user_list = user_list * follow_config_record["weight"]["overall"]
	
	user_list = Counter(user_list)

	for user,weight in user_list.most_common():

		data = get_user_follow(user_name=follow_config_record["user_name"], 
			ig_username=follow_config_record["ig_username"], 
			target_user_id=user)

		if data == None:

			data = {}

			data["user_name"] = follow_config_record["user_name"]
			data["ig_username"] = follow_config_record["ig_username"]
			data["target_user_id"] = user

			data["weight"] = weight
			data["status"] = -1

			add_user_follow(data)

		else:
			data["weight"] += weight
			update_user_follow(data)


def get_active_user_activity(timestamp):

	config_coll = mongo_db[TABLES["USER_ACTIVITY"]]

	key = {
		"$or":[ 
			{"next_like_ts":{"$lt": timestamp}}, 
			{"next_follow_ts":{"$lt": timestamp}}, 
			{"next_unfollow_ts":{"$lt": timestamp}}
		]
	}

	return list(config_coll.find(key))

def update_user_activity(data):

	config_coll = mongo_db[TABLES["USER_ACTIVITY"]]

	key = {"_id" : data["_id"]}
	config_coll.replace_one(key, data)



def create_job_record(job_type, linked_job_id, specific_username=None, weight=0):

	job_config_coll = mongo_db[TABLES["JOB_CONFIG"]]

	data = {}

	data["type"] = job_type
	data["linked_job_id"] = linked_job_id

	if specific_username is not None:
		data["specific_username"] = specific_username

	data["weight"] = weight
	data["release_time"] = get_current_time()
	data["completion_time"] = -1

	data["ran_once"] = False


	job_config_coll.insert_one(data)






def check_pending_activity():

	### Checking which influencer data to capture

	for record in get_active_influencer_config():

		print("Adding grad_data job for username: ", record["ig_username"])

		create_job_record(job_type="get_data", linked_job_id=record["_id"])

		record["next_run_ts"] = get_current_time() + (record["delay_mins"] * 60)
		update_active_influencer_config(record)


	### Updating ig_user's user_follow table

	for record in get_active_follow_config():

		user_record = get_user_data(ig_username=record["target_ig_username"])
		download_data = True

		if len(user_record) > 0:

			user_record = user_record[0]

			if (user_record["info_at_utc"] + FOLLOW_DOWNLOAD_BUFFER) >= get_current_time():
				download_data = False


		if download_data:

			if "download_scheduled" in record and record["download_scheduled"] == True:
				# Already downloading. Wait for being downloaded.
				pass
			else:
				create_job_record(job_type="update_follow", linked_job_id=record["_id"])

				record["download_scheduled"] = True
				update_active_follow_config(record)
			
		else:

			# TODO: Run this on a separate thread
			refresh_user_follow(follow_config_record=record, user_record=user_record)
			
			record["active"] = False
			update_active_follow_config(record)


	### Getting ig_user's next_follow, next_unfollow, next_like
	timestamp = get_current_time()

	for record in get_active_user_activity(timestamp=timestamp):

		if "next_like_ts" in record and "like_delay" in record and record["next_like_ts"] < timestamp:

			print("Adding like hashtag job")
			create_job_record(job_type="like_hashtag", linked_job_id=record["_id"], specific_username=record["ig_username"])
			record["next_like_ts"] = timestamp + (record["like_delay"] * 60)


		if "next_follow_ts" in record and "follow_delay" in record and record["next_follow_ts"] < timestamp:

			print("Adding follow user job")
			create_job_record(job_type="follow", linked_job_id=record["_id"], specific_username=record["ig_username"])
			record["next_follow_ts"] = timestamp + (record["follow_delay"] * 60)


		if "next_unfollow_ts" in record and "unfollow_delay" in record and record["next_unfollow_ts"] < timestamp:

			print("Adding unfollow user job")
			create_job_record(job_type="unfollow", linked_job_id=record["_id"], specific_username=record["ig_username"])
			record["next_unfollow_ts"] = timestamp + (record["unfollow_delay"] * 60)

		update_user_activity(record)


if __name__ == '__main__':
	while True:
		check_pending_activity()
		print("Going to sleep")
		time.sleep(30)





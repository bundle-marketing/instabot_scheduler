from config import (MONGO_DB_URL, MONGO_DB_NAME, TABLES)

import argparse
import os
import sys
import time
import json
import calendar
import datetime

from tqdm import tqdm
from pymongo import MongoClient

from bson.objectid import ObjectId


## Setting up Database connection ##

client = MongoClient(MONGO_DB_URL)
db = client[MONGO_DB_NAME]


def get_job_record():
	job_config_coll = db[TABLES["JOB_CONFIG"]]


	key = {"success" : True}

	return list(job_config_coll.find(key))

def get_user_data(ig_username):
	coll = db[TABLES["INFLUENCER_DATA"]]


	key = {"ig_username" : ig_username}

	records = list(coll.find(key))

	if len(records) != 1 :
		return None

	return records[0]


def get_config(id, table_name=TABLES["UPDATE_FOLLOW_CONFIG"]):
	config_coll = db[table_name]


	key = {"_id" : id}

	records = list(config_coll.find(key))

	if len(records) != 1 :
		return None

	return records[0]



if __name__ == '__main__':
	count = 0
	zero_count = 0
	unique_users = []
	for rec in get_job_record():

		# print(count)
		count += 1

		config = get_config(rec["linked_job_id"])

		if config == None:
			continue

		data = get_user_data(config["target_ig_username"])

		if data == None:
			continue

		if len(data["follower"]) == 0:
			print(data)
			zero_count += 1
		else:
			print(len(data["follower"]))
		
		unique_users.extend(data["follower"])
		unique_users.extend(data["following"])

		for med in data["media"]:
			unique_users.extend(med["likers"])

	print("Totoal count ", count)
	print("Unique users ", len(set(unique_users)))
	print("Users wwith 0 followers ", zero_count)
			# print(config["ig_username"])










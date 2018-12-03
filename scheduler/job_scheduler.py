import os
import sys
import time
import json
import calendar
import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId

import docker


sys.path.append(os.path.join(sys.path[0], '../'))
from db_config.config import (MONGO_DB_URL, MONGO_DB_NAME, TABLES)


### Setup database ####

mongo_client = MongoClient(MONGO_DB_URL)
mongo_db = mongo_client[MONGO_DB_NAME]


### Setup docker client ####

docker_client = docker.from_env()

def check_pending_jobs(max_jobs=50):

	job_config_coll = mongo_db[TABLES["JOB_CONFIG"]]

	key = {"specific_username" : "" , "completion_time" : -1}
	sort_key = [ ("weight", -1), ("release_time", 1) ]
	
	return list(job_config_coll.find(key).sort(sort_key).limit(max_jobs))

def update_job_record(job_record):

	print(job_record)

	job_config_coll = mongo_db[TABLES["JOB_CONFIG"]]

	key = { "_id" : job_record["_id"]}
	job_config_coll.replace_one(key, job_record)



def get_running_ig_mining_bots():
	running_cred = []

	for container in docker_client.containers.list():

		read_labels = container.labels

		if "bot_type" in read_labels and read_labels["bot_type"] == "instagram":
			if "can_mine" in read_labels and read_labels["can_mine"] == "yes":
				if "bot_username_in_use" in read_labels:
					running_cred.append(read_labels["bot_username_in_use"])
	
	print(running_cred)

	return running_cred


## static global variable
##TODO: Ensure faire round-bin
# avail_cred = get_running_ig_mining_bots()

def schedule_jobs():

	# global avail_cred
	avail_cred = get_running_ig_mining_bots()
	

	for job in check_pending_jobs():

		if len(avail_cred) == 0:
			# avail_cred = get_running_ig_mining_bots()
			break

		job["specific_username"] = avail_cred.pop()
		update_job_record(job)


def main():
	while True:
		schedule_jobs()
		print("Going to sleep")
		time.sleep(30)


if __name__ == '__main__':
	main()





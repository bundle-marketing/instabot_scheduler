import os
import sys
import time
import json
import calendar
import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId

import docker


from config import (MONGO_DB_URL, MONGO_DB_NAME, TABLES)




### Setup database ####

mongo_client = MongoClient(MONGO_DB_URL)
mongo_db = mongo_client[MONGO_DB_NAME]


### Setup docker client ####

docker_client = docker.from_env()
IMAGE_NAME = "instabot:latest"

IMAGE_COMMAND = list("python3 bot/runner.py".split(' '))
PORT_DICT = {'80/tcp': None}



def check_pending_jobs():

	job_config_coll = mongo_db[TABLES["JOB_CONFIG"]]

	key = {"completion_time" : -1}
	sort_key = [ ("weight", -1), ("release_time", 1) ]
	
	return list(job_config_coll.find(key).sort(sort_key))#.limit(max_jobs))


def get_all_bot_credentials():

	insta_cred_coll = mongo_db[TABLES["IG_CRED"]]

	key = {"can_mine" : True}

	return insta_cred_coll.find(key)


def get_bot_credentials(username):

	insta_cred_coll = mongo_db[TABLES["IG_CRED"]]

	key = {"ig_username" : username}

	return list(insta_cred_coll.find(key))[0]


def get_running_jobs():
	running_cred = []
	running_jobs = []

	for container in docker_client.containers.list():
		##Container name = JOBID_CRED
		job, cred  = container.name.split('_')

		running_cred.append(cred)
		running_jobs.append(job)

	return ( set(running_cred), set(running_jobs))


def schedule_job_now(job_id, cred_to_use):
	if cred_to_use == None:
		return

	environment_var = {
		"JOB_ID" : str(job_id), 
		
		"USERNAME" : cred_to_use["ig_username"],
		"PASSWORD" : cred_to_use["ig_password"],
		"PROXY" : cred_to_use["proxy"]

	}

	container_name = str(job_id) + "_" +  environment_var["USERNAME"]

	print("Going to run job " + container_name)

	docker_client.containers.run(image=IMAGE_NAME, 
		command=IMAGE_COMMAND,
		remove=True,
		environment=environment_var,
		name=container_name,
		detach=True)





def schedule_jobs():
	running_cred, running_jobs = get_running_jobs()
	pending_jobs = check_pending_jobs()

	valid_cred = []

	for cred in get_all_bot_credentials():
		if cred["ig_username"] not in running_cred:
			valid_cred.append(cred)

	for job in pending_jobs:
		if str(job["_id"]) in running_jobs:
			continue

		#TODO: Temp fix
		if "ran_once" in job and job["ran_once"] == True:
			continue

		cred_to_use = None

		if job["type"] == "follow" or job["type"] == "unfollow" or job["type"] == "hashtag":

			# BOt credentials must be same as user_owened IG
			if "specific_username" not in job or job["specific_username"] in running_cred:
				continue

			cred_to_use = get_bot_credentials(job["specific_username"])

		else:

			if len(valid_cred) > 0:
				cred_to_use = valid_cred[-1]
				running_cred.add(cred_to_use["ig_username"])
				valid_cred.pop()

			else:
				continue

		schedule_job_now(job_id=str(job["_id"]), cred_to_use=cred_to_use)


def main():
	while True:
		schedule_jobs()
		print("Going to sleep")
		time.sleep(2 * 60)


if __name__ == '__main__':
	main()





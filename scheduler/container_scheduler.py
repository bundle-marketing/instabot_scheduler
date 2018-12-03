# TODO: Get current running containers to grab running credentials
# TODO: Run containers for creredentials not running
# TODO: Perfrom login time enforcement


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

IMAGE_NAME = "instabot:latest"
IMAGE_COMMAND = list("python3 bot/runner.py".split(' '))


def get_current_time():
	return calendar.timegm(time.gmtime())

def run_ig_bot(cred_to_use):
	if cred_to_use == None:
		return

	environment_var = {}

	try:

		environment_var["USERNAME"] = cred_to_use["ig_username"]
		environment_var["PASSWORD"] = cred_to_use["ig_password"]
		environment_var["PROXY"] = cred_to_use["proxy"]
	except:

		return

	label = {
		"bot_type" : "instagram",
		"can_mine" : "yes" if cred_to_use["can_mine"] else "no",
		"bot_username_in_use" : environment_var["USERNAME"]
	}

	container_name = environment_var["USERNAME"] + "__" + str(get_current_time())

	print("Starting a container with name ", container_name)
	print(label)
	print(environment_var)


	docker_client.containers.run(image=IMAGE_NAME, 
		command=IMAGE_COMMAND,
		environment=environment_var,
		detach=True,
		labels=label,
		# remove=True,
		name=container_name)


def get_all_bot_credentials():

	insta_cred_coll = mongo_db[TABLES["IG_CRED"]]
	key = {}

	return list(insta_cred_coll.find(key))


def get_running_ig_bots():
	running_cred = []

	for container in docker_client.containers.list():

		read_labels = container.labels

		if "bot_type" in read_labels and read_labels["bot_type"] == "instagram":
			if "bot_username_in_use" in read_labels:
				running_cred.append(read_labels["bot_username_in_use"])
	
	return running_cred


def run_bots():

	running_cred = get_running_ig_bots()
	for cred_to_run in get_all_bot_credentials():

		if cred_to_run["ig_username"] not in running_cred:
			run_ig_bot(cred_to_run)



def main():
	while True:
		run_bots()
		print("Going to sleep")
		time.sleep(30)


if __name__ == '__main__':
	main()

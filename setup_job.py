import os
import sys
import time
import json
import calendar
import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId


from config import (MONGO_DB_URL, MONGO_DB_NAME, TABLES)



target_usernames = list("Driftcollective Muurphh Emma.sassaman Maggieeweltonn Lilyrimel Asudeltazeta Asualphaphi Asu_deltagamma Asu_kd Howdoyouwearthat Addysonrae Carlieedaviss14 Kelcboydd Addyythuerck Lizziedonohue Kpsunshine Best.dressed Charmcd Jamielynkane Allisonfishh Oliviaaadillon Mollyxworld Psychedelic_hh Cameron_mccreight Littleromans Seepayy Sav_wade Vedatappin Maddietyerech Micjanee Hauteinstinct Misslucyfleur Ihateblonde Alliemalaway Sara_waiste Kyliecallander Alittlepaperdoll Nicolealyseee mirandanugentt Jessicawoods Chapmanaphi Gracieaber Carrie_connelly Iindiefoxx Alexismaymcmullin Electricwest Megmoroney Miracleeye Thevintagetwin Allie_franz Marissabrunoo  Coddderbe Alix_earle Mo0orgs Sammy.levine Morgan.yates Brit_harvey Mackday Keegannesharko Kylieklemps Jenwetton Audreykazmar 8otherreasons Kennedyvantrump Kaileehall Eileencassidy".split(' '))
# Sydfrenkel




client = MongoClient(MONGO_DB_URL)
db = client[MONGO_DB_NAME]
job_config_coll = db[TABLES["JOB_CONFIG"]]
influencer_config_coll = db[TABLES["INFLUENCER_CONFIG"]]




for user in target_usernames:


	data = {}

	data["ig_username"] = user
	data["media"] = {}
	data["media"]["count"] = 10
	data["media"]["likers"] = True
	data["media"]["comment"] = True

	influencer_config_coll.insert_one(data)

	key = {"ig_username" : user}

	rec_data = list(influencer_config_coll.find(key))[0]


	data = {}

	data["type"] = "get_data"
	data["linked_job_id"] = rec_data["_id"]

	data["weight"] = 0
	data["release_time"] = calendar.timegm(time.gmtime())
	data["completion_time"] = -1

	job_config_coll.insert_one(data)
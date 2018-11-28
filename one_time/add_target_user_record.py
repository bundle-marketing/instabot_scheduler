import os
import sys
import time
import json
import calendar
import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId


from config import (MONGO_DB_URL, MONGO_DB_NAME, TABLES)



target_usernames = list("Sydfrenkel Driftcollective Muurphh Emma.sassaman Maggieeweltonn Lilyrimel Asudeltazeta Asualphaphi Asu_deltagamma Asu_kd Howdoyouwearthat Addysonrae Carlieedaviss14 Kelcboydd Addyythuerck Lizziedonohue Kpsunshine Best.dressed Charmcd Jamielynkane Allisonfishh Oliviaaadillon Mollyxworld Psychedelic_hh Cameron_mccreight Littleromans Seepayy Sav_wade Vedatappin Maddietyerech Micjanee Hauteinstinct Misslucyfleur Ihateblonde Alliemalaway Sara_waiste Kyliecallander Alittlepaperdoll Nicolealyseee mirandanugentt Jessicawoods Chapmanaphi Gracieaber Carrie_connelly Iindiefoxx Alexismaymcmullin Electricwest Megmoroney Miracleeye Thevintagetwin Allie_franz Marissabrunoo  Coddderbe Alix_earle Mo0orgs Sammy.levine Morgan.yates Brit_harvey Mackday Keegannesharko Kylieklemps Jenwetton Audreykazmar 8otherreasons Kennedyvantrump Kaileehall Eileencassidy".split(' '))
# 




client = MongoClient(MONGO_DB_URL)
db = client[MONGO_DB_NAME]

update_follow_coll = db[TABLES["UPDATE_FOLLOW_CONFIG"]] 


# job_config_coll = db[TABLES["JOB_CONFIG"]]
# influencer_config_coll = db[TABLES["INFLUENCER_CONFIG"]]




for user in target_usernames:


	data = {}

	data["user_name"] = "melrose"
	data["ig_username"] = "melrosethriftco"
	data["target_ig_username"] = user

	data["active"] = True


	data["weight"] = {}
	data["weight"]["overall"] = 1
	data["weight"]["follower"] = 3
	data["weight"]["following"] = 1
	data["weight"]["media"] = 2
	

	data["media"] = {}
	data["media"]["count"] = 10
	data["media"]["likers"] = True
	data["media"]["comment"] = False

	update_follow_coll.insert_one(data)




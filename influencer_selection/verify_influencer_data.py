import argparse
import os
import sys
import time
import json
import calendar
import datetime
# from tqdm import tqdm

from pymongo import MongoClient
from collections import Counter 

sys.path.append(os.path.join(sys.path[0], '../'))
from db_config.config import (MONGO_DB_URL, MONGO_DB_NAME, TABLES)


client = MongoClient(MONGO_DB_URL)
db = client[MONGO_DB_NAME]


with open('to_track.json') as f:
	target_list = json.load(f)

def get_current_time():
	return calendar.timegm(time.gmtime())


def get_influencer_data(username):

	infl_data_coll = db[TABLES["INFLUENCER_DATA"]]

	key = {"ig_username" : username}
	sort_key = [ ("info_at_utc" , 1) ]

	return list(infl_data_coll.find(key).sort(sort_key))


change_dict = {}

def calculate_follower_change():


	for target_rec in target_list:

		target = target_rec[1]
		change_dict[target] = []

		data_records = get_influencer_data(target)

		count = 0

		prev_follow_count = target_rec[0]
		prev_following_count = 0


		for rec in data_records:

			# Unfinished downloads
			if rec["follower_count"] == 0: # or rec["follower_count"] < prev_follow_count*(0.95)
				continue
			
			# count += 1

			change = round(((rec["follower_count"] - prev_follow_count) / float(prev_follow_count)) * 100, 2)
			if abs(change) > 20.0:
				continue

			change_following = 0
			
			if prev_following_count == 0:
				change_following = round(((rec["following_count"] - prev_following_count) / float(prev_following_count)) * 100, 2)

			change_dict[target].append( (rec["info_at_utc"], change, change_following)  )

			# print(rec["info_at_utc"], " : ", rec["follower_count"]  ," : ", change)

			prev_follow_count = rec["follower_count"]
			prev_following_count = rec["following_count"]



	print(change_dict)

	with open('change_follower.json', 'w') as outfile:
	    json.dump(change_dict, outfile)
	# print("Valid records for ", target, " : ", count, " : ", target_rec[0])



# def calculate_current_media_stats():
	
# 	for target_rec in target_list:

# 		target = target_rec[1]
# 		change_dict[target] = []

# 		data_records = get_influencer_data(target)

# 		count = 0

# 		prev_follow_count = target_rec[0]


# 		for rec in data_records:

# 			# Unfinished downloads
# 			if rec["follower_count"] == 0: # or rec["follower_count"] < prev_follow_count*(0.95)
# 				continue
			
# 			# count += 1

# 			change = round(((rec["follower_count"] - prev_follow_count) / float(prev_follow_count)) * 100, 2)
# 			if abs(change) > 20.0:
# 				continue

# 			change_dict[target].append( (rec["info_at_utc"], change)  )

# 			# print(rec["info_at_utc"], " : ", rec["follower_count"]  ," : ", change)

# 			prev_follow_count = rec["follower_count"]



# 	print(change_dict)

# 	with open('change_follower.json', 'w') as outfile:
# 	    json.dump(change_dict, outfile)



def main():
	calculate_follower_change()



if __name__ == '__main__':
	main()






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


def calculate_new_follower(input_data_records):

	change_dict = {}

	for target_rec in target_list:

		target = target_rec[1]
		change_dict[target] = {}
		change_dict[target]["follower"] = []
		change_dict[target]["following"] = []

		data_records = input_data_records[target]

		count = 0

		prev_follow = None
		prev_following = None

		for rec in data_records:

			# Unfinished downloads
			if rec["follower_count"] == 0: # or rec["follower_count"] < prev_follow_count*(0.95)
				continue

			if prev_follow is not None:
				new_follower = set(rec["follower"]) - prev_follow

				follower_change = len(new_follower) / float(rec["follower_count"])
				follower_change = round(follower_change * 100, 2)

				change_dict[target]["follower"].append((rec["info_at_utc"],follower_change))

			if prev_following is not None:
				new_follower = set(rec["following"]) - prev_following

				follower_change = 0

				if rec["following_count"] == 0:
					if len(prev_following) != 0:
						follower_change = 100
				else:
					follower_change = len(new_follower) / float(rec["following_count"])
					follower_change = round(follower_change * 100, 2)

				change_dict[target]["following"].append((rec["info_at_utc"],follower_change))

			prev_follow = set(rec["follower"])
			prev_following = set(rec["following"])

	with open('new_follower.json', 'w') as outfile:
	    json.dump(change_dict, outfile)

def calculate_follower_change(input_data_records):

	change_dict = {}


	for target_rec in target_list:

		target = target_rec[1]
		change_dict[target] = []

		data_records = input_data_records[target]

		count = 0

		prev_follow_count = target_rec[0]
		prev_following_count = 0

		for rec in data_records:

			# Unfinished downloads
			if rec["follower_count"] == 0: # or rec["follower_count"] < prev_follow_count*(0.95)
				continue

			count += 1

			change = ((rec["follower_count"] - prev_follow_count) / float(prev_follow_count)) * 100
			change = round(change, 2)
			# if abs(change) > 20.0:
			# 	print(target, " : ", change)
			# 	continue

			change_following = 0
			
			if prev_following_count != 0:
				change_following = round(((rec["following_count"] - prev_following_count) / float(prev_following_count)) * 100, 2)

			change_dict[target].append( (rec["info_at_utc"], change, change_following)  )

			# print(rec["info_at_utc"], " : ", rec["follower_count"]  ," : ", change)

			prev_follow_count = rec["follower_count"]
			prev_following_count = rec["following_count"]


		print("Valid records for ", target, " : ", count, " : ", target_rec[0])
	# print( )

	with open('change_follower.json', 'w') as outfile:
	    json.dump(change_dict, outfile)



def calculate_current_media_stats(input_data_records):

	change_dict = {}
	
	for target_rec in target_list:

		target = target_rec[1]
		change_dict[target] = {}

		data_records = input_data_records[target]

		count = 0

		prev_likers_dict = {}
		prev_comment_dict = {}

		for rec in data_records:

			# Unfinished downloads
			if rec["follower_count"] == 0 or "media" not in rec: # or rec["follower_count"] < prev_follow_count*(0.95)
				continue

			# print()

			for media_entry in rec["media"]:

				if "media_id" not in media_entry:
					continue

				if media_entry["media_id"] not in change_dict[target]:
					change_dict[target][media_entry["media_id"]] = {}
					change_dict[target][media_entry["media_id"]]["like"] = []
					change_dict[target][media_entry["media_id"]]["like_new"] = []

					change_dict[target][media_entry["media_id"]]["comment"] = []
					# change_dict[target][media_entry["media_id"]]["comment_new"] = []

				if "like_count" in media_entry and "likers" in media_entry and len(media_entry["likers"]) == media_entry["like_count"]:

					# print(media_entry)

					change_likers = 0
					prev_likers = set([])
					prev_likers_count = 0

					if media_entry["media_id"] in prev_likers_dict:
						prev_likers = prev_likers_dict[media_entry["media_id"]]
						prev_likers_count = len(prev_likers)


					if prev_likers_count != 0 and media_entry["like_count"] != 0:

						change_likers = round(((media_entry["like_count"] - prev_likers_count) / float(media_entry["like_count"])) * 100, 2)
						change_dict[target][media_entry["media_id"]]["like"].append( (media_entry["timestamp"], change_likers)  )

						change_likers = round((len(set(media_entry["likers"]) - prev_likers) / float(media_entry["like_count"])) * 100, 2)
						change_dict[target][media_entry["media_id"]]["like_new"].append( (media_entry["timestamp"], change_likers)  )

					prev_likers_dict[media_entry["media_id"]] = set(media_entry["likers"])


				if "comment_count" in media_entry and "comments" in media_entry and len(media_entry["comments"]) == media_entry["comment_count"]:

					change_comment = 0
					# prev_comment = set([])
					prev_comment_count = 0

					if media_entry["media_id"] in prev_comment_dict:
						 # prev_comment = prev_comment_dict[media_entry["media_id"]]
						 # prev_comment_count = len(prev_comment)

						 prev_comment_count = prev_comment_dict[media_entry["media_id"]]

					if prev_comment_count != 0 and media_entry["comment_count"] != 0:
						change_comment = round(((media_entry["comment_count"] - prev_comment_count) / float(media_entry["comment_count"])) * 100, 2)
						change_dict[target][media_entry["media_id"]]["comment"].append( (media_entry["timestamp"], change_comment)  )

						# change_comment = round(((media_entry["comment_count"] - prev_comment_count) / float(media_entry["comment_count"])) * 100, 2)
						# change_dict[target][media_entry["media_id"]]["comment"].append( (media_entry["timestamp"], change_comment)  )

					prev_comment_dict[media_entry["media_id"]] = media_entry["comment_count"]

		# print(change_dict[target])
		# break



	# print(change_dict)

	with open('change_media.json', 'w') as outfile:
	    json.dump(change_dict, outfile)



def main():

	input_data_records = {}

	for target_rec in target_list:

		target = target_rec[1]
		input_data_records[target] = get_influencer_data(target)

	# calculate_follower_change(input_data_records)
	calculate_current_media_stats(input_data_records)

	# calculate_new_follower(input_data_records)



if __name__ == '__main__':
	main()






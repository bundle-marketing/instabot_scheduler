import argparse
import os
import sys
import time
import json
import calendar
import datetime
from tqdm import tqdm

from pymongo import MongoClient
from collections import Counter 

sys.path.append(os.path.join(sys.path[0], '../'))
from db_config.config import (MONGO_DB_URL, MONGO_DB_NAME, TABLES)

# import numpy

# import matplotlib as mpl
# mpl.use('Agg')
# from matplotlib import pyplot


def binary_search(inp, target):

	left, right = 0, len(inp)

	while (left < right):
		mid = (left + right) // 2

		if inp[mid][0] == target:
			return mid

		elif inp[mid][0] > target:
			right = mid-1

		else:

			left = mid+1

	return min(left, right)






client = MongoClient(MONGO_DB_URL)
db = client[MONGO_DB_NAME]

pot_infl_coll = db[TABLES["POTENTIAL_INFLUENCER"]]



influencer_records = list(pot_infl_coll.find({}))
print("Records recieved: " + str(len(influencer_records)))

follower_freq = []
user_id_list = []

for rec in influencer_records:
	follower_freq.append( rec["follower_count"] )

	user_id_list.append(  (rec["follower_count"], rec["username"], rec["user_id"]) )


user_id_list.sort()
# print(user_id_list[:10])

follower_freq = Counter(follower_freq)


x_data, y_data = [], [] 

for key,val in follower_freq.most_common():
	x_data.append(key)
	y_data.append(val)

for_sort = sorted(zip(x_data, y_data), key=lambda x: x[0])

x_data = [x[0] for x in for_sort]
y_data = [x[1] for x in for_sort]


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-num_bars', type=int, help="Number of bars")
parser.add_argument('--min_follow', type=int, help="Minumum number of followers to be included")
parser.add_argument('--max_follow', type=int, help="Maximum number of followers to be included.")
parser.add_argument('--user_count', type=int, help="Number of users from each side to be grabbed")
args = parser.parse_args()

# python3 user_visualizer.py -num_bars 20 --min_follow 10000 --max_follow 100000 --user_count 50



NUM_BARS = int(args.num_bars)
MIN_FOLLOWERS = min(x_data)
MAX_LIMIT = max(x_data)

if args.max_follow is not None:
	MAX_LIMIT = int(args.max_follow)

if args.min_follow is not None:
	MIN_FOLLOWERS = int(args.min_follow)

print("Minimum limit on followers: "+str(MIN_FOLLOWERS))
print("Maximum limit on followers: "+str(MAX_LIMIT))



if args.user_count is not None:

	min_idx = binary_search(user_id_list, MIN_FOLLOWERS)

	if user_id_list[min_idx][0] < MIN_FOLLOWERS:
		min_idx += 1

	max_idx = binary_search(user_id_list, MAX_LIMIT)
	
	if user_id_list[max_idx][0] > MAX_LIMIT:
		max_idx -= 1

	to_write = user_id_list[ min_idx : min_idx+args.user_count ] + user_id_list[ max_idx-args.user_count+1 : max_idx+1 ]
	
	with open('to_track.json', 'w') as outfile:
		json.dump(to_write, outfile)




x, y = [], []
x_str = MIN_FOLLOWERS

step_increase = int((MAX_LIMIT - MIN_FOLLOWERS) / NUM_BARS)

print("Step increase: "+str(step_increase))

for i in range(NUM_BARS):

	new_str = int(MIN_FOLLOWERS + (step_increase * (i+1)) )
	x.append(str(x_str) + '-' + str(new_str))

	x_str = new_str + 1

	

y = [0] * NUM_BARS
for i in range(len(x_data)):
	
	if x_data[i] < MIN_FOLLOWERS or x_data[i] > MAX_LIMIT:
		continue


	# y_ind = int(x_data[i] / (MAX_LIMIT/NUM_BARS))
	y_ind = int((x_data[i] - MIN_FOLLOWERS) / step_increase)

	if y_ind >= len(y) or x_data[i] < MIN_FOLLOWERS:
		continue

	y[ y_ind ] += y_data[i]


print("Sum of bar area : " + str(sum(y)))
print(x)
print(y)


# pyplot.bar(x, y, align = 'center') 

# pyplot.title('Bar graph') 

# pyplot.ylabel('Frequency') 
# pyplot.xlabel('Follower count')  

# pyplot.show()



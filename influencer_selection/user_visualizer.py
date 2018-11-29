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

import numpy

import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot





client = MongoClient(MONGO_DB_URL)
db = client[MONGO_DB_NAME]

pot_infl_coll = db[TABLES["POTENTIAL_INFLUENCER"]]

# records = pot_infl_coll.find({})



following_count = list(pot_infl_coll.find({}))

# for rec in records:
# 	if rec["follower_count"] > FOLLOWER_BASE:
# 		following_count.append(rec)

print("Records recieved: " + str(len(following_count)))

follower_freq = []
user_id_list = []

for rec in following_count:

	# if rec["following_count"] == 0:
	# 	follower_freq.append(0)

	# else:
		# follower_freq.append( int((rec["follower_count"]/rec["following_count"])*100) )

	follower_freq.append( rec["follower_count"] )
	# user_id_list.append( rec["user_id"] )

follower_freq = Counter(follower_freq)

# print(len(set(user_id_list)))


x_data, y_data = [], [] 

for key,val in follower_freq.most_common():
	x_data.append(key)
	y_data.append(val)

for_sort = sorted(zip(x_data, y_data), key=lambda x: x[0])

x_data = [x[0] for x in for_sort]
y_data = [x[1] for x in for_sort]


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-num_bars', type=int, help="Number of bars")
parser.add_argument('-min_follow', type=int, help="Minumum number of followers to be included")
parser.add_argument('-max_follow', type=int, help="Maximum number of followers to be included. -1 for max")
args = parser.parse_args()

# python3 user_visualizer.py -num_bars 20 -min_follow 10000 -max_follow 100000



NUM_BARS = int(args.num_bars)
MIN_FOLLOWERS = int(args.min_follow)
MAX_LIMIT = int(args.max_follow)

if MAX_LIMIT == -1:
	MAX_LIMIT = max(x_data)

print("Minimum limit on followers: "+str(MIN_FOLLOWERS))
print("Maximum limit on followers: "+str(MAX_LIMIT))


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


pyplot.bar(x, y, align = 'center') 

pyplot.title('Bar graph') 

pyplot.ylabel('Frequency') 
pyplot.xlabel('Follower count')  

pyplot.show()




		# data["user_id"] = user_id
		# data["username"] = user_id_info["username"]
		# data["info_at_utc"] = calendar.timegm(time.gmtime())

		# data["following_count"] = user_id_info["following_count"]
		# data["follower_count"] = user_id_info["follower_count"]



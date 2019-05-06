import argparse
import os
import sys
import time
import json
import calendar
import datetime

sys.path.append(os.path.join(sys.path[0], '../'))
from db_config.config import (MONGO_DB_URL, MONGO_DB_NAME, TABLES)

# from tqdm import tqdm
from pymongo import MongoClient, IndexModel, ASCENDING, DESCENDING


mongo_client = MongoClient(MONGO_DB_URL)
mongo_db = mongo_client[MONGO_DB_NAME]


### Table USER_CONFIG ####

index_list = [
	IndexModel( [("user_name", DESCENDING)], name="unique_username", unique=True, dropDups=True)
	]

mongo_db[TABLES["USER_CONFIG"]].create_indexes(index_list)


### Table USER_ACTIVITY ####

index_list = [
	IndexModel( [("user_name", DESCENDING), ("ig_username", DESCENDING)], name="unique_user_ig", unique=True, dropDups=True),
	IndexModel( [("next_like_ts", DESCENDING)]),
	IndexModel( [("next_follow_ts", DESCENDING)]),
	IndexModel( [("next_unfollow_ts", DESCENDING)])
	]

mongo_db[TABLES["USER_ACTIVITY"]].create_indexes(index_list)



### Table USER_FOLLOW ####

index_list = [
	IndexModel( [("user_name", DESCENDING), ("target_user_id", DESCENDING)], name="unique_target_id", unique=True, dropDups=True),
	IndexModel( [("user_name", DESCENDING), ("ig_username", DESCENDING)], name="unique_target", unique=True, dropDups=True),
	IndexModel( [("status", ASCENDING), ("weight", DESCENDING)], name="find_next_follow"),
	IndexModel( [("status", ASCENDING), ("unfollowed_time", DESCENDING), ("weight", DESCENDING)], name="find_next_unfollow")
	]

mongo_db[TABLES["USER_FOLLOW"]].create_indexes(index_list)


### Table USER_HASHTAG #### 

index_list = [
	IndexModel( [("user_name", DESCENDING), ("ig_username", DESCENDING), ("hashtag", DESCENDING)], name="unique_hashtag", unique=True, dropDups=True),
	IndexModel( [("last_liked", ASCENDING)])
	]

mongo_db[TABLES["USER_HASHTAG"]].create_indexes(index_list)


### Table UPDATE_FOLLOW_CONFIG ####

index_list = [
	IndexModel( [("user_name", DESCENDING), ("ig_username", DESCENDING), ("target_ig_username", DESCENDING)], name="unique_target", unique=True, dropDups=True),
	IndexModel( [("active", ASCENDING)])
	]

mongo_db[TABLES["UPDATE_FOLLOW_CONFIG"]].create_indexes(index_list)


### Table INFLUENCER_CONFIG ####

index_list = [
	IndexModel( [("user_id", DESCENDING), ("ig_username", DESCENDING)], name="unique_target", unique=True, dropDups=True),
	IndexModel( [("active", ASCENDING), ("next_run_ts", ASCENDING)])
	]

mongo_db[TABLES["INFLUENCER_CONFIG"]].create_indexes(index_list)


### Table IG_CRED ####

index_list = [
	IndexModel( [("ig_username", DESCENDING)], name="unique_cred", unique=True, dropDups=True),
	IndexModel( [("can_mine", ASCENDING)])
	]

mongo_db[TABLES["IG_CRED"]].create_indexes(index_list)


### Table INFLUENCER_DATA ####

index_list = [
	IndexModel( [("user_id", DESCENDING), ("ig_username", DESCENDING), ("info_at_utc", DESCENDING)], name="unique_data", unique=True, dropDups=True),
	IndexModel( [("ig_username", DESCENDING), ("info_at_utc", DESCENDING)], name="sorted_ig_username_data"),
	IndexModel( [("user_id", DESCENDING), ("info_at_utc", DESCENDING)], name="sorted_userd_id_data")
	]

mongo_db[TABLES["INFLUENCER_DATA"]].create_indexes(index_list)


### Table JOB_CONFIG ####

index_list = [
	IndexModel( [("completion_time", ASCENDING), ("weight", DESCENDING), ("release_time", ASCENDING)]),
	IndexModel( [("specific_username", ASCENDING), ("completion_time", ASCENDING), ("weight", DESCENDING), ("release_time", ASCENDING)])
	]

mongo_db[TABLES["JOB_CONFIG"]].create_indexes(index_list)













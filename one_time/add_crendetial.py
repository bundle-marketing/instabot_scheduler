import os
import sys
import time
import json
import calendar
import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId

sys.path.append(os.path.join(sys.path[0], '../'))
from db_config.config import (MONGO_DB_URL, MONGO_DB_NAME, TABLES)

from collections import Counter 



### Setup database ####

mongo_client = MongoClient(MONGO_DB_URL)
mongo_db = mongo_client[MONGO_DB_NAME]



data = {}

data["ig_username"] = "melrosethriftco"
data["ig_password"] = "Rocco1224"
data["can_mine"] = False
data["proxy"] = "104.140.211.13:3128"

key = {}
key["ig_username"] = "melrosethriftco"



cred_coll = mongo_db[TABLES["IG_CRED"]]

cred_coll.update(key, data)
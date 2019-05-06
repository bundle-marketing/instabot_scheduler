import matplotlib.pyplot as plt
import numpy as np
import json


from pprint import pprint

with open('change_media.json') as f:
    data = json.load(f)

with open('to_track.json') as f2:
    username = json.load(f2)

    to_follow = [  d[1] for d in username  ]
    print(to_follow)



for username in to_follow[-1::-1]:

    # if not (username == "sensual_shots_"):
    #     continue

    entry = data[username]
    
    print(username, " : " , len(entry))

    time_taken = []
    follower_percent = []
    following_percent = []

    for val in entry:
        x, y, z = val
        time_taken.append(x)
        follower_percent.append(y)
        following_percent.append(z)

    plt.plot(time_taken, follower_percent)
    plt.show()
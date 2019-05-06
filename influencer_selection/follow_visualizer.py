import matplotlib.pyplot as plt
import numpy as np
import json


from pprint import pprint

with open('to_track.json') as f2:
    username = json.load(f2)

    to_follow = [  d[1] for d in username  ]
    print(to_follow)



def reduce_time(input_arr):

    to_detuct = min(input_arr)
    return [x - to_detuct for x in input_arr]

def create_change_follow_chart(username):

    data = {}

    with open('change_follower.json') as f:
        data = json.load(f)

    # for username in to_follow[-1::-1]:

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

    return [ (follower_percent, time_taken) ]

        # plt.plot(time_taken, follower_percent)
        # plt.show()



def create_new_follow_chart(username):

    data = {}

    with open('new_follower.json') as f:
        data = json.load(f)

    # for username in to_follow:#[-1::-1]:

    entry = data[username]

    follower_percent = []
    follower_percent_time = []


    following_percent = []
    following_percent_time = []

    for val in entry["follower"]:
        x, y = val

        follower_percent_time.append(x)
        follower_percent.append(y)

    # follower_percent_time = reduce_time(follower_percent_time)

    for val in entry["following"]:
        x, y = val

        following_percent_time.append(x)
        following_percent.append(y)

        # following_percent_time = reduce_time(following_percent_time)


        # plt.plot(follower_percent_time, follower_percent)
        # plt.show()

    return [  (follower_percent, follower_percent_time), (following_percent, following_percent_time)  ]


def create_new_media_chart(username):

    data = {}

    with open('change_media.json') as f:
        data = json.load(f)

    # for username in to_follow:#[-1::-1]:

    media_entry = data[username]

    for id_, entry in media_entry.items():

        time , data = [], []

        for val in entry["like_new"]:
            x, y = val

            time.append(x)
            data.append(y)

        plt.plot(time, data)
        # print(time, data)

    print(username)
    plt.show()

        # follower_percent_time = reduce_time(follower_percent_time)

        # for val in entry["comment"]:
        #     x, y = val

        #     following_percent_time.append(x)
        #     following_percent.append(y)

        # following_percent_time = reduce_time(following_percent_time)


        # plt.plot(follower_percent_time, follower_percent)
        # plt.show()

    # return [  (follower_percent, follower_percent_time), (following_percent, following_percent_time)  ]


def main():

    chosen = ["alechipolechi", "rodrigocacampos", "tiphaine.marfil"]

    for username in to_follow:

        if username not in chosen:
            continue

        to_ret_data = []

        # to_ret_data.extend(create_change_follow_chart(username))
        # to_ret_data.extend(create_new_follow_chart(username))

        # # print(to_ret_data)

        # for data,time in to_ret_data:
        #     # plt.plot(time, data)
        #     plt.plot(time, data)

        # plt.legend(['follower change', 'new follower', 'new following'], loc='upper left')





        create_new_media_chart(username)
        # to_ret_data.extend(create_new_follow_chart(username))

        # print(to_ret_data)

        # for data,time in to_ret_data:
        #     # plt.plot(time, data)
        #     plt.plot(time, data)

        # plt.legend(['follower change', 'new follower', 'new following'], loc='upper left')

        # plt.show()



        

if __name__ == '__main__':
    main()




# plt.show()
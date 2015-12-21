import tweepy
import os, os.path
import sys
import time
#text = open('text.txt', 'w')
#fri = open('friend.txt', 'w')
#new_file = open('followings.txt', 'a')
#Use your own key here for authorization
access_token =
access_token_secret =
consumer_key =
consumer_secret =

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

userfile = open("DIR",'r')
user_list = []
i = 1
success = 0
for line in userfile.readlines():
    line = line.strip('\n')
    line = line.split('/')[0]
    user_list.append(line)
for k in range(i, len(user_list)):
    screenname=str(user_list[i-1])
    print screenname
    followings = api.friends_ids(screenname)
    new_new_file = open('%d.txt'%(int(i)), 'a')
    new_new_file.write(str(followings)+'\n')
    i = i+1
    time.sleep(0.1)
    success = success +1
    print success

    if success == 11:
        time.sleep(15*60)
        success = 0
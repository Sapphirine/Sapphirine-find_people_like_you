import tweepy
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

linked = open('new_linked.txt', 'r')
fri = open('new_linked_user.txt', 'w')

#Use your own key here for authorization
access_token =
access_token_secret =
consumer_key =
consumer_secret =

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth,parser=tweepy.parsers.JSONParser())

pattern_usr=re.compile(r'\s+u+\'+id+\'+\:+\s')


linked_list = []
linked_list = linked.readline()
success = 0
while linked_list:
    user = api.search_users(linked_list)
    NOTFIND = True
    for user_ in user:
        if str(user_['name']).find(linked_list) and NOTFIND:
            fri.write(str(user_['id']) + '/' + linked_list)
            NOTFIND = False
            success= success+1
            
            print success
        else:
            print('wrong person')

        if success == 150:
           time.sleep(15*60)
           success = 0

    linked_list = linked.readline()
    time.sleep(0.1)
            

            
#print user.followers_count
#for frilinked_userend in user.friends():
#    fri.write(friend.screen_name + '\n')
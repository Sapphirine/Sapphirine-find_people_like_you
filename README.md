README

Asume Tweepy, nltk, Spark and SystemGlite environmets are properly set in your computer
Insert your own Twitter Secrect Keys

The coding for this project contains the following steps:
(1)     Get people's basic public linkedin information using /linkedin/3.py

(2)     Use people's name to do search these people in Twitter and return Twitter user_id using /twitter_search/find.py

(3)     (a)Use Twitter user_id to find users' most recent 100 tweets, text mining preprocesing is also included in /restapi/get_tweets.py

	(b)Use Twitter user_id to find users' followings using /restapi/get_followings.py

(4)     Clustering based on tweets using /restapi/use_tweets/tf.py under spark environment
	group.py can remove each person to the corresbonding cluster

(5)     Clustering based on tweets using /restapi/use_followings/mutal_friend_score.py under spark environment
	group.py can remove each person to the corresbonding cluster

(6)     On the Ubuntu terminal
        $sudo service apache2 start
        $cd /DIR/gshell 
        $./sysGSuperMgr 6688 10
    Then open the browers and upload the node and edge to generate graphs

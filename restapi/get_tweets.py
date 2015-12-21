import tweepy
import re
import nltk
from nltk.corpus import brown
import time
import sys




#Do preprocessing and save the new file to saveFile_result	
def preprocessing(list, number):
	text = []
	hashtaglines = open('hashtaglines_%d.txt'%(number),'w')
	for item in list:
	#delete with http
		pattern_http=re.compile(r'http[^\s]+\s|http[^\s]+\n')
		if pattern_http.findall(str(item))!=[]:
		#delete http and replace data
			item=pattern_http.sub(r'',item)
	#delete friend names
		pattern_friends=re.compile(r'RT @[^\s]+\s|RT @[^\s]+\n|RT @[^\s]+\:|@[^\s]+\S|@[^\s]+\s|@[^\s]+\n')
		if pattern_friends.findall(str(item))!=[]:
			item=pattern_friends.sub(r'',item)	
	#deal with hashtag '#'
		pattern = re.compile(r'#[^\s]+ |#[^\s]+\n')
		if pattern.findall(str(item))!=[]:
			hashtaglines.write(str(item))
			hashtaglines.write('\n')
	#no hashtag found
		item=pattern.sub(r'',item)	
		if pattern.findall(str(item))==[]:
			text.append(str(item))  
			continue 
	#delete hashtag in the newfile and save it in hashtag file


	#save the result 
	text.append(str(item))
	return text


# coding=UTF-8


# This is a fast and simple noun phrase extractor (based on NLTK)
# Feel free to use it, just keep a link back to this post
# http://thetokenizer.com/2013/05/09/efficient-way-to-extract-the-main-topics-of-a-sentence/
# Create by Shlomi Babluki
# May, 2013


# This is our fast Part of Speech tagger
#############################################################################
brown_train = brown.tagged_sents(categories='news')
regexp_tagger = nltk.RegexpTagger(
	[(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
	 (r'(-|:|;)$', ':'),
	 (r'\'*$', 'MD'),
	 (r'(The|the|A|a|An|an)$', 'AT'),
	 (r'.*able$', 'JJ'),
	 (r'^[A-Z].*$', 'NNP'),
	 (r'.*ness$', 'NN'),
	 (r'.*ly$', 'RB'),
	 (r'.*s$', 'NNS'),
	 (r'.*ing$', 'VBG'),
	 (r'.*ed$', 'VBD'),
	 (r'.*', 'NN')
])
unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)
#############################################################################


# This is our semi-CFG; Extend it according to your own needs
#############################################################################
cfg = {}
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NNI"
cfg["NNI+NN"] = "NNI"
cfg["JJ+JJ"] = "JJ"
cfg["JJ+NN"] = "NNI"
#############################################################################


class NPExtractor(object):

	def __init__(self, sentence):
		self.sentence = sentence

	# Split the sentence into singlw words/tokens
	def tokenize_sentence(self, sentence):
		tokens = nltk.word_tokenize(sentence)
		return tokens

	# Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")
	def normalize_tags(self, tagged):
		n_tagged = []
		for t in tagged:
			if t[1] == "NP-TL" or t[1] == "NP":
				n_tagged.append((t[0], "NNP"))
				continue
			if t[1].endswith("-TL"):
				n_tagged.append((t[0], t[1][:-3]))
				continue
			if t[1].endswith("S"):
				n_tagged.append((t[0], t[1][:-1]))
				continue
			n_tagged.append((t[0], t[1]))
		return n_tagged

	# Extract the main topics from the sentence
	def extract(self):

		tokens = self.tokenize_sentence(self.sentence)
		tags = self.normalize_tags(bigram_tagger.tag(tokens))

		merge = True
		while merge:
			merge = False
			for x in range(0, len(tags) - 1):
				t1 = tags[x]
				t2 = tags[x + 1]
				key = "%s+%s" % (t1[1], t2[1])
				value = cfg.get(key, '')
				if value:
					merge = True
					tags.pop(x)
					tags.pop(x)
					match = "%s %s" % (t1[0], t2[0])
					pos = value
					tags.insert(x, (match, pos))
					break

		matches = []
		for t in tags:
			if t[1] == "NNP" or t[1] == "NNI":
			#if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN":
				matches.append(t[0])
		return matches



def main():
	userfile = open('new.txt','r')
	user_list = []
	i = 175
	success = 0

#Use your own key here for authorization
	access_token =
	access_token_secret =
	consumer_key =
	consumer_secret = 

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)
	

	for line in userfile.readlines():
		line = line.strip('\n')
		line = line.split('/')[0]
		user_list.append(line)

	for a in range(i,len(user_list)-1):
		screenname = str(user_list[i-1])
		print screenname
		new_file = open('%d.txt'%(i), 'a')
		original_text = []
		preprocessed = []
		count = 0
		for tweet in tweepy.Cursor(api.user_timeline,id=screenname).items():
			if count < 90:
				original_text.append(tweet.text.encode("ascii", "ignore"))
				count = count + 1
			else:
				break
		preprocessed = preprocessing(original_text, i)	
		for line in preprocessed:
			np_extractor = NPExtractor(line)
			result = np_extractor.extract()
	#       print "This sentence is about: %s" % ", ".join(result)
			result = map(str.lower, result)
			new_file.write(str(result) + '\n')
		i = i +1
		success = success+1
		if success == 35:
			time.sleep(15*60)
			success=0






if __name__ == '__main__':
	main()

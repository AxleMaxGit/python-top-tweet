#CLS
import os
os.system('clear')

import datetime

#Twitter API ackage
import tweepy

#Auth to Twitter
auth = tweepy.OAuthHandler('fCT6csJua6NcI7GZoWpTyeIoK', 'QmNviZzpTZMYBS4JZcVtyckddSaeUpjhG0HUyvIwKgaHupTnis')
auth.set_access_token('2474914111-eRhcmxIfi2o5SWCJjc5LVE2Tl0FnhHFD0KktIIC', 'ZvcPcWsHPa5H03CIzZ6UJq9r1d1sFjIV7coOZG4Q0WCVv')

#connect to API
#currently in a try/catch block to avoid blowing out the API rate limit
try:
	api
	print("Twitter API connection already set.")
except NameError:
	api = tweepy.API(auth)
	print("Setting Twitter API connection.")

#FUNCTIONS
def get_tweets(search_term, num_results):
	#This pulls down 450 tweets. Not sure why it is 450
	print "Get tweet start: ", datetime.datetime.now()
	tweet_set = tweepy.Cursor(api.search,
				                   q=search_term,
				                   rpp=100,
				                   result_type="recent",
				                   include_entities=True,
				                   #the final bracket limits no. of loops
				                   lang="en").items(num_results)
	print "Get tweet end ", datetime.datetime.now()
	return tweet_set

def count_top_rt(tweet_set):
	print "Count RT start ", datetime.datetime.now()
	for tweet in tweet_set:
		#test if this is a retweet
		if hasattr(tweet, 'retweeted_status'):
			#if already in top rt list, increment count
			if tweet.retweeted_status.id_str in top_retweets:
				top_retweets[tweet.retweeted_status.id_str] += 1
			else:
				#if not in top rt list, add it
				top_retweets[tweet.retweeted_status.id_str] = 1
		else:
			pass
	print "Count RT end ", datetime.datetime.now()

def count_top_htag(tweet_set):
	for tweet in tweet_set:
		#parse the hashtags in the tweet
	    hstgl = tweet.entities.get('hashtags')
	    for tags in hstgl:
	    	this_tag = str(tags['text'])
	    	#If the tag exists then increment the count
	    	if this_tag in top_tags:
	    		top_tags[this_tag] += 1
	    	#if the tag doesn't exist initiate it	
	    	else:
	    		top_tags[this_tag] = 1

def show_top_rt(top_retweets):
	print 
	print "Most Retweeted"
	rt_count = -1
	sort_most_rt = sorted(top_retweets.iteritems(), key=lambda (k,v): (v,k))
	for key, value in sort_most_rt:
		rt_count += 1
		#minimum number of retweets before displaying
		if value > 3:
			print "(Tweet #" + str(rt_count) + ")" + "%s: %s" % (key, value)
			tweet = api.get_status(key)
			print(tweet.text)
			print("Tweeted by " + tweet.user.screen_name) + "\n"

def show_top_htag(tweet_set):
	#Not written yet - Display the top hashtags
	print "Top Hashtags"
	# #show the top_tags dict   
	# for key, value in sorted(top_tags.iteritems(), key=lambda (k,v): (v,k)):
	#    print "%s: %s" % (key, value)

#ACTION ITEMS

# 1: Search 
# 2: Edit saved terms
# 3: Open linked page
# 4: Retweet (auto follow poster) (queue all retweeters for follow)  (auto favourite tweet. Queue tweet for unfave)

def show_search_options():
	print("\nSELECT AN OPTION\n")
	
	print("Enter search term number to search")
	#print("Enter [a] to search all search terms as a group")
	print("Enter [e] to edit saved search terms")

def show_edit_options():
	print("\nSELECT AN OPTION\n")
	# 1: Run Twitter search using term
	# 2: Add a new saved tern for reuse
	print("[1] Add a new search term")
	print("[2] Remove a search term from the list")
	# 4: Set RT threshold
	print("[3] Back to search mode")
	print("")

def search_prompt(fname):
	disp_list(fname)
	show_search_options()
	search_item1 = raw_input("\n: ")
	#allow user to select search term from saved list
	try:
		#If it's an int
		int(search_item1)
		#P&& is in range
		list1 = mk_list(fname)
		if 0 <= int(search_item1) <= len(list1):
			#return the search term for processing
			search_tally(list1[int(search_item1)-1])
		else:
			print('number out of range')
			search_prompt(fname)
	except ValueError:
		#allow user to edit saved list
		if search_item1 == "e":
			print("Edit mode")
			edit_prompt(fname)
		#allow user to type  search term
		else:
			search_prompt(fname)
			#return <the search term>

def edit_prompt(fname):
	disp_list(fname)
	show_edit_options()
	prompt1 = raw_input(": ")
	try:
		int(prompt1)
		#Add new term to list
		if int(prompt1) == 1:
			#addf
			new_term = raw_input("Enter your new search term: ")
			try:
				addf(fname, [new_term])
				print(new_term + " added to list")
			except ValueError:
				print("Value Error")
		#Remove term from list
		elif int(prompt1) == 2:
			#remf
			del_item = raw_input("Select number for the term you want removed: ")
			#get the list
			list1 = mk_list(fname)
			#make sure user selects valid number to remove
			if 0 <= int(del_item) <= len(list1):
				#delete the entry by index
				del list1[int(del_item)-1]
				#cler the file
				clrf(fname)
				#write the new list back to file
				addf(fname, list1)
		elif int(prompt1) == 3:
			#remf
			search_prompt(fname)
		else:
			print("# out of range")
	except ValueError:
		print("Not int")
	edit_prompt(fname)

def show_tweet_options():
	print("\nSELECT AN OPTION\n")

	print("Select tweet number to RT")
	print("[n] Next search")
	# 4: Set RT threshold
	print("")


def tweet_prompt():
	sort_most_rt = sorted(top_retweets.iteritems(), key=lambda (k,v): (v,k))
	show_tweet_options()
	rt = raw_input(": ")
	#test if the input is an integer
	try:
		int(rt)
		#RT the selected tweet
		if 0 <= int(rt) <= len(sort_most_rt):
			#<NEED CODE HERE FOR RT> RT the selected tweet
			api.retweet(sort_most_rt[int(rt)][0])
			print("RT posted by <insert @account-name>")
			#print(sort_most_rt[int(rt)])
			tweet_prompt()
		else:
			#make sure the tweet is in range 
			print("out of numeric range")
			tweet_prompt()
	except ValueError:
		#allow user to terminate
		if rt == 'n':
			os.system('clear')
			search_prompt(fname)
		#prompt user to select number of tweet to RT
		else:
			print("Please select a number")
			tweet_prompt()
	
# def usr_post_rt():
# 	rt = raw_input("RT # ?? ")
# 	#test if the input is an integer
# 	try:
# 		int(rt)
# 	except ValueError:
# 		#allow user to terminate
# 		if rt == 'x':
# 			os.system('clear')
# 			pass
# 		#prompt user to select number of tweet to RT
# 		else:
# 			print("Please select a number")
# 			usr_post_rt()
# 	else:
# 		#RT the selected tweet
# 		if 0 <= int(rt) <= len(sort_most_rt):
# 			#<NEED CODE HERE FOR RT> RT the selected tweet
# 			api.retweet(sort_most_rt[int(rt)][0])
# 			#print(sort_most_rt[int(rt)])
# 			usr_post_rt()
# 		else:
# 			#make sure the tweet is in range 
# 			print("out of numeric range")
# 			usr_post_rt()

def search_tally(search_item1):
	#print(search_item1)
	print("Searching Twitter for \"" + search_item1 + "\"\n")
	#get X tweets for the search term. Using 0 for X = max results
	tweet_set = get_tweets(search_item1, 0)
	#Count the top retweets
	count_top_rt(tweet_set)
	#Count the top hashtags 
		#count_top_htag(tweet_set)
	#DISPLAY RESULTS
	show_top_rt(top_retweets)
	#allow the user to post selected retweets
	tweet_prompt()


#MAIN
#dictionary to store popular tweets
top_retweets = {}
#dictionary to store popular tags
top_tags = {}
#list to temp store hashtags
hstgl = []

print "Time now is", datetime.datetime.now()

from easy_file import *

fname = "workfile.txt"

search_prompt(fname)

	
# def count_top_rt(tet):
# 	for tweet in tweet_set:
# 		print(tweet)

# tweet_set = ["Sydney", "London", "Paris"]
# count_top_rt(tweet_set)

# Method to list key and value of list
# for k,v in enumerate(tweet_set):  
# 	print(str(k+1) + ": " + v)


# webbrowser.open("http://www.google.com.au")














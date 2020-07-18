import tweepy
import requests
import json
import locale
import time
from keys import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)#Authenticating the keys
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def create_tweet():
	locale.setlocale(locale.LC_ALL,'en_IN.utf8')  #For getting comma's in huge numbers in Indian format
	response = requests.get('https://api.covid19india.org/data.json')#Getting the data from api
	data = response.json()
	
	actual_data=data["statewise"][0] 
	
	dltconf = int(actual_data["deltaconfirmed"])
	dltrecv = int(actual_data["deltarecovered"])
	dltdecs = int(actual_data["deltadeaths"])
	time = actual_data["lastupdatedtime"]
	ttlconf = int(actual_data["confirmed"])
	ttlrecv = int(actual_data["recovered"])
	ttlactv = int(actual_data["active"])
	ttldecs = int(actual_data["deaths"])
	
	tweet = f"""	Covid19 Updates(INDIA)
	
Last updated on : {time}

Today's Report:
New Cases : {locale.format_string("%d",dltconf,grouping=True)}
New Recoveries: {locale.format_string("%d",dltrecv,grouping=True)}
New Deaths: {locale.format_string("%d",dltdecs,grouping=True)}

Overall:	
Total : {locale.format_string("%d",ttlconf,grouping=True)}
Recovered : {locale.format_string("%d",ttlrecv,grouping=True)}
Active : {locale.format_string("%d",ttlactv,grouping=True)}
Deaths : {locale.format_string("%d",ttldecs,grouping=True)}

#covid19 #coronavirus #India #Updates	   
	
"""
	return tweet


	


def tweeting():
	
	try:
		api.verify_credentials()
		print('Authentication Successful')
	except:
		print('Error while authenticating API')
		sys.exit(1)
	tweet = create_tweet()
	try:
		api.update_status(tweet)
		print("Tweet Successful")
	except tweepy.TweepError as error:
		if error.api_code == 187:
			print("Duplicate message")  	#Duplicate tweets wil not be tweeted
		else:
			raise error			
     	
while True:
	tweeting() 	
	time.sleep(16800)   # Giving delay of around 4.5hrs
	       






	

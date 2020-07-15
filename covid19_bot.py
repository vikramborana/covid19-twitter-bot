import tweepy
import requests
import json
import locale
import time



def create_tweet():
	locale.setlocale(locale.LC_ALL,'en_IN.utf8')  #For getting comma's in huge numbers in Indian format
	response = requests.get('https://api.covid19india.org/data.json')#Getting the data from api
	data = response.json()
	
	actual_data=data["statewise"][0] 
	
	deltaconfirmed = int(actual_data["deltaconfirmed"])
	deltarecovered = int(actual_data["deltarecovered"])
	deltadeaths = int(actual_data["deltadeaths"])
	time = actual_data["lastupdatedtime"]
	totconfirmed = int(actual_data["confirmed"])
	totrecovered = int(actual_data["recovered"])
	totdeaths = int(actual_data["deaths"])
	
	tweet = f"""	Covid19 Updates(INDIA)          
	
Last updated on : {time}

Todays Report:
New Cases : {locale.format_string("%d",deltaconfirmed,grouping=True)}
New Recovery: {locale.format_string("%d",deltarecovered,grouping=True)}
New Deaths: {locale.format_string("%d",deltadeaths,grouping=True)}

Overall:	
Total : {locale.format_string("%d",totconfirmed,grouping=True)}
Recovered : {locale.format_string("%d",totrecovered,grouping=True)}
Deaths : {locale.format_string("%d",totdeaths,grouping=True)}	   
	
"""
	return tweet


	


def tweeting():
	CONSUMER_KEY =''   #Add ur own keys
	CONSUMER_SECRET =''
	ACCESS_KEY = ''
	ACCESS_SECRET = ''


	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)#Authenticating the keys
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)
	
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
	       






	

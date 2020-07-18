import tweepy
import requests
import json
import locale
from keys import *
from tweepy import Stream
from tweepy.streaming import StreamListener

class StdOutListener(StreamListener): #Predifined class from module tweepy to stream tweets
	def on_data(self,data):#predefined Class
		clean_data = json.loads(data)           #Getting tweet raw data in json . So cleaning it.
		user_mentions = clean_data["entities"]["user_mentions"][0]["screen_name"]            
		tweet_id = clean_data["id"]                     #Getting required data from tweet like text ,tweet id etc.
		tweet_text = clean_data["text"]
		tweeted_by = clean_data["user"]["screen_name"]
		
		if(user_mentions == ACCOUNT_NAME):          #run only if someone mentions the bot in the tweet
			place,sym = decodeTweet(tweet_text)
			if(place != "Nothing" and sym == "#"):      
				print("Found District....Tweeting")
				tweet=createTweetDistrict(place)
				replyToTweet(tweet,tweet_id)
				print("Successfully Tweeted")
			elif(place!= "Nothing" and sym == "$"):
				print("Found State ... Tweeting")
				tweet = createTweetState(place)
				replyToTweet(tweet,tweet_id)
				print("Successfully Tweeted")	


		
		
	def on_error(self, status_code): #Again predefined class 
		if status_code == 420:
			#returning False in on_error disconnects the stream
			return False	

def setAuth():                      #Authorizing the keys
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)
	return api,auth

def followStream():                 #Setting up Stream 
	listener = StdOutListener()
	stream = Stream(auth,listener)
	stream.filter(track=[ACCOUNT_NAME])

def replyToTweet(tweet,tweet_id):   #This function Tweets the tweet
	api.update_status(tweet,in_reply_to_status_id =tweet_id,auto_populate_reply_metadata =True)

def decodeTweet(text):          #finding if its state or district data to be found
	if("#" in text):                # Districts -"#"
		district = text.split("#",1)[1]
		sym = "#"
		return district,sym
	if("$" in text):                # State and UT - "$"
		state = text.split("$",1)[1]
		sym = "$"
		return state,sym		
	return "Nothing"

def createTweetDistrict(district):      #getting particular district data
	state = dist_dict[district]
	dltconf = int(cdata[state]['districtData'][district]['delta']['confirmed'])
	dltrecv = int(cdata[state]['districtData'][district]['delta']['recovered'])
	dltdecs = int(cdata[state]['districtData'][district]['delta']['deceased'])
	ttlconf = int(cdata[state]['districtData'][district]['confirmed'])
	ttlactv = int(cdata[state]['districtData'][district]['active'])
	ttlrecv = int(cdata[state]['districtData'][district]['recovered'])
	ttldecs = int(cdata[state]['districtData'][district]['deceased'])

	tweet = createTweet(district,dltconf,dltrecv,dltdecs,ttlconf,ttlactv,ttlrecv,ttldecs)
	return tweet

def createTweetState(state):        #Getting particular state data
	state_no = state_dict[state]
	dltconf = int(scdata["statewise"][state_no]["deltaconfirmed"])
	dltrecv = int(scdata["statewise"][state_no]["deltarecovered"])
	dltdecs = int(scdata["statewise"][state_no]["deltadeaths"])
	ttlconf = int(scdata["statewise"][state_no]["confirmed"])
	ttlactv = int(scdata["statewise"][state_no]["active"])
	ttlrecv = int(scdata["statewise"][state_no]["recovered"])
	ttldecs = int(scdata["statewise"][state_no]["deaths"])

	tweet =createTweet(state,dltconf,dltrecv,dltdecs,ttlconf,ttlactv,ttlrecv,ttldecs)
	return tweet

def createTweet(place,dltconf,dltrecv,dltdecs,ttlconf,ttlactv,ttlrecv,ttldecs):# Tweet Format

	tweet = f"""	
	{place}'s Updates

Overall:	
Total : {locale.format_string("%d",ttlconf,grouping=True)}
Recovered : {locale.format_string("%d",ttlrecv,grouping=True)}
Active : {locale.format_string("%d",ttlactv,grouping=True)}
Deaths : {locale.format_string("%d",ttldecs,grouping=True)}

Today's Report:
New Cases : {locale.format_string("%d",dltconf,grouping=True)}
New Recoveries: {locale.format_string("%d",dltrecv,grouping=True)}
New Deaths: {locale.format_string("%d",dltdecs,grouping=True)}

"""
	return(tweet) 



def distToStateDict():                  #Function for creating District to state dictionary
	d ={}
	for key , value in cdata.items():
		l = list(value['districtData'])
		for x in l:
			d[x] = key
			if(x == 'Unknown'):
				del d['Unknown']
			if(x == 'Unassigned'):
				del d['Unassigned']
			if(x == 'Foreign Evacuees'):
				del d['Foreign Evacuees']
			if(x == 'Italians'):
				del d['Italians']
			if(x == 'Airport Quarantine'):
				del d['Airport Quarantine']

	return d		 

def stateDict():                #Function to create State numbering dictionary 
	sdata = scdata['statewise']
	sdict={}

	for i in range(len(sdata)):
	 	sdict[sdata[i]['state']] = i
	return sdict	 



if __name__ == "__main__":
	api,auth = setAuth()        #Setting up authorization
	locale.setlocale(locale.LC_ALL,'en_IN.utf8')    #Used for Indian format digits
	response = requests.get('https://api.covid19india.org/state_district_wise.json')#api for district wise data
	cdata = response.json()
	dist_dict = distToStateDict()  #Dictionary that contains keys as district and value as its state
	response1 = requests.get('https://api.covid19india.org/data.json')#api for getting state data
	scdata = response1.json()
	state_dict = stateDict() #dictionary that contains key as states and value as number corresponding to it according to the api
	followStream()          #Starting the Stream	 

    #Made by Vikram #Made in India 😜
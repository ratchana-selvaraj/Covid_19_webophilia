import GetOldTweets3 as got3
from flask import *
from flask import request
import langid
app=Flask(__name__)
from translation import google,bing,ConnectError
class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 
@app.route('/',methods=['POST','GET'])
def tweet_scrap():
	username="Vijayabaskarofl"
	count=30
	tweetCriteria=got3.manager.TweetCriteria().setUsername(username).setMaxTweets(count)
	dict_obj=my_dictionary()
	for i in range(count):
		tweets=got3.manager.TweetManager.getTweets(tweetCriteria)[i]
		result=langid.classify(tweets.text)
		if(result[0]=='en'):
			dict_obj.add(str(tweets.date),tweets.text)
	return render_template("tweets.html",dict_obj=dict_obj)
if __name__=='__main__':
	app.run()


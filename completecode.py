#final code
#imports
from flask import *
from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
import MySQLdb
import pandas as pd
import sys
import GetOldTweets3 as got3
import langid
from translation import google,bing,ConnectError
from googletrans import Translator
import nltk
from nltk.stem import WordNetLemmatizer
import numpy
from tensorflow.python.framework import ops
import tensorflow
import random
import json
import tflearn
app=Flask(__name__)
db=MySQLdb.connect("localhost","root","Goodluck","pm")
#-------CHATBOT SECTION-------#
#class to create dictionary that stores the dates and tweets
class my_dictionary(dict): 
    # __init__ function 
    def __init__(self): 
        self = dict()       
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 
lemmatizer = WordNetLemmatizer()
ignore_words=['?','.','!']
with open('intents.json') as file:
    data = json.load(file)
words = []
labels = []
docs_x = []
docs_y = []
for intent in data['intents']:
	for pattern in intent['patterns']:
		wrds = nltk.word_tokenize(pattern)
		words.extend(wrds)
		docs_x.append(wrds)
		docs_y.append(intent["tag"])
		if intent['tag'] not in labels:
			labels.append(intent['tag'])
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
labels = sorted(labels)
training = []
output = []
out_empty = [0 for _ in range(len(labels))]
for x, doc in enumerate(docs_x):
	bag = []
	wrds = [lemmatizer.lemmatize(w.lower()) for w in doc]
	for w in words:
		if w in wrds:
			bag.append(1)
		else:
			bag.append(0)
	output_row = out_empty[:]
	output_row[labels.index(docs_y[x])] = 1
	training.append(bag)
	output.append(output_row)
training = numpy.array(training)
output = numpy.array(output)
try:
    model.load("model.tflearn")
except:
	ops.reset_default_graph()
	net = tflearn.input_data(shape=[None, len(training[0])])
	net = tflearn.fully_connected(net, 8)
	net = tflearn.fully_connected(net, 8)
	net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
	net = tflearn.regression(net)
	model = tflearn.DNN(net)
	model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
	model.save("model.tflearn")
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [lemmatizer.lemmatize(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)
@app.route('/get')
def get_bot_response():
	while True:
		inp = request.args.get('msg')    
		results = model.predict([bag_of_words(inp, words)])
		results_index = numpy.argmax(results)
		tag = labels[results_index]
		for tg in data["intents"]:
			if tg['tag'] == tag:
				responses = tg['responses']
		if(random.choice(responses)=="See you later, thanks for visiting" or random.choice(responses)== "Have a nice day" or random.choice(responses)=="Bye! Come back again soon." or random.choice(responses)=="Its was nice to talk"):
			return(str(random.choice(responses))) 
			quit()
		else:
			return(str(random.choice(responses)))
#-------TWEETS SCRAPING SECTION-------#			
translator = Translator()
@app.route('/',methods=['POST','GET'])
def tweet_scrap():
	username1="Vijayabaskarofl"
	count=20
	username2="SuVe4Madurai"
	username3="narendramodi"
	tweetCriteria1=got3.manager.TweetCriteria().setUsername(username1).setMaxTweets(count)
	tweetCriteria2=got3.manager.TweetCriteria().setUsername(username2).setMaxTweets(count)
	tweetCriteria3=got3.manager.TweetCriteria().setUsername(username3).setMaxTweets(count)
	dict_obj_eng1=my_dictionary()
	dict_obj_tam1=my_dictionary()
	dict_obj_eng2=my_dictionary()
	dict_obj_tam2=my_dictionary()
	dict_obj_eng3=my_dictionary()
	dict_obj_tam3=my_dictionary()
	for i in range(count):
		tweets1=got3.manager.TweetManager.getTweets(tweetCriteria1)[i]
		result1=langid.classify(tweets1.text)
		try:		
			if(result1[0]=='en'):
				dict_obj_eng1.add(str(tweets1.date),tweets1.text)
				translated = translator.translate(tweets1.text,src='en',dest='ta')
				dict_obj_tam1.add(str(tweets1.date),translated.text)
			elif(result1[0]=='ta'):
				dict_obj_tam1.add(str(tweets1.date),tweets1.text)
				translated = translator.translate(tweets1.text,src='ta',dest='en')
				dict_obj_eng1.add(str(tweets1.date),translated.text)
		except:
			continue
	for i in range(count):
		tweets2=got3.manager.TweetManager.getTweets(tweetCriteria2)[i]
		result2=langid.classify(tweets2.text)
		try:
			if(result2[0]=='en'):
				dict_obj_eng2.add(str(tweets2.date),tweets2.text)
				translated = translator.translate(tweets2.text,src='en', dest='ta')
				dict_obj_tam2.add(str(tweets2.date),translated.text)
			elif(result2[0]=='ta'):
				dict_obj_tam2.add(str(tweets2.date),tweets2.text)
				translated = translator.translate(tweets2.text,src='ta', dest='en')
				dict_obj_eng2.add(str(tweets2.date),translated.text)
		except:
			continue
	for i in range(count):
		tweets3=got3.manager.TweetManager.getTweets(tweetCriteria3)[i]
		result3=langid.classify(tweets3.text)
		try:
			if(result3[0]=='en'):
				dict_obj_eng3.add(str(tweets3.date),tweets3.text)
				translated = translator.translate(tweets2.text,src='en', dest='ta')
				dict_obj_tam3.add(str(tweets3.date),translated.text)
			elif(result3[0]=='hi'):
				translatedt= translator.translate(tweets3.text,src='hi', dest='ta')
				dict_obj_tam3.add(str(tweets3.date),translatedt.text)
				translated = translator.translate(tweets2.text,src='hi', dest='en')
				dict_obj_eng3.add(str(tweets3.date),translated.text)
		except:
			continue
	return render_template('tweets.html',dict_obj_eng1=dict_obj_eng1,dict_obj_eng2=dict_obj_eng2,dict_obj_eng3=dict_obj_eng3,dict_obj_tam1=dict_obj_tam1,dict_obj_tam2=dict_obj_tam2,dict_obj_tam3=dict_obj_tam3)
#-------DONATION FORM SECTION-------#
@app.route("/index")
def index():
	return render_template("form.html")
	return render_template("contact.html")
@app.route("/donate",methods=["GET","POST"])
def donate():
    if request.method=="POST":
        pd=request.form
        Amount=pd['amt']
        payment=pd['pay']
        fname=pd['fname']
        lname=pd['lname']
        Mail=pd['email']
        phone=pd['phn']
        db=MySQLdb.connect("localhost","root","Goodluck","pm")
        cur=db.cursor()
        cur.execute("INSERT INTO Donation1(Firstname,Lastname,Email,Phone,Amount,Method) VALUES(%s,%s,%s,%s,%s,%s)",(fname,lname,Mail,phone,Amount,payment))
        cur1=db.cursor()
        cur.execute("INSERT INTO Donate(Firstname,Lastname,Email,Phone,Amount,Method) VALUES(%s,%s,%s,%s,%s,%s)",(fname,lname,Mail,phone,Amount,payment))
        db.commit()
        cur.close()
        return render_template("checkout.html")
        return redirect(url_for('checkout', phone=phone))
@app.route("/checkout/<phone>")
def checkout(phone):
    db=MySQLdb.connect("localhost","root","Goodluck","pm")
    cur=db.cursor()
    query="select * from Donate where Phone="+phone
    cur.execute(query)
    m=cur.fetchone()
    cur.close()
    return render_template("checkout.html" ,m=m)
@app.route("/Thankyou",methods=["GET","POST"])
def thankyou():
    return render_template("Thankyou.html")
#-------LIVE TRACKER SECTION-------#
def Corona_State():
	coronadf=pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
	coronadf.head()
	corona_count=coronadf.groupby('State').sum()[['Delta_Confirmed','Delta_Deaths','Delta_Recovered']]
	corona_count.head()
	return corona_count
def corona_dist():
	corona2=pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv')
	corona2.head()
	mdu=corona2[corona2['District'].str.contains('Madurai')]
	mdu_c=mdu.groupby('District').sum()[['Confirmed','Recovered','Active']]
	mdu_c.head()
	return mdu_c
def graph_1():
    df=pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')
    df
    cdf=df[df['Country/Region'].str.contains('India')]
    cols=['Date','Confirmed']
    cdf1=cdf[cols]
    cdf1
    fig=pg.bar(cdf1,x='Date',y='Confirmed',title = 'Corona confirmation all across India : Time series')
    return fig
fig=graph_1()
mdu_c=corona_dist()
pair1=[(District,Confirmed,Recovered,Active) for District,Confirmed,Recovered,Active in zip(mdu_c.index,mdu_c['Confirmed'],mdu_c['Recovered'],mdu_c['Active'])]
corona_count = Corona_State()
pair2=[(State,Delta_Confirmed,Delta_Deaths,Delta_Recovered) for State,Delta_Confirmed,Delta_Deaths,Delta_Recovered in zip(corona_count.index,corona_count['Delta_Confirmed'],corona_count['Delta_Deaths'],corona_count['Delta_Recovered'])]
@app.route('/')
def live_tracker():
	mdu_c=corona_dist()
	corona_count = Corona_State()
	fig=graph_1().to_html()
	return render_template('index.html',table = mdu_c,map=corona_count,pair1=pair1,pair2=pair2,fig=fig)
#News flash
#def flashnews():
#search button function
@app.route('/')
def home():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)

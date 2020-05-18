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
app=Flask(__name__)
db=MySQLdb.connect("localhost","root","Goodluck","pm")#connecting to db
#class to create dictionary that stores the dates and tweets
class my_dictionary(dict): 
    # __init__ function 
    def __init__(self): 
        self = dict()       
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 
@app.route('/tweet_scrap',methods=['POST','GET'])
#function to scrap tweets
def tweet_scrap():
	username="Vijayabaskarofl"
	count=30
	tweetCriteria=got3.manager.TweetCriteria().setUsername(username).setMaxTweets(count)#Specifying criteria of tweets to be extracted
	dict_obj=my_dictionary()
	for i in range(count):
		tweets=got3.manager.TweetManager.getTweets(tweetCriteria)[i]#Scrapping the tweets
		result=langid.classify(tweets.text)#Identifies the language of tweets
		if(result[0]=='en'):
			dict_obj.add(str(tweets.date),tweets.text)#adding only English tweets to dictionary with date as key
	return render_template("tweets.html",dict_obj=dict_obj)
@app.route("/index")
def index():
	return render_template("form.html")
@app.route("/donate",methods=["GET","POST"])
#Donation form processing
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
        query=select * from Donation where Phone=phone
        db.commit()
        cur.close()
        return render_template("checkout.html")
#live Covid-19 tracker state wise
def Corona_State():
	coronadf=pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
	coronadf.head()
	corona_count=coronadf.groupby('State').sum()[['Delta_Confirmed','Delta_Deaths','Delta_Recovered']]
	corona_count.head()
	return corona_count
#live Covid-19 tracker district wise
def corona_dist():
	corona2=pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv')
	corona2.head()
	mdu=corona2[corona2['District'].str.contains('Madurai')]#identifying Madurai's cases
	mdu_c=mdu.groupby('District').sum()[['Confirmed','Recovered','Active']]
	mdu_c.head()
	return mdu_c
mdu_c=corona_dist()
pair1=[(District,Confirmed,Recovered,Active) for District,Confirmed,Recovered,Active in zip(mdu_c.index,mdu_c['Confirmed'],mdu_c['Recovered'],mdu_c['Active'])]
corona_count = Corona_State()
pair2=[(State,Delta_Confirmed,Delta_Deaths,Delta_Recovered) for State,Delta_Confirmed,Delta_Deaths,Delta_Recovered in zip(corona_count.index,corona_count['Delta_Confirmed'],corona_count['Delta_Deaths'],corona_count['Delta_Recovered'])]

#Chatbot for mental support
#def chatbot():
#News flash
#def flashnews():
#Public advice
#def advice_display():
#Symptoms 
#def tell_symptoms():
#natural remedies
#def display_remedies():
#FAQ's
#def faq_Show():
@app.route('/')
def home():
	mdu_c=corona_dist()
	corona_count = Corona_State()
    return render_template('corona.html',table= mdu_c,)
if __name__ == '__main__':
    app.run(debug=True)

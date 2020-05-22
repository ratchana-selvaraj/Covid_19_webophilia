from flask import Flask, render_template
import pandas as pd
import plotly.express as pg
import folium
import urllib
import GetOldTweets3 as got3
import langid
from newsapi import NewsApiClient
app = Flask(__name__)
from translation import google,bing,ConnectError
from googletrans import Translator
class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 
translator = Translator()
@app.route('/')
def Index():
    newsapi = NewsApiClient(api_key="b0f75ce660c0466a9a98c2478f8abb62")
    topheadlines = newsapi.get_top_headlines(sources="the-times-of-india")
    articles = topheadlines['articles']
    desc = []
    news = []
    img = []
    for i in range(len(articles)):
        myarticles = articles[i]
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
    mylist = zip(news, desc, img)
    mdu_c=corona_dist()
    corona_count = Corona_State()
    fig=graph_1().to_html()
    html_map=m._repr_html_()
    return render_template('index.html', context = mylist,table = mdu_c,map=corona_count,pair1=pair1,pair2=pair2,fig=fig,cmap=html_map)
def Corona_State():
    coronadf=pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
    coronadf.head()
    corona_count=coronadf.groupby('State').sum()[['Delta_Confirmed','Delta_Deaths','Delta_Recovered']]
    corona_count.head()
    pair2=[(State,Delta_Confirmed,Delta_Deaths,Delta_Recovered) for State,Delta_Confirmed,Delta_Deaths,Delta_Recovered in zip(corona_count.index,corona_count['Delta_Confirmed'],corona_count['Delta_Deaths'],corona_count['Delta_Recovered'])]
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
df=pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')
df= df[(df.Date.isin(['2020-05-19']))]
m=folium.Map(location=[33.000000,65.000000],tiles='Stamen toner',zoom_start= 4 )
folium.Circle(location= [33.000000,65.000000],radius=10000, color='gold', fill=True,popup='{}Confirmed'.format(5)).add_to(m)
def circle_maker(x):
    folium.Circle(location= [x[0],x[1]],
                  radius=float(x[2]*10),
                  color='gold',
                  fill=True,
                  popup='{}\nConfirmed cases: {}'.format(x[3], x[2])).add_to(m)
df[['Lat','Long','Confirmed','Country/Region']].apply(lambda x: circle_maker(x),axis =1)
html_map=m._repr_html_()    
fig=graph_1()
mdu_c=corona_dist()
pair1=[(District,Confirmed,Recovered,Active) for District,Confirmed,Recovered,Active in zip(mdu_c.index,mdu_c['Confirmed'],mdu_c['Recovered'],mdu_c['Active'])]
corona_count = Corona_State()
pair2=[(State,Delta_Confirmed,Delta_Deaths,Delta_Recovered) for State,Delta_Confirmed,Delta_Deaths,Delta_Recovered in zip(corona_count.index,corona_count['Delta_Confirmed'],corona_count['Delta_Deaths'],corona_count['Delta_Recovered'])]

@app.route("/public")
def public():
    return render_template("font-awesome.html")
@app.route("/donation")
def donation():
	return render_template("basic_elements.html")
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
        cur.execute("INSERT INTO Donate(Firstname,Lastname,Email,Phone,Amount,Method) VALUES(%s,%s,%s,%s,%s,%s)",(fname,lname,Mail,phone,Amount,payment))
        db.commit()
        cur.close()
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
    return render_template("volenteer.html")
@app.route("/volenteer",methods=["GET","POST"])
def volenteer():
    return render_template("volenteer.html")
@app.route("/helpdesk")
def helpdesk():
    return render_template("helpdesk.html")
@app.route('/tweets',methods=['POST','GET'])
def tweet_scrap():
	username1="Vijayabaskarofl"
	count=30
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
	return render_template('tweet.html',dict_obj_eng1=dict_obj_eng1,dict_obj_eng2=dict_obj_eng2,dict_obj_eng3=dict_obj_eng3,dict_obj_tam1=dict_obj_tam1,dict_obj_tam2=dict_obj_tam2,dict_obj_tam3=dict_obj_tam3)



if __name__ == "__main__":
    app.run(debug=True)
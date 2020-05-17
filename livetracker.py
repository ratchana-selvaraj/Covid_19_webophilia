import pandas as pd
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
mdu_c=corona_dist()
pair1=[(District,Confirmed,Recovered,Active) for District,Confirmed,Recovered,Active in zip(mdu_c.index,mdu_c['Confirmed'],mdu_c['Recovered'],mdu_c['Active'])]
corona_count = Corona_State()
pair2=[(State,Delta_Confirmed,Delta_Deaths,Delta_Recovered) for State,Delta_Confirmed,Delta_Deaths,Delta_Recovered in zip(corona_count.index,corona_count['Delta_Confirmed'],corona_count['Delta_Deaths'],corona_count['Delta_Recovered'])]
from flask import Flask,render_template,request
import sys
app=Flask(__name__)
@app.route('/')
def home():
    return render_template('corona.html',table = mdu_c,map=corona_count,pair1=pair1,pair2=pair2)
if __name__=="__main__":
	app.run(debug='True')

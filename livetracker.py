def Corona_State():
	import pandas as pd
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
corona_count = Corona_State()
from flask import Flask,render_template,request
import sys
app=Flask(__name__)
@app.route('/')
def home():
    return render_template('corona.html',table= mdu_c)
if __name__=="__main__":
	app.run(debug='True')

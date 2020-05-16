def corona_details():
    import pandas as pd
    cor_df=pd.read_csv('https://raw.githubusercontent.com/h2oai/covid19-datasets/master/data/India/CaseDetailsIndia.csv')
    cor_df.head()
    corona_count=cor_df.groupby('State/UnionTerritory').sum()[['Cured','Deaths','Confirmed']]
    return corona_count
corona_count = corona_details()

from flask import Flask,render_template,request
import sys
app=Flask(__name__)
@app.route('/')
def home():
    return render_template('corona.html',table= corona_count)
if __name__=="__main__":
	app.run(debug='True')

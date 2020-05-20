import pandas as pd
import json
import plotly.express as pg
def graph_1():
    df=pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')
    df
    cdf=df[df['Country/Region'].str.contains('India')]
    cols=['Date','Confirmed']
    cdf1=cdf[cols]
    cdf1
    fig=pg.bar(cdf1,x='Date',y='Confirmed',title = 'Corona confirmation all across India : Time series')
    return fig
from flask import Flask,render_template,request
app=Flask(__name__)
@app.route('/')
def graph():
    fig=graph_1().to_html()
    return render_template('index.html',fig=fig)

if __name__=="__main__":
	app.run(debug=True)

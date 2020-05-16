from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
import MySQLdb
db=MySQLdb.connect("localhost","root","Goodluck","pm")
app=Flask(__name__)
@app.route("/")
def index():
	return render_template("form.html")
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
        query=select * from Donation where Phone=phone
        db.commit()
        cur.close()
        return render_template("checkout.html")
if __name__ == '__main__':
    app.run(debug=True)
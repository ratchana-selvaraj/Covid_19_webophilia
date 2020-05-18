from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
import MySQLdb
db=MySQLdb.connect("localhost","root","Goodluck","pm")
app=Flask(__name__)
@app.route("/")
def index():
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
    return render_template("Thankyou.html")
if __name__ == '__main__':
    app.run(debug=True)
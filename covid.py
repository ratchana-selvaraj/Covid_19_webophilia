from flask import Flask,render_template,request,redirect,url_for
app = Flask(__name__)
dfname=[]
dlname=[]
demails=[]
dmoney=[]
dphones=[]
@app.route("/")
def index():
	return render_template("index.html")
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
        dfname.append(fname) 
        dlname.append(lname)
        demails.append(Mail)
        dmoney.append(Amount)
        dphones.append(phone)
        return render_template('checkout.html',firstname=fname,lastname=lname,mail=Mail,phn=phone,amount=Amount,pm=payment)      
@app.route("/Thankyou",methods=["GET","POST"])
def thankyou():
    return render_template("volenteer.html")
if __name__ == "__main__":
    app.run(debug=True)
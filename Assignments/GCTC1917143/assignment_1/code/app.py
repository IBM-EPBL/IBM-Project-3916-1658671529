from flask import Flask,url_for,redirect
from markupsafe import escape
from flask import request
from flask import render_template
app = Flask(__name__) #constructor

@app.route("/home") #binding url
def home():
    return render_template("login.html")

@app.route("/login",methods=["POST","GET"]) #binding url
def login():
    if request.method=="POST":
        user=request.form["username"]
        email=request.form["email"]
        phoneno=request.form["phoneno"]
        return redirect(url_for("success",name=user,email=email,phoneno=phoneno))
    
@app.route("/success/<name>/<email>/<phoneno>") #binding url
def success(name,email,phoneno):
    return f"welcome {name} {email} {phoneno}"

if __name__=='__main__':
    app.run(debug=True)
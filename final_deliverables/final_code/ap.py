from flask import Flask,url_for,redirect
from markupsafe import escape
from flask import request
from flask import render_template
app = Flask(__name__) #constructor

@app.route("/", methods=['GET']) #binding url
def hello_world():
    if request.method == 'GET':
        return ("<p>Hello, World!</p>")
        
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/redirect/<name>')
def show_redirect(name):
    if(name=='admin'):
        return redirect(url_for("hello"))
    else:
        return redirect(url_for("content",name=name))

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('home.html', name=name)

@app.route('/content')
@app.route('/content/<name>')
def content(name=None):
    dic={'phy':50,'che':60,'mat':80}
    return render_template('content.html', name=name,result=dic)

@app.route("/home") #binding url
def home():
    return render_template("login.html")

@app.route("/login",methods=["POST"]) #binding url
def login():
    if request.method=="POST":
        user=request.form["nm"]
        return render_template("login.html",y=user)

@app.route("/login1",methods=["POST","GET"]) #binding url
def login1():
    if request.method=="POST":
        user=request.form["nm"]
        return redirect(url_for("success",name=user))
    else:
        user=request.args.get('nm')
        return redirect(url_for("success",name=user))

@app.route("/success/<name>") #binding url
def success(name):
    return "welcome %s" %name

if __name__=='__main__':
    app.run(debug=True)
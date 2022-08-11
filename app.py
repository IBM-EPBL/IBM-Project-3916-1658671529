from flask import Flask
from markupsafe import escape
from flask import request
from flask import render_template
app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello_world():
    if request.method == 'GET':
        return "<p>Hello, World!</p>"
        
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

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
    return render_template('content.html', name=name)
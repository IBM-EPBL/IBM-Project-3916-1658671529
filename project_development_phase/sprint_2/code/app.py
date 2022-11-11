from flask import Flask,url_for,redirect,session
from flask import request
from flask import render_template
import ibm_db
import re
from datetime import datetime

app = Flask(__name__) #constructor
app.secret_key='a'

conn=ibm_db.connect('')


@app.route("/", methods=['GET']) #binding url
def hello_world():
    return render_template('register.html')



@app.route("/login", methods=['GET', "POST"])
def login():
    global userid
    msg=""
    if request.method=="POST": 
        name=request.form['username'] 
        password=request.form['password']
        sql="SELECT * FROM CPG44748.users WHERE name=? AND password=?"
        stmt=ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.bind_param(stmt,2, password)
        print(stmt)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)

        if account:
            session['Loggedin']=True
            session['id']=account["ID"] 
            userid=account["NAME"]
            session['username']=account["NAME"] 
            msg='Logged in successfully!'
            return render_template("dashboard.html", msg=msg)
        else:
            msg="Incorrect username/password"
            return render_template('login.html',msg=msg)

    if request.method=="GET": 
        msg="Pls login"
        return render_template('login.html',msg=msg)

@app.route("/register", methods=["GET", "POST"]) 
def register():
    msg=""
    if request.method=="POST":
        username=request.form['username'] 
        email=request.form['email'] 
        password=request.form['password']
        sql= "SELECT * FROM users WHERE name=?"
        stmt=ibm_db.prepare(conn, sql) 
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        
        if account:
            msg="Account already exists!"
        # elif not re.match(r'[^]+@[^]+\.[^@]+', email):
        #     msg="Invalid email address"
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg="name must contain only characters and numbers"
        else:
            insert_sql="INSERT INTO users(name,email,password) VALUES (?,?,?)"
            prep_stmt=ibm_db.prepare (conn, insert_sql) 
            ibm_db.bind_param(prep_stmt, 1, username) 
            ibm_db.bind_param(prep_stmt, 2, email) 
            ibm_db.bind_param(prep_stmt, 3, password) 
            ibm_db.execute(prep_stmt)
            msg='You have successfully Registered!'
        return render_template( 'login.html', msg=msg)

    elif request.method=='GET':
        msg='Please fill out of the form' 
        return render_template( 'register.html', msg=msg)

@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')

@app.route('/add_data')
def dash_add():
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    return render_template('add.html',day=currentDay,month=currentMonth,year=currentYear)
    
@app.route('/add', methods=['GET', 'POST'])
def apply():
    msg=" "
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
        
    if request.method=="POST":
        expense=float(request.form['expense'])
        sql="SELECT * FROM expenses WHERE e_day=? and e_month=? and e_year=?"
        stmt=ibm_db.prepare (conn, sql)
        ibm_db.bind_param(stmt, 1, currentDay)
        ibm_db.bind_param(stmt, 2, currentMonth)
        ibm_db.bind_param(stmt, 3, currentYear)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg="Updated successfully"
            edit_sql="UPDATE expenses SET (total) = (?) WHERE e_day=? and e_month=? and e_year=? and user_id=?;"
            prep_stmt=ibm_db.prepare(conn, edit_sql)
            expense=expense+account["TOTAL"]
            ibm_db.bind_param(prep_stmt, 1, expense)
            ibm_db.bind_param(prep_stmt, 2, currentDay)
            ibm_db.bind_param(prep_stmt, 3, currentMonth)
            ibm_db.bind_param(prep_stmt, 4, currentYear)
            ibm_db.bind_param(prep_stmt, 5, session['id'])
            ibm_db.execute(prep_stmt)
            return render_template('add.html',day=currentDay,month=currentMonth,year=currentYear,msg=msg)
            
        insert_sql="INSERT INTO expenses(e_day,e_month,e_year,total,user_id) VALUES (?,?,?,?,?)"
        prep_stmt=ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, currentDay)
        ibm_db.bind_param(prep_stmt, 2, currentMonth)
        ibm_db.bind_param(prep_stmt, 3, currentYear)
        ibm_db.bind_param(prep_stmt, 4, expense)
        ibm_db.bind_param(prep_stmt, 5, session['id'])
        ibm_db.execute(prep_stmt)
        session["LoggedIn"]=True
        msg="Added successfully"
        return render_template('add.html',day=currentDay,month=currentMonth,year=currentYear,msg=msg)

        
    elif request.method=="GET": 
        msg='Please fill out the form' 
        return render_template("add.html",msg=msg,day=currentDay,month=currentMonth,year=currentYear)

@app.route('/edit_data')
def dash_edit():
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    sql="SELECT * FROM expenses WHERE e_day=? and e_month=? and e_year=?"
    stmt=ibm_db.prepare (conn, sql)
    ibm_db.bind_param(stmt, 1, currentDay)
    ibm_db.bind_param(stmt, 2, currentMonth)
    ibm_db.bind_param(stmt, 3, currentYear)
    ibm_db.execute(stmt)
    account=ibm_db.fetch_assoc(stmt)
    print(account)
    if not account:
        msg="Please insert the data"
        return render_template('add.html',day=currentDay,month=currentMonth,year=currentYear,msg=msg)
    return render_template('edit.html',day=currentDay,month=currentMonth,year=currentYear,expense=account["TOTAL"])

@app.route('/edit', methods=['GET', 'POST']) 
def edit():
    msg=" "
    if request.method=="POST":
        expense=request.form['expense']
        currentDay = datetime.now().day
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        sql="SELECT * FROM expenses WHERE e_day=? and e_month=? and e_year=?"
        stmt=ibm_db.prepare (conn, sql)
        ibm_db.bind_param(stmt, 1, currentDay)
        ibm_db.bind_param(stmt, 2, currentMonth)
        ibm_db.bind_param(stmt, 3, currentYear)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if not account:
            msg="Please insert the data"
            return render_template('add.html',day=currentDay,month=currentMonth,year=currentYear,msg=msg)
            
        edit_sql="UPDATE expenses SET (total) = (?) WHERE e_day=? and e_month=? and e_year=? and user_id=?;"
        prep_stmt=ibm_db.prepare(conn, edit_sql)
        ibm_db.bind_param(prep_stmt, 1, expense)
        ibm_db.bind_param(prep_stmt, 2, currentDay)
        ibm_db.bind_param(prep_stmt, 3, currentMonth)
        ibm_db.bind_param(prep_stmt, 4, currentYear)
        ibm_db.bind_param(prep_stmt, 5, session['id'])
        ibm_db.execute(prep_stmt)
        session["LoggedIn"]=True
        msg="Edited successfully"
        return render_template('edit.html',day=currentDay,month=currentMonth,year=currentYear,msg=msg)

        
    elif request.method=="GET": 
        msg='Please fill out the form' 
        return render_template("edit.html",msg=msg)

if __name__=='__main__':
    app.run(debug=True)
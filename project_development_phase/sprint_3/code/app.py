from flask import Flask,url_for,redirect,session
from flask import request
from flask import render_template
import ibm_db
import re
from sendmail import send_data
from datetime import datetime
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__) #constructor
app.secret_key='a'

conn=ibm_db.connect("")



@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    sql="SELECT * FROM expenses WHERE user_id=?"
    stmt=ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1, session['id'])
    ibm_db.execute(stmt)
    expense=[]
    month=[]
    while ibm_db.fetch_row(stmt) != False:
        expense.append(ibm_db.result(stmt, 4))
        month.append(ibm_db.result(stmt, 2))
    axis.plot(month,expense)
    axis.set_title("Day vs Expenses")

    # Adding the labels
    axis.set_ylabel("Expenses")
    axis.set_xlabel("Day")
    return fig


@app.route('/plot1.png')
def plot1_png():
    fig = create_figure1()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure1():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    sql="SELECT * FROM expenses WHERE user_id=?"
    stmt=ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1, session['id'])
    ibm_db.execute(stmt)
    expense=[]
    month=[]
    while ibm_db.fetch_row(stmt) != False:
        expense.append(ibm_db.result(stmt, 4))
        month.append(ibm_db.result(stmt, 1))
    axis.plot(month,expense)
    axis.set_title("Month vs Expenses")
 
    # Adding the labels
    axis.set_ylabel("Expenses")
    axis.set_xlabel("Month")
    return fig

@app.route('/plot2.png')
def plot2_png():
    fig = create_figure2()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure2():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    sql="SELECT * FROM expenses WHERE user_id=?"
    stmt=ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1, session['id'])
    ibm_db.execute(stmt)
    expense=[]
    year=[]
    while ibm_db.fetch_row(stmt) != False:
        expense.append(ibm_db.result(stmt, 4))
        year.append(ibm_db.result(stmt, 3))
    axis.plot(year,expense)
    axis.set_title("Year vs Expenses")
 
    # Adding the labels
    axis.set_ylabel("Expenses")
    axis.set_xlabel("Year")
    return fig

@app.route("/", methods=['GET']) #binding url
def hello_world():
    return render_template('register.html')


@app.route('/login', defaults={'msg': ''}, methods=['GET', "POST"])
@app.route("/login/<msg>", methods=['GET', "POST"])
def login(msg):
    global userid
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
            session['email']=account["EMAIL"]
            userid=account["NAME"]
            session['username']=account["NAME"] 
            msg='Logged in successfully!'
            return redirect(url_for("dash",msg=msg))
        else:
            msg="Incorrect username/password"
            
            return render_template('login.html',msg=msg)


    if request.method=="GET": 
        return render_template('login.html',msg=msg)

@app.route('/register', defaults={'msg': ''}, methods=['GET', "POST"])
@app.route("/register/<msg>", methods=['GET', "POST"])
def register(msg):
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
        return redirect(url_for("login",msg=msg))

    elif request.method=='GET':
        msg='Please fill out of the form' 
        return render_template( 'register.html', msg=msg)

@app.route('/dashboard', defaults={'msg': ''}, methods=['GET', "POST"])
@app.route("/dashboard/<msg>", methods=['GET', "POST"])
def dash(msg):
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
        
    if request.method=="POST":
        budget=float(request.form['budget'])
        sql="SELECT * FROM budget WHERE id=1"
        stmt=ibm_db.prepare (conn, sql)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg="Updated successfully"
            edit_sql="UPDATE budget SET year = (?),month=(?),total=(?) WHERE id=1 ;"
            prep_stmt=ibm_db.prepare(conn, edit_sql)
            ibm_db.bind_param(prep_stmt, 1, currentYear)
            ibm_db.bind_param(prep_stmt, 2, currentMonth)
            ibm_db.bind_param(prep_stmt, 3, budget)
            ibm_db.execute(prep_stmt)
            msg="Set budget successfully!"
            return render_template('dashboard.html',month=currentMonth,year=currentYear,msg=msg)

    elif request.method=="GET": 
        return render_template('dashboard.html',month=currentMonth,year=currentYear)
    
@app.route('/add', defaults={'msg': ''}, methods=['GET', "POST"])
@app.route("/add/<msg>", methods=['GET', "POST"])
def apply(msg):
    msg=" "
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
        
    if request.method=="POST":
        expense=float(request.form['expense'])
        sql="SELECT * FROM budget WHERE id=1 and year = (?) and month=(?)"
        stmt=ibm_db.prepare (conn, sql)
        ibm_db.bind_param(stmt, 1, currentYear)
        ibm_db.bind_param(stmt, 2, currentMonth)
        ibm_db.execute(stmt)
        account1=ibm_db.fetch_assoc(stmt)

        if account1:
            sql="SELECT * FROM expenses WHERE e_day=? and e_month=? and e_year=? and user_id=?"
            stmt=ibm_db.prepare (conn, sql)
            ibm_db.bind_param(stmt, 1, currentDay)
            ibm_db.bind_param(stmt, 2, currentMonth)
            ibm_db.bind_param(stmt, 3, currentYear)
            ibm_db.bind_param(stmt,4, session['id'])
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
                if(expense>account1["TOTAL"]):
                    send_data(session["email"])
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
            if(expense>account1["TOTAL"]):
                send_data(session["email"])
            return render_template('add.html',day=currentDay,month=currentMonth,year=currentYear,msg=msg)
        else:
            msg="Set budget!!"
            return redirect(url_for('dash',msg=msg))
        
    elif request.method=="GET": 
        msg='Please fill out the form' 
        return render_template("add.html",msg=msg,day=currentDay,month=currentMonth,year=currentYear)

@app.route('/edit_data', defaults={'msg': ''}, methods=['GET', "POST"])
@app.route("/edit_data/<msg>", methods=['GET', "POST"])
def dash_edit(msg):
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    sql="SELECT * FROM expenses WHERE e_day=? and e_month=? and e_year=? and user_id=?;"
    stmt=ibm_db.prepare (conn, sql)
    ibm_db.bind_param(stmt, 1, currentDay)
    ibm_db.bind_param(stmt, 2, currentMonth)
    ibm_db.bind_param(stmt, 3, currentYear)
    ibm_db.bind_param(stmt, 4, session['id'])
    ibm_db.execute(stmt)
    account=ibm_db.fetch_assoc(stmt)
    print(account)
    if not account:
        msg="Please insert the data"
        return redirect(url_for('apply',msg=msg))
    return render_template('edit.html',day=currentDay,month=currentMonth,year=currentYear,expense=account["TOTAL"],msg=msg)

@app.route('/edit', methods=['GET', 'POST']) 
def edit():
    msg=" "
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    if request.method=="POST":
        expense=request.form['expense']
        sql="SELECT * FROM expenses WHERE e_day=? and e_month=? and e_year=? and user_id=?;"
        stmt=ibm_db.prepare (conn, sql)
        ibm_db.bind_param(stmt, 1, currentDay)
        ibm_db.bind_param(stmt, 2, currentMonth)
        ibm_db.bind_param(stmt, 3, currentYear)
        ibm_db.bind_param(stmt, 4, session['id'])
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if not account:
            msg="Please insert the data"
            return redirect(url_for('add',msg=msg))
            
        edit_sql="UPDATE expenses SET (total) = (?) WHERE e_day=? and e_month=? and e_year=? and user_id=?;"
        prep_stmt=ibm_db.prepare(conn, edit_sql)
        ibm_db.bind_param(prep_stmt, 1, expense)
        ibm_db.bind_param(prep_stmt, 2, currentDay)
        ibm_db.bind_param(prep_stmt, 3, currentMonth)
        ibm_db.bind_param(prep_stmt, 4, currentYear)
        ibm_db.bind_param(prep_stmt, 5, session['id'])
        ibm_db.execute(prep_stmt)
        session["LoggedIn"]=True
        print(float(expense),account["TOTAL"])
        if(float(expense)>account["TOTAL"]):
            send_data(session["email"])
        msg="Edited successfully"
        return redirect(url_for("dash_edit",msg=msg))

    elif request.method=="GET":  
        return redirect(url_for("dash_edit"))


@app.route("/survey")
def survey():
    return render_template('survey.html')

if __name__=='__main__':
    app.run(debug=True)

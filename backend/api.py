import datetime
from flask import Flask, render_template, request, redirect, url_for, session, json, jsonify 
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
import numpy as np
import MySQLdb.cursors
import re
from models import db, User

# x = datetime.datetime.now()

app = Flask(__name__)

app.secret_key = "27eduCBA09"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'shop'
app.config['SECRET_KEY'] = 'mikuabe-flaskreactapp'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost:3306/shop"

CORS(app, suppors_credentials=True)
mysql = MySQL(app)

@app.route('/')

@app.route('/login', methods=['POST','GET'])
def login():

     result = {
        "msg": "login"
    }
    msg = ''
    # if request.method == 'GET':
    #     return render_template('login.html')
    #     # return 'Please login via login form'
    # if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.json['username']
        password = request.json['password']

        # cursor = mysql.connection.cursor()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(''' SELECT * FROM Users WHERE UserName =%s and Password=%s;''', (username, password))
        account = cursor.fetchone()

        if account:
            # set data to session
            # session['login'] = True
            # session['id'] = account['ID']
            # session['firstname'] = account['FirstName']
            # session['lastname'] = account['LastName']
            # session['username'] = account['UserName']
            # session['email'] = account['Email']
            # session['password'] = account['Password']
            # msg = 'You logged in successfully!'
            # return render_template('home.html', msg=msg)
            result["msg"] = 'successfully logged in'
        else:
            result["msg"] = 'Incorrect username or password !'
            # msg = 'Incorrect username or password !'
            # return render_template('login.html', msg=msg)
        mysql.connection.commit()
        cursor.close()
        return jsonify(result)
        # return f'Done!!'
    #     return render_template('home.html', msg=msg)
    # return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    # delete from session
    session.pop('login', None)
    session.pop('id', None)
    session.pop('firstname', None)
    session.pop('lastname', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('password', None)
    return redirect(url_for('login'))


@app.route('/signup', methods=['POST'])
def signup():
    firstname = request.json["firstname"]
    lastname = request.json["lastname"]
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    result = {
        "msg": "signup"
    }

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT * FROM Users WHERE UserName=%s;''', (username, ))
    account = cursor.fetchone()
    if account:
        # msg = 'Accout already exist, please use other username'
        result["msg"] = 'Accout already exist'
    # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
    #     msg = 'Invalid email address !'
    # elif not re.match(r'[A-Za-z0-9]+', username):
    #     msg = 'name must contain only characters and numbers !'
    else:
        cursor.execute(''' INSERT INTO Users (FirstName, LastName, UserName, Email, Password) VALUES (%s,%s,%s,%s,%s);''', (firstname, lastname, username, email, password))
        result["msg"] = 'You have successfully registered !'

    mysql.connection.commit()
    cursor.close()
    return jsonify(result)
    # return render_template('login.html', msg=msg)

    # return jsonify({
    #     "id": "000",
    #     "firstname": firstname
    #     })

# show all records from the MySQL Users table
@app.route('/users')
def users():
    # if 'login' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''SELECT * FROM Users;''')
        users = cursor.fetchall()
        if len(users) > 0:
            return json.dumps(users)
            # return np.asarray(users)
            # return render_template('userslist.html', users=users)
        # return render_template('home.html')

# show all records from the MySQL Products table
@app.route('/products')
def products():
    # if 'login' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''SELECT * FROM Products ;''')
        products = cursor.fetchall()
        if len(products) > 0:
            return json.dumps(products)
        #     return render_template('productslist.html', products=products)
        # return render_template('home.html')
        

if __name__ == '__main__':
    app.run(debug=True)
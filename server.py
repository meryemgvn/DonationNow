import os
import sys
from os.path import dirname, join, realpath
from datetime import datetime
from flask import (Flask,render_template,request,redirect,url_for,flash,abort,session)
from flask_login import (LoginManager,login_user,current_user,login_required,logout_user)
from passlib.hash import pbkdf2_sha256 as hasher
from wtforms import Form, BooleanField, StringField, validators,PasswordField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from user import get_user_2, get_user
import psycopg2
import dbinit
import views
import database

url = "postgres://vahbelka:oXTNFzp-WxAaS-pvu50bh9dhGxBp4kjl@otto.db.elephantsql.com:5432/vahbelka"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisisSecret'
app.config.from_object("settings")

today = datetime.today()
day_name = today.strftime("%d %B, %Y")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)



@app.route("/")
def home_page():
     logout_user()
     return redirect(url_for("index_page"))

@app.route("/index",methods=['GET', 'POST'])
def index_page():
    return render_template("index.html", day=day_name)



#def create_app():
    
    #app.config.from_object("settings")

    #app.add_url_rule("/", view_func=views.home_page)
    #app.add_url_rule("/login", view_func=views.login_page)
    #app.add_url_rule("/signup", view_func=views.signup_page)
    #return app

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

@app.route("/login",methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        obje = database.Database()

@app.route("/signup",methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return render_template('signup.html')

if __name__ == "__main__":
    port = app.config.get("PORT", 8080)
    app.run(host="127.0.0.1", port=port)
"""
app = Flask(__name__)

@app.route("/")
def home_page():

    return render_template("index.html", day=day_name)

@app.route("/login")
def login_page():

    return render_template("login.html",day=day_name)

@app.route("/signup")
def signup_page():
    
    return render_template("signup.html",day=day_name)
"""


"""
conn = psycopg2.connect(dbname= "postgres", user="postgres", password="0000", port="5432", host="localhost")
cursor = conn.cursor()
cursor.execute("DROP TABLE Users; ")
conn.commit()
cursor.close()
conn.close()
"""

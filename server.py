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
    obje = database.Donation()
    cursor = obje.All_request()
    return render_template("index.html", day=day_name, cursor=cursor)



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
        obje = database.Donation()
        cursor=obje.Check_existing_user(username)
        if len(cursor) != 1:
            flash("Warning!")
            flash('Username or password is wrong')
            return redirect(url_for("login_page"))
        else:
            if not hasher.verify(password, cursor[0][1]):
                flash("Warning!")
                flash('Username or password is wrong!')
                return redirect(url_for("login_page"))
            else:
                user = get_user_2(cursor[0][0], cursor[0][1])
                login_user(user, remember=True)
                next_page = request.args.get("next", url_for("my_profile_page"))
                return redirect(next_page)

@app.route("/")
def logout_page():
    print("1")
    logout_user()
    flash("Info!")
    flash("You have logged out.")
    return redirect(url_for("home_page"))
login_manager.init_app(app)
login_manager.login_view = "login_page"

@app.route("/signup",methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        name= request.form["name"]
        surname= request.form["surname"]
        email= request.form["email"]
        password = request.form["password"]
        register_time = datetime.now()
       # photo = request.form["photo"]
        city = request.form["city"]
        username = request.form["username"]
        obje = database.Donation()
        cursor=obje.Check_username(username)
        print(cursor)
        if cursor == False:
            flash("Warning!")
            flash("Please select a different username!")
            return redirect(url_for("signup_page"))
        else:
            obje.User_Add(name, surname,email, hasher.hash(password), register_time, city, username)
        flash("Info!")
        flash("You have crated your account, please login!")
        return redirect(url_for("login_page"))

@app.route('/profile/request',methods=['GET','POST'])
@login_required
def request_page(user_key):
    obje = database.Donation()
    if request.method == "POST":
        #report = request.form.get('buttonName')
        #donate = request.form.get('buttonName')
        add = request.form.get('buttonName')
        #if donate== "donate":
            #return redirect(url_for("donate_page"))
       # elif report== "report":
            #form_report_keys = request.form.getlist("report_keys")
           # for form_report_key in form_report_keys:
               # obje.adding_report(int(form_report_key))
            #cursor = obje.Requests(current_user.username)
            #return render_template('index.html',cursor=cursor, username=current_user.username, currentuser=current_user.username)
        if add == "adding":
            return redirect(url_for("request_adding_page"))
    cursor = obje.Requests(user_key)
    return render_template('requests.html',cursor=cursor, username=current_user.username, currentuser=current_user.username)
app.add_url_rule("/profile/request/<user_key>", view_func=request_page)

@app.route('/profile/request/add',methods=['GET','POST'])
@login_required
def request_adding_page():
    obje = database.Donation()
    if request.method == 'GET':
        return render_template('add_request.html')
    elif request.method == 'POST':
        req_name = str(request.form["req_name"])
        amount = request.form["amount"]
        req_time= datetime.now()
        obje.request_add(current_user.username,req_time,req_name,amount)
        flash("You have added.")
        return redirect(url_for('request_page', user_key=current_user.username ))
    return render_template('add_request.html')
app.add_url_rule("/profile/request/<user_key>", view_func=request_page,methods=['GET','POST'])



@app.route('/profile')
@login_required
def my_profile_page():
    return render_template('profile.html', username=current_user.username)

@app.route('/profile')
@login_required
def user_key(user_key):
    if current_user.username == user_key:
        return redirect(url_for('my_profile_page'))
    #return render_template("other_profiles.html",username=user_key)
#app.add_url_rule("/myprofile/<user_key>", view_func=user_key)

@app.route('/profile/delete_account',methods=['GET','POST'])
@login_required
def delete_my_account_page(user_key):
    if user_key == current_user.username:
        if request.method == 'POST':
            password = request.form["password"]
            obje = database.Donation()
            cursor=obje.Check_existing_user(current_user.username)
            if not hasher.verify(password, cursor[0][1]):
                flash("Warning!")
                flash("Password is wrong!")
                return redirect(url_for("delete_my_account_page",user_key=current_user.username))
            else:
                obje.Delete_account(current_user.username)
                return redirect(url_for('home_page'))
        return render_template('delete_account.html',username=user_key)
    return redirect(url_for("index_page"))
app.add_url_rule("/profile/delete_account/<user_key>", view_func=delete_my_account_page,methods=['GET','POST'])



if __name__ == "__main__":
    port = app.config.get("PORT", 8080)
    app.run(host="127.0.0.1", port=port)


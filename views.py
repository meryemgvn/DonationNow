from datetime import datetime

from flask import render_template

today = datetime.today()
day_name = today.strftime("%d %B, %Y")

def home_page():

    return render_template("index.html", day=day_name)

def signup_page():
    
    return render_template("signup.html",day=day_name)

def login_page():

    return render_template("login.html",day=day_name)
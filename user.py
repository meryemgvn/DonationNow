from flask import current_app
from flask_login import UserMixin
url = "postgres://vahbelka:oXTNFzp-WxAaS-pvu50bh9dhGxBp4kjl@otto.db.elephantsql.com:5432/vahbelka"

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active
    
def get_user(user_id):
    password = 0
    user = User(user_id, password)
    return user

    
def get_user_2(user_id, Password):
    password = Password
    user = User(user_id, password)
    return user
       # password = current_app.config["PASSWORDS"].get(user_id)
       # user = User(user_id, password) if password else None
       # if user is not None:
        #    user.is_admin = user.username in current_app.config["ADMIN_USERS"]
        #return user
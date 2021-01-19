import psycopg2 as dbapi
import os

url = "postgres://vahbelka:oXTNFzp-WxAaS-pvu50bh9dhGxBp4kjl@otto.db.elephantsql.com:5432/vahbelka"

class Database:
	def Check_username(self, username):
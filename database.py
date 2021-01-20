import psycopg2 as dbapi
import os

url = "postgres://vahbelka:oXTNFzp-WxAaS-pvu50bh9dhGxBp4kjl@otto.db.elephantsql.com:5432/vahbelka"

class Donation:
	def Check_username(self, username):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """Select username FROM users Where username=%s;"""
				cursor.execute(statement,([username]))
				cursor_list=cursor.fetchall()
				len_c = len(cursor_list)
				if len_c == 1:
					return False
				else:
					return True

	def User_Add(self, name, surname,email, password, register_time, city, username):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """INSERT INTO users (name, surname, email, password, register_time, city, username) VALUES(%s,%s,%s,%s,%s,%s,%s);"""
				cursor.execute(statement,([name, surname, email, password, register_time, city, username]))
	
	def Check_existing_user(self, username):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """Select username, password FROM users Where username=%s;"""
				cursor.execute(statement,([username]))
				cursor_list=cursor.fetchall()
				return cursor_list

	def Delete_account(self, username):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement1 = """Delete FROM donations Where userid=(Select userid FROM users Where username=%s);"""
				statement2 = """Delete FROM requests Where userid=(Select userid FROM users Where username=%s);"""
				statement3 = """Delete FROM users Where username=%s;"""
				cursor.execute(statement1,([username]))
				cursor.execute(statement2,([username]))
				cursor.execute(statement3,([username]))

	def Requests(self,username):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """Select req_id, requests.userid, req_time, req_name, amount, report,users.username From requests left join users on users.userid=requests.userid where users.username=%s and is_paid='0';"""
				cursor.execute(statement,([username]))
				cursor_list=cursor.fetchall()
				return cursor_list
	
	def All_request(self):
			with dbapi.connect(url) as connection:
				with connection.cursor() as cursor:
					statement = """Select req_id, requests.userid, req_time, req_name, amount, report,users.username From requests left join users on users.userid=requests.userid where is_paid='0';"""
					cursor.execute(statement)
					cursor_list=cursor.fetchall()
					return cursor_list

	def request_add(self,username,req_time, req_name, amount):
			with dbapi.connect(url) as connection:
				with connection.cursor() as cursor:
					statement0 = """Select userid FROM users Where username=%s;"""
					cursor.execute(statement0)
					userid = cursor_list=cursor.fetchall()
					statement = """INSERT INTO requests (userid, req_time, req_name, amount) VALUES(%s) Where username = %s;"""
					cursor.execute(statement,([userid,req_time,req_name,amount]))
					cursor_list=cursor.fetchall()
					return cursor_list
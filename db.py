import csv
import sqlite3
from sqlite3 import Error

def create_connection(db_filename):
	"""
		open connection with database by name

		:param db_filename: database file
		:return connection object 
	"""
	try:
		conn = sqlite3.connect(db_filename)
		print("Connecting to %s" % db_filename)
		return conn
	except Error as e:
		print("Error: %s" % e)

	return None

def create_table(conn, create_table_sql):
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)
	# conn.close()

def insert_data(conn, sql_insert):
	try:
		c = conn.cursor()
		c.execute(sql_insert)
		conn.commit()
	except Error as e:
		print("Error! can`t insert data %s" % e)

	# conn.close()

def multy_insert(conn, data):
	query = """INSERT INTO cigarettes(name, image) values (?, ?)"""
	try:
		c = conn.cursor()
		c.executemany(query, data)
		conn.commit()
	except Error as e:
		print("Error! can`t insert data %s" % e)

def select_all(conn):
	query = """SELECT name, image FROM cigarettes"""
	try:
		c = conn.cursor()
		c.execute(query)
		results = c.fetchall()
		# conn.commit()
		return results
	except Error as e:
		print("Error! can`t select data %s" % e)

def select_item(conn, item):
	query = """SELECT name, image FROM cigarettes WHERE name='%s'""" % item
	try:
		c = conn.cursor()
		c.execute(query)
		results = c.fetchone()
		return results
	except Error as e:
		print("Error! can`t select data %s" % e)

def test():
	database = 'test.db'

	sql_create_cigarettes_table = """CREATE TABLE IF NOT EXISTS cigarettes (
										id integer AUTO_INCREMENT PRIMARY KEY,
										name text NOT NULL,
										image text NOT NULL
										);"""
	# data = ('Bond', 'Bond.jpg')
	# sql_insert = INSERT INTO cigarettes(name, image) values ("LM", "LM.jpg")
	# sql_select = """SELECT * FROM cigarettes"""

	conn = create_connection(database)

	if conn is not None:
		create_table(conn, sql_create_cigarettes_table)
		print("Creating table")
		# insert_data(conn, sql_insert)
		# res = select_data(conn, sql_select)
		# print(res)

	else:
		print("Error! cannot create database connecion.")

	conn.close()

if __name__ == "__main__":
	# conn = create_connection('test.db')
	# # test()
	# name, image = select_item(conn, 'Bond')
	# print(name, image)
	test()
	ls = []
	with open("class_cigarettes.csv", "r") as f:
		reader = csv.reader(f)

		for row in reader:
			data = row[0].split(',')[0]
			name = data
			image = "images/%s.jpg" % data
			ls.append((name, image))
	print(ls)
	conn = create_connection("test.db")
	multy_insert(conn, ls)
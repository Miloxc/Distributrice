import sqlite3

#CHECK IF TABLES ARE ALREADY CREATED
def isInitialized(cur):
	check_tables = "SELECT name FROM sqlite_master WHERE type='table'"
	cur.execute(check_tables)
	if c.fetchall():
		return True
	else:
		return False

#INITIALIZING TABLES WITH <amount> OF EACH
def initialize(cur, amount):
	#Setting querry strings
	create_stock = """
		CREATE TABLE stock(
		id integer PRIMARY KEY,
		name text NOT NULL,
		amount integer NOT NULL,
		price REAL NOT NULL);"""
	insert_stock = "INSERT INTO stock (name, amount, price) VALUES (?, ?, ?)"
	food = ["Chocolate Bar", "Chips", "Pop", "Candy"]
	prices = [0.75, 1.00, 1.25, 0.75]
	
	cur.execute(create_stock)

	for i in range(4):
		cur.execute(insert_stock, (food[i], amount, prices[i]))








#ESTABLISHING CONNECTION
conn = sqlite3.connect('distributrice.db')
c = conn.cursor()

if not isInitialized(c):
	initialize(c, 15)

conn.close()
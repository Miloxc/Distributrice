# distributrice.py
# Description:	La script primaire (python) pour la distributrice

import sqlite3
import os.path
import datetime




#Fonction qui check si un item a deja une entree dans la base de donnees
#Input:
#	c - la connection sqlite
#	item_name - le nom de l'item qu'on veut verifier
#Output:
#	exists - Vrai si l'item existait deja
def stock_item_exists(c, item_name):
	#Retrouver tous les noms d'items
	names = get_all(c, 'names')
	exists = True if item_name in names else False
	return exists




#Fonction qui initialise la base de donnees
#Input:
#	db_file - le fichier de la base de donnees (complete path)
#Output: 
#	aucun
def initialize_db(db_file):


	#Verifier si la base de donnees exist deja
	if os.path.isfile(db_file):
		#Demande si on veut re-initialiser
		print("Le fichier exist deja, aimeriez vous re-initialiser la base de donnees?")
		re_initialize = int(input("\t1 pour oui, 0 pour non: "))
		while re_initialize != 1 and re_initialize != 0:
			re_initialize = int(input("Veuillez entrez 1 pour oui, 0 pour non: "))
		print("")

		if not re_initialize:
			return
		else:
			#Effacer le fichier pour re-initialiser
			print("La distributrice sera re-initialisee.\n")
			os.remove(db_file)


	#Creer la connection a sqlite
	conn = sqlite3.connect(db_file)
	c = conn.cursor()


	#Initialisation de variables pour les donees initiales
	names = []
	numbers = []
	prices = []

	#Trouver le nobre d'item de l'utilisateur
	n = int(input("Entrez le nombre d'items dans la distributrice: "))
	print("")
	
	#L'utilisateur entre l'information pour les items initiales
	for i in range(n):
		names.append(input("Entrez le nom de l'item: "))
		numbers.append(int(input("Entrez le montant dans la distributrice: ")))
		prices.append(float(input("Entrez le priz par item: ")))
		print("")
	

	#Creer la table 'stock'
	create_stock_table = """
		CREATE TABLE stock(
		id integer PRIMARY KEY,
		name text NOT NULL UNIQUE,
		amount integer NOT NULL,
		price REAL NOT NULL);"""
	create_report_table = """
		CREATE TABLE report(
		id integer PRIMARY KEY,
		name text NOT NULL,
		amount integer NOT NULL,
		price real NOT NULL,
		date TEXT NOT NULL)"""
	c.execute(create_stock_table)
	c.execute(create_report_table)


	#Inserer les donnes initiales
	insert_stock = "INSERT INTO stock (name, amount, price) VALUES ('%s', %d, %f)"
	for i in range(n): #Inserer chaque item
		insert_query = insert_stock % (names[i], numbers[i], prices[i])
		c.execute(insert_query)
		create_report(c, names[i], numbers[i])

	conn.commit()
	conn.close()




#Fonction pour ajouter du stock
#Input:
#	c - la connection sqlite
#Output:
#	aucun
def add_stock(c):

	#Inseration de donnees pour la table stock
	insert_stock = "INSERT INTO stock (name, amount, price) VALUES ('%s', %d, %f)"
	update_stock = "UPDATE stock SET amount = %d WHERE name = '%s'"

	#L'utilisateur entre l'information pour les items a ajouter
	while True:
		#L'utilisateur entre le nom de l'item
		name = input("Entrez le nom de l'item (Entrez rien pour arreter): ")
		if name == "":
			return

		#L'utilisateur entre le nombre d'item 
		number = int(input("Entrez le montant a inserer: "))

		#Ajoute du stock si l'item exist deja
		if stock_item_exists(c, name):
			#Retrouver le nombre de stock qui exist deja
			fetch_amount = "SELECT amount FROM stock WHERE name = '%s'" % name
			c.execute(fetch_amount)
			current_num = c.fetchall()[0][0]

			#Trouver le nombre finale de stock
			new_num = current_num + number

			#Inserer le nouveau montant de stock
			update_string = update_stock % (new_num, name)
			c.execute(update_string)
			create_report(c, name, number)
		else:
			#L'utilisateur entre le prix de chaque item
			price = float(input("Entrez le prix par item: "))
			insert_string = insert_stock % (name, number, price)
			c.execute(insert_string)
			create_report(c, name, number)

		


#Fonction qui montre tous les options de l'utilisateur
#Input:
#	aucun
#Output:
#	aucun
def print_main_menu():	
	print("Veuillez selectionner une des options suivantes")
	print("=================================================")
	print("\t[1] Voir les items en stock.")
	print("\t[2] Voir les items pas en stock.")
	print("\t[3] Voir tous les items.")
	print("\t[4] Ajouter de l'inventaire.")
	print("\t[5] Placer une commande.")
	print("\t[0] Arreter.")
	print("=================================================\n")




#Fonction qui montre les items qui sont en stock
#Input:
#	c - La connection SQLite
#	mode - Un string qui specifie les donnees a montrer
#		(soit "en stock", "pas en stock", ou "" pour tous les items)
#Output:
#	aucun
def list_inventory(c, mode):
	
	#Creating de la commande SQL
	query_string = "SELECT name, price, amount FROM stock"
	if mode == "en stock":
		query_string += " WHERE amount > 0"
	elif mode == "pas en stock":
		query_string += " WHERE amount = 0"

	#Retrouver les ranges
	c.execute(query_string)
	data = c.fetchall()

	#Montrer les donnees
	print("Voici les items %s:" % mode)
	for i in range(len(data)):
		print("\t%-12s\t$%-12.2f\t(x%d)\n" % (data[i][0], data[i][1], data[i][2]))




#Fonction pour placer une commande
#Input:
#	c - La connection SQLite
#Output:
#	aucun
def place_order(c):
	#Montrer les items en stock
	list_inventory(c, "en stock")

	#Determiner l'item a acheter
	all_names = get_all(c, "names")
	name = input("Entrez le nom de l'item que vous voullez acheter: ")
	while not name in all_names:
		print("Cet item n'est pas une option.")
		name = input("Entrez le nom de l'item que vous voullez acheter: ")

	#Determiner le nombre de cet item en stock ainsi que le prix
	query_string = "SELECT amount, price FROM stock WHERE name = '%s'" % name
	c.execute(query_string)
	data = c.fetchall()
	amount = data[0][0]
	price = data[0][1]

	#Determiner le nombre pour la commande
	n = int(input("Entrez le nombre d'item que vous voulez acheter: "))
	while (n <= 0 or n > amount):
		print("Ce nombre d'items n'est pas possible.")
		n = int(input("Entrez le nombre d'item que vous voulez acheter: "))

	#Determiner le prix pour la commande
	total_cost = price*n
	payment = float(input("Le prix de la commande est $%.2f. (Entrez 0 pour annuler)\nEntrez votre paiment: " % total_cost))
	while (payment < total_cost and payment != 0):
		print("Ce n'est pas assez d'argent.")
		payment = float(input("Le prix de la commande est $%.2f. (Entrez 0 pour annuler)\nEntrez votre paiment: " % total_cost))

	#Check si la commande est annule
	if payment == 0:
		print("Commande annule.")
		return

	#Calculer et montrer la monnaie
	change = payment - total_cost;
	print("Voici votre monnaie: $%.2f\nMerci!" % change)

	#Mis a jour de la base de donnees
	new_amount = amount - n
	update_string = "UPDATE stock SET amount = %d WHERE name = '%s'"
	c.execute(update_string % (new_amount, name))
	create_report(c, name, -1*n)




def get_all(c, mode):
	#Commande SQL
	query_string = "SELECT %s FROM stock"

	#Determiner ce qu'on cherche
	if mode == "names":
		c.execute(query_string % "name")
	elif mode == "amounts":
		c.execute(query_string % "amount")
	elif mode == "prices":
		c.execute(query_string % "price")

	#Creer une list des donnees trouves
	result = c.fetchall()
	data = []
	for i in range(len(result)):
		data.append(result[i][0])

	return data




def create_report(c, name, amount):
	time = datetime.datetime.now()
	c.execute("SELECT price FROM stock WHERE name = '%s'" % name)
	price = c.fetchall()
	price = price[0][0]
	insert_str = "INSERT INTO report (name, amount, price, date) VALUES ('%s', %d, %f, '%s')"
	insert_str = insert_str % (name, amount, price, time)
	c.execute(insert_str)





if __name__ == '__main__':
	#Creer le fichier pour utiliser
	db_path = "C:\\Users\\Owner\\Documents\\GitHub"
	db_file = db_path + "\\distributrice.db"

	#Initialisation de la base de donnees
	initialize_db(db_file)

	#Creation de la connection
	conn = sqlite3.connect(db_file)
	c = conn.cursor()

	
	stop = False
	while not stop:
		#Montrer le menu principal
		print_main_menu()
		option = int(input(">"))

		#Determine l'option choisi
		if option == 0:
			stop = True
		elif option == 1:
			list_inventory(c, "en stock")
		elif option == 2:
			list_inventory(c, "pas en stock")
		elif option == 3:
			list_inventory(c, "")
		elif option == 4:
			add_stock(c)
		elif option == 5:
			place_order(c)
		else:
			print("Cet option n'est pas valide.\n")



	#Fermeture de la connection
	conn.commit()
	conn.close()


#On veut 1) La date 2 Le nom de l'item 3) Le montant de changement (+/-) 4) Le prix de l'item dans le temps de l'achat
	#Creer la table 'stock'

# distributrice.py
# Description:	La script primaire (python) pour la distributrice

import sqlite3
import os.path




#Fonction qui check si un item a deja une entree dans la base de donnees
#Input:
#	c - la connection sqlite
#	item_name - le nom de l'item qu'on veut verifier
#Output:
#	exists - Vrai si l'item existait deja
def stock_item_exists(c, item_name):

	#Retrouver tous les noms d'items
	c.execute("SELECT name FROM stock")
	names = c.fetchall()
	num_names = len(names)

	exists = False

	#Verifier chaque nom
	for i in range(num_names):
		current_name = names[i][0]		
		if current_name == item_name:
			exists = True

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
	create_stock = """
		CREATE TABLE stock(
		id integer PRIMARY KEY,
		name text NOT NULL UNIQUE,
		amount integer NOT NULL,
		price REAL NOT NULL);"""
	c.execute(create_stock)


	#Inserer les donnes initiales
	insert_stock = "INSERT INTO stock (name, amount, price) VALUES ('%s', %d, %f)"
	for i in range(n): #Inserer chaque item
		insert_query = insert_stock % (names[i], numbers[i], prices[i])
		c.execute(insert_query)

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
		else:
			#L'utilisateur entre le prix de chaque item
			price = float(input("Entrez le prix par item: "))
			insert_string = insert_stock % (name, number, price)
			c.execute(insert_string)

		


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
		else:
			print("Cet option n'est pas valide.\n")

	#Fermeture de la connection
	conn.commit()
	conn.close()

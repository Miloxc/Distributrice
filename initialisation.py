# initialisation.py
# Description: Initialisation de la base de données. Le programme qu'on appel si une 
#		base de données n'existe pas encore. (On donne l'option de ré-initialiser si non).
#		L'utilisateur entre les items initiales et leur informations, ceux-ci sont sauvé
#		dans un fichier appelé distributrices.db

import sqlite3
import os.path

def initialize_db(path):
	db_file = path + "\\distributrice.db"


	#Verifier si la base de donnees exist deja
	if os.path.isfile(db_file):
		#Demande si on veut re-initialiser
		print("Le fichier exist deja, aimeriez vous re-initialiser la base de donnees?")
		re_initialize = int(input("1 pour oui, 0 pour non: "))
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
		name text NOT NULL,
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

if __name__ == '__main__':
	initialize_db("C:\\Users\\Owner\\Documents\\GitHub")


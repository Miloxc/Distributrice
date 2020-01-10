/*
Ce programme simule une machine distributrice ou tout est gratuit et le stock est infini

Ce programme prend son inventaire d'un fichier "Inventaire.txt" (maximum de 10 choses en inventaire en même temps)
Il préserve toutes les transactions faites dans le fichier "Rapport_Transaction.txt"

Comme la vitrine d'une machine distributrice, l'usager peut voir l'inventaire (et le numéro associé) puisqu'il est imprimer dans le terminal
L'usager selecitonne ce qu'il veut
Pour sortir du mode ou la machine s'attend à une transaction écrire : DONE

Note : il est vrm long de faire graphique directement en c++, si on veut faire graphique, mieux d'importer les données dans excel
*/

#include <iostream>
#include <time.h>
#include <string>
#include <fstream>
using namespace std;

struct un_Item//on pourrait possiblement ajouté l'information de profit margin ici
{
	string Nom;
	float unPrix;
};

struct une_transaction
{
	time_t temps;
	int NbrdeItem;
};

void LectureFichierInventaireDansMachine(int &NbrItem, un_Item Item[])
{
	string nomFichierDonnees = "Inventaire.txt";

	//code demandant à l'usager de quel fichier il faut faire la lecture
	/*cout << "Nom du fichier de donnees : ";
	cin >> nomFichierDonnees;
	*/

	ifstream donnees;
	donnees.open(nomFichierDonnees, ios::in);

	donnees >> NbrItem;

	//assume qu'il n'y a pas d'erreur dans le fichier d'entrée de données pour l'inventaire
	string NomProduit;
	float prix;

	for (int identifiant = 0; identifiant < NbrItem; identifiant++)
	{
		donnees >> NomProduit;
		Item[identifiant].Nom = NomProduit;
		donnees >> prix;
		Item[identifiant].unPrix = prix;
	}

	donnees.close();

}

//imprime dans le terminal
void ImprimerInventaire(const int NbrItem, un_Item Item[])
{
	for (int k = 0; k < NbrItem; k++)
	{
		cout << k << "\t" << Item[k].Nom << "\t" << Item[k].unPrix << endl;
	}
}
void ImprimerTransaction(int Nbr_Transaction_a_Imprimer, une_transaction Transaction[]) //faudrais faire la verif que Nbr_Transaction_a_Imprimer ne dépasse pas le montatn d'espace dans le tableau
{
	ofstream sortieTransa; // sortie est un conduit vers un fichier.

	string nomFichierSortie = "Rapport_Transaction.txt";

	//prompt l'usager pour ou imprimer les transactions
	/*cout << "Nom du fichier de sortie : ";
	cin >> nomFichierSortie;
	*/
	sortieTransa.open(nomFichierSortie, ios::app);


	for (int k = 0; k < Nbr_Transaction_a_Imprimer; k++)
	{
		sortieTransa << Transaction[k].NbrdeItem << "\t" << Transaction[k].temps << endl;
	}
}

void EnregistrerTransaction(int &K, int ItemDansTransaction, une_transaction Transaction[])
{
	Transaction[K].NbrdeItem = ItemDansTransaction;
	Transaction[K].temps = time(NULL);
	K++;
}
void MachinePreteTransac(int &numbTransaction, une_transaction Transaction[])
{
	cout << "rentrer l'item que vous voulez (doit etre un chiffre de 0 a 3), ecrire DONE quand termine: "; //pourrait coder la verification qeu c'est bien un chiffre qui a été rentrer
	string donnee_entree;
	while (donnee_entree != "DONE")
	{
		cin >> donnee_entree;
		if (donnee_entree == "1" || donnee_entree == "2" || donnee_entree == "3" || donnee_entree == "0")
		{
			int donnee = stoi(donnee_entree); //conversion a un nombre
			EnregistrerTransaction(numbTransaction, donnee, Transaction);
		}
	}

}

int main()
{
	const int grandeurTableau = 10; //Il faut écrire la grandeur du tableau (pas besoin d'être juste) dans le programme sinon doit utiliser pointeurs
	un_Item Item[grandeurTableau]; //cree l'espace de stockage pour les données des 4 items
	int NbrItem;

	LectureFichierInventaireDansMachine(NbrItem,Item);

	ImprimerInventaire(NbrItem, Item);


	const int NbrTransaction = 100; //mettre safe garde si dépasse (base de donnée s'occupe de ça)
	une_transaction Transaction[NbrTransaction]; //cree l'espace de stockage pour les données enregistrant les transactions
	int numbTransaction = 0;
	MachinePreteTransac(numbTransaction, Transaction);
												 
	ImprimerTransaction(numbTransaction, Transaction);
	
}

/*
Du testing 

	

	int numbTransaction = 0;
	EnregistrerTransaction(numbTransaction, 1, Transaction);
	EnregistrerTransaction(numbTransaction, 3, Transaction);

	ImprimerTransaction(2, Transaction);

*/


/*void definition_de_Base_des_4_items(un_Item Item[])
{
	Item[0].Nom = "Chocolat Bar";
	Item[0].unPrix = 0.75;

	Item[1].Nom = "Chips";
	Item[1].unPrix = 1.00;

	Item[2].Nom = "Pop";
	Item[2].unPrix = 1.25;

	Item[3].Nom = "Candy";
	Item[3].unPrix = 0.75;
}*/



//maniere plus interessante de presenter le temps

/*
int prompt_Nbr_item()
{
	int NbrItem;
	cout << "combien y a-t-il d'items : ";
	cin >> NbrItem;
	return NbrItem;
}

void cree_inventaire()
{
	const int NbrItem = prompt_Nbr_item(); //Apres cette fonction, NbrItem à la valeur voulu par l'utilisateur
	probleme avec le fait que la fonction peut être appeler plusieurs fois et donc la valeur pourrait ne plus devenir constante

	un_Item T[NbrItem];
}
*/

from model import tournoi
from model import tours
from rich import print
from datetime import datetime

"""
1 : demarrer un tournoi
    # - Création d'un tournoi
    #     - Nom
    #     - Lieu
    #     ...
    # - inscrire joueurs
    - Déroulement du 1er tour
        - génerer 1ères paires
        - inscrire résultats
    - Déroulement 2e tour
        - génerer paires
            - Liste des joueurs triés par points
            - Joueur n'ayant jamais rencontré son adversaire
        - inscrire résultats
    ...
    - Génerer un rapport de tournoi avec toutes les infos possibles
    - Choix Génerer un rapport VS retour menu principal

2 : afficher un rapport
    liste de tous les joueurs par ordre alphabétique ;
    liste de tous les tournois ;
    nom et dates d’un tournoi donné ;
    liste des joueurs du tournoi par ordre alphabétique ;
    liste de tous les tours du tournoi et de tous les matchs du tour

3 : gestion utilisateurs
    - Modifier informations
    - Créer un nouvel utilisateur
    - Supprimer un joueur
    - Afficher utilisateurs


https://rich.readthedocs.io/en/stable/introduction.html
https://rich.readthedocs.io/en/stable/tables.html
"""


def create_tournament_view():
    tournament_inputs = {
        'name': input("Quel est le nom du tournoi ?\n"),
        'location': input("Où se déroule le tournoi ?\n"),
        'start_date': datetime.now().strftime("%d/%m/%Y, %H:%M"),
        'end_date': datetime.now().strftime("%d/%m/%Y, %H:%M"),
        'description': input("Ajoutez une description pour ce tournoi (facultatif)\n"),
        'round_number': get_round_number()
    }
    return tournament_inputs


def afficher_rapport():
    pass


def gerer_utilisateurs():
    pass


def read_menu_selection():
    main_menu = int(input("\nQue souhaitez-vous faire ? \n\n1 : Démarrer un tournoi\n2 : Afficher un rapport\n3 : Gerer des utilisateurs\n"))
    return main_menu


def get_round_number():
    while True:
        try:
            return int(input("Combien de tours pour votre tournoi ? "))
        except ValueError:
            print("Merci de saisir un nombre entier.")

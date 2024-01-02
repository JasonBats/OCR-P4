from rich import print
from datetime import datetime

from model import tournoi
from model.player import Player

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
        'start_date': datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),  # Meilleures start_date et end_date
        'end_date': datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
        'description': input("Ajoutez une description pour ce tournoi (facultatif)\n"),
        'round_number': get_round_number()  # Fonction pour verifier le nombre de tours
    }
    return tournament_inputs


def show_report_view():
    show_report_inputs = int(input("Quel rapport souhaitez-vous afficher ? \n"
                                   "\n1 : Liste de tous les joueurs"
                                   "\n2 : Liste de tous les tournois"
                                   "\n3 : Détails d'un tournoi"
                                   "\n4 : Liste des joueurs d'un tournoi"
                                   "\n5 : Liste de tous les tours d'un tournoi"))
    return show_report_inputs


def gerer_utilisateurs():
    pass


def read_menu_selection():
    main_menu = int(input("\nQue souhaitez-vous faire ? \n"
                          "\n1 : Démarrer un tournoi"
                          "\n2 : Afficher un rapport"
                          "\n3 : Gerer des utilisateurs\n"))
    return main_menu


def get_round_number():
    while True:
        try:
            return int(input("Combien de tours pour votre tournoi ? "))
        except ValueError:
            print("Merci de saisir un nombre entier.")


def write_score(player):
    try:
        score = input(f"Quel score pour {player} ?")
        return score
    except ValueError:
        print("Merci de saisir un nombre")


def score_review(player_1, player_2, score_1, score_2):
    verif = int(input(f"Le score est bien {player_1} {score_1}"
                      f"VS {player_2} {score_2} ? 1 = OUI / 2 = NON"))
    return verif


def add_player():
    add = int(input("Ajouter un joueur ? 1 = OUI / 0 = NON"))
    return add


def build_player():
    new_player = Player(
                nom=input("Quel est le nom du joueur ?"),
                prenom=input("Quel est son prénom ?"),
                date_naissance=input("Quelle est sa date de naissance ?"))
    return new_player


def chose_tournament_to_show():
    tournament_list = tournoi.tournament_list
    for index, tournament in enumerate(tournament_list):
        print(f"{index} - {tournament.name}")
    chosen_tournament = int(input(f"De quel tournoi souhaitez-vous voir le détail ?"))
    return chosen_tournament

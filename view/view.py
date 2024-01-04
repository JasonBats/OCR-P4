from rich import print
from datetime import datetime
from model import tournoi
from model.player import Player
import os
import json

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
                                   "\n5 : Liste de tous les tours d'un tournoi\n"))
    return show_report_inputs


def edit_player_informations(player):
    for key in player.keys():
        new_value = input(f"{key} [{player[key]}] :")
        if new_value:
            player[key] = new_value
    return player


def show_all_players():
    player_base = open_players_database()
    print("Liste de tous les joueurs :")
    for index, player in enumerate(player_base):
        player_instance = Player(player["nom"], player["prenom"], player["date_naissance"])
        print(f"{index} - {player_instance}")


def open_players_database():
    database_path = os.path.join(os.path.dirname(__file__), os.pardir, 'model', 'players_database.json')

    with open(database_path, "r", encoding="utf-8") as file:
        player_base = json.load(file)
    return player_base


def save_player_database(player_base):
    database_path = os.path.join(os.path.dirname(__file__), os.pardir, 'model', 'players_database.json')
    with open(database_path, 'w', encoding="utf-8") as file:
        json.dump(player_base, file, ensure_ascii=False, indent=2)


def manage_players():
    player_base = open_players_database()
    manage_players_menu = int(input("Que souhaitez-vous faire ? \n"
                                    "\n1 : Modifier un joueur"
                                    "\n2 : Ajouter un joueur"
                                    "\n3 : Supprimer un joueur"
                                    "\n4 : Afficher la liste des joueurs\n"))
    if manage_players_menu == 1:
        show_all_players()
        chosen_player = int(input("Quel joueur souhaitez-vous modifier ?"))
        edit_player_informations(player_base[chosen_player])
        save_player_database(player_base)
        print(f"Modifications apportées à {player_base[chosen_player]}")
    elif manage_players_menu == 2:
        new_player = build_player()
        player_base.append(new_player.to_dict())
        print(f"\n[{new_player}] ajouté à la base de données des joueurs.")
        save_player_database(player_base)
    elif manage_players_menu == 3:
        show_all_players()
        chosen_player = int(input("Quel joueur souhaitez-vous supprimer ?"))
        print(f"{player_base[chosen_player]} supprimé")
        del player_base[chosen_player]
        save_player_database(player_base)
    elif manage_players_menu == 4:
        show_all_players()


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


def show_tournament_name_dates():
    print("Liste des tournois existants :")
    for index, tournament in enumerate(tournoi.tournament_list):
        print(f"{index} - {tournament.name}")
    chosen_tournament = int(input(f"De quel tournoi souhaitez-vous voir le détail ?"))
    print(f"Tournoi {tournoi.tournament_list[chosen_tournament].name} du "
          f"{tournoi.tournament_list[chosen_tournament].start_date} au "
          f"{tournoi.tournament_list[chosen_tournament].end_date}")
    return chosen_tournament


def show_tournament_participants():
    print("Liste des tournois existants :")
    for index, tournament in enumerate(tournoi.tournament_list):
        print(f"{index} - {tournament.name}")
    chosen_tournament = int(input(f"De quel tournoi souhaitez-vous voir le détail ?"))
    print(f"Tournoi {tournoi.tournament_list[chosen_tournament].list_participants}")
    return chosen_tournament


def show_tournament_rounds():
    for index, tournament in enumerate(tournoi.tournament_list):
        print(f"{index} - {tournament.name}")
    chosen_tournament = int(input(f"De quel tournoi souhaitez-vous voir le détail ?"))
    print(f"Tournoi {tournoi.tournament_list[chosen_tournament].round_list}")
    return chosen_tournament

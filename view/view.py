from rich import print
from rich.console import Console
from rich.table import Table
from datetime import datetime
from model.player import Player
import os
import json


class TournamentView:
    @staticmethod
    def create_tournament_view():
        tournament_inputs = {
            'name': input("Quel est le nom du tournoi ?\n"),
            'location': input("Où se déroule le tournoi ?\n"),
            'start_date': datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            'end_date': datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            'description': input("Ajoutez une description pour ce tournoi (facultatif)\n"),
            'round_number': TournamentView.get_round_number()  # Fonction pour verifier le nombre de tours
        }
        print("Tournoi créé !")
        return tournament_inputs

    @staticmethod
    def get_round_number():
        while True:
            try:
                return int(input("Combien de tours pour votre tournoi ?\n"))
            except ValueError:
                print("Merci de saisir un nombre entier.")

    @staticmethod
    def write_score(player):
        try:
            score = input(f"Quel score pour {player} ?\n")
            return score
        except ValueError:
            print("Merci de saisir un nombre")

    @staticmethod
    def score_review(player_1, player_2, score_1, score_2):
        try:
            verif = int(input(f"Le score est bien {player_1} {score_1}"
                              f"VS {player_2} {score_2} ? 1 = OUI / 2 = NON\n"))
            return verif
        except ValueError:
            print("Merci de saisir 1 pour OUI et 2 pour NON")

    @staticmethod
    def register_players():
        player_view = PlayerView()
        contenders = []
        number_of_contenders = int(input("Combien de participants à ce tournoi ?\n"))
        player_base = player_view.show_all_players()
        while len(contenders) < number_of_contenders:
            chosen_player = int(input("Quel joueur souhaitez-vous inscrire à ce tournoi ?\n"))
            player = Player(player_base[chosen_player]['nom'], player_base[chosen_player]['prenom'],
                            player_base[chosen_player]['date_naissance'])
            contenders.append(player)
            print(f"{player} inscrit au tournoi ! [{len(contenders)}/{number_of_contenders}]")
        os.system('cls')
        return contenders


class PlayerView:
    @staticmethod
    def show_all_players():
        functional = Functional()
        player_base = functional.open_players_database()
        console_view = ConsoleView("Liste de tous les joueurs :")
        player_list = []
        for index, player in enumerate(player_base):
            player_instance = Player(player["nom"], player["prenom"], player["date_naissance"])
            player_list.append(player_instance)
        console_view.display_player_list(player_list)
        return player_base

    def manage_players(self):
        functional = Functional()
        player_base = functional.open_players_database()
        manage_players_menu = int(input("Que souhaitez-vous faire ? \n"
                                        "\n1 : Modifier un joueur"
                                        "\n2 : Ajouter un joueur"
                                        "\n3 : Supprimer un joueur"
                                        "\n4 : Afficher la liste des joueurs\n"))
        if manage_players_menu == 1:
            self.show_all_players()
            chosen_player = int(input("Quel joueur souhaitez-vous modifier ?\n"))
            self.edit_player_informations(player_base[chosen_player])
            functional.save_player_database(player_base)
            print(f"Modifications apportées à {player_base[chosen_player]}")
        elif manage_players_menu == 2:
            new_player = self.build_player()
            player_base.append(new_player.to_dict())
            print(f"\n[{new_player}] ajouté à la base de données des joueurs.")
            functional.save_player_database(player_base)
        elif manage_players_menu == 3:
            self.show_all_players()
            chosen_player = int(input("Quel joueur souhaitez-vous supprimer ?\n"))
            print(f"{player_base[chosen_player]} supprimé")
            del player_base[chosen_player]
            functional.save_player_database(player_base)
        elif manage_players_menu == 4:
            self.show_all_players()

    @staticmethod
    def edit_player_informations(player):
        for key in player.keys():
            new_value = input(f"{key} [{player[key]}] :\n")
            if new_value:
                player[key] = new_value
        return player

    @staticmethod
    def build_player():
        new_player = Player(
            nom=input("Quel est le nom du joueur ?\n"),
            prenom=input("Quel est son prénom ?\n"),
            date_naissance=input("Quelle est sa date de naissance ? (AAAA-MM-JJ)\n"))
        return new_player


class TournamentReports:
    @staticmethod
    def show_report_view():
        show_report_inputs = int(input("Quel rapport souhaitez-vous afficher ? \n"
                                       "\n1 : Liste de tous les joueurs"
                                       "\n2 : Liste de tous les tournois"
                                       "\n3 : Détails d'un tournoi"
                                       "\n4 : Liste des joueurs d'un tournoi"
                                       "\n5 : Liste de tous les tours d'un tournoi\n"))
        return show_report_inputs

    @staticmethod
    def show_tournament_name_dates():
        print("Liste des tournois existants :")
        functional = Functional()
        console_view = ConsoleView("Détails d'un tournoi :")
        database = functional.open_database()
        console_view.display_tournament_name_dates(database)
        chosen_tournament = input(f"De quel tournoi souhaitez-vous voir les détails ?\n")
        tournament_name = database['Tournaments'][chosen_tournament]['Tournament name']
        tournament_start_date = database['Tournaments'][chosen_tournament]['Start Date']
        tournament_end_date = database['Tournaments'][chosen_tournament]['End Date']
        print(f"Tournoi '{tournament_name}'. S'est déroulé du {tournament_start_date} au {tournament_end_date}")
        return chosen_tournament

    @staticmethod
    def show_tournament_list():
        functional = Functional()
        database = functional.open_database()
        console_view = ConsoleView("Liste de tous les tournois")
        console_view.display_tournament_name_dates(database)

    @staticmethod
    def show_tournament_participants():
        functional = Functional()
        database = functional.open_database()
        participants = []
        console_view = ConsoleView("Liste des tournois existants :")
        console_view.display_tournament_name_dates(database)
        chosen_tournament = input(f"De quel tournoi souhaitez-vous voir les participants ?\n")
        for index, participant in enumerate(database['Tournaments'][chosen_tournament]['Contenders list']):
            participant_name = database['Tournaments'][chosen_tournament]['Contenders list'][index]['nom']
            participant_first_name = database['Tournaments'][chosen_tournament]['Contenders list'][index]['prenom']
            participant_birthdate = database['Tournaments'][chosen_tournament]['Contenders list'][index][
                'date_naissance']
            participant = Player(participant_name, participant_first_name, participant_birthdate)
            participants.append(participant)
        participants_alphabetical = sorted(participants, key=lambda player_sorted: (player_sorted.nom,
                                                                                    player_sorted.prenom))
        console_view.display_player_list(participants_alphabetical)
        return chosen_tournament

    @staticmethod
    def show_tournament_rounds():
        functional = Functional()
        database = functional.open_database()
        console_view = ConsoleView("Liste des tournois existants :")
        console_view.display_tournament_name_dates(database)
        chosen_tournament = input(f"De quel tournoi souhaitez-vous voir les matchs de chaque tour ?\n")
        console_view.display_tournament_details(database, chosen_tournament)
        return chosen_tournament


class PlayerReports:
    @staticmethod
    def sort_all_players_alphabetical():
        functional = Functional()
        player_base = functional.open_players_database()
        all_players = []
        for index, player in enumerate(player_base):
            player_instance = Player(player["nom"], player["prenom"], player["date_naissance"])
            all_players.append(player_instance)
        sorted_player_base = sorted(all_players, key=lambda player_sorted: (player_sorted.nom, player_sorted.prenom))
        return sorted_player_base


class Functional:
    @staticmethod
    def open_players_database():
        database_path = os.path.join(os.path.dirname(__file__), os.pardir, 'model', 'players_database.json')
        with open(database_path, "r", encoding="utf-8") as file:
            player_base = json.load(file)
        return player_base

    @staticmethod
    def save_player_database(player_base):
        database_path = os.path.join(os.path.dirname(__file__), os.pardir, 'model', 'players_database.json')
        with open(database_path, 'w', encoding="utf-8") as file:
            json.dump(player_base, file, ensure_ascii=False, indent=2)

    @staticmethod
    def open_database():
        database_path = os.path.join(os.path.dirname(__file__), os.pardir, 'model', 'database.json')

        with open(database_path, "r", encoding="utf-8") as file:
            database = json.load(file)
        return database


class MainView:
    @staticmethod
    def read_menu_selection():
        main_menu = int(input("\nQue souhaitez-vous faire ? \n"
                              "\n1 : Démarrer un tournoi"
                              "\n2 : Afficher un rapport"
                              "\n3 : Gerer des utilisateurs\n"))
        return main_menu


class ConsoleView:
    def __init__(self, table_title):
        self.table = Table(title=table_title)
        self.console = Console()
        self.database = []

    def display_player_list(self, database):
        self.table = Table()
        self.table.add_column("Index")
        self.table.add_column("Nom")
        self.table.add_column("Prenom")
        self.database = database
        for index, player in enumerate(database):
            self.table.add_row(str(index), player.nom, player.prenom)
        self.console.print(self.table)

    def display_tournament_name_dates(self, database):
        self.table.add_column("Index")
        self.table.add_column("Nom du tournoi")
        for tournament_id in database['Tournaments']:
            self.table.add_row(tournament_id, database['Tournaments'][tournament_id]['Tournament name'])
        self.console.print(self.table)

    def display_tournament_details(self, database, chosen_tournament):
        self.table = Table()
        self.table.add_column("Tour n°")
        self.table.add_column("Liste des matchs")
        for index, tournament_round in enumerate(database['Tournaments'][chosen_tournament]['Round list']):
            self.table.add_section()
            round_number = database['Tournaments'][chosen_tournament]['Round list'][index]['Tour n°']
            round_match_list = database['Tournaments'][chosen_tournament]['Round list'][index]['Match List']
            for match in round_match_list:
                self.table.add_row(str(round_number), str(match))
        self.console.print(self.table)

    def display_ranking(self, ranking):
        self.table = Table()
        self.table.add_column("Joueur")
        self.table.add_column("Score")
        for player, score in ranking:
            self.table.add_row(str(player), str(score))
        self.console.print(self.table)

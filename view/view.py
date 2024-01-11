from rich import print
from datetime import datetime
from model.player import Player
import os
import json


class TournamentView:
    def create_tournament_view(self):
        tournament_inputs = {
            'name': input("Quel est le nom du tournoi ?\n"),
            'location': input("Où se déroule le tournoi ?\n"),
            'start_date': datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            'end_date': datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            'description': input("Ajoutez une description pour ce tournoi (facultatif)\n"),
            'round_number': self.get_round_number()  # Fonction pour verifier le nombre de tours
        }
        return tournament_inputs

    def get_round_number(self):
        while True:
            try:
                return int(input("Combien de tours pour votre tournoi ?\n"))
            except ValueError:
                print("Merci de saisir un nombre entier.")

    def write_score(self, player):
        try:
            score = input(f"Quel score pour {player} ?\n")
            return score
        except ValueError:
            print("Merci de saisir un nombre")

    def score_review(self, player_1, player_2, score_1, score_2):
        verif = int(input(f"Le score est bien {player_1} {score_1}"
                          f"VS {player_2} {score_2} ? 1 = OUI / 2 = NON\n"))
        return verif

    def register_players(self):
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
        print(contenders)
        return contenders

class PlayerView:
    def show_all_players(self):
        functional = Functional()
        player_base = functional.open_players_database()
        print("Liste de tous les joueurs :")
        for index, player in enumerate(player_base):
            player_instance = Player(player["nom"], player["prenom"], player["date_naissance"])
            print(f"{index}. {player_instance}")
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

    def edit_player_informations(self, player):
        for key in player.keys():
            new_value = input(f"{key} [{player[key]}] :\n")
            if new_value:
                player[key] = new_value
        return player

    def add_player(self):
        add = int(input("Ajouter un joueur ? 1 = OUI / 0 = NON\n"))
        return add

    def build_player(self):
        new_player = Player(
            nom=input("Quel est le nom du joueur ?\n"),
            prenom=input("Quel est son prénom ?\n"),
            date_naissance=input("Quelle est sa date de naissance ? (AAAA-MM-JJ)\n"))
        return new_player


class TournamentReports:
    def show_report_view(self):
        show_report_inputs = int(input("Quel rapport souhaitez-vous afficher ? \n"
                                       "\n1 : Liste de tous les joueurs"
                                       "\n2 : Liste de tous les tournois"
                                       "\n3 : Détails d'un tournoi"
                                       "\n4 : Liste des joueurs d'un tournoi"
                                       "\n5 : Liste de tous les tours d'un tournoi\n"))
        return show_report_inputs
    def show_tournament_name_dates(self):
        print("Liste des tournois existants :")
        functional = Functional()
        database = functional.open_database()
        for tournament_id in database['Tournaments']:
            tournament_name = database['Tournaments'][tournament_id]['Tournament name']
            print(f"{tournament_id} - {tournament_name}")
        chosen_tournament = input(f"De quel tournoi souhaitez-vous voir les détails ?\n")
        tournament_name = database['Tournaments'][chosen_tournament]['Tournament name']
        tournament_start_date = database['Tournaments'][chosen_tournament]['Start Date']
        tournament_end_date = database['Tournaments'][chosen_tournament]['End Date']
        print(f"Tournoi '{tournament_name}'. S'est déroulé du {tournament_start_date} au {tournament_end_date}")
        return chosen_tournament

    def show_tournament_list(self):
        functional = Functional()
        database = functional.open_database()
        for tournament_id in database['Tournaments']:
            tournament_name = database['Tournaments'][tournament_id]['Tournament name']
            print(f"{tournament_id} - {tournament_name}")

    def show_tournament_participants(self):
        print("Liste des tournois existants :")
        functional = Functional()
        database = functional.open_database()
        participants = []
        for tournament_id in database['Tournaments']:
            tournament_name = database['Tournaments'][tournament_id]['Tournament name']
            print(f"{tournament_id} - {tournament_name}")
        chosen_tournament = input(f"De quel tournoi souhaitez-vous voir les participants ?\n")
        for index, participant in enumerate(database['Tournaments'][chosen_tournament]['Contenders list']):
            participant_name = database['Tournaments'][chosen_tournament]['Contenders list'][index]['nom']
            participant_first_name = database['Tournaments'][chosen_tournament]['Contenders list'][index]['prenom']
            participant_birthdate = database['Tournaments'][chosen_tournament]['Contenders list'][index][
                'date_naissance']
            participant = participant_name, participant_first_name, participant_birthdate
            participants.append(participant)
        participants_alphabetical = sorted(participants)
        for element in participants_alphabetical:
            print(element)
        return chosen_tournament

    def show_tournament_rounds(self):
        functional = Functional()
        database = functional.open_database()
        for tournament_id in database['Tournaments']:
            tournament_name = database['Tournaments'][tournament_id]['Tournament name']
            print(f"{tournament_id} - {tournament_name}")
        chosen_tournament = input(f"De quel tournoi souhaitez-vous voir les matchs de chaque tour ?\n")
        for index, tournament_round in enumerate(database['Tournaments'][chosen_tournament]['Round list']):
            round_number = database['Tournaments'][chosen_tournament]['Round list'][index]['Tour n°']
            round_start_date = database['Tournaments'][chosen_tournament]['Round list'][index]['Start Date']
            round_end_date = database['Tournaments'][chosen_tournament]['Round list'][index]['End Date']
            round_match_list = database['Tournaments'][chosen_tournament]['Round list'][index]['Match List']
            print(f"Tour n° {round_number} : Du {round_start_date} au {round_end_date}. \n"
                  f"Liste des matchs : {round_match_list}")
        return chosen_tournament


class PlayerReports:
    def show_all_players_alphabetical(self):
        functional = Functional()
        player_base = functional.open_players_database()
        print("Liste de tous les joueurs :")
        all_players = []
        for index, player in enumerate(player_base):
            player_instance = Player(player["nom"], player["prenom"], player["date_naissance"])
            all_players.append(player_instance)
        sorted_player_base = sorted(all_players, key=lambda player: (player.nom, player.prenom))
        print(sorted_player_base)


class Functional:
    def open_players_database(self):
        database_path = os.path.join(os.path.dirname(__file__), os.pardir, 'model', 'players_database.json')
        with open(database_path, "r", encoding="utf-8") as file:
            player_base = json.load(file)
        return player_base

    def save_player_database(self, player_base):
        database_path = os.path.join(os.path.dirname(__file__), os.pardir, 'model', 'players_database.json')
        with open(database_path, 'w', encoding="utf-8") as file:
            json.dump(player_base, file, ensure_ascii=False, indent=2)

    def open_database(self):
        database_path = os.path.join(os.path.dirname(__file__), os.pardir, 'model', 'database.json')

        with open(database_path, "r", encoding="utf-8") as file:
            database = json.load(file)
        return database


class MainView:
    def read_menu_selection(self):
        main_menu = int(input("\nQue souhaitez-vous faire ? \n"
                              "\n1 : Démarrer un tournoi"
                              "\n2 : Afficher un rapport"
                              "\n3 : Gerer des utilisateurs\n"))
        return main_menu

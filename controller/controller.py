from model import match, tournoi
from model.tours import Tour
from view import view
from model.tournoi import Tournoi
from model.player import Player
from model.match import Match
from rich import print
import json
import os
import random
from view.view import TournamentView
from datetime import datetime
from tinydb import TinyDB, Query


# TODO : Maincontroller doit gérer ce qui est propre au programme. clean MainController et TournamentController


class MainController:

    def __init__(self):
        self.tournament_controller = TournamentController()
        self.data_controller = DataController("Tournaments")

    def run_tournament(self):
        tournament_view = TournamentView()
        tournament_inputs = tournament_view.create_tournament_view()
        created_tournament = Tournoi(**tournament_inputs)
        tournoi.tournament_list.append(created_tournament)
        print("Tournoi créé !")
        self.tournament_controller.add_player()
        _, _, created_tournament.list_participants = self.tournament_controller.register_players()
        print(created_tournament)
        for i in range(1, int(created_tournament.round_number) + 1):
            self.tournament_controller.soft_shuffle_counter = 0
            start_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            tour_obj = Tour(i, start_date=start_date, end_date="", match_list=[])
            print("Tour n°:", i)
            created_tournament.current_round += 1
            if i == 1:
                pairs = self.tournament_controller.generate_first_pairs()
            else:
                pairs = self.tournament_controller.generate_pairs(created_tournament)
            print("Paires du tour", i, ":", pairs)
            for pair in pairs:
                match_obj = Match(*pair)
                match_obj.encounter()
                print(match_obj)
                tour_obj.match_list.append(match_obj)
                created_tournament.match_list.append(match_obj)
            tour_obj.end_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            created_tournament.round_list.append(tour_obj)
            print(tour_obj)
            print("ROUND LIST:::::::::", created_tournament.round_list)
        created_tournament.end_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.data_controller.data_save(created_tournament.to_dict())
        print(created_tournament)

        print("Générer un rapport :")
        print("retour au menu principal :")
        print("Saisissez le chiffre correspondant à votre choix.")

    def show_report(self):
        tournament_reports = view.TournamentReports()
        player_reports = view.PlayerReports()
        report_choice = tournament_reports.show_report_view()
        if report_choice == 1:
            player_reports.show_all_players_alphabetical()
        if report_choice == 2:
            tournament_reports.show_tournament_list()
        if report_choice == 3:
            tournament_reports.show_tournament_name_dates()
        if report_choice == 4:
            tournament_reports.show_tournament_participants()
        if report_choice == 5:
            print("Liste de tous les tours du tournoi et de tous les matchs du tour")
            tournament_reports.show_tournament_rounds()

    def players_management(self):
        player_view = view.PlayerView()
        player_view.manage_players()

    menu_principal = {
        1: run_tournament,
        2: show_report,
        3: players_management
    }

    def run(self):
        main_view = view.MainView()
        while True:
            try:
                main_menu = main_view.read_menu_selection()
                if main_menu == 0:
                    break
                if main_menu in self.menu_principal:
                    self.menu_principal[main_menu](self)
                else:
                    print("Veuillez saisir le chiffre correspondant à votre choix.")
            except ValueError:
                print("Veuillez saisir un nombre entier")


class TournamentController:
    database_path = os.path.join(os.path.dirname(__file__), os.pardir, 'model', 'players_database.json')

    with open(database_path, "r", encoding='utf-8') as file:
        players_data = json.load(file)

    all_contenders = [Player(joueur["nom"], joueur["prenom"], joueur["date_naissance"]) for joueur in players_data]

    def __init__(self):
        self.tour_obj = None

    def add_player(self):
        player_view = view.PlayerView()
        add = player_view.add_player()
        while add:
            new_player = player_view.build_player()
            try:
                with open(self.database_path, "r", encoding="utf-8") as file:
                    player_base = json.load(file)
            except FileNotFoundError:
                player_base = []

            player_base.append(new_player.to_dict())
            print("Liste de tous les joueurs :", player_base)
            print(new_player)

            with open(self.database_path, "w", encoding="utf-8") as file:
                json.dump(player_base, file, default=lambda obj: new_player.__json__(), ensure_ascii=False, indent=2)

            print(new_player, " : Joueur inscrit avec succès")
            add = player_view.add_player()  # TODO : Vraie inscription

    def register_players(self):
        self.list_participants = random.sample(self.all_contenders, 6)
        self.initial_list = []
        print("Liste des participants au tournoi :", self.list_participants)
        self.left_opponents_by_player = {}
        for index, element in enumerate(self.list_participants):
            self.initial_list.append(element)
            self.list_participants_copy = self.list_participants.copy()
            self.list_participants_copy.pop(index)
            self.left_opponents_by_player[element] = self.list_participants_copy
        return self.left_opponents_by_player, self.list_participants, self.initial_list

    def generate_first_pairs(self):
        generated_pairs = []

        # TODO créer une liste plus intelligente (possibilité de sélectionner 6 joueurs)
        def pop_random(liste_participants):
            id_random = random.randrange(0, len(liste_participants))
            return liste_participants.pop(id_random)

        while self.list_participants:
            player_1 = pop_random(self.list_participants)
            player_2 = pop_random(self.list_participants)
            self.left_opponents_by_player[player_1].remove(player_2)
            self.left_opponents_by_player[player_2].remove(player_1)
            random_pair = (player_1, player_2)
            generated_pairs.append(random_pair)
        return generated_pairs

    def generate_pairs(self, tour_obj):
        current_ranking = self.ranking(tour_obj.match_list)
        ranked_players = [player for player, _ in current_ranking]
        next_pairs = []

        while ranked_players:
            while True:  # TODO : Essayer une autre manière en parallèlle
                index = 0
                player_1 = ranked_players.pop(index)
                try:
                    if ranked_players[index] in self.left_opponents_by_player[player_1]:
                        player_2 = ranked_players.pop(index)
                    else:
                        search_player = ranked_players[index]
                        while search_player not in self.left_opponents_by_player[player_1]:
                            index += 1
                            search_player = ranked_players[index]
                            if index >= len(ranked_players):
                                index = 0
                        player_2 = ranked_players.pop(index)
                    break
                except IndexError:
                    next_pairs = []
                    ranked_players = TournamentController.shuffle_players(self, tour_obj.match_list)
            pair = (player_1, player_2)
            next_pairs.append(pair)

        for pair in next_pairs:
            self.left_opponents_by_player[pair[0]].remove(pair[1])
            self.left_opponents_by_player[pair[1]].remove(pair[0])

        return next_pairs

    soft_shuffle_counter = 0

    def shuffle_players(self, tour_obj):
        while self.soft_shuffle_counter < 50:
            current_ranking = self.ranking(tour_obj)
            random.shuffle(current_ranking)
            sorted_ranking = sorted(current_ranking, key=lambda x: x[1], reverse=True)
            ranked_players = [player_name for player_name, player_score in sorted_ranking]
            print("Jouers mélangés ! Nouvelle liste :", ranked_players, self.soft_shuffle_counter)
            self.soft_shuffle_counter += 1
            return ranked_players  # TODO : Le soft_shuffle n'est jamais return
        if self.soft_shuffle_counter >= 50:
            current_ranking = self.ranking(tour_obj)
            random.shuffle(current_ranking)
            ranked_players = [player_name for player_name, player_score in current_ranking]
        print("Joueurs mélangés mais alors genre VRAIMENT !!", ranked_players)
        return ranked_players

    def ranking(self, match_list):
        print(match_list)
        previous_matches = match_list
        scores_list_dict = {}
        for num, outcome in enumerate(previous_matches):
            player_1 = outcome.player_1
            score_player_1 = float(outcome.score_1)
            player_2 = outcome.player_2
            score_player_2 = float(outcome.score_2)
            scores_list_dict.setdefault(player_1, 0)
            scores_list_dict[player_1] += score_player_1
            scores_list_dict.setdefault(player_2, 0)
            scores_list_dict[player_2] += score_player_2
        ranking = sorted(scores_list_dict.items(), key=lambda item: item[1], reverse=True)
        print("Liste des matchs :", match_list)
        print("Classement :", ranking)
        return ranking


class DataController:
    def __init__(self, dataname):
        self.database_path = os.path.join(os.path.dirname(__file__), os.pardir, 'model', 'database.json')
        self.database = TinyDB(self.database_path, indent=4, encoding='utf-8', ensure_ascii=False)
        self.database.default_table_name = dataname

    def data_save(self, datas):
        self.database.insert(datas)

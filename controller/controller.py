from model.player import Player
from model.tours import Round
from view import view
from model.tournoi import Tournoi
from model.match import Match
import os
import random
from view.view import TournamentView, ConsoleView
from datetime import datetime
from tinydb import TinyDB, Query
import json


class MainController:

    def __init__(self):
        self.tournament_controller = TournamentController()
        self.data_controller = DataController("Tournaments")

    def run_tournament(self):
        os.system('cls')
        tournament_view = TournamentView
        console_view = ConsoleView("Informations")
        tournament_inputs = tournament_view.create_tournament_view()
        created_tournament = Tournoi(**tournament_inputs)
        left_opponents_by_player, _, created_tournament.list_participants = (
            self.tournament_controller.players_registration())  # TODO : Pourquoi les deux vides ?
        created_tournament.left_opponents_by_player = left_opponents_by_player
        view.TournamentView.print_created_tournament(created_tournament)

        for i in range(1, int(created_tournament.round_number) + 1):
            self.run_round(created_tournament, i, console_view)

        created_tournament.end_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.data_controller.data_save(created_tournament.to_dict())  # Sauvegarde à la fin du tournoi
        view.TournamentView.print_created_tournament(created_tournament)

    def continue_tournament(self):
        console_view = ConsoleView("Informations")
        unfinished_tournament = self.data_controller.resume_tournament()

        for i in range(unfinished_tournament.current_round, int(unfinished_tournament.round_number)):
            self.run_round(unfinished_tournament, unfinished_tournament.current_round, console_view)

    def run_round(self, created_tournament, i, console_view):
        self.tournament_controller.soft_shuffle_counter = 0
        start_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        created_tournament.current_round += 1
        view.TournamentView.print_round_number(created_tournament.current_round)
        round_obj = Round(created_tournament.current_round, start_date=start_date, end_date="", match_list=[])
        if created_tournament.current_round == 1:
            pairs = self.tournament_controller.generate_first_pairs()
        else:
            pairs = self.tournament_controller.generate_pairs(created_tournament)
        view.TournamentView.print_current_round_pairs(created_tournament.current_round, pairs)
        for pair in pairs:
            match_obj = Match(*pair)
            match_obj.encounter()
            view.TournamentView.print_match_obj(match_obj)
            round_obj.match_list.append(match_obj)
            created_tournament.match_list.append(match_obj)
        round_obj.end_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        created_tournament.round_list.append(round_obj)
        os.system('cls')
        view.TournamentView.print_round_list(created_tournament.round_list)
        console_view.display_ranking(TournamentController.get_ranking(created_tournament.match_list))
        self.data_controller.data_save(created_tournament.to_dict())

    def show_report(self):
        tournament_reports = view.TournamentReports()
        report_choice = tournament_reports.show_report_view()
        player_reports = view.PlayerReports()
        console = view.ConsoleView("Liste des joueurs par ordre alphabétique :")
        if report_choice == 1:
            console.display_player_list(player_reports.sort_all_players_alphabetical())
        if report_choice == 2:
            tournament_reports.show_tournament_list()
        if report_choice == 3:
            tournament_reports.show_tournament_name_dates()
        if report_choice == 4:
            tournament_reports.show_tournament_participants()
        if report_choice == 5:
            tournament_reports.show_tournament_rounds()

    def players_management(self):
        player_view = view.PlayerView()
        player_view.manage_players()

    menu_principal = {
        1: run_tournament,
        2: continue_tournament,
        3: show_report,
        4: players_management
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
                    main_view.incorrect_menu_selection()
            except ValueError:
                main_view.menu_selection_value_error()


class TournamentController:
    def __init__(self):
        self.round_obj = None
        self.list_participants = []
        self.initial_list = []
        self.left_opponents_by_player = {}

    def players_registration(self):
        tournament_view = view.TournamentView()
        self.list_participants = tournament_view.register_players()
        self.initial_list = []
        for index, element in enumerate(self.list_participants):
            self.initial_list.append(element)
            list_participants_copy = self.list_participants.copy()
            list_participants_copy.pop(index)
            self.left_opponents_by_player[element] = list_participants_copy
        return self.left_opponents_by_player, self.list_participants, self.initial_list

    def generate_first_pairs(self):
        generated_pairs = []

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

    def generate_pairs(self, round_obj):
        self.left_opponents_by_player = round_obj.left_opponents_by_player
        current_ranking = self.get_ranking(round_obj.match_list)
        ranked_players = [player for player, _ in current_ranking]
        next_pairs = []

        while ranked_players:
            while True:
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
                    ranked_players = TournamentController.shuffle_players(self, round_obj.match_list)
            pair = (player_1, player_2)
            next_pairs.append(pair)

        for pair in next_pairs:
            self.left_opponents_by_player[pair[0]].remove(pair[1])
            self.left_opponents_by_player[pair[1]].remove(pair[0])

        return next_pairs

    soft_shuffle_counter = 0

    def shuffle_players(self, round_obj):
        ranked_players = []
        while self.soft_shuffle_counter < 50:
            current_ranking = self.get_ranking(round_obj)
            random.shuffle(current_ranking)
            sorted_ranking = sorted(current_ranking, key=lambda x: x[1], reverse=True)
            ranked_players = [player_name for player_name, player_score in sorted_ranking]
            view.TournamentView.print_shuffled_players(ranked_players)
            self.soft_shuffle_counter += 1
            return ranked_players
        if self.soft_shuffle_counter >= 50:
            current_ranking = self.get_ranking(round_obj)
            random.shuffle(current_ranking)
            ranked_players = [player_name for player_name, player_score in current_ranking]
            view.TournamentView.shuffled_players_view(ranked_players)
        return ranked_players

    @staticmethod
    def get_ranking(match_list):
        scores_list_dict = {}
        players_dict = {}

        for outcome in match_list:
            player_1_id = outcome.player_1['chess_id'] if not isinstance(outcome.player_1,
                                                                         Player) else outcome.player_1.chess_id
            if player_1_id not in players_dict:
                players_dict[player_1_id] = Player(**outcome.player_1) if not isinstance(outcome.player_1,
                                                                                         Player) else outcome.player_1
            player_1 = players_dict[player_1_id]

            player_2_id = outcome.player_2['chess_id'] if not isinstance(outcome.player_2,
                                                                         Player) else outcome.player_2.chess_id
            if player_2_id not in players_dict:
                players_dict[player_2_id] = Player(**outcome.player_2) if not isinstance(outcome.player_2,
                                                                                         Player) else outcome.player_2
            player_2 = players_dict[player_2_id]

            score_player_1 = float(outcome.score_1)
            score_player_2 = float(outcome.score_2)

            scores_list_dict.setdefault(player_1, 0)
            scores_list_dict[player_1] += score_player_1
            scores_list_dict.setdefault(player_2, 0)
            scores_list_dict[player_2] += score_player_2

        ranking = sorted(scores_list_dict.items(), key=lambda item: item[1], reverse=True)
        return ranking


class DataController:
    def __init__(self, dataname):
        self.database_path = os.path.join(os.path.dirname(__file__), os.pardir, 'model', 'database.json')
        self.database = TinyDB(self.database_path, indent=4, encoding='utf-8', ensure_ascii=False)
        self.database.default_table_name = dataname

    def data_save(self, datas):
        tournament_query = Query()
        search_result = self.database.search(tournament_query['Tournament ID'] == datas['Tournament ID'])

        if search_result:
            self.database.update(datas, tournament_query['Tournament ID'] == datas['Tournament ID'])
        else:
            self.database.insert(datas)

    def get_unfinished_tournaments(self):
        unfinished_tournaments = []
        unfinished_tournaments_extended = []
        for tournament in self.database:
            if tournament['Current Round'] < tournament['Total Round(s)']:
                unfinished_tournaments.append(tournament.doc_id)
                unfinished_tournaments_extended.append(tournament)
        view.TournamentReports.show_unfinished_tournaments_view(unfinished_tournaments_extended)
        if unfinished_tournaments:
            return unfinished_tournaments

    def choose_unfinished_tournament(self):
        unfinished_tournaments = self.get_unfinished_tournaments()
        if unfinished_tournaments:
            choice = int(input())
            if choice in unfinished_tournaments:
                return choice
            else:
                view.TournamentReports.unfinished_tournament_wrong_id()
                return None
        else:
            main_controller = MainController()
            main_controller.run()

    def load_tournament(self, tournament_id):
        tournament_data = self.database.get(doc_id=tournament_id)
        if tournament_data:
            return tournament_data
        else:
            return None

    def resume_tournament(self):
        tournament_id = self.choose_unfinished_tournament()
        if tournament_id:
            tournament_data = self.load_tournament(tournament_id)
            if tournament_data:
                tournament_id = tournament_data['Tournament ID']
                resumed_tournament = Tournoi(name=tournament_data['Tournament name'],
                                             location=tournament_data['Place'],
                                             start_date=tournament_data['Start Date'],
                                             end_date=tournament_data['End Date'],
                                             description=tournament_data['Tournament description'],
                                             round_number=tournament_data['Total Round(s)'])
                resumed_tournament.current_round = tournament_data['Current Round']
                resumed_tournament.list_participants = (
                    self.deserialize_contenders_list(tournament_data['Contenders list']))
                resumed_tournament.tournament_id = tournament_id

                round_list = []
                complete_match_list = []
                for round_data in tournament_data['Round list']:
                    round_obj = Round(round_data['Tour n°'], round_data['Start Date'],
                                      round_data['End Date'], round_data['Match List'])
                    match_list = []
                    for match_entry in round_data['Match List']:
                        match = Match(player_1=Player(**match_entry['player_1']), score_1=match_entry['score_1'],
                                      player_2=Player(**match_entry['player_2']), score_2=match_entry['score_2'])
                        match_list.append(match)
                        complete_match_list.append(match)
                    round_obj.match_list = match_list
                    round_list.append(round_obj)
                    resumed_tournament.match_list = complete_match_list
                resumed_tournament.round_list = round_list
                resumed_tournament.left_opponents_by_player = (
                    self.deserialize_left_opponents_by_player(tournament_data['left_opponents_by_player']))

                return resumed_tournament

    def unpack_left_opponents_by_player(self, tournament_data):
        database_path = os.path.join(os.path.dirname(__file__), os.pardir, 'model', 'players_database.json')
        with open(database_path, "r", encoding="utf-8") as file:
            player_database = json.load(file)

        left_opponents_by_player = {}
        left_opponents_by_player_dict = tournament_data['left_opponents_by_player']
        for pid, opponents_data in left_opponents_by_player_dict.items():
            player_info = self.find_player_by_id(player_database, pid)
            main_player = Player(**player_info)
            opponents = [Player(**self.find_player_by_id(player_database, opponent['pid']))
                         for opponent in opponents_data]
            left_opponents_by_player[main_player] = opponents
        return left_opponents_by_player

    def find_player_by_id(self, player_database, chess_id):
        for player in player_database:
            if player['chess_id'] == chess_id:
                return player
        return None

    def deserialize_contenders_list(self, contenders_list):
        deserialized_contenders_list = []
        list_participants = []
        for player_json in contenders_list:
            player_data = json.loads(player_json)
            deserialized_contenders_list.append(player_data)
        for player in deserialized_contenders_list:
            player_instance = Player(**player)
            list_participants.append(player_instance)
        return list_participants

    def deserialize_left_opponents_by_player(self, left_opponents_by_player):
        deserialized_left_opponents_by_player = json.loads(left_opponents_by_player)
        new_left_opponents_by_player = {}
        for player, left_opponents in deserialized_left_opponents_by_player.items():
            deserialized_player = Player(**self.get_player_by_chess_id(player))
            opponents_deserialized = [Player(**json.loads(opponent)) for opponent in left_opponents]
            new_left_opponents_by_player[deserialized_player] = opponents_deserialized
        return new_left_opponents_by_player

    def get_player_by_chess_id(self, chess_id):
        database_path = os.path.join(os.path.dirname(__file__), os.pardir, 'model', 'players_database.json')
        with open(database_path, "r", encoding="utf-8") as file:
            player_database = json.load(file)
        for player in player_database:
            if player['chess_id'] == chess_id:
                search_player_by_id = player
                return search_player_by_id

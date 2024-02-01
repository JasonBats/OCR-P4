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
        """
        Initiates and runs the tournament
        """
        os.system('cls')
        tournament_view = TournamentView
        console_view = ConsoleView("Informations")
        tournament_inputs = tournament_view.create_tournament_view()
        created_tournament = Tournoi(**tournament_inputs)
        left_opponents_by_player, _, created_tournament.list_participants = (
            self.tournament_controller.players_registration())  # TODO : Pourquoi les deux vides ? > Parce qu'une des deux est pop()
        created_tournament.left_opponents_by_player = left_opponents_by_player
        self.data_controller.data_save(created_tournament.to_dict())
        view.TournamentView.print_created_tournament(created_tournament)

        for i in range(1, int(created_tournament.round_number) + 1):
            self.run_round(created_tournament, i, console_view)

        created_tournament.end_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.data_controller.data_save(created_tournament.to_dict())  # Sauvegarde à la fin du tournoi
        view.TournamentView.print_created_tournament(created_tournament)

    def continue_tournament(self):
        """
        Continue a previously started and saved tournament
        """
        console_view = ConsoleView("Informations")
        unfinished_tournament = self.data_controller.resume_tournament()

        for i in range(unfinished_tournament.current_round, int(unfinished_tournament.round_number) + 1):
            self.run_round(unfinished_tournament, unfinished_tournament.current_round, console_view)

    def run_round(self, created_tournament, i, console_view):
        """
        Executes a round of the tournament.
        :param created_tournament: Can be loaded from the database or directly a Tournoi instance.
        :param i: Used for the current round of an instance, not for a loaded tournament.
        :param console_view: Used to display information.
        """
        self.tournament_controller.soft_shuffle_counter = 0
        start_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        # self.tournament_controller.list_participants = created_tournament.list_participants
        # self.tournament_controller.left_opponents_by_player = created_tournament.left_opponents_by_player
        if created_tournament.current_round != 0:
            # Si score_1 n'est pas Null ET score_2 n'est pas null pour chaque match dans dernier_round.match_list
            if all(match.score_1 is not None and match.score_2 is not None for match in
                   created_tournament.round_list[-1].match_list):
                created_tournament.current_round += 1
                view.TournamentView.print_round_number(created_tournament.current_round)
                round_obj = Round(created_tournament.current_round, start_date=start_date, end_date="", match_list=[])
                created_tournament.round_list.append(round_obj)
            else:
                round_obj = created_tournament.round_list[-1]
        else:
            created_tournament.current_round += 1
            view.TournamentView.print_round_number(created_tournament.current_round)
            round_obj = Round(created_tournament.current_round, start_date=start_date, end_date="", match_list=[])
            created_tournament.round_list.append(round_obj)
        if created_tournament.current_round == 1:
            pairs = self.tournament_controller.generate_first_pairs()
        else:
            pairs = self.tournament_controller.generate_pairs(
                created_tournament)  # TODO : Vérifier qu'il n'y a pas déjà des matchs dans le round sinon left_opponents_by_player est vide au round 4 donc crash
        view.TournamentView.print_current_round_pairs(created_tournament.current_round,
                                                      pairs)  # TODO : Attention, mauvaises paires quand reprise
        while len(round_obj.match_list) < 3:
            for pair in pairs:
                match_obj = Match(*pair, score_1=None, score_2=None)
                round_obj.match_list.append(match_obj)
                created_tournament.match_list.append(match_obj)
        self.data_controller.data_save(created_tournament.to_dict())
        for match in round_obj.match_list:
            if match.score_1 is None or match.score_2 is None:
                match.encounter()
                view.TournamentView.print_match_obj(match)
                self.data_controller.data_save(created_tournament.to_dict())
        round_obj.end_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        created_tournament.round_list[-1] = round_obj
        self.data_controller.data_save(created_tournament.to_dict())
        os.system('cls')
        view.TournamentView.print_round_list(created_tournament.round_list)
        console_view.display_ranking(TournamentController.get_ranking(created_tournament.match_list))

    def show_report(self):
        """
        Used to show various reports, managed in view.py
        """
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
        """
        Opens players database and show options to manage players.
        """
        player_view = view.PlayerView()
        player_view.manage_players()

    menu_principal = {
        1: run_tournament,
        2: continue_tournament,
        3: show_report,
        4: players_management
    }

    def run(self):
        """
        Entry point of the main menu.
        """
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
        """
        Where a new tournament is initiated.
        Uses prompts to create a contenders list and attribute them an opponents list.
        :return: A tuple containing 3 elements :
            — A dictionary of left opponents to play with for every player.
            — A list of all participants, assigned to the created tournament.
        """
        tournament_view = view.TournamentView()
        self.list_participants = tournament_view.register_players()
        self.initial_list = []
        for index, element in enumerate(self.list_participants):
            self.initial_list.append(element)
            list_participants_copy = self.list_participants.copy()
            list_participants_copy.pop(index)
            self.left_opponents_by_player[element] = list_participants_copy
        return self.left_opponents_by_player, self.list_participants, self.initial_list  # TODO : initial_list utile ? OUI car list_participants est pop()

    def generate_first_pairs(self):
        """
        Randomly pairs players for first tournament round.

        Selects players from the participants list and forms pairs.
        Each selected player is removed from his opponent's list of remaining opponents.
        The process continues until all players are paired.
        :return: A list of pairs, where each pair is a tuple.
        """
        generated_pairs = []

        def pop_random(liste_participants):
            """
            Picks a random player from the participants list.
            :param liste_participants: List of instances of the Player class.
            :return: A random player of the Player class.
            """
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
        """
        Generates pairs after the current ranking of the tournament, and the player's opponents lists.
        If these two conditions can't be satisfied, players order will be shuffled.
        :param round_obj: To get the left_opponents_by_player dictionaries and the current ranking.
        :return: A list of pairs, where each pair is a tuple.
        """
        self.left_opponents_by_player = round_obj.left_opponents_by_player
        current_ranking = self.get_ranking(round_obj.match_list)
        ranked_players = [player for player, _ in current_ranking]
        next_pairs = []
        print(self.left_opponents_by_player)

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
        """
        Shuffle all players and sort them by their score.
        If shuffled and sorted players keeps creating unmatching pairs, they will be shuffled without sorting.
        :param round_obj: To get current ranking.
        :return: ranked_players: A list of Players, sorted by their score or not.
        """
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
        """
        Uses previous matches to determine the score for each Player.
        Creates a dictionary with Players chess_id as keys, and increment the score for each Match.
        Sort each Player by score.
        :param match_list: To get the previous matches. From the database or from Round instances.
        :return: ranking: A list of tuples, composed by a Player and his current score.
        """
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

            score_player_1 = float(outcome.score_1) if outcome.score_1 is not None else None
            score_player_2 = float(outcome.score_2) if outcome.score_2 is not None else None

            scores_list_dict.setdefault(player_1, 0)
            if score_player_1 is not None:
                scores_list_dict[player_1] += score_player_1
            scores_list_dict.setdefault(player_2, 0)
            if score_player_2 is not None:
                scores_list_dict[player_2] += score_player_2

        ranking = sorted(scores_list_dict.items(), key=lambda item: item[1], reverse=True)
        return ranking


class DataController:
    def __init__(self, dataname):
        self.database_path = os.path.join(os.path.dirname(__file__), os.pardir, 'model', 'database.json')
        self.database = TinyDB(self.database_path, indent=4, encoding='utf-8', ensure_ascii=False)
        self.database.default_table_name = dataname

    def data_save(self, datas):
        """
        Opens database, saves tournament's data.
        :param datas: To check if the tournament already exists by his Tournament ID.
        :return: None, insert or updates database.json.
        """
        tournament_query = Query()
        search_result = self.database.search(tournament_query['Tournament ID'] == datas['Tournament ID'])

        if search_result:
            self.database.update(datas, tournament_query['Tournament ID'] == datas['Tournament ID'])
            view.Functional.saved_tournament_message("update")
        else:
            self.database.insert(datas)
            view.Functional.saved_tournament_message("first save")

    def get_unfinished_tournaments(self):
        """
        Checks if the database contains unfinished tournaments, by comparing
        every tournament's current_round and total_round.  # TODO : Docstring périmée
        :return: unfinished_tournaments: a list of unfinished tournaments.
        """
        unfinished_tournaments = []
        unfinished_tournaments_extended = []
        for tournament in self.database:
            if tournament['Round list'][-1]['Match List'][-1]['score_1'] is None or \
                    tournament['Round list'][-1]['Match List'][-1]['score_2'] is None:
                unfinished_tournaments.append(tournament.doc_id)
                unfinished_tournaments_extended.append(tournament)
        view.TournamentReports.show_unfinished_tournaments_view(unfinished_tournaments_extended)
        if unfinished_tournaments:
            return unfinished_tournaments

    def choose_unfinished_tournament(self):
        """
        Gets the user to chose among the unfinished tournaments, which one he wants to continue.
        :return: choice: an integer representing the index of the unfinished tournament.
        """
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
            main_controller.run()  # TODO : Trouver une autre manière de revenir au menu principal

    def load_tournament(self, tournament_id):
        """
        Loads all the datas of a chosen tournament from the database.
        :param tournament_id: Integer chosen by the user, index of the tournament.
        :return: tournament_data: the values of the tournament from the database.
        """
        tournament_data = self.database.get(doc_id=tournament_id)
        if tournament_data:
            return tournament_data
        else:
            return None

    def resume_tournament(self):
        """
        Recreates an instance of Tournoi from the data obtained from the database.
        :return: resumed_tournament: an instance of Tournoi usable by the rest of the functions.
        """
        tournament_id = self.choose_unfinished_tournament()
        tournament_controller = TournamentController()
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
                resumed_tournament.left_opponents_by_player = (
                    self.deserialize_left_opponents_by_player(tournament_data['left_opponents_by_player']))
                resumed_tournament.tournament_id = tournament_id
                round_list = []
                complete_match_list = []
                if tournament_data['Round list']:
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

                return resumed_tournament

    def deserialize_contenders_list(self, contenders_list):
        """
        Recreates instances of Player objects from the database's contenders_list
        :param contenders_list: List of dictionaries containing the tournament's contenders and their information.
        :return: list_participants: A list of Player objects.
        """
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
        """
        Recreates Player objects from the database's left_opponents_by_player dictionary.
        :param left_opponents_by_player: All the player's left opponents to play against.
        :return: new_left_opponents_by_player: A dictionary of Player objects, with a list of opponents as values.
        """
        deserialized_left_opponents_by_player = json.loads(left_opponents_by_player)
        new_left_opponents_by_player = {}
        for player, left_opponents in deserialized_left_opponents_by_player.items():
            deserialized_player = Player(**self.get_player_by_chess_id(player))
            opponents_deserialized = [Player(**json.loads(opponent)) for opponent in left_opponents]
            new_left_opponents_by_player[deserialized_player] = opponents_deserialized
        return new_left_opponents_by_player

    def get_player_by_chess_id(self, chess_id):
        """
        Find a player in players_database using his chess_id.
        :param chess_id: Player's unique ID, used as a key.
        :return: search_player_by_id: The player this chess_id belongs to.
        """
        database_path = os.path.join(os.path.dirname(__file__), os.pardir, 'model', 'players_database.json')
        with open(database_path, "r", encoding="utf-8") as file:
            player_database = json.load(file)
        for player in player_database:
            if player['chess_id'] == chess_id:
                search_player_by_id = player
                return search_player_by_id

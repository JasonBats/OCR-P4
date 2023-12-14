from model import match
from model.tours import Tour
from view import view
from model.tournoi import Tournoi
from model.player import Player
from model.match import Match
from rich import print
import json
import os
import random
from view.view import create_tournament_view
from datetime import datetime


class MainController:

    def __init__(self):
        self.tournament_controller = TournamentController()

    def run_tournament(self):
        tournament_inputs = create_tournament_view()
        created_tournament = Tournoi(**tournament_inputs)
        print("Tournoi créé !")
        print(created_tournament)
        self.tournament_controller.add_player()
        _, created_tournament.list_participants = self.tournament_controller.register_players()
        print(created_tournament)
        for i in range(1, int(created_tournament.round_number) + 1):
            print("Tour n°:", i)
            index = 0
            created_tournament.current_round += 1
            if i == 1:
                pairs = self.tournament_controller.generate_first_pairs()
            else:
                pairs = self.tournament_controller.generate_pairs()
            start_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            tour_obj = Tour(i, start_date=start_date, end_date="", match_list=[])
            print("Paires du tour", i, ":", pairs)
            for pair in pairs:
                match_obj = Match(*pair)
                match_obj.combat()
                print(match_obj)
                tour_obj.match_list.append(match_obj)
                index += 1
            tour_obj.end_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            created_tournament.round_list.append(tour_obj)
            print(tour_obj)
            print("ROUND LIST:::::::::", created_tournament.round_list)
        created_tournament.end_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        print(created_tournament)

        print("Générer un rapport :")
        print("retour au menu principal :")
        print("Saisissez le chiffre correspondant à votre choix.")

    def afficher_rapport(self):
        pass

    def gerer_utilisateurs(self):
        pass

    menu_principal = {
        1: run_tournament,
        2: afficher_rapport,
        3: gerer_utilisateurs
    }

    def run(self):
        while True:
            try:
                main_menu = view.read_menu_selection()
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
    print("liste des joueurs :", all_contenders)

    def add_player(self):
        add = int(input("Ajouter un joueur ? 1 = OUI / 0 = NON"))
        while add:
            new_player = Player(
                nom=input("Quel est le nom du joueur ?"),
                prenom=input("Quel est son prénom ?"),
                date_naissance=input("Quelle est sa date de naissance ?"))
            try:
                with open(self.database_path, "r", encoding="utf-8") as fichier:
                    joueurs = json.load(fichier)
                    print("Liste de tous les joueurs :", joueurs)
            except FileNotFoundError:
                joueurs = []

            joueurs.append(new_player.to_dict())
            print(new_player)

            with open(self.database_path, "w", encoding="utf-8") as fichier:
                json.dump(joueurs, fichier, default=lambda obj: new_player.__json__(), ensure_ascii=False, indent=2)

            print(new_player, " : Joueur inscrit avec succès")
            add = int(input("Ajouter un autre joueur ? 1 = OUI / 2 = NON"))

    def register_players(self):
        self.list_participants = random.sample(self.all_contenders, 6)
        print("Liste des participants au tournoi :", self.list_participants)
        self.left_opponents_by_player = {}
        for index, element in enumerate(self.list_participants):
            self.list_participants_copy = self.list_participants.copy()
            self.list_participants_copy.pop(index)
            self.left_opponents_by_player[element] = self.list_participants_copy
        return self.left_opponents_by_player, self.list_participants

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

    def generate_pairs(self):
        current_ranking = self.ranking()
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
                    ranked_players = []
                    ranked_players = TournamentController.shuffle_equal_players(self)
            pair = (player_1, player_2)
            next_pairs.append(pair)
            index = 0

        for pair in next_pairs:
            self.left_opponents_by_player[pair[0]].remove(pair[1])
            self.left_opponents_by_player[pair[1]].remove(pair[0])

        return next_pairs

    def shuffle_equal_players(self):
        current_ranking = TournamentController.ranking(self)
        ranked_players_by_score = {}

        for player_name, player_score in current_ranking:
            if player_score not in ranked_players_by_score:
                ranked_players_by_score[player_score] = [player_name]
            else:
                ranked_players_by_score[player_score].append(player_name)

        for score, player_list in ranked_players_by_score.items():
            if len(player_list) > 1:
                player_list = random.shuffle(player_list)
            else:
                pass

        ranked_players = [player for score, players in ranked_players_by_score.items() for player in players]
        return ranked_players

    def ranking(self):
        previous_matches = match.matchs_list.copy()
        scores_list_dict = {}
        for num, outcome in enumerate(previous_matches):
            index = 0
            player_1 = outcome[index][index]
            score_player_1 = float(outcome[index][index + 1])
            player_2 = outcome[index + 1][index]
            score_player_2 = float(outcome[index + 1][index + 1])
            scores_list_dict.setdefault(player_1, 0)
            scores_list_dict[player_1] += score_player_1
            scores_list_dict.setdefault(player_2, 0)
            scores_list_dict[player_2] += score_player_2
        ranking = sorted(scores_list_dict.items(), key=lambda item: item[1], reverse=True)
        print("Liste des matchs :", match.matchs_list)
        print("Classement :", ranking)
        return ranking


# Logique revue de choix d'adversaire : Avant, si l'adversaire n'était pas dans la liste des adversaires,
# je prenais le +1 dans la liste : qu'il soit ou non dans la liste des adversaires.

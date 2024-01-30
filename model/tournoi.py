import json
import uuid


class Tournoi:
    def __init__(self,
                 tournament_id="",
                 name="",
                 location="",
                 start_date="",
                 end_date="",
                 description="",
                 round_number=4):
        self.tournament_id = str(uuid.uuid4())
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.current_round = 0
        self.round_list = []
        self.list_participants = []
        self.description = description
        self.round_number = round_number
        self.match_list = []
        self.left_opponents_by_player = {}

    def to_dict(self):
        return {
            'Tournament ID': self.tournament_id,
            'Tournament name': self.name,
            'Place': self.location,
            'Tournament description': self.description,
            'Start Date': self.start_date,
            'End Date': self.end_date,
            'Current Round': self.current_round,
            'Total Round(s)': self.round_number,
            'Round list': [tour.__json__() for tour in self.round_list],
            'Contenders list': [player.to_json() for player in self.list_participants],
            'left_opponents_by_player': self.serialization_left_opponents_by_player(),
        }

    def serialization_left_opponents_by_player(self):
        left_players_prepare = {}

        for key_player, opponents in self.left_opponents_by_player.items():
            left_players_prepare[key_player.chess_id] = [
                opponent.to_json() for opponent in opponents
            ]

        left_players_json = json.dumps(left_players_prepare)
        return left_players_json

    def __repr__(self):
        return (f"Nom du tournoi : {self.name}, à {self.location}, du {self.start_date} au {self.end_date}."
                f"Tour actuel : {self.current_round} / {self.round_number}."
                f"Description : {self.description}"
                f"\nListe des participants : {self.list_participants}")

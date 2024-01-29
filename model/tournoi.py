import json
import uuid


class Tournoi:
    def __init__(self, name="",
                 location="",
                 start_date="",
                 end_date="",
                 description="",
                 round_number=4):
        self.id = str(uuid.uuid4())
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
            'Tournament ID': self.id,
            'Tournament name': self.name,
            'Place': self.location,
            'Tournament description': self.description,
            'Start Date': self.start_date,
            'End Date': self.end_date,
            'Current Round': self.current_round,
            'Total Round(s)': self.round_number,
            'Round list': [tour.__json__() for tour in self.round_list],
            'Contenders list': [player.to_json() for player in self.list_participants],
            'left_opponents_by_player': self.serialization_left_opponents_by_player_2(),
        }

    def serialization_left_opponents_by_player(self):
        # json.dump({"id": "sss"})
        # return {
        #     "":
        # }
        serialized_data = {}
        for player, opponents in self.left_opponents_by_player.items():
            player_dict = player.to_dict()
            opponents_list = [opponent.to_dict() for opponent in opponents]
            player_key = player.chess_id
            serialized_data[player_key] = opponents_list
        return serialized_data

    def serialization_left_opponents_by_player_2(self):
        left_players_prepare = {}

        for key_player, opponents in self.left_opponents_by_player.items():
            left_players_prepare[key_player.to_json()] = [
                opponent.to_json() for opponent in opponents
            ]

        # Then, we jsonify the container dictionary to a string
        left_players_json = json.dumps(left_players_prepare)

        # Data will be stored like this in database
        print(left_players_json)
        return left_players_json

    def __repr__(self):
        return (f"Nom du tournoi : {self.name}, à {self.location}, du {self.start_date} au {self.end_date}."
                f"Tour actuel : {self.current_round} / {self.round_number}."
                f"Description : {self.description}"
                f"\nListe des participants : {self.list_participants}")

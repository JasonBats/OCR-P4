import json


class Player:

    chess_id: str
    firstname: str
    lastname: str
    birthdate: str

    def __init__(self, chess_id: str, firstname: str, lastname: str, birthdate: str):
        self.chess_id = chess_id
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate

    def to_dict(self):
        return {
            "chess_id": self.chess_id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "birthdate": self.birthdate
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def __repr__(self):
        return f"{self.firstname} {self.lastname}"

    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented
        return self.chess_id == other.chess_id

    def __hash__(self):
        return hash((self.chess_id, self.firstname, self.lastname, self.birthdate))

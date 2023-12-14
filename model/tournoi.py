from datetime import datetime


class Tournoi:
    def __init__(self, name="Nom par défaut",
                 location="lieu par défaut",
                 start_date="01/01/2000",
                 end_date="01/01/2000",
                 description="",
                 round_number=4):
        self.name = name
        self.lieu = location
        self.start_date = datetime.now()
        self.end_date = datetime.now()  # TODO: Modifier la date à la fin du dernier tour
        self.current_round = 1
        self.round_list = []
        self.list_participants = []
        self.description = description
        self.round_number = round_number
            
    def __repr__(self):
        return (f"Nom du tournoi : {self.name}, à {self.lieu}, du {self.start_date} au {self.end_date}."
                f"Tour actuel : {self.current_round} / {self.round_number}."
                f"Les participants : {self.list_participants}. Description : {self.description}")

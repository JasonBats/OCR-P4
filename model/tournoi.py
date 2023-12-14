class Tournoi:
    def __init__(self, name="",
                 location="",
                 start_date="",
                 end_date="",
                 description="",
                 round_number=4):
        self.name = name
        self.lieu = location
        self.start_date = start_date
        self.end_date = end_date
        self.current_round = 0
        self.round_list = []
        self.list_participants = []
        self.description = description
        self.round_number = round_number
            
    def __repr__(self):
        return (f"Nom du tournoi : {self.name}, à {self.lieu}, du {self.start_date} au {self.end_date}."
                f"Tour actuel : {self.current_round} / {self.round_number}."
                f"Description : {self.description}"
                f"\nListe des participants : {self.list_participants}")

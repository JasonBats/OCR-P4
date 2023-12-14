class Tour:
    def __init__(self, name, start_date, end_date, match_list):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.match_list = match_list

    def __repr__(self):
        return (f'Tour n° : {self.name}'
                f'\nDate de début : {self.start_date}'
                f'\nDate de fin : {self.end_date}'
                f'\nListe des matchs :\n{self.match_list}')

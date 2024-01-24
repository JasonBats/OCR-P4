class Round:
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

    def to_dict(self):
        return {
            'Tour n°': self.name,
            'Start Date': self.start_date,
            'End Date': self.end_date,
            'Match List': [match.to_dict() for match in self.match_list]
        }

    def __json__(self):
        return {
            'Tour n°': self.name,
            'Start Date': self.start_date,
            'End Date': self.end_date,
            'Match List': [match.__json__() for match in self.match_list]
        }
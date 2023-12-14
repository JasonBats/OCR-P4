class Tour:
    def __init__(self, name, start_date, end_date, match_list):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.match_list = match_list

    def __repr__(self):
        return f'{self.name} - {self.start_date} - {self.end_date} - {self.match_list}'
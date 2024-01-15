class Player:
    def __init__(self, name, first_name, birth_date):
        self.name = name
        self.first_name = first_name
        self.birth_date = birth_date

    def __repr__(self):
        return f"{self.name} {self.first_name}"

    def to_dict(self):
        return {
            'name': self.name,
            'first_name': self.first_name,
            'birth_date': self.birth_date
        }

    def __json__(self):
        return self.to_dict()

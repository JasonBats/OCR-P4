class Player:
    def __init__(self, nom, prenom, date_naissance):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance

    def __repr__(self):
        return f"{self.nom} {self.prenom}"
    
    def to_dict(self):
        return {
            'nom': self.nom,
            'prenom': self.prenom,
            'date_naissance': self.date_naissance
        }
    
    def __json__(self):
        return self.to_dict()

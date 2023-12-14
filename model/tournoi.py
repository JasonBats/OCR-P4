import random
from . import player
import datetime
import json


class Tournoi:
    def __init__(self, nom="Nom par défaut", lieu="lieu par défaut", date_debut="01/01/2000", date_fin="01/01/2000", description="", nombre_tours=4):
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.tour_actuel = 1
        self.liste_tours = []
        self.liste_participants = []
        self.description = description
        self.nombre_tours = nombre_tours

    # def __len__(self):
    #     return len(self.liste_participants)

    # paires = []
    
    # def generer_paires(liste_participants):
    #     def pop_random(liste_participants):
    #         id_random = random.randrange(0, len(liste_participants))
    #         return liste_participants.pop(id_random)

    #     while liste_participants:
    #         joueur1 = pop_random(liste_participants)
    #         joueur2 = pop_random(liste_participants)
    #         paire = joueur1, joueur2
    #         Tournoi.paires.append(paire)
            
    def __repr__(self):
        return f"Nom du tournoi : {self.nom}, à {self.lieu}, du {self.date_debut} au {self.date_fin}. Tour actuel : {self.tour_actuel} / {self.nombre_tours}. Les participants : {self.liste_participants}. Description : {self.description}"


# Tournoi.generer_paires(liste_participants)

# tournoi1 = Tournoi()
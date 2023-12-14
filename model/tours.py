# Un tour est composé de X paires
# Le 1er tour reçoit les 3 paires de controller.Tournament_Controller.generer_paires()
# le tour suivant utilise les résultats du tour 1 pour avoir la liste des 6 joueurs classés par points
# while tour_actuel <= nombre_tours:
    #tour_actuel += 1
from model import match


# définir un tour
# créer le tour 1

class Tour:
    instances = []
    def __init__(self, joueur1, joueur2, score1= 0, score2= 0):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.score1 = score1
        self.score2 = score2
        self.paire = joueur1, joueur2
        Tour.instances.append(self)

    def modifier_score(self):
        self.score1 = input(f"Quel score pour {self.joueur1} ?")
        if self.score1 == "1":
            self.score2 = "0"
        elif self.score1 == "0":
            self.score2 = "1"
        elif self.score1 == "0.5":
            self.score2 = "0.5"
        verif = int(input(f"Le score est-il bien {self.joueur1} {self.score1} VS {self.joueur2} {self.score2} ? 1 = OUI / 2 = NON"))
        if verif == 1:
            pass
        elif verif == 2:
            self.modifier_score()
        else:
            print("Choix invalide. Saisissez 1 pour OUI et 2 pour NON")
            self.modifier_score()

    def __str__(self):
        return f"{self.joueur1} {self.score1} VS {self.score2} {self.joueur2} ! (str)"
    
    def __repr__(self):
        return f"{self.joueur1} {self.score1} VS {self.score2} {self.joueur2} ! (repr)"


class Liste_Tour_2:
    def __init__(self):
        self.classement = []

    points_accumules_par_joueur = []

    def get_scores(liste_tour_1):
        scores_joueurs = []
        ranking = match.matchs_list
        index_paire = 0
        for item1 in ranking:
            joueur = ranking[index_paire].player_1
            score = ranking[index_paire].score_1
            entree = joueur, score
            scores_joueurs.append(entree)
            Liste_Tour_2.points_accumules_par_joueur.append(entree)
            index_paire += 1
        index_paire = 0
        for item2 in liste_tour_1:
            joueur = liste_tour_1[index_paire].player_2
            score = liste_tour_1[index_paire].score_2
            entree = joueur, score
            scores_joueurs.append(entree)
            Liste_Tour_2.points_accumules_par_joueur.append(entree)
            index_paire += 1
        liste_triee = sorted(scores_joueurs, key=lambda x: float(x[1]))
        liste_inversee = liste_triee[::-1]
        print("Liste inversée :::::", liste_inversee)
        print("Liste tour 1 :::::", liste_tour_1)
        return liste_inversee
    
    def create_second_round(liste_inversee):
        
        paires_second_tour = []
        
        while liste_inversee:
            joueur1 = liste_inversee.pop(0)[0]
            print(joueur1)
            joueur2 = liste_inversee.pop(0)[0]
            print(joueur2)
            paire = Tour(joueur1, joueur2)
            paires_second_tour.append(paire)
        return paires_second_tour

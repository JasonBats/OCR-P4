from rich import print

import view.view


class Match:

    def __init__(self, player_1, player_2, score_1=0, score_2=0):
        self.player_1 = player_1
        self.player_2 = player_2
        self.score_1 = score_1
        self.score_2 = score_2
        self.match_data = [(player_1, score_1), (player_2, score_2)]

    def encounter(self):
        self.score_1 = view.view.write_score(self.player_1)
        if self.score_1 == "1":
            self.score_2 = "0"
        elif self.score_1 == "0":
            self.score_2 = "1"
        elif self.score_1 == "0.5":
            self.score_2 = "0.5"
        else:
            print("Ce score n'existe pas. Saisissez 1 pour une victoire, 0.5 pour une égalité ou 0 pour une défaite")
            self.encounter()
        verif = view.view.score_review(self.player_1, self.player_2, self.score_1, self.score_2)
        if verif == 1:
            pass
        elif verif == 2:
            self.encounter()
        else:
            print("Choix invalide. Saisissez 1 pour OUI et 2 pour NON")
            self.encounter()

    def __repr__(self):
        return f"\n{self.player_1} {self.score_1} VS {self.score_2} {self.player_2}\n"

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
        tournament_view = view.view.TournamentView()
        self.score_1 = tournament_view.write_score(self.player_1)
        if self.score_1 == "1":
            self.score_2 = "0"
        elif self.score_1 == "0":
            self.score_2 = "1"
        elif self.score_1 == "0.5":
            self.score_2 = "0.5"
        else:
            view.view.TournamentView.incorrect_score()
            self.encounter()
        verification = tournament_view.score_review(self.player_1, self.player_2, self.score_1, self.score_2)
        if verification == 1:
            pass
        elif verification == 2:
            self.encounter()
        else:
            view.view.TournamentView.incorrect_verif()
            self.encounter()

    def __repr__(self):
        return f"\n{self.player_1} {self.score_1} VS {self.score_2} {self.player_2}\n"

    # def to_dict(self):
    #     return {
    #         "Match": f"{self.player_1} {self.score_1} VS {self.score_2} {self.player_2}"
    #     }

    def to_dict(self):
        return {
            "player_1": self.player_1.to_dict(),
            "score_1": self.score_1,
            "player_2": self.player_2.to_dict(),
            "score_2": self.score_2
        }

    def __json__(self):
        return {
            "player_1": self.player_1.to_dict(),
            "score_1": self.score_1,
            "player_2": self.player_2.to_dict(),
            "score_2": self.score_2
        }

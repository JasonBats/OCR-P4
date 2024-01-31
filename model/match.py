import view.view


class Match:

    def __init__(self, player_1, player_2, score_1=0, score_2=0):
        self.player_1 = player_1
        self.player_2 = player_2
        self.score_1 = score_1
        self.score_2 = score_2
        self.match_data = [(player_1, score_1), (player_2, score_2)]

    def encounter(self):
        """
        User inputs the first player's score.
        The second player's score is determined by the first one.
        This function also verifies if the user is sure about the outcome he wrote.
        The function just updates the scores to the tournament's data.
        """
        tournament_view = view.view.TournamentView()
        while True:
            self.score_1 = tournament_view.write_score(self.player_1)
            if self.score_1 in ["1", "0.5", "0"]:
                self.score_2 = "0" if self.score_1 == "1" else "1" if self.score_1 == "0" else "0.5"

                verification = tournament_view.score_review(self.player_1, self.player_2, self.score_1, self.score_2)
                if verification == 1:
                    break
                elif verification == 2:
                    continue
                else:
                    view.view.TournamentView.incorrect_verif()
            else:
                view.view.TournamentView.incorrect_score()

    def __repr__(self):
        return f"\n{self.player_1} {self.score_1} VS {self.score_2} {self.player_2}\n"

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

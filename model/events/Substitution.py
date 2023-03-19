from model.events.Event import Event


class Substitution(Event):

    def __init__(self, minute, team, extra, player_in, player_out):
        super().__init__(minute, team, extra)
        self.player_in = player_in
        self.player_out = player_out

    def __str__(self):
        return f"Substitution: {self.minute}' {self.team} {self.player_in} {self.player_out}"

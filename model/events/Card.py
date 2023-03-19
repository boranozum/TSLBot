from model.events.Event import Event


class Card(Event):

    def __init__(self, minute, team, extra, player, card_type):
        super().__init__(minute, team, extra)
        self.player = player
        self.card_type = card_type

    def __str__(self):
        return f"Card: {self.minute}' {self.team} {self.player} {self.card_type}"
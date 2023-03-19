from model.events.Event import Event


class Goal(Event):

    def __init__(self, minute, team, extra, scorer, assist=None, own_goal=False, penalty=False):
        super().__init__(minute, team, extra)
        self.team = team
        self.scorer = scorer
        self.assist = assist
        self.own_goal = own_goal
        self.penalty = penalty

    def __str__(self):
        return f"Goal: {self.minute}' {self.team} {self.scorer} {self.assist} {self.own_goal}"

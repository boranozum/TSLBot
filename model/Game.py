from Parser import Parser
from model.events.Card import Card
from model.events.Goal import Goal
from model.events.Substitution import Substitution


class Game:

    def __init__(self, fixture_id, home_team, away_team, home_score, away_score, status=None, date=None, time=None,day=None, elapsed=None):
        self.fixture_id = fixture_id
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score
        self.status = status
        self.date = date
        self.time = time
        self.elapsed = elapsed
        self.day = day
        self.events = []

    def __str__(self):
        if self.home_score is None:
            return "{:>22} {:<2} {:<20}".format(
                self.home_team,
                'vs',
                self.away_team
            )

        return "{:>20} {} - {} {:<20}".format(
            self.home_team,
            str(self.home_score),
            str(self.away_score),
            self.away_team
        )

    def __repr__(self):
        if self.status == 'NS':
            return "{:<10} {:>22} {} {:<20}".format(
                self.time,
                self.home_team,
                '-',
                self.away_team
            )
        elif self.status == 'FT':
            return "{:<10} {:>20} {} - {} {:<20}".format(
                self.time,
                self.home_team,
                str(self.home_score),
                str(self.away_score),
                self.away_team
            )

        else:
            return "{:<10}* {:>20} {} - {} {:<20} {:<2}".format(
                self.time,
                self.home_team,
                str(self.home_score),
                str(self.away_score),
                self.away_team,
                str(self.elapsed)
            )

    def get_events(self):
        return self.events

    def set_events(self):

        response = Parser('https://api-football-v1.p.rapidapi.com/v3/fixtures/events', {
            'fixture': self.fixture_id,
        }).get_data()

        for event in response:
            if event['type'] == 'Goal':
                e = Goal(
                    event['minute'],
                    event['team']['name'],
                    event['extra']['time'],
                    event['player']['name'],
                    event['assist']['name'])

                if event['detail'] == 'Own Goal':
                    e.own_goal = True

                elif event['detail'] == 'Penalty':
                    e.penalty = True

            elif event['type'] == 'Card':
                self.events.append(
                    Card(
                        event['time']['elapsed'],
                        event['team']['name'],
                        event['time']['extra'],
                        event['player']['name'],
                        event['detail']
                    )
                )
            elif event['type'] == 'subst':
                self.events.append(
                    Substitution(
                        event['time']['elapsed'],
                        event['team']['name'],
                        event['time']['extra'],
                        event['assist']['name'],
                        event['player']['name']
                    )
                )
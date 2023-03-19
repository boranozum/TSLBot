from Parser import Parser
from model.Game import Game


class Team:

    def __init__(self, team_id, name, logo, rank=None, points=None, goalsDiff=None, played=None, won=None, draw=None,
                 lost=None, goalsFor=None, goalsAgainst=None):
        self.form = None
        self.lost = None
        self.draw = None
        self.won = None
        self.played = None
        self.goalsDiff = None
        self.points = None
        self.rank = None
        self.goalsFor = None
        self.goalsAgainst = None
        self.team_id = team_id
        self.name = name
        self.logo = logo
        self.matches = []

    def setStandings(self, rank, points, goalsDiff, form, played, won, draw, lost, goalsFor, goalsAgainst):
        self.rank = rank
        self.points = points
        self.goalsDiff = goalsDiff
        self.played = played
        self.won = won
        self.draw = draw
        self.lost = lost
        self.goalsFor = goalsFor
        self.goalsAgainst = goalsAgainst
        self.form = form

    def printStandings(self):

        return "{:<4} {:<20} {:<3} {:<3} {:<3} {:<3} {:<3} {:<3} {:<3} {:<3}".format(
            self.rank,
            self.name,
            self.played,
            self.won,
            self.draw,
            self.lost,
            self.goalsFor,
            self.goalsAgainst,
            self.goalsDiff,
            self.points,
            self.form
        )

    def setMatches(self):

        response = Parser('https://api-football-v1.p.rapidapi.com/v3/fixtures', {
            'season': '2022',
            'team': self.team_id,
        }).get_data()

        for match in response:

            if match['league']['id'] == 203:
                self.matches.append(
                    Game(
                        match['fixture']['id'],
                        match['teams']['home']['name'],
                        match['teams']['away']['name'],
                        match['goals']['home'],
                        match['goals']['away']))

    def printMatches(self):

        return '```' + '\n'.join([str(match) for match in self.matches]) + '```'
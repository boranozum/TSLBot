from Parser import Parser
from model.Game import Game


class Lineup(Game):

    def __init__(self,fixture_id, home_team, away_team, home_score, away_score, status, date, time, elapsed, day):
        super().__init__( fixture_id, home_team, away_team, home_score, away_score, status, date, time, elapsed, day)
        self.players = {'G': [], 'D': [], 'M': [], 'F': []}
        self.substitutes = []
        self.formation = []
        self.coach = None

    def setLineup(self, team_id):

        response = Parser('https://api-football-v1.p.rapidapi.com/v3/lineups', {
            'fixture': self.fixture_id,
        }).get_data()

        for key in response:
            if key['team']['id'] == team_id:
                # split formation into an int array
                self.formation = [int(x) for x in key['formation'].split('-')]
                self.coach = key['coach']['name']

                for player in key['startXI']:
                    self.players[player['position']].append(player['player']['name'])

                for player in key['substitutes']:
                    self.substitutes.append(player['player']['name'])

    def __str__(self):

        # join players into a string
        players = '\n'.join(
            [f'{position}: {", ".join(self.players[position])}' for position in self.players if self.players[position]])

        # join substitutes into a string
        substitutes = '\n'.join(self.substitutes)

        return players + '\n\nSubstitutes:\n' + substitutes
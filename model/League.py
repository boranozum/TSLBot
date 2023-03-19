from Parser import Parser
from model.Team import Team


class League:

    def __init__(self, league_id):
        self.league_id = league_id
        self.teams = {}

        response = Parser('https://api-football-v1.p.rapidapi.com/v3/teams',
                          {'league': '203', 'season': '2022'}).get_data()

        for key in response:
            self.teams[key['team']['id']] = Team(key['team']['id'], key['team']['name'], key['team']['logo'])

    def setStandings(self):

        response = Parser('https://api-football-v1.p.rapidapi.com/v3/standings', {
            'league': '203',
            'season': '2022'
        }).get_data()[0]['league']

        for key in response['standings'][0]:
            self.teams[key['team']['id']].setStandings(
                key['rank'],
                key['points'],
                key['goalsDiff'],
                key['form'],
                key['all']['played'],
                key['all']['win'],
                key['all']['draw'],
                key['all']['lose'],
                key['all']['goals']['for'],
                key['all']['goals']['against']
            )

        # sort teams by rank
        self.teams = dict(sorted(self.teams.items(), key=lambda item: item[1].rank))

    def printStandings(self):
        header = "{:<4} {:<20} {:<3} {:<3} {:<3} {:<3} {:<3} {:<3} {:<3} {:<3}".format(
            'Rank', 'Team', 'Pl', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'P'
        )

        # join header and standings as a string
        standings = '```' + header + '\n' + '\n'.join([self.teams[key].printStandings() for key in self.teams]) + '```'

        return standings
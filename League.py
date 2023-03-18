from Parser import Parser


def getTeamIdByName(name):
    response = Parser('https://api-football-v1.p.rapidapi.com/v3/teams', {
        'name': name
    }).get_data()

    return response[0]['team']['id']


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
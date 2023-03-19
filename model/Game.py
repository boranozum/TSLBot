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
            return "    {:<6} {:>22} {} {:<20}".format(
                self.time,
                self.home_team,
                '-',
                self.away_team
            )
        elif self.status == 'FT':
            return "    {:<6} {:>20} {} - {} {:<20}".format(
                self.time,
                self.home_team,
                str(self.home_score),
                str(self.away_score),
                self.away_team
            )

        else:
            return "    {:<6}* {:>20} {} - {} {:<20} {:<2}".format(
                self.time,
                self.home_team,
                str(self.home_score),
                str(self.away_score),
                self.away_team,
                str(self.elapsed)
            )
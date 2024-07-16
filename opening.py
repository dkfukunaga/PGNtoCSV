class Opening:
    def __init__(self, eco, result, white_elo, black_elo):
        self.eco = eco
        self.opening_category = eco[0]
        self._decodeEco(self.eco) # set opening type
        self.games = 1
        self.black_wins = result
        self._white_elo_subtotal = white_elo
        self._black_elo_subtotal = black_elo
        self._recalc()
        self.changed = False

    def add_game(self, result, white_elo, black_elo):
        self.black_wins += result
        self.games += 1
        self._white_elo_subtotal += white_elo
        self._black_elo_subtotal += black_elo
        # set flag that averages needs to be recalculated
        self.changed = True

    def getEco(self):
        return self.eco

    def getOpeningCategory(self):
        return self.opening_category

    def getOpeningType(self):
        return self.opening_type

    def getGames(self):
        return self.games

    def getBlackWins(self):
        return self.black_wins

    def getBlackWinRate(self):
        if self.changed:
            self._recalc()
        return self.black_win_rate

    def getAvgWhiteElo(self):
        if self.changed:
            self._recalc()
        return self.avg_white_elo

    def getAvgBlackElo(self):
        if self.changed:
            self._recalc()
        return self.avg_black_elo

    def getAvgEloDiff(self):
        if self.changed:
            self._recalc()
        return self.avg_elo_diff

    def getLine(self):
        return self.getEco() + ',' + self.getOpeningCategory() + ',' + self.getOpeningType() + ',' \
            + str(self.getGames()) + ',' + str(self.getBlackWins()) + ',' \
            + str(self.getBlackWinRate()) + ',' + str(self.getAvgWhiteElo()) \
            + ',' + str(self.getAvgBlackElo()) + ',' + str(self.getAvgEloDiff()) + '\n'

    def _decodeEco(self, eco):
        if eco[0] == 'B' or eco[0] == 'C':
            self.opening_type = "King's Pawn Opening"
        elif eco[0] == 'D' or eco[0] == 'E':
            self.opening_type = "Queen's Pawn Opening"
        elif eco[0] == 'A':
            if int(eco[1]) >= 4:
                self.opening_type = "Queen's Pawn Opening"
            else:
                self.opening_type = "Other"
        else:
            self.opening_type = "NA"

    def _recalc(self):
        self.black_win_rate = round(self.black_wins / self.games, 2)
        self.avg_white_elo = round(self._white_elo_subtotal / self.games, 2)
        self.avg_black_elo = round(self._black_elo_subtotal / self.games, 2)
        self.avg_elo_diff = round(self.avg_white_elo - self.avg_black_elo, 2)
        self.changed = False

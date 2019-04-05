import math
import agent
import time

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        return self.makeMove(brd)

    def heuristics(self, brd, player):

        # determine players to be able to assign different heuristic values
        # opponent heuristics are worth more (negatively) than my player's
        if player == 1:
            me = 1
            opponent = 2
        else:
            me = 2
            opponent = 1

        # brd.get_outcome() will tell if there is a winning or losing board
        # if this is the situation, return high number to override all other
        # possible moves. If I can win, I want to make that move first, even
        # if the opponent has a winning move
        if brd.get_outcome() == me and brd.player == opponent:
            return 99999999
        if brd.get_outcome() == opponent and brd.player == me:
            return -99999999

        # severity is the heuristic value of the board
        severity = 0

        # go through the board
        for i in range(0, brd.w):
            for j in range(0, brd.h):
                # ignore spaces that are empty to improve search time
                if brd.board[j][i] != 0:
                    if brd.is_any_line_at(i, j):
                        # apply severity to play primarily defensive
                        # every spot opponent has, -5
                        # every spot I have, +1
                        if brd.board[j][i] == opponent:
                            severity -= 5
                        elif brd.board[j][i] == me:
                            severity += 1
                        else:
                            severity += 0
        # return heuristic value
        return severity

    # maximum for alpha beta
    # finds & returns the highest severity board state
    def maxValue(self, brd, n, alpha, beta, player):
        bestMove = -999999999
        bestBoard = None

        # check terminal condition
        if self.terminalCondition(n) == -1:
            return None, self.heuristics(brd, player)

        # check possible moves on given board
        for i in self.get_successors(brd):
            (board, move) = self.minValue(i[0], n - 1, alpha, beta, player)
            if move > bestMove:
                bestMove = move
                bestBoard = i
            if bestMove >= beta:
                break
            if bestMove >= alpha:
                alpha = bestMove
        return bestBoard, bestMove

    # minimum for alpha beta
    # finds & returns the lowest severity board state
    def minValue(self, brd, n, alpha, beta, player):
        worstMove = 999999999
        worstBoard = None

        # check terminal condition
        if self.terminalCondition(n) == -1:
            return None, self.heuristics(brd, player)

        # check possible moves on given board
        for i in self.get_successors(brd):
            (board, move) = self.maxValue(i[0], n - 1, alpha, beta, player)
            if move < worstMove:
                worstMove = move
                worstBoard = i
            if worstMove <= beta:
                break
            if worstMove <= alpha:
                alpha = worstMove
        return worstBoard, worstMove

    # terminal condition for alpha beta
    # return -1 if there is no more depth to traverse
    def terminalCondition(self, n):
        if n == 0:
            return -1

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ

    # make move based on best possible outcome (clock added to ensure no time out)
    def makeMove(self, brd):
        # track best possible moves thus far
        bestSeverity = 0
        bestMove = 0

        # start clock to make sure move doesn't take longer than 15 seconds
        clock = time.time()

        # go through
        for i in range (0, self.max_depth):
            (board, state) = self.minValue(brd, i, -99999999, 99999999, brd.player)
            if state >= 9999999:
                return board[1]
            if state <= -9999999:
                return board[1]
            if state > bestSeverity:
                bestSeverity = state
                bestMove = board
            else:
                bestMove = board

            # check time at end of loop
            curTime = time.time() - clock

            # if its getting close to 15 seconds, break loop
            # bumped down from 13 to 12 because 13 took too long once
            if curTime > 12:
                break
        # make the best move found so far
        return bestMove[1]

THE_AGENT = AlphaBetaAgent("SullivanDaniel", 7)
"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!
    # Tom M Implementation
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    # Three heuristic methodologies listed here.  One will be chosen but all three will be analyzed in heuristic_analysis.pdf

    # Heuristic #1 - Multiply opponent's moves by two
    #return float(own_moves - (2 * opp_moves))
    # Heuristic #2 - Halve opponent's moves
    return float(own_moves - (.5 * opp_moves))
    # Heuristic #3 - Multiply opponent's moves by two, then divide total by blank spaces on board
    #return float( (own_moves - (2 * opp_moves)) / (49 - game.move_count) )

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)  This parameter should be ignored when iterative = True.

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).  When True, search_depth should
        be ignored and no limit to search depth.

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            DEPRECATED -- This argument will be removed in the next release

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Implemented by Tom M
        # set which search method to call in try block for best move found
        search_method = self.minimax if self.method is 'minimax' else self.alphabeta

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring

            # TODO: check maximizing_player arg for each search function
            if self.iterative:
                depth = 0
                while True:
                    depth += 1
                    _, cur_best_move = search_method(game, depth) # _ is unused placeholder
            else:
                _, cur_best_move = search_method(game, self.search_depth) # _ is unused placeholder

        except Timeout:
            # Handle any actions required at timeout, if necessary
            return cur_best_move

        # Return the best move from the last completed search iteration
        return cur_best_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        # Tom M Implementation
        if maximizing_player:
            return self.maxvalue(game, depth)
        else:
            return self.minvalue(game, depth)

    def minvalue(self, game, depth):
        possible_moves = {}
        if len(game.get_legal_moves()) == 0:
            return (float('inf'), (-1, -1))
        for move in game.get_legal_moves():
            game_copy = game.forecast_move(move)
            if depth == 1:
                possible_moves[move] = self.score(game_copy, game.inactive_player)
            else:
                possible_moves[move] = self.maxvalue(game_copy, depth - 1)[0]
        best_move = min(possible_moves, key=possible_moves.get)
        return (possible_moves[best_move], best_move)

    def maxvalue(self, game, depth):
        possible_moves = {}
        if len(game.get_legal_moves()) == 0:
            return (float('-inf'), (-1, -1))
        for move in game.get_legal_moves():
            game_copy = game.forecast_move(move)
            if depth == 1:
                possible_moves[move] = self.score(game_copy, game.active_player)
            else:
                possible_moves[move] = self.minvalue(game_copy, depth - 1)[0]
        best_move = max(possible_moves, key=possible_moves.get)
        return (possible_moves[best_move], best_move)

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        # Tom M. Implementation
        legal_moves = game.get_legal_moves()

        if depth == 0 or not legal_moves:
            return self.score(game, self), (-1, -1)

        if maximizing_player:
            max_score = float('-inf')
            max_m = None
            for m in legal_moves:
                score = self.alphabeta(game.forecast_move(m), depth - 1, alpha, beta, False)[0]
                if score > max_score:
                    max_score = score
                    max_m = m
                if score >= beta:  # prune
                    return score, m
                alpha = max(alpha, score)
            return max_score, max_m

        else:  # min node
            min_score = float('inf')
            min_m = None
            for m in legal_moves:
                score = self.alphabeta(game.forecast_move(m), depth - 1, alpha, beta, True)[0]
                if score < min_score:
                    min_score = score
                    min_m = m
                if score <= alpha:  # prune
                    return score, m
                beta = min(beta, score)
            return min_score, min_m

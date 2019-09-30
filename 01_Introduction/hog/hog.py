"""CS 61A Presents The Game of Hog."""
"""
In Hog, two players alternate turns trying to be the first to end a turn with at least 100 total points.
On each turn, the current player chooses some number of dice to roll, up to 10. That player's score for the
turn is the sum of the dice outcomes.
To spice up the game, we will play with some special rules:

Pig Out. If any of the dice outcomes is a 1, the current player's score for the turn is 1.
Example 1: The current player rolls 7 dice, 5 of which are 1's. They score 1 point for the turn.
Example 2: The current player rolls 4 dice, all of which are 3's. Since Pig Out did not occur, they score 12
points for the turn.

Free Bacon. A player who chooses to roll zero dice scores one more than the largest digit in the opponent's
total score.
Example 1: If the opponent has 42 points, the current player gains 1 + max(4, 2) = 5 points by rolling zero
dice.
Example 2: If the opponent has 48 points, the current player gains 1 + max(4, 8) = 9 points by rolling zero
dice.
Example 3: If the opponent has 7 points, the current player gains 1 + max(0, 7) = 8 points by rolling zero
dice.

Hogtimus Prime. If a player's score for the turn is a prime number, then the turn score is increased to the
next larger prime number. For example, if the dice outcomes sum to 11, given that none of the dice outcomes
are 1, the current player scores 13 points for the turn. This boost only applies to the current player.
Note: 1 is not a prime number!

Perfect Piggy. If a player's score for the turn is not a 1, but is a perfect square or a perfect cube, the
player scores the turn score but swaps the normal six-sided dice with four-sided dice for all subsequent
turns. The next time either player activates Perfect Piggy, the six-sided dice will be swapped back.
Subsequent activations of Perfect Piggy will continue swapping the dice.

Swine Swap. After the turn score is added, if one of the scores is double the other, then the two scores are
swapped.
Example 1: The current player has a total score of 37 and the opponent has 92. The current player rolls two
dice that total 9. The current player's new total score (46) is half of the opponent's score. These scores
are swapped! The current player now has 92 points and the opponent has 46. The turn ends.
Example 2: The current player has 91 and the opponent has 55. The current player rolls five dice that total
17, a prime that is boosted to 19 points for the turn (Hogtimus Prime). The current player has 110, so the
scores are swapped. The opponent ends the turn with 110 and wins the game.
"""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    num_roll = 0
    sum = 0
    pig_out = False                     # Pig Out rule
    while num_roll < num_rolls:
        roll = dice()
        if roll == 1:
            pig_out = True
        sum += roll
        num_roll += 1
    if pig_out: return 1
    else: return sum
    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    digits = opponent_score
    max_digit = digits % 10             # take last digit as starting point
    while digits > 0:
        digit = digits % 10             # take last digit
        digits = digits // 10           # eliminate last digit from digits
        if digit > max_digit:
            max_digit = digit
    return max_digit + 1
    # END PROBLEM 2


def is_prime(n):
    """Return True if a number is prime and False otherwise."""
    if n == 1:
        return False
    else:
        i = 2
        while i < n:
            if n % i == 0:
                return False
            i += 1
    return True


def next_prime(n):
    """Return the next prime greater than n."""
    i = n + 1
    while not is_prime(i):
        i += 1
    return i


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime rule.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    if num_rolls == 0:                  # Free Bacon rule
        score = free_bacon(opponent_score)
    else:
        score = roll_dice(num_rolls, dice)
    if is_prime(score):                 # Hogtimus Prime rule
        score = next_prime(score)
    return score
    # END PROBLEM 2


def select_dice(dice_swapped):
    """Return a six-sided dice unless four-sided dice have been swapped in due
    to Perfect Piggy. DICE_SWAPPED is True if and only if four-sided dice are in
    play.
    """
    # BEGIN PROBLEM 3
    if dice_swapped:
        return four_sided
    else:
        return six_sided
    # END PROBLEM 3


def is_perfect_square(turn_score):
    square_root = round(pow(turn_score, 1 / 2))
    return turn_score == square_root * square_root


def is_perfect_cube(turn_score):
    cube_root = round(pow(turn_score, 1 / 3))
    return turn_score == cube_root * cube_root * cube_root


def is_perfect_piggy(turn_score):
    """Returns whether the Perfect Piggy dice-swapping rule should occur."""
    # BEGIN PROBLEM 4
    return (is_perfect_square(turn_score) or is_perfect_cube(turn_score)) and turn_score != 1
    # END PROBLEM 4


def is_swap(score0, score1):
    """Returns whether one of the scores is double the other."""
    # BEGIN PROBLEM 5
    s0_is_double_s1 = score0 // 2 == score1 and score0 % 2 == 0
    s1_is_double_s0 = score1 // 2 == score0 and score1 % 2 == 0
    return s0_is_double_s1 or s1_is_double_s0
    # END PROBLEM 5


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0:     The starting score for Player 0
    score1:     The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    dice_swapped = False # Whether 4-sided dice have been swapped for 6-sided
    # BEGIN PROBLEM 6
    def game_end():
        return score0 >= goal or score1 >= goal

    def num_rolls_for_player():
        if player == 0:
            return strategy0(score0, score1)
        else:
            return strategy1(score1, score0)

    def opponent_score():
        if player == 0:
            return score1
        else:
            return score0

    def updated_scores(score):
        if player == 0:
            return score0 + score, score1
        else:
            return score0, score1 + score

    while not game_end():
        num_rolls = num_rolls_for_player()
        score = take_turn(num_rolls, opponent_score(), select_dice(dice_swapped))
        score0, score1 = updated_scores(score)
        if is_perfect_piggy(score):     # Perfect Piggy rule
            dice_swapped = not dice_swapped
        if is_swap(score0, score1):     # Swine Swap rule
            score0, score1 = score1, score0
        player = other(player)
    # END PROBLEM 6
    return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from 0 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert 0 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the strategy
    returns a valid input. Use `check_strategy_roll` to raise an error with a
    helpful message if the strategy returns an invalid output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 7
    for score in range(0, 159):
        for opponent_score in range(0, 159):
            num_rolls = strategy(score, opponent_score)
            check_strategy_roll(score, opponent_score, num_rolls)
    # END PROBLEM 7


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    def average(*args):
        sum = 0
        for i in range(num_samples):
            sum += fn(*args)
        return sum / num_samples
    return average
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    averaged_dice = make_averaged(roll_dice, num_samples)
    max_score = 0
    result = 0
    for num_rolls in range(1, 11):
        average_turn_score = averaged_dice(num_rolls, dice)
        if average_turn_score > max_score:
            max_score = average_turn_score
            result = num_rolls
        elif average_turn_score == max_score:   # if tied, lower num rolls
            if num_rolls < result:
                max_score = average_turn_score
                result = num_rolls
    return result
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if True:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True:
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    fb_score = free_bacon(opponent_score)
    if is_prime(fb_score):              # Hogtimus Prime rule
        fb_score = next_prime(fb_score)

    if fb_score >= margin:
        return 0
    else:
        return num_rolls
    # END PROBLEM 10
check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    def is_benefical_swap():
        fb_score = free_bacon(opponent_score)
        if is_prime(fb_score):              # Hogtimus Prime rule
            fb_score = next_prime(fb_score)
        if score < opponent_score and is_swap(score + fb_score, opponent_score):
            return True
        else:
            return False

    if is_benefical_swap():
        return 0
    else:
        return bacon_strategy(score, opponent_score, margin, num_rolls)
    # END PROBLEM 11
check_strategy(swap_strategy)


def final_strategy(score, opponent_score):
    """
    1- Try force a swap (must be losing).
    2- When losing, if in proper range, try to get half score from opponent to
        increase chances for a swap in further rounds.
    3- When winning. When doubling opponent score, get conservative and try to
        avoid having and even score to reduce chances for a swap. When not dou-
        bling opponent's score, try free bacon and avoiding an even score.
    4- When not in any of the previous situations, roll 4 (best baseline strt.).
    """
    # BEGIN PROBLEM 12
    def is_odd(n):
        return n % 2 != 0

    margin = 8
    num_rolls = 4
    # 1 try to force swap
    if swap_strategy(score, opponent_score, margin, num_rolls) == 0:
        num_rolls = 0
    # 2 when losing
    elif score < opponent_score:
        # 2.1 in this range, let opponent get ahead for better chances for swap
        if 0.43 * opponent_score < score < 0.50 * opponent_score:
            num_rolls = 9   # high chances for a Pig Out
        # 2.2 baseline strategy
        else:
            num_rolls = 4
    # 3 when winning
    else:
        # 3.1 when at least doubling the opponent score, get more conservative
        if score >= opponent_score * 1.95:
            if score >= 78:
                num_rolls = 0
            else:
                margin = 6
                if bacon_strategy(score, opponent_score, margin, num_rolls) == 0:
                    fb_score = free_bacon(score)
                    if is_odd(fb_score + score):    # avoid even to reduce chance of swap
                        num_rolls = 0
                else:
                    num_rolls = round((100 - score) / 23) # por prueba y error
        # 3.2 when barely over opponent's score, stay here to avoid a bad swap
        elif opponent_score * 1.5 < score < opponent_score * 1.7:
            fb_score = free_bacon(score)
            if fb_score < 8:
                num_rolls = 0
            else:
                num_rolls = 9   # high chances for a Pig Out
        # 3.3 when winning, but not doubling opponent's score
        else:
            margin = round((100 - score) / 2)
            if bacon_strategy(score, opponent_score, margin, num_rolls) == 0:
                fb_score = free_bacon(score)
                if is_odd(fb_score + score):    # avoid even to reduce chance of swap
                    num_rolls = 0
                else:                           # more chances to get a 1 and reduce chance of swap
                    num_rolls = 10
    return num_rolls
    # END PROBLEM 12
check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()

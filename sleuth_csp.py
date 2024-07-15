from constraint import Problem, ExactSumConstraint, MinConflictsSolver
import random
from pprint import PrettyPrinter 
pp = PrettyPrinter(indent=4)

NUM_CARDS = 36
NUM_SLEUTH = 1
SELF_NAME = 'ben'
MIN_PLAYERS = 3
MAX_PLAYERS = 7
COLORS = ['red', 'yellow', 'green', 'blue']
SHAPES = ['diamond', 'opal', 'pearl']
LENGTHS = ['solitaire', 'pair', 'cluster']
SPECIAL_GROUPS = ['faceup', 'sleuth'] # Cards can be in player's hands, faceup, or be the sleuth card.

players = [SELF_NAME, 'landon', 'kay', 'joseph', 'veronica', 'amin', 'claire']
assert len(players) in range(MIN_PLAYERS, MAX_PLAYERS + 1) # Game supports 3 to 7 players.
groups = players + SPECIAL_GROUPS
num_faceup = (NUM_CARDS - NUM_SLEUTH) % len(players)
num_cards_per_player = (NUM_CARDS - NUM_SLEUTH) // len(players)


def get_vars(group_match='any', color_match='any', shape_match='any', length_match='any', get_cards=False):
    '''
    Function for outputting sequences of variable or card names.
    Both variables and cards follow the pattern of dash separated words.
    e.g. Boolean variable names for expressing whether joseph has red opals: get_vars(group_match='joseph', color_match='red')
    e.g. All the cards: get_vars(group_match='joseph', color_match='red', get_cards=True)
    '''
    if get_cards:
        if color_match == 'any':
            outputs = [color for color in COLORS]
        else:
            assert color_match in COLORS
            outputs = [color_match]

    else:
        if group_match == 'any':
            outputs = [group for group in groups]
        else:
            assert group_match in groups
            outputs = [group_match]
        
        if color_match == 'any':
            outputs = ['-'.join([output, color]) for color in COLORS for output in outputs]
        else:
            assert color_match in COLORS
            outputs = ['-'.join([output, color_match]) for output in outputs]
    
    if shape_match == 'any':
        outputs = ['-'.join([output, shape]) for shape in SHAPES for output in outputs]
    else:
        assert shape_match in SHAPES
        outputs = ['-'.join([output, shape_match]) for output in outputs]

    if length_match == 'any':
        outputs = ['-'.join([output, length]) for length in LENGTHS for output in outputs]
    else:
        assert length_match in LENGTHS
        outputs = ['-'.join([output, length_match]) for output in outputs]

    return outputs


def random_sample(sequence, num_to_remove):
    samples = random.sample(sequence, num_to_remove)
    for sample in samples:
        sequence.remove(sample)
    return samples


def deal_cards():
    undealt = get_vars(get_cards=True)
    [sleuth_card] = random_sample(undealt, NUM_SLEUTH)
    faceup_cards = random_sample(undealt, num_faceup)
    player_cards = {player: random_sample(undealt, num_cards_per_player) for player in players}
    return sleuth_card, faceup_cards, player_cards


# Variables express where the card is. 
# E.g. joseph-blue-pearl-cluster=1 means that the blue-pearl-cluster is in joseph's hand.
# Initially, all of the variables are unknown except for those starting with 'faceup-...' or 'me-...'.
all_vars = get_vars()
problem = Problem()
problem.addVariables(all_vars, [0, 1])

# CONSTRAINT Only one sleuth card:
problem.addConstraint(ExactSumConstraint(1), get_vars(group_match='sleuth'))

# CONSTRAINT Only num_faceup faceup cards:
problem.addConstraint(ExactSumConstraint(num_faceup), get_vars(group_match='faceup'))

# CONSTRAINTS Players have same number of cards:
for player in players:
    problem.addConstraint(ExactSumConstraint(num_cards_per_player), get_vars(group_match=player))

# CONSTRAINTS Every card can only be in one group:
for color in COLORS:
    for shape in SHAPES:
        for length in LENGTHS:
            problem.addConstraint(ExactSumConstraint(1), get_vars(color_match=color, shape_match=shape, length_match=length))

sleuth_card, faceup_cards, player_cards = deal_cards()

# CONSTRAINT Faceup cards are known: (adding to num_faceup means that they are all 1)
faceup_vars = [f'faceup-{card}' for card in faceup_cards]
if faceup_vars != []:
    problem.addConstraint(ExactSumConstraint(num_faceup), faceup_vars)

# CONSTRAINT Self cards are known:
problem.addConstraint(ExactSumConstraint(num_cards_per_player), [f'{SELF_NAME}-{card}' for card in player_cards[SELF_NAME]])

pp.pprint(problem.getSolution())

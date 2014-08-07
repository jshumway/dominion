from collections import namedtuple
from functools import wraps

Expansion = namedtuple('Expansion', ['id', 'title', 'cards'])

base_cards = Expansion('DO', 'Dominion', [
    'adventurer', 'bureaucrat', 'cellar', 'chancellor', 'chapel',
    'council room', 'feast', 'festival', 'gardens', 'laboratory', 'library',
    'market', 'militia', 'mine', 'moat', 'moneylender', 'remodel', 'smithy',
    'spy', 'thief', 'throne room', 'village', 'witch', 'woodcutter', 'workshop'
])

# Dominion Core is a subset of the base set. I have removed all of the cards
# that are generally ranked poorly or that I do not enjoy playing with
# (f**king Woodcutter). It retains the interesting cards like Chapel and
# Gardens.
base_core_cards = Expansion('DC', 'Dominion Core', [
    'cellar', 'chapel', 'council room', 'festival', 'gardens', 'laboratory',
    'library', 'market', 'militia', 'moneylender', 'smithy', 'throne room',
    'village', 'witch'
])

intrigue_cards = Expansion('IN', 'Intrigue', [
    'baron', 'bridge', 'conspirator', 'coppersmith', 'courtyard', 'duke',
    'great hall', 'harem', 'ironworks', 'masquerade', 'mining village',
    'minion', 'nobles', 'pawn', 'saboteur', 'scout', 'secret chamber',
    'shanty town', 'steward', 'swindler', 'torturer', 'trading post',
    'tribute', 'upgrade', 'wishing well'
])

seaside_cards = Expansion('SE', 'Seaside', [
    'ambassador', 'bazaar', 'caravan', 'cutpurse', 'embargo', 'explorer',
    'fishing village', 'ghost ship', 'haven', 'island', 'lighthouse',
    'lookout', 'merchant ship', 'native village', 'navigator', 'outpost',
    'pearl diver', 'pirate ship', 'salvager', 'sea hag', 'smugglers',
    'tactician', 'treasure map', 'treasury', 'warehouse', 'wharf'
])

prosperity_cards = Expansion('PR', 'Prosperity', [
    'bank', 'bishop', 'city', 'contraband', 'counting house', 'expand',
    'forge', 'goons', 'grand market', 'hoard', "king's court", 'loan', 'mint',
    'monument', 'mountebank', 'peddler', 'quarry', 'rabble', 'royal seal',
    'talisman', 'trade route', 'vault', 'venture', 'watchtower',
    "worker's village"
])

dark_ages_cards = Expansion('DA', 'Dark Ages', [
    'altar', 'armory', 'band of misfits', 'bandit camp', 'beggar', 'catacombs',
    'count', 'counterfeit', 'cultist', 'death cart', 'feodum', 'forager',
    'fortress', 'graverobber', 'hermit', 'hunting grounds', 'ironmonger',
    'junk dealer', 'knights', 'marauder', 'market square', 'mystic', 'pillage',
    'poor house', 'procession', 'rats', 'rebuild', 'rogue', 'sage',
    'scavenger', 'squire', 'storeroom', 'urchin', 'vagrant',
    'wandering minstrel'
])

expansion_list = [
    base_cards,
    base_core_cards,
    intrigue_cards,
    seaside_cards,
    prosperity_cards,
    dark_ages_cards,
]

expansions = {expansion.id: expansion for expansion in expansion_list}


def save(f):
    ''' Like memoize but operates on a function of no arguments. '''
    value = []

    @wraps(f)
    def wrap():
        if value == []:
            value.append(f())
        return value[0]
    return wrap


@save
def from_exp():
    ''' Return a map of a card names to expansion ids. '''

    card_from_map = {}

    for expansion in expansions.itervalues():
        for card in expansion.cards:
            card_from_map[card] = expansion.id

    return card_from_map

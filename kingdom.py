#!/usr/bin/env python

''' Randomly generate kingdoms for Dominion. '''

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import logging
import random

import blessings

import cards

exclusive_sets = [
    set(["king's court", 'throne room', 'procession']),
    set(['bishop', 'fortress']),
    set(['bandit camp', 'bazaar', 'fortress', 'mining village', 'village',
        "worker's village",'city'])
]

FAIL_THRESHOLD = 10

terminal = blessings.Terminal()

color_map = {
    'DA': terminal.bright_red,
    'DC': terminal.blue,
    'DO': terminal.blue,
    'IN': terminal.bright_magenta,
    'PR': terminal.yellow,
    'SE': terminal.green,
}


def color(expansion, string):
    return color_map[expansion](string)


def expansion_help():
    output = []

    for i, expansion in enumerate(cards.expansion_list):
        exp_string = color(
            expansion.id, '%s - %s' % (expansion.id, expansion.title))

        if not i % 2:
            output.append('\t%s\t\t' % exp_string)
        else:
            output.append('%s\n' % exp_string)

    return ''.join(output)


def display_set(kingdom, script_output):
    ''' Print out all of the cards in |kingdom|. '''

    def sort_key(card):
        return (cards.from_exp()[card], card)

    for i, card in enumerate(sorted(kingdom, key=sort_key)):
        if script_output:
            print '%s %s' % (cards.from_exp()[card], card)
        else:
            print '  %2d  %s' % (i + 1, color(cards.from_exp()[card], card))


def check_exclusive_sets(kingdom):
    for eset in exclusive_sets:
        if len(eset & kingdom) > 1:
            return False

    return True


def generate_kingdom(card_pool, kingdom_size, required):
    failures = 0

    while failures < FAIL_THRESHOLD:
        kingdom = set(random.sample(card_pool, kingdom_size))

        if not check_exclusive_sets(kingdom):
            failures += 1
            continue

        return required | kingdom

    logging.error('failed to generate a kingdom :(')


def create_kingdom(args):
    ''' Generate a random kingdom as specified by args. '''

    def parse_list_string(lstr):
        return set(s.strip() for s in lstr.split(',') if s)

    if not args.expansions:
        expansions = cards.expansions.keys()
        expansions.remove('DO')
    else:
        expansions = parse_list_string(args.expansions)

    kingdom_size = args.size
    required = parse_list_string(args.require)
    forbidden = parse_list_string(args.forbid)
    card_pool = set()

    for expansion_id in expansions:
        card_pool.update(cards.expansions[expansion_id].cards)

    card_pool.difference_update(forbidden)
    card_pool.difference_update(required)

    return generate_kingdom(card_pool, kingdom_size, required)


def main():
    help_text = '%s\n\n%s' % (__doc__.strip(), expansion_help())

    parser = ArgumentParser(
        description=help_text,
        formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument(
        'size', default=10, type=int, nargs='?',
        help='size of kingdom to generate')
    parser.add_argument(
        '-e', '--expansions', type=str, metavar='LIST',
        help='comma seperated list of expansions to draw from')
    parser.add_argument(
        '-r', '--require', type=str, default='', metavar='LIST',
        help='comma seperated list of cards to include')
    parser.add_argument(
        '-f', '--forbid', type=str, default='', metavar='LIST',
        help='comma seperated list of cards to ignore')
    parser.add_argument(
        '-s', '--script-output', action='store_true',
        help='format output in a script friendly way')

    args = parser.parse_args()
    display_set(create_kingdom(args), args.script_output)
    copper_count = random.randint(2, 5)
    print 'each player starts with %d coppers and %d estates' % (
        copper_count, 5 - copper_count)


if __name__ == '__main__':
    main()

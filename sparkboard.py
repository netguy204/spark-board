#!/usr/bin/env python

import sys
import random

GOALS = [
    "1111" +
    "1000" +
    "1000" +
    "1111",

    "1111" +
    "0010" +
    "0100" +
    "1111",

    "1000" +
    "1000" +
    "1000" +
    "1111"
]

COLORS = ['r', 'b']

# clockwise starting topleft
alternating_switches = 'rbbrrbbrrbbrrbbr'
def idx2switch(idx): return '%c%d' % ('trbl'[idx/4], idx % 4)


# row major starting top left
alternating_lights = 'rbrbbrbrrbrbbrbr'
def idx2light(idx): return '%d%d' % ((idx/4)+1, (idx%4)+1)


TRIVIAL_CONFIG = [
    (0, [0], []),
    (1, [1], []),
    (2, [2], []),
    (3, [3], []),
    (4, [4], []),
    (5, [5], []),
    (6, [6], []),
    (7, [7], []),
    (8, [8], []),
    (9, [9], []),
    (10, [10], []),
    (11, [11], []),
    (12, [12], []),
    (13, [13], []),
    (14, [14], []),
    (15, [15], [])
]

def gen_config(switches, lights, ccount=3, dcount=2):
    elights = [(i,l) for i, l in enumerate(lights)]
    config = []

    for si, switch in enumerate(switches):
        cset = []
        dset = []
d        for light in random.sample(elights, len(elights)):
            if light[1] == switch and len(cset) < ccount:
                cset.append(light)
            elif light[1] != switch and len(dset) < dcount:
                dset.append(light)
        config.append((si, [l[0] for l in cset], [l[0] for l in dset]))

    return config

def config_is_valid(config):
    actives = set()
    for s in config:
        actives = actives.union(s[1])
    return len(actives) == 16

def gen_valid_config(switches, lights, ccount=3, dcount=2):
    while True:
        c = gen_config(switches, lights, ccount, dcount)
        if config_is_valid(c): return c

def render(config, sstates):
    cset = set()
    dset = set()

    for si, switch in enumerate(sstates):
        if switch == '1':
            cset = cset.union(config[si][1])
            dset = dset.union(config[si][2])

    lights = cset.difference(dset)

    result = ['0' for i in range(16)]
    for l in lights:
        result[l] = '1'
    return ''.join(result)

def switch_configs():
    for ii in range(2**16):
        yield '{0:016b}'.format(ii)

def goals_for_config(config, goals):
    score = {}

    for sstate in switch_configs():
        r = render(config, sstate)
        if r in goals:
            if not r in score:
                score[r] = []
            score[r].append(sstate)

    return score

def config_for_goals(goals, ccount=3, dcount=2):
    while True:
        c = gen_valid_config(alternating_switches, alternating_lights, ccount, dcount)
        g = goals_for_config(c, goals)
        if g: yield c, g
        sys.stderr.write('.')
        sys.stderr.flush()

def enumerate_configs_for_goals(goals, ccount=3, dcount=2):
    for c, g in config_for_goals(goals, ccount, dcount):
        # only one goal should be achieveable
        if len(g) > 1: continue

        # the goal should have a range of non-trivial solutions
        sols = g.values()[0]
        if len(sols) > 5 or len(sols) < 2: continue

        if min([s.count('1') for s in sols]) < 3: continue

        print
        print 'config:'
        print c
        print 'goals:'
        print g


"""
config:[(0, [0, 2, 15], [12]), (1, [4, 6, 9], [5]), (2, [6, 12, 3], [15]), (3, [0, 8, 15], [4]), (4, [13, 0, 15], [6]), (5, [12, 1, 4], [10]), (6, [9, 1, 12], [0]), (7, [0, 10, 15], [9]), (8, [2, 0, 15], [11]), (9, [14, 11, 6], [2]), (10, [11, 3, 1], [7]), (11, [13, 7, 5], [6]), (12, [13, 5, 8], [11]), (13, [4, 6, 9], [2]), (14, [6, 3, 14], [10]), (15, [8, 7, 2], [1])]
goals:
{'1111100010001111': ['0100010110111010', '0100110110001010', '0100110110101010', '0100110110111010']}

config:
[(0, [7, 0, 13], [12]), (1, [9, 1, 14], [5]), (2, [11, 4, 6], [7]), (3, [2, 15, 5], [4]), (4, [8, 13, 7], [11]), (5, [4, 1, 12], [5]), (6, [9, 1, 3], [5]), (7, [7, 15, 13], [14]), (8, [5, 13, 0], [14]), (9, [9, 6, 14], [10]), (10, [9, 1, 4], [2]), (11, [13, 0, 10], [4]), (12, [8, 10, 13], [11]), (13, [1, 14, 9], [0]), (14, [1, 9, 11], [15]), (15, [8, 2, 5], [9])]
goals:
{'1111001001001111': ['0001011001010000', '0101011001010000']}


My favorite:

Looks like a C and I can drop a set of buttons to break the symmetry

config:
[
 (0, [0, 13, 7], [1]),
 (1, [12, 1, 11], [0]),
 (2, [4, 9, 3], [15]),
 (3, [5, 15, 10], [1]),
 (4, [13, 2, 8], [9]),
 (5, [4, 1, 9], [7]),
 (6, [12, 6, 4], [8]),
 (7, [15, 8, 0], [6]),
 (8, [10, 7, 15], [4]),
 (9, [9, 14, 11], [5]),
 (10, [12, 6, 9], [5]),
 (11, [8, 15, 2], [3]),
 (12, [7, 10, 8], [1]),
 (13, [3, 6, 14], [7]),
 (14, [3, 11, 9], [10]),
 (15, [13, 5, 10], [11])
]

goals:
{'1111100010001111': ['0000110100100100', '0000110100100111', '0000110101100011', '0000110101100111']}
"""


"""

Old goal set: Square, X, left slash, right slash

Interesting solutions found:

config:
[(0, [2, 8, 15, 13], [3, 1]), (1, [14, 11, 12, 3], [2, 5]), (2, [6, 12, 3, 4], [13, 15]), (3, [8, 0, 2, 10], [14, 11]), (4, [8, 15, 2, 13], [9, 14]), (5, [14, 6, 1, 11], [2, 10]), (6, [6, 12, 4, 9], [2, 0]), (7, [13, 7, 10, 2], [4, 9]), (8, [2, 7, 0, 13], [1, 6]), (9, [3, 14, 9, 6], [8, 10]), (10, [12, 4, 6, 14], [15, 5]), (11, [5, 2, 10, 13], [9, 14]), (12, [5, 13, 8, 7], [14, 6]), (13, [11, 12, 3, 9], [15, 0]), (14, [11, 6, 14, 12], [0, 8]), (15, [2, 7, 15, 5], [6, 3])]
goals:
{'0001001001001000': ['0101000001000010', '0101000001000100', '0101000001000110']}

config:
[(0, [15, 10, 13, 2], [1, 11]), (1, [11, 3, 1, 14], [15, 5]), (2, [4, 3, 11, 14], [10, 2]), (3, [2, 15, 13, 0], [1, 4]), (4, [13, 0, 8, 7], [1, 4]), (5, [6, 11, 12, 1], [7, 2]), (6, [11, 6, 12, 3], [13, 2]), (7, [7, 2, 10, 5], [11, 3]), (8, [2, 5, 8, 10], [3, 14]), (9, [12, 1, 9, 3], [7, 10]), (10, [1, 12, 3, 11], [15, 7]), (11, [2, 10, 5, 8], [12, 1]), (12, [5, 13, 2, 8], [14, 4]), (13, [9, 3, 6, 4], [0, 7]), (14, [11, 1, 14, 4], [10, 0]), (15, [8, 15, 5, 0], [9, 14])]
goals:
{'0001001001001000': ['1000001001100000', '1000011001100000', '1001001001100100', '1001011001100100']}

config:
[(0, [2, 8, 7, 0], [14, 11]), (1, [9, 3, 14, 6], [0, 2]), (2, [12, 1, 6, 9], [7, 15]), (3, [15, 10, 5, 8], [12, 4]), (4, [0, 8, 5, 7], [14, 11]), (5, [14, 11, 3, 9], [7, 0]), (6, [6, 12, 1, 14], [10, 15]), (7, [7, 10, 0, 13], [4, 9]), (8, [5, 2, 0, 13], [9, 12]), (9, [3, 6, 12, 11], [8, 7]), (10, [6, 14, 12, 9], [8, 13]), (11, [15, 2, 8, 0], [14, 9]), (12, [7, 10, 15, 2], [4, 12]), (13, [9, 3, 4, 11], [0, 10]), (14, [12, 4, 14, 11], [13, 0]), (15, [7, 13, 15, 10], [6, 14])]
goals:
{'0001001001001000': ['1100000001000000', '1100000001100000', '1100010000100000', '1100010001000000', '1100010001100000']}

config:
[(0, [7, 2, 15, 10], [11, 6]), (1, [1, 11, 9, 14], [13, 0]), (2, [6, 11, 1, 12], [2, 7]), (3, [15, 2, 13, 8], [6, 9]), (4, [0, 15, 8, 5], [9, 3]), (5, [12, 9, 1, 3], [8, 15]), (6, [3, 14, 9, 4], [7, 8]), (7, [2, 8, 10, 7], [14, 1]), (8, [13, 2, 7, 10], [1, 12]), (9, [14, 1, 9, 6], [5, 13]), (10, [11, 6, 3, 9], [7, 10]), (11, [0, 5, 8, 7], [3, 11]), (12, [8, 0, 10, 7], [11, 3]), (13, [1, 14, 11, 9], [0, 15]), (14, [11, 1, 4, 3], [13, 10]), (15, [10, 2, 5, 8], [11, 14])]
goals:
{'0001001001001000': ['0010010101100001', '0010010101100101', '0110010101100001', '0110010101100101']}


"""

#!/usr/bin/env python

import sys
import random

GOALS = [
    "1001" +
    "0110" +
    "0110" +
    "1001",

    "1111" +
    "1001" +
    "1001" +
    "1111",

    "1000" +
    "0100" +
    "0010" +
    "0001",

    "0001" +
    "0010" +
    "0100" +
    "1000"
]

COLORS = ['r', 'b']

# clockwise starting topleft
alternating_switches = 'rbbrrbbrrbbrrbbr'
def idx2switch(idx): return '%c%d' % ('trbl'[idx/4], idx % 4)


# row major starting top left
alternating_lights = 'rbrbbrbrrbrbbrbr'
def idx2light(idx): return '%d%d' % ((idx/4)+1, (idx%4)+1)

def gen_config(switches, lights, ccount=3, dcount=2):
    elights = [(i,l) for i, l in enumerate(lights)]
    config = []

    for si, switch in enumerate(switches):
        cset = []
        dset = []
        for light in random.sample(elights, len(elights)):
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

    result = ['.' for i in range(16)]
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
        if g: return c
        sys.stderr.write('.')
        sys.stderr.flush()

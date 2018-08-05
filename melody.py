from __future__ import division
import config
#import random
from numpy import random

"""
TODO
fitovani
    rytmus:
        delka na zacatku
        pocet rozdeleni ruznych typu
        pocatek a nasobic pravdepodobnosti zvoleni do vycerpani
    melodie:
evoluce
neuronka
    predat tomu radek tonu a radek delek a na to dat treba 2x3 a dal delat v 1d, nakonec udelat globalAveragePooling \
    (vyhodi prumernou hodnotu na cele vrstve do jednoho neuronu na konecne vrstve) a z toho vzit kvalitu sklatby
"""

rythm = []
melody = []

def generate():
    random.seed()
    for i in range(config.patternLen):
        rythm.append(1.0/config.patternLen)
    while len(rythm) < config.patternNoteNum:
        chance = random.random()
        choice = random.choice(range(len(rythm)), p=rythm)
        if chance < config.rythm_split_11:
            rythm.insert(choice+1, rythm[choice] / 2.0)
            rythm[choice] = rythm[choice] / 2.0
        elif chance < config.rythm_split_31:
            rythm.insert(choice+1, rythm[choice] / 4.0)
            rythm[choice] = rythm[choice] * 3.0 / 4.0

    for i in range(len(rythm)):
        rythm[i] = rythm[i] * config.patternLen

    if len(rythm) > 0:
        melody.append(0)

    for i, size in enumerate(rythm):
        if i == 0: continue
        melody.append(melody[i-1]+random.choice(config.jumps, p=config.jumpScaleWeights[melody[i-1]]))

from __future__ import division
from operator import mul
import config
# import random
from numpy import random

patterns = []
composition = []

rhythms = []
melodies = []

rhythm = []
melody = []


def generate_rhythm():
    global rhythm
    rhythm = []
    for i in range(config.patternLen):
        rhythm.append(1.0 / config.patternLen)
    while len(rhythm) < config.patternNoteNumMul * config.patternLen:
        chance = random.random()
        choice = random.choice(range(len(rhythm)), p=rhythm)
        if rhythm[choice] * config.patternLen <= config.minNoteLen: continue
        if chance < config.rhythm_split_11:
            rhythm.insert(choice + 1, rhythm[choice] / 2.0)
            rhythm[choice] = rhythm[choice] / 2.0
        else:
            rhythm.insert(choice + 1, rhythm[choice] / 4.0)
            rhythm[choice] = rhythm[choice] * 3.0 / 4.0

    for i in range(len(rhythm)):
        rhythm[i] = rhythm[i] * config.patternLen


def generate_melody():
    global melody
    melody = []
    if len(rhythm) > 0:
        melody.append(0)

    for i, size in enumerate(rhythm):
        if i == 0: continue
        melody.append(melody[i - 1] + random.choice(config.jumps, p=config.jumpScaleWeights[melody[i - 1]]))


def generate_patterns():
    for i in range(config.patternRhythmNum):
        generate_rhythm()
        rhythms.append(rhythm)
        for j in range(config.patternMelodyNum):
            generate_melody()
            melodies.append(melody)
            patterns.append([len(rhythms) - 1, len(melodies) - 1])


def generate():
    global melody
    global rhythm
    random.seed()
    generate_patterns()
    melody = []
    rhythm = []
    for i in range(int(config.overallLen / config.patternLen)):
        patternWeights = [[(config.sameRhythmWeight[b] if patterns[a][0] == patterns[composition[-(b+1)]][0] else
                               1) * (
                               config.sameMelodyWeight[b] if patterns[a][1] == patterns[composition[-(b+1)]][1] else
                               1)
                               for b in range(min(len(config.sameRhythmWeight), len(composition) + 1) - 1)]
                               for a in range(len(patterns))]
        for j in range(len(patternWeights)):
            patternWeights[j] = reduce(mul, patternWeights[j], 1)
        patternWeightsSum = sum(patternWeights)
        for j in range(len(patternWeights)):
            patternWeights[j] = patternWeights[j] / patternWeightsSum
        composition.append(random.choice(range(len(patterns)), p=patternWeights))
        rhythm.extend(rhythms[patterns[composition[-1]][0]])
        melody.extend(melodies[patterns[composition[-1]][1]])
    print composition


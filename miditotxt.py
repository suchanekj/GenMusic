import midi
import os
from numpy import random
import config


# pattern = midi.read_midifile("output.mid")
# print pattern[1]

outputcounter = 1

quality = []

def makerandom(target):
    global outputcounter
    global quality
    hmin = 21
    hmax = 108  # standard piano range
    output = [[-1 for x in range(config.patternLen * 16 * config.overallLen)] for y in range(hmax - hmin + 1)]
    for i in range(len(output)):
        value = 0.0
        for j in range(len(output[0])):
            if random.random() < 0.05 and value == 0: value = 1.0
            elif random.random() < 0.2 and value == 1: value = 0.0
            output[i][j] = value
    f = open(target + "%d.txt" % outputcounter, "w+")
    outputcounter += 1
    quality.append(0)
    for i in output:
        f.write(','.join(map(str, i)))
        f.write("\n")

def rewrite(source, target):
    global outputcounter
    global quality
    hmin = 21
    hmax = 108  # standard piano range
    pattern = midi.read_midifile(source)
    for a in range(1000):
        endoftrack = 0
        output = [[-1 for x in range(config.patternLen*16*config.overallLen)] for y in range(hmax-hmin+1)]
        for i in pattern:
            foundnote = 0
            time = 0
            for j in i:
                time += j.tick
                if (time - a * 1920 * 12) < 0: continue
                if (time - a * 1920 * 12) >= 120 * len(output[0]): break
                if type(j) is midi.EndOfTrackEvent:
                    if foundnote == 1:
                        endoftrack = 1
                    break
                if type(j) is midi.NoteOnEvent:
                    foundnote = 1
                    output[j.data[0]-hmin][(time - a * 1920 * 12)/120] = j.data[1] / 100.0
                if type(j) is midi.NoteOffEvent:
                    foundnote = 1
                    output[j.data[0]-hmin][(time - a * 1920 * 12)/120] = (100 - j.data[1]) / 100.0
            if endoftrack == 1: break
        if endoftrack == 1: break
        for i in range(len(output)):
            value = 0.0
            for j in range(len(output[0])):
                if output[i][j] < 0:
                    output[i][j] = value
                else:
                    value = output[i][j]
        f = open(target + "%d.txt" % outputcounter, "w+")
        outputcounter += 1
        quality.append(1)
        for i in output:
            f.write(','.join(map(str, i)))
            f.write("\n")


def makecorpus():
    if not os.path.exists("pianotxt/"):
        os.makedirs("pianotxt/")
    for i in range(len([name for name in os.listdir('pianomidi/') if os.path.isfile('pianomidi/' + name)])):
        rewrite("pianomidi/%d.mid" % (i+1), "pianotxt/")
        for j in range(int(random.random()*10) + 1): makerandom("pianotxt/")
        print i
    f = open("pianotxt/quality.txt", "w+")
    for i in quality:
        f.write("%d\n" % i)


makecorpus()

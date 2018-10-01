import mido
import os
from numpy import random
import config
import melody
import write


# pattern = midi.read_midifile("output.mid")
# print pattern[1]

outputcounter = 1

quality = []

def makerandom(target):
    global quality
    ind = []
    for i in range(config.IND_SIZE):
        ind.append(random.random())
    config.listToConfig(ind)
    config.init()
    melody.generate()
    write.write([melody.melody], [melody.rhythm])
    # print sum(melody.rhythm)
    rewrite("output.mid",target,0)


def rewrite(source, toSave=0, target="", q=-1):
    global outputcounter
    global quality
    hmin = 21
    hmax = 108  # standard piano range
    mid = mido.MidiFile(source)
    pattern = mid.tracks
    for a in range(1000):
        endoftrack = 0
        output = [[-1 for x in range(16*config.overallLen)] for y in range(hmax-hmin+1)]
        foundnote = 0
        for i in pattern:
            foundnote = 0
            time = 0
            for j in i:
                time += j.time
                if (time - a * 1920 * 12) < 0: continue
                if (time - a * 1920 * 12) >= config.notetomiditime * len(output[0]): break
                if j.type == 'end_of_track':
                    if foundnote == 1:
                        endoftrack = 1
                    break
                if j.type == 'note_on':
                    foundnote = 1
                    output[int(j.note-hmin)][int((time - a * 1920 * 12)/config.notetomiditime)] = j.velocity / 100.0
                if j.type == 'note_off':
                    foundnote = 1
                    output[int(j.note-hmin)][int((time - a * 1920 * 12)/config.notetomiditime)] = (100 - j.velocity) / 100.0
            if endoftrack == 1: break
        if endoftrack == 1: break
        for i in range(len(output)):
            value = 0.0
            for j in range(len(output[0])):
                if output[i][j] < 0:
                    output[i][j] = value
                else:
                    value = output[i][j]
        if(toSave):
            save(output, target, q)
        else:
            return output


def save(output, target, q):
    if q < 0:
        f = open(target, "w+")
    else:
        f = open(target + "%d.txt" % outputcounter, "w+")
        outputcounter += 1
        quality.append(q)
    for i in output:
        f.write(','.join(map(str, i)))
        f.write("\n")


def makecorpus():
    if not os.path.exists("pianotxt/"):
        os.makedirs("pianotxt/")
    for i in range(len([name for name in os.listdir('pianomidi/') if os.path.isfile('pianomidi/' + name)])):
        rewrite("pianomidi/%d.mid" % (i+1), 1, "pianotxt/", 1)
        for j in range(int(random.random()*10) + 1): makerandom("pianotxt/")
        print(i)
    f = open("pianotxt/quality.txt", "w+")
    for i in quality:
        f.write("%d\n" % i)


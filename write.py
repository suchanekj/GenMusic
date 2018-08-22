#!/usr/bin/env python

from midiutil import MIDIFile
import config


def write(melodies, rhythms):
    degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 0.5  # In beats
    tempo    = 60   # In BPM
    volume   = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                          # automatically)
    for i, instrument in enumerate(config.instruments):
        MyMIDI.addProgramChange(0, i, 0, instrument)
    MyMIDI.addTempo(track, time, tempo)

    for i, pitch in enumerate(melodies[0]):
        melodies[0][i] = melodies[0][i] + config.tone0
        MyMIDI.addNote(track, channel, melodies[0][i], time, rhythms[0][i], volume)
        time += rhythms[0][i]
        # print rhythms[0][i]

    with open("output.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)
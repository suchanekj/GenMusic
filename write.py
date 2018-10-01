import time
from midiutil import MIDIFile
import config


def write(melodies, rhythms):
    global tim
    global MyMIDI
    tim -= time.process_time()
    degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
    track    = 0
    channel  = 0
    starttime     = 0    # In beats
    duration = 0.5  # In beats
    tempo    = 60   # In BPM
    volume   = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                          # automatically)
    for i, instrument in enumerate(config.instruments):
        MyMIDI.addProgramChange(0, i, 0, instrument)
    MyMIDI.addTempo(track, starttime, tempo)

    # print len(melodies[0])
    # print len(rhythms[0])
    for i, pitch in enumerate(melodies[0]):
        melodies[0][i] = melodies[0][i] + config.tone0
        MyMIDI.addNote(track, channel, melodies[0][i], starttime, rhythms[0][i], volume)
        starttime += rhythms[0][i]
        # print rhythms[0][i]

    tim += time.process_time()

def save():
    with open("output.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)


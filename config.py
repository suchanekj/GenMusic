from __future__ import division

# fittable
channels = 1
instruments = [1]
rythm_split_11 = 0.8
rythm_split_31 = 0.2 # must add up to one
patternLen = 4
patternNoteNum = patternLen * 4
scaleWeights = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
jumpWeights = [  1,   1,   1,  1,  1,  1,  2,  2,  3,  3,  4,  4, 1, 4, 4, 3, 3, 2, 2, 1, 1, 1,  1,  1,  1]
minTone = -12
maxTone = 12
patternRhythmNum = 3
patternMelodyNum = 3
overallLen = 12  # in number of patterns
sameRhythmWeight = [1, 1, 3, 2]  # no, as 1 ago, as 2 ago..., first one MUST be 1
sameMelodyWeight = [1, 0, 2, 1]  # no, as 1 ago, as 2 ago..., must be same length as sameRhythmWeight

# constants
tone0 = 60
jumps =       [-12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
scaleLen = len(scaleWeights)
minNoteLen = 1/16


# edit the probabilities to sum to 1
# jumpWeightsSum = sum(jumpWeights)
# for i in range(len(jumpWeights)):
#     jumpWeights[i] = jumpWeights[i] / jumpWeightsSum
#
# scaleWeightsSum = sum(scaleWeights)
# for i in range(len(scaleWeights)):
#     scaleWeights[i] = scaleWeights[i] / scaleWeightsSum


# create jump probabilities
scaleWeights3 = scaleWeights + scaleWeights + scaleWeights
jumpScaleWeights = []
for i in range(maxTone - minTone + 1):
    jumpScaleWeights.append([a*b*(1 if i + c >= 0 and i + c + minTone <= maxTone else 0) for a,b,c in
                    zip(jumpWeights,scaleWeights3[((i+minTone) % scaleLen) : ((i+minTone) % scaleLen)+2*scaleLen+1], jumps)])
    jumpScaleWeightsSum = sum(jumpScaleWeights[i])
    # print("sum: " + repr(jumpScaleWeightsSum))
    # print("i: " + repr(i))
    for j in range(len(jumpScaleWeights[i])):
        # print(jumpScaleWeights[i][j])
        jumpScaleWeights[i][j] = jumpScaleWeights[i][j] / jumpScaleWeightsSum

from music21 import *
import random

def createDict(fileName):
    """Gets musicXML file name and create a dictionary from it
       here the key is the Chord and the value is sequence of notes play while chord plays

    Parameter
    ----------
    fileName : str
        The file name of the musicXML file with suffix (.xml)

    Returns
    -------
    dict
        a dictionary where the key is the Chord
        and the value is sequence of notes play while chord plays
    """

    dict = {}
    myScore = converter.parse(fileName)
    for inx in range(len(myScore.recurse().notes)):
        item = myScore.recurse().notes[inx]
        seq = []
        j = 0
        if isinstance(item, chord.Chord):
            figure = item.figure
            notes = myScore.recurse().notes[inx + 1:]
            while (j < len(notes)):
                if not isinstance(notes[j], chord.Chord):
                    seq.append(notes[j])
                    j += 1
                else:
                    break

            if figure in dict:
                dict[figure].append(seq)
            else:
                dict[figure] = [seq]
    return dict

def swap(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


dict = createDict('Anthropology.xml')
# print(dict)

# Convert Duration into str of number
def durationToInt(d):
    if d == 'Half':
        return '0.5'
    if d == 'Quarter':
        return '0.25'
    if d == 'Eighth':
        return '0.125'

# Calculate each seq duration in dict values
#for k in dict.keys():
chordDuration = []
for i in list(dict.values())[1]:
    duration = 0
    for item in i:
       #  if it is a note
       if isinstance(item,note.Note):
           duration = duration + float(item.quarterLength)

       else:  # if it is a Rest
           if durationToInt(item.duration.fullName) is not None:
            duration = duration + float(durationToInt(item.duration.fullName))
    chordDuration.append(duration)

#print(chordDuration)
# [4.0, 4.0, 3.625, 2.875, 4.0, 1.625, 3.625, 2.5, 3.25, 4.0, 4.0, 2.5, 3.625, 2.0, 0.5, 4.0, 2.875, 4.0, 4.0, 1.833333333333333, 2.5, 4.0, 4.0, 4.0, 1.25, 2.875, 2.125, 4.0, 4.0, 2.0, 2.125, 4.0]
randIndx = random.randint(1,len(list(dict.values())[0]))

# seqBm = list(dict.values())[1]
# print(seqBm)
# sortedSeq = sorted(chordDuration,reverse= True)
# maxSeq = max(chordDuration)
# maxIndex = chordDuration.index(maxSeq)
# halfDurationIndex = chordDuration.index(maxSeq/2)
#
# if halfDuration == None:
#     # swap max duration chord with min Duration and add suitable notes
#     minSeq = min(chordDuration)
#     minIndex = chordDuration.index(minSeq)
# else:
#     newMelody = [chordDuration[halfDurationIndex] chordDuration[halfDurationIndex]]
#     improvisation = swap(chordDuration[halfDurationIndex] , chordDuration[maxIndex])
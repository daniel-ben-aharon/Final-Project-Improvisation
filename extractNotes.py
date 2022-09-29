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
    chordOrder = []
    dict = {}
    myScore = converter.parse(fileName)
    for inx in range(len(myScore.recurse().notesAndRests)):
        item = myScore.recurse().notesAndRests[inx]
        seq = []
        j = 0
        if isinstance(item, chord.Chord):
            figure = item.figure
            chordOrder.append(figure)
            notes = myScore.recurse().notesAndRests[inx + 1:]
            while j < len(notes):
                if not isinstance(notes[j], chord.Chord):
                    seq.append(notes[j])
                    j += 1
                else:
                    break

            if figure in dict:
                dict[figure].append(seq)
            else:
                dict[figure] = [seq]
    return dict,chordOrder


#charlie1 = converter.parse('Anthropology.xml')
filename = 'Anthropology.xml'
dictionary, chordsByOrder = createDict(filename)

# val1 = list(dict.values())[0]
#
# seq1Val1 = val1[0]
#
# for note in seq1Val1:
#     print(note)


# Convert Duration into str of number
def durationToInt(d):
    if d == 'Half':
        return '0.5'
    if d == 'Quarter':
        return '0.25'
    if d == 'Eighth':
        return '0.125'



#Calculate each seq duration in dict values
keysDurations = []

# for each key
for k in list(dictionary.keys()):
    chordDuration = []
    # for each sequence
    for seq in dictionary[k]:
        # calculate duration of each sequance
        seqDuration = 0
        for item in seq:
            #  if it is a note
            if isinstance(item, note.Note):
                seqDuration = seqDuration + float(item.quarterLength)

            # if it is a Rest
            else:
              if durationToInt(item.duration.fullName) is not None:
                seqDuration = seqDuration + float(durationToInt(item.duration.fullName))
        chordDuration.append(seqDuration)
    #
    # create list of list duration of each sequence in each key
    keysDurations.append(chordDuration)


for l in list(keysDurations):
   print(l)
# [4.0, 4.0, 3.625, 2.875, 4.0, 1.625, 3.625, 2.5, 3.25, 4.0, 4.0, 2.5, 3.625, 2.0, 0.5, 4.0, 2.875, 4.0, 4.0, 1.833333333333333, 2.5, 4.0, 4.0, 4.0, 1.25, 2.875, 2.125, 4.0, 4.0, 2.0, 2.125, 4.0]
# randIndx = random.randint(1,len(list(dict.values())[0]))

# for d in chordDuration[1:]:
#     if chordDuration[0] == d
#         #  swap sequences
#
#
# seqBm = list(dict.values())[1]
# print(seqBm)

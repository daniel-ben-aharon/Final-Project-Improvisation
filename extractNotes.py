import re                 # for regular expressions
import mysql.connector
from music21 import *
import random
import xml.etree.ElementTree as et
import time    # for extimate runtime of the algorithm

# Each time we add a musicXML file we add its data to our dictionary
def add2Dict(dictionary, file_content):
    """Gets musicXML file name and create a dictionary from it
       here the key is the Chord and the value is sequence of notes play while chord plays

    Parameter
    ----------
    dictionary : dictionary
        A dictionary

    file_content:  str
         File content
    """

    myScore = converter.parse(file_content)

    for inx in range(len(myScore.recurse().notesAndRests)):
        item = myScore.recurse().notesAndRests[inx]
        seq = []
        j = 0
        if isinstance(item, chord.Chord):
            chordOrder.append(item)

            figure = item.figure
            notes = myScore.recurse().notesAndRests[inx + 1:]
            while j < len(notes):
                if not isinstance(notes[j], chord.Chord):
                    seq.append(notes[j])
                    j += 1
                else:
                    break

            if figure in dictionary:
                dictionary[figure].append(seq)
            else:
                dictionary[figure] = [seq]



# The function return chordOrder of a given musicXML file
def getChordOrder(xmlfileContent):
    chordOrder = []
    myScore = converter.parse(xmlfileContent)

    for inx in range(len(myScore.recurse().notes)):
        item = myScore.recurse().notesAndRests[inx]
        if isinstance(item, chord.Chord):
            chordOrder.append(item)
    return chordOrder


# The function implement the improvisation algorithm
def improvise(file_name,dictionary,file_content='', speed=150):

    # Beginning of the program
    st = time.time()

    chordOrder = getChordOrder(file_content)
    # Calculate each seq duration in dict values
    durationDict = {}
    keyDurationsDict = {}
    # for each key
    for k in list(dictionary.keys()):
        chordDuration = []
        # for each sequence
        for seq in dictionary[k]:
            # calculate duration of each sequence
            seqDuration = 0
            for item in seq:
               seqDuration = seqDuration + float(item.duration.quarterLength)

            chordDuration.append(seqDuration)

        # create list of list duration of each sequence in each key
        keyDurationsDict[k] = chordDuration

    #print(f"keyDurationsDict: {keyDurationsDict}")
    improvise_stream = stream.Stream()
    improvise_stream.append(tempo.MetronomeMark(number=speed))

    # update title name
    original_title = file_name.split(".")[0]
    improvise_stream.insert(0, metadata.Metadata())
    improvise_stream.metadata.title = 'Improvised - ' + original_title

    improvise_stream.insert(0, metadata.Metadata())
    improvise_stream.metadata.composer = " "  # we should change it to modulary

    # configure.run()  ## To use show() method - run this function once, choose No options and then put it on comment in next time

    # chosen_chord = list(dictionary.keys())[chosen_chord_Indx]

    # run over all chord of the original musicXML file by order
    currentChordIndx = 0
    idx = 1
    #print(f"dictionary: {dictionary}")
    # loop over all chords in chosen file by order
    # for c in chordOrder:

    for c in chordOrder:

       indexesSameDuration = []
       currentSeqDurationList = []
       # add Chord sign to the improvised music sheet
       improvise_stream.append(c)

       # gets Chord short name: 'F7', 'B-' etc.
       chordName = c.figure


       currentSeqDurationList = keyDurationsDict[chordName]

       #  create array of all sequence last as current sequence
    # if len(keyDurationsDict[chordName]) == 1:
    #     rand_indx = 0

    # else:
       for seqDur in keyDurationsDict[chordName][1:]:
           if seqDur == keyDurationsDict[chordName][0]:
               indexesSameDuration.append(idx)
           idx += 1

       # pick random index of sequence with same duration
       rand_indx = random.randint(0, len(indexesSameDuration) - 1)

       # copy a suitable random seq to output stream
       for item in (dictionary[chordName])[rand_indx]:
           improvise_stream.append(item)

       # delete original sequence
       del dictionary[chordName][rand_indx]
       del keyDurationsDict[chordName][rand_indx]

    # End of the program
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    print('Execution time:', elapsed_time / 60, 'minutes')

    # Show the improvised music sheet (in musescore3)
    improvise_stream.show()

    # Show the improvised music sheet (in musescore3)
    ################# how do we know temp_file_name is the improve file?##############
    temp_file_name = 'temp.musicxml'
    improvise_stream.write('musicxml', temp_file_name)
    temp_file = open(temp_file_name, 'r')
    file_content = temp_file.read()
    updated = file_content.replace('<part-name />', '<part-name>p</part-name>')

    return updated, dictionary

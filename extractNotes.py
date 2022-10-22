import re                 # for regular expressions
import mysql.connector
from music21 import *
import random
import xml.etree.ElementTree as et
import time    # for extimate runtime of the algorithm

# Each time we add a musicXML file we add its data to our dictionary
def addToDict(dictionary, file_content):
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

    for inx in range(len(myScore.recurse().notesAndRests)):
        item = myScore.recurse().notesAndRests[inx]
        if isinstance(item, chord.Chord):
            chordOrder.append(item)
    return chordOrder

# function get dict of xmlfile where (key, value) = (Chord, seq)
# and return dict of duration where (key, value) = (Chord, list(seq_duration) )
def createDurationDict(mydict):
    keyDurationsDict = {}

    # for each key
    for k in mydict.keys():
        chordDuration = []
        # for each sequence
        for seq in mydict[k]:
            # calculate duration of each sequence
            seqDuration = 0
            for item in seq:
               seqDuration = seqDuration + float(item.duration.quarterLength)

            chordDuration.append(seqDuration)

        # create list of duration of each sequence in each key
        if chordDuration is not None:
             keyDurationsDict[k] = chordDuration

    return keyDurationsDict

# The function implement the improvisation algorithm
def improvise(file_name,dictionary,file_content='', speed=150):

    # # Beginning of the program
    st = time.time()
    temp_dict = dictionary        # use a copy of big dictionary

    file_to_improvised_dict = {}
    addToDict(file_to_improvised_dict, file_content)  # create dictionary of file to improvise on

    # Calculate each seq duration in original dictionary values and chosen file
    chosenFileDurationDict = createDurationDict(file_to_improvised_dict)
    oldDurationDict =  createDurationDict(temp_dict)

    improvise_stream = stream.Stream()
    improvise_stream.append(tempo.MetronomeMark(number=speed))

    # update title name
    original_title = file_name.split(".")[0]
    improvise_stream.insert(0, metadata.Metadata())
    improvise_stream.metadata.title = 'Improvised - ' + original_title

    improvise_stream.insert(0, metadata.Metadata())
    improvise_stream.metadata.composer = " "  # we should change it to modulary

    # configure.run()  ## To use show() method - run this function once, choose No options and then put it on comment in next time

    chordOrder = getChordOrder(file_content)       # get chordOrder of file to improvise on

    # run over all chord of the original musicXML file by order
    for c in chordOrder:
       # temp variables
       idx = 0
       indexesSameDuration = []      # list of all indexes in big dict with same duration as current seq
       currentSeqsDurationList = []

       # add Chord sign to the improvised music sheet
       improvise_stream.append(c)

       # gets Chord short name: 'F7', 'B-' etc.
       chordName = c.figure

       currentSeqsDurationList = chosenFileDurationDict[chordName]
       currentSeqDuration = currentSeqsDurationList[0]

       for seqDur in oldDurationDict[chordName]:
           if seqDur == currentSeqDuration:
               indexesSameDuration.append(idx)
           idx += 1

       #pick random index of sequence with same duration
       if len(indexesSameDuration) > 1:
            rand_indx = indexesSameDuration[random.randint(0, len(indexesSameDuration) - 1)]

       else:
           # chose the same sequence as original file
           rand_indx = 0

       # copy a suitable random seq to output stream
       for item in (temp_dict[chordName])[rand_indx]:
           improvise_stream.append(item)

       # delete original sequence
       del chosenFileDurationDict[chordName][0]
       del file_to_improvised_dict[chordName][0]

       # delete seq from copy dict
       del temp_dict[chordName][rand_indx]
       del oldDurationDict[chordName][rand_indx]

    # End of the program
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')

    # Show the improvised music sheet (in musescore3)
    improvise_stream.show()

    # Show the improvised music sheet (in musescore3)
    ################# how do we know temp_file_name is the improve file?##############
    temp_file_name = 'temp.musicxml'
    improvise_stream.write('musicxml', temp_file_name)
    temp_file = open(temp_file_name, 'r')
    file_content = temp_file.read()
    updated = file_content.replace('<part-name />', '<part-name>p</part-name>')

    return updated

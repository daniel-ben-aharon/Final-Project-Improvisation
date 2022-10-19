import re                 # for regular expressions
import mysql.connector
from music21 import *
import random
import xml.etree.ElementTree as et
import time

#  To load dictionary:
# with open('mydict.txt') as f:
#     lines = f.readlines()
#
# dictionary = ((str(lines))[2:len(lines)-3])

dictionary = {}
chordOrder = []
durations_dictionary = {}

# Each time we add a musicXML file we add its data to our dictionary
def add2Dict(file_content, file_name, chosen_file_name):
    """Gets musicXML file name and create a dictionary from it
       here the key is the Chord and the value is sequence of notes play while chord plays

    Parameter
    ----------
    chosen_file_name : str
        The file name of the musicXML file to improvised on with a suffix (.xml)

    file_content:  str
         File content
    """

    myScore = converter.parse(file_content)

    for inx in range(len(myScore.recurse().notesAndRests)):
        item = myScore.recurse().notesAndRests[inx]
        seq = []
        j = 0
        if isinstance(item, chord.Chord):
            if file_name == chosen_file_name:
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
                dictionary[figure] = [seq]    # tuple([seq],file_name)


def improvise(file_name,file_content='', speed=150):
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
    improvise_stream.insert(0, metadata.Metadata())
    improvise_stream.metadata.title = 'Improvised - ' + chosen_file_name

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
    print('Execution time:', elapsed_time, 'seconds')

    # Show the improvised music sheet (in musescore3)
    improvise_stream.show()

# Show the improvised music sheet (in musescore3)
    ################# how do we know temp_file_name is the improve file?##############
    # temp_file_name = 'temp.musicxml'
    # improvise_stream.write('musicxml', temp_file_name)
    # temp_file = open(temp_file_name, 'r')
    # file_content = temp_file.read()
    # updated = file_content.replace('<part-name />', '<part-name>p</part-name>')
    #
    # return updated, dictionary

if __name__ == '__main__':

    # Beginning of the program
    st = time.time()

    riginal_dict = {}
    dictForImprovisation = {}  # the big dict compose all

    mydb = mysql.connector.connect(host="localhost", user="root", passwd="danielmysql123benaharondb#&12*-a",database="userdb")
    db_cursor = mydb.cursor()
    query1 = 'SELECT id FROM xmltable ORDER BY ID DESC LIMIT 1'
    db_cursor.execute(query1)
    last_id = db_cursor.fetchall()[0][0]

    chosen_file_name = 'Anthropology.xml'   # arbitrary
    #title_music_sheet = chosen_file_name.split(".")[0]
    chose_file_id = 2
    #create temp dict of chosen original file
    query = f'SELECT XML from xmltable WHERE id=2'
    db_cursor.execute(query)
    r_xml = db_cursor.fetchall()[0]
    ifile_content = ""
    for row in r_xml:
        ifile_content += "" + str(row)
    add2Dict(ifile_content, chosen_file_name, chosen_file_name)

    #  run over all files in corpus except chosen one
    for i in range(1, last_id + 1):
        if i == chose_file_id:
            continue
        query2 = f'SELECT XML from xmltable WHERE id={i}'
        db_cursor.execute(query2)
        xml = db_cursor.fetchall()[0]
        file_content = ""
        file_name = ""
        for row in xml:
            file_name = re.search('<work-title>(.*)</work-title>', row).group(1)
            file_content += "" + str(row)

        add2Dict(file_content, file_name, chosen_file_name)

        #dictForImprovisation = {**dictForImprovisation, **newDict}   # merge dicts

    improvise(chosen_file_name, ifile_content)
    #result = improvise(file_name, file_content)

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
            chordOrder.append(item)
            figure = item.figure
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

filename = 'Anthropology.xml'      # better recieve file's name from the user to prevent error code
dictionary, chordsByOrder = createDict(filename)

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

    # create list of list duration of each sequence in each key
    keysDurations.append(chordDuration)


###########################################################################################
####################### get a chord by the user  ##########################################
chosen_chord_Indx = 0    # by default for our improvisation algorithm

#######################################################################################################
##  lines 89-90, 104-105, 108 in comment - if we chose random sequence from all the possible options
#######################################################################################################

# locs = []    ## if we pick a random index
# chosen chord
for i in range(len(keysDurations[chosen_chord_Indx])):
     item = (keysDurations[chosen_chord_Indx])[i]
     try:
         loc =  (keysDurations[chosen_chord_Indx]).index(item,i+1)
     except ValueError:
         pass
     else:
         if loc is not None:
            swap_l = i       # first occurence seq - left index to swap
            swap_r = loc     # second occurence seq - right index to swap
            # if we pick randomly index
            # loc.append(loc)
            break

# randIndx = locs[random.randint(0,locs)]  # pick one sequence randomally


improvise_stream = stream.Stream()

#####################################################################################
#   Following code Lines Test show method only
#####################################################################################

#configure.run()  ## To use show() method - run this function once, choose No options and then put it on comment in next time

chosen_chord = list(dictionary.keys())[chosen_chord_Indx]
print(chosen_chord)

i = 0    # index of seq of chosen_chord

# # run over all chord of the original musicXML file by order
for c in chordsByOrder:

    # add Chord sign to the improvised music sheet
    improvise_stream.append(c)

    # gets Chord short name:  'F7', 'B-' etc.
    chordName = c.figure

    # copy the non-improvise parts the same as original
    if chordName != chosen_chord:
         # copy the suitable sequence
         for item in (dictionary[chordName])[0]:
            improvise_stream.append(item)

         # delete it from original dict to copy from
         del (dictionary[chordName])[0]


     # if we reached to the improvised chord
    else:
        #  swap the sequence to improvise
        if i == swap_l:
            # copy the suitable sequence
            for item in (dictionary[chordName])[swap_r]:
                improvise_stream.append(item)
            i += 1

        elif i == swap_r:
            # copy the suitable sequence
            for item in (dictionary[chordName])[swap_l]:
                improvise_stream.append(item)
            i += 1

        else:
            # copy the suitable sequence
            for item in (dictionary[chordName])[i]:
                improvise_stream.append(item)
            i += 1

# Show the improvised music sheet (in musescore3)
improvise_stream.show()

from music21 import *
import random


def createDict(file_name, file_content):
    """Gets musicXML file name and create a dictionary from it
       here the key is the Chord and the value is sequence of notes play while chord plays

    Parameter
    ----------
    file_name : str
        The file name of the musicXML file with suffix (.xml)

    file_content:  str
         File content
         
    Returns
    -------
    dict
        a dictionary where the key is the Chord
        and the value is sequence of notes play while chord plays
        
    chordByOrder:  list
        list of all music file's chords by the original order
    """
    chordOrder = []
    dict = {}
    myScore = converter.parseData(file_content)
    tempo_f = myScore.getElementsByClass('tempo.MetronomeMark')

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

# Convert Duration into str of number
def durationToInt(d):
    if d == 'Half':
        return '0.5'
    if d == 'Quarter':
        return '0.25'
    if d == 'Eighth':
        return '0.125'


def improvise(file_name, file_content = ''):
  #Calculate each seq duration in dict values
  dictionary, chordsByOrder = createDict(file_name, file_content)
  title_music_sheet = file_name.split(".")[0]
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
  chosen_chord_Indx = 0  # by default for our improvisation algorithm




    #######################################################################################################
    ##  lines 101, 113-114, 117 in comment - if we chose random sequence from all the possible options
    #######################################################################################################
  # chosen chord
  for i in range(len(keysDurations[chosen_chord_Indx])):
      item = (keysDurations[chosen_chord_Indx])[i]
      try:
          loc = (keysDurations[chosen_chord_Indx]).index(item, i + 1)
      except ValueError:
          pass
      else:
          if loc is not None:
              swap_l = i  # first occurence seq - left index to swap
              swap_r = loc  # second occurence seq - right index to swap
              # if we pick randomly index
              # loc.append(loc)
              break

  # randIndx = locs[random.randint(0,locs)]  # pick one sequence randomally


  improvise_stream = stream.Stream()

  # another parameter improvisation - fast
  #improvise_stream.append(tempo.MetronomeMark(number=150))
  #improvise_stream.append(old_tempo)
  # update title name
  improvise_stream.insert(0, metadata.Metadata())
  improvise_stream.metadata.title = 'Improvised - ' + title_music_sheet

  improvise_stream.insert(0, metadata.Metadata())
  improvise_stream.metadata.composer = " "  # we should change it to modulary
  # configure.run()  ## To use show() method - run this function once, choose No options and then put it on comment in next time

  chosen_chord = list(dictionary.keys())[chosen_chord_Indx]

  indx = 0  # index of seq of chosen_chord
  # swap_l = 0
  # swap_r = 0
  # run over all chord of the original musicXML file by order
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
          if indx == swap_l:
              # copy the suitable sequence
              for item in (dictionary[chordName])[swap_r]:
                  improvise_stream.append(item)
              indx += 1

          elif indx == swap_r:
              # copy the suitable sequence
              for item in (dictionary[chordName])[swap_l]:
                  improvise_stream.append(item)
              indx += 1

          else:
              # copy the original sequences from musicXML file
              for item in (dictionary[chordName])[indx]:
                  improvise_stream.append(item)
              indx += 1

  # Show the improvised music sheet (in musescore3)
  temp_file_name = 'temp.musicxml'
  improvise_stream.write('musicxml', temp_file_name)
  temp_file = open(temp_file_name, 'r')
  file_content = temp_file.read()
  return file_content
  
  

#######################################################################################################################
##################################  Test improvise function  ##########################################################
#######################################################################################################################

if __name__ == '__main__':
    file_name = 'Another_Hairdo.xml'      # better recieve file's name from the user to prevent error code
    file = open(file_name, 'r')
    file_content = file.read()
    result = improvise(file_name, file_content)
    print(result)

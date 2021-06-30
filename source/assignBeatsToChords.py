# Calculate Bars for each Chord

# Imports

import os
import sys

import numpy as np

from rdflib import Graph


# Define paths for Beat and Chords

chord_folder = "/Beatles/chordlab/The_Beatles"
beat_folder = "/Beatles/beat/The_Beatles"


"""
Define a class for track Info:
    --> Model: {
        title: # Type str(),
        chords: chord # Type List of dict(),
        zero_ration: # Type int(),
        
        ...        
        }
    
    --> chord Object: A python dictionary with records:
            {
                "chord_id":String, 
                "chord":String, 
                "start":Float, 
                "end":Float, 
                "duration":Float, 
                "m__type":String, 
                "m_duration":ListOfStrings
            } 
    
"""

#
# Class Song Additional Info
class SongInfo:
    #
    def __init__(self, title, chords, zero_ratio, beats):
        self.title = title
        self.chords = chords
        self.zero_ratio = zero_ratio
        self.beats = beats


#
# Analyzer
def beatAndChords(f1, f2, song):

    """
    Read .txt files into python dictionaries
    f1: beats
    f2: chords
    song: title
    """


    beats = []	# list of objects
    dict_a = {}	# beat object

    f1 = open(f1,"r")
    for line in f1:
        currentline=line.split()
        beat=dict_a.copy()
        beat["beat"] = currentline[1]
        beat["start"] = float(currentline[0])
        if beats:
            beat["duration"] = beat["start"]-beats[len(beats)-1]["start"]
        else:
            beat["duration"] = 0.0
        beats.append(beat)

    # beat mean duration
    b_mean_duration = sum(b["duration"] for b in beats) / len(beats)

    # Measure Zones for beats
    b_zones = beatRateZone(beats)



    # Beat Variance

    chords = []
    dict_b = {
        "chord_id":" Undefined"
    }
    
    bz_index = 0 # find zone index for chords

    count_bars = 0
    f2 = open(f2,"r")
    prev_chord = {}
    chord_counter = 1
    for line in f2:

        currentline=line.split()
        chord=dict_b.copy() 
        chord["chord"] = updateChord(currentline[2])


        # Find same chords ---------------
        if prev_chord == {}:
            chord["start"] = float(currentline[0])
            prev_chord = chord
            pass

        elif prev_chord['chord'] == chord['chord']:
            pass

        else: # if chord is different then store the previous with the total duration etc.
            chord["start"] = float(currentline[0])
            prev_chord["end"] = chord["start"]
        # ---------------------------------------------------------------



            chord["start"] = float(currentline[0])
            chord["end"] = float(currentline[1])

            prev_chord["duration"] = prev_chord["end"]-prev_chord["start"]


            if prev_chord["end"]<b_zones[bz_index]["end"]:
                prev_chord["m_type"]=b_zones[bz_index]["measure"]
            else:
                bz_index+=1
                if bz_index+1>len(b_zones):
                    #print("unable to define m_type for chord: ", chord["chord"])
                    #song ending
                    prev_chord["m_type"] = "0"
                    prev_chord["m_duration"] = ["0", "0/1"]
                    prev_chord["chord_id"] = song + '_' + 'chord' + '_' + str(chord_counter) + '_' + prev_chord['chord']
                    chords.append(prev_chord)
                    break
                else:
                    prev_chord["m_type"]=b_zones[bz_index]["measure"]
            # print(check)
            prev_chord["m_duration"], check = findChordMeasure(prev_chord["duration"], b_mean_duration, prev_chord["m_type"])

            # Check for bad measure type
            if prev_chord["m_type"] in "New, Undefined":
                bad_measure = True
            else:
                bad_measure = False

            if check:
                count_bars+=1

            # append chord
            prev_chord["chord_id"] = song + '_' + 'chord' + '_' + str(chord_counter) + '_' + prev_chord['chord']
            # print(prev_chord)
            chords.append(prev_chord)

            chord_counter+=1
            # Update prev_chord after appending ------------------------
            prev_chord = chord
    # last chord ----
    chord["chord_id"] = song + '_' + 'chord' + '_LastChord'
    # print(chord['chord'])
    chord["start"] = float(currentline[0])
    chord["end"] = float(currentline[1])
    chord["duration"] = chord["end"] - chord["start"]
    chord["m_type"] = "0"
    chord["m_duration"] = ["0", "0/1"]
    chords.append(chord)

    if not bad_measure:
        zero_ratio = count_bars/len(chords)
    else:
        zero_ratio = 10

    return beats, chords, zero_ratio



#
# Describe chord's measure based on beat zones
def findChordMeasure(ch_duration, b_duration, m):
    #
    if m == 'New' or m == 'Undefined':
        return 'Undefined', False
    else:
        m = int(m)
    count = 0 # beat counter
    while ch_duration>0:
        count+=1
        ch_duration-=b_duration
    chord_measure = [str(count//m), str(count%m)+'/'+str(m)]
    check = count%m==0

    return chord_measure, check


#
# Calculate beat Zones
# (type of beat through song's duration)
def beatRateZone(beats):
    #
    beatZones = []
    prev_beat = None
    zone = dict()
    zone["measure"] = None
    first_beat = True
    pending = False
    for b in beats:

        if b["beat"]=="1" or first_beat:
            first_beat = False
            if prev_beat is None:
                zone["start"]=b["start"]
            else:
                if not zone["measure"]:
                    zone["measure"]=prev_beat
                    zone["end"] = b["start"]
                elif zone["measure"]==prev_beat:
                    zone["end"] = b["start"]
                    pending = True
                    pass
                else:
                    beatZones.append(zone)
                    pending = False
        prev_beat=b["beat"]

    if b["beat"] in "1":
        if pending:
            beatZones.append(zone)
        zone = dict()
        zone["start"] = b["start"]
        zone["end"] = b["duration"]
        zone["measure"] = "1"
        beatZones.append(zone)

    # FINISHING -----
    if b["beat"] not in "1":
        last_bar = b["beat"]
        last_bar_end = b["start"]+b["duration"]
        beats.reverse()
        for b in beats:
            if b["beat"]=="1":
                last_bar_start = b["start"]
                zone["end"]=b["start"]
                beatZones.append(zone)
                break
        zone = dict()
        zone["start"]=last_bar_start
        zone["measure"]=last_bar
        zone["end"]=last_bar_end
        beatZones.append(zone)

    return beatZones


#
# .lab to .txt
def labToTxt(path):
    #

    if path:
        pass
    else:
        return "No path parameter in labToTxt()"

    entries = os.listdir(path)

    for i in entries:
        x = os.listdir(path + "/" + i)
        for j in x:
            if '.lab' in j:
                new = j.replace('.lab', '.txt')
                os.rename(path + "/" + i + "/" + j, path + "/" + i + "/" + new)

    return 'Done'



#
# list all songs with beat and chord records
def listSongsPaths(path):
    #
    if path:
        pass
    else:
        return "No path parameter in listSongs()"

    albms = os.listdir(path)
    fileExt = ".txt"
    all_songs = []
    all_paths = []
    for al in albms:
        # print("Album: " + str(al))

        songs = [_ for _ in os.listdir(path+'/'+str(al)) if _.endswith(fileExt)]
        songs_paths = []
        for s in songs:
            songs_paths.append('/'+str(al)+'/'+str(s))
        all_songs.extend(songs)
        all_paths.extend(songs_paths)

    return all_songs, all_paths



#
# Chord Update: chord value
def updateChord(chord):
    #
    spl2 = chord.split('/')
    new = spl2[0]
    new = new.replace('#', 's')
    spl3 = new.split('(')
    new = spl3[0]
    if '6' in new:
        new = new.replace('6', '')
    if '9' in new:
        y = new.replace('9', '7')
    elif '7' in new:
        y = new
    elif 'maj' in new:
        spl4 = new.split(':')
        y = spl4[0]
    elif len(new) <= 3:
        if new == 'N':
            y = 'NoChord'
        elif ':' in new:
            spl5 = new.split(':')
            y = spl5[0] + ':maj'
        else:
            y = new + ':maj'
    else:
        y = new
    y = y.replace(':', '')
    return y




"""

Run Functions for every song of the dataset

Update files' extension from .lab to .txt for the chords records. 
*(It is necessary on the first processing)
 
"""


# Do this once!!
labToTxt(beat_folder)

# Find Songs
songs, songs_paths = listSongsPaths(beat_folder)


# Additional Info for the dataset is retrieved
ratios = []
i = 0
record = {}
results = []
all_chords = []
for sp in songs_paths:

    # Check if song exists
    if songs[i] not in sp:
        break
    else:
        pass
    if os.path.exists(beat_folder+sp) and os.path.exists(chord_folder+sp):
        pass
    else:
        print(sp)

    # Define: Title / path to beats and chords
    title = songs[i].rsplit('.',1)[0]
    beat_f = beat_folder+sp
    chord_f = chord_folder + sp

    # Run Analyzer
    beats, chords, zero_ratio = beatAndChords(beat_f, chord_f, title)
    if zero_ratio != 10:
        all_chords.append(chords)
    # Append object (class SongInfo) to a list
    record = SongInfo(title, chords, zero_ratio, beats)
    results.append(record)

    # Store Zero Ratio to calculate average
    ratios.append(zero_ratio)
    i+=1



# Store the Results
with open('chords_beats_beatles.py', 'w') as f:
    f.write('all_chords = %s' % all_chords)

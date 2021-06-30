import os
import sys 
import rdflib
import csv
folder = # chordlab destination
folder_2 = # keylab destination

entries = os.listdir(folder)
entries_2 = os.listdir(folder_2)

def convert_lab_to_txt(e,f):
    for i in e:
        x = os.listdir(f + "/" + i)
        for j in x:
            if '.lab' in j:
                new = j.replace('.lab','.txt')
                os.rename(f + "/" + i + "/" + j, f + "/" + i + "/" + new)

disc_dict = {}

def return_key(disc,song,path):
    p = []
    r = []
    song_path = path + "/" + disc + "/" + song
    if os.path.exists(song_path):
        with open(song_path, 'r') as f:
            lines = list(f)
        for i in lines:
            p = i.split()
            if p[2] == 'Key':
                p[2] = p[2] + '_' + p[3]
                p.remove(p[3])
            if p:
                r.append(p)
    return(r)

def return_chords(disc,song,path):
    p = []
    r = []
    song_path = path + "/" + disc + "/" + song
    if os.path.exists(song_path):
        with open(song_path, 'r') as f:
            lines = list(f)
        for i in lines:
            p = i.split()
            if p:
                r.append(p)

    return(r)

def assign_key_to_chord(key,chords):

    new_dict = {}
    for i in chords:
        song_list = []
        for j in chords[i]:
            chord_start = float(j[0])
            n = ''
            for k in key[i]:
                if (chord_start <= float(k[1])):
                    n = k[2]
                    if k[2] != 'Silence':
                        song_list.append((j[2], k[2])) 
                        n = k[2]
                    if (j[2] == 'N') and (k[2] == 'Silence'):
                        song_list.append((j[2], 'Silence')) 
                    break 
        new_dict[i] = song_list
        
    return(new_dict)


convert_lab_to_txt(entries,folder)
convert_lab_to_txt(entries_2,folder_2)
disc_dict = {}
for i in entries:
    disc_list = []
    x = os.listdir(folder + "/" + i)
    for j in x:
        if '.txt' in j:
            disc_list.append(j)
    disc_dict[i] = disc_list

key_dict = {}
chords_dict = {}
for i in disc_dict:
    for j in disc_dict[i]:
        key_dict[j] = return_key(i,j,folder_2)
        chords_dict[j] = return_chords(i,j,folder)

y =  assign_key_to_chord(key_dict,chords_dict)

chords_list = []
for i in chords_dict:
    for j in chords_dict[i]:
        if j[2] not in chords_list:
            chords_list.append(j[2])


with open('chords_list_beatles.py', 'w') as f:
    f.write('chords_list = %s' % y)
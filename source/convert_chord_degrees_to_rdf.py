from rdflib import Namespace
from rdflib import Graph
from rdflib.namespace import RDF
from rdflib import URIRef, BNode, Literal

n = Namespace("file://onto.owl#")
to = Namespace("http://purl.org/ontology/tonality/")
g = Graph()
nx = n.hasNext
pr = n.hasPrevious
no = n.NoChord
hs = n.hasKey
no = n.NoChord

from chords_graph_dict_beatles import graph_dict as graph_dict

for song in graph_dict:
    chord_list = []
    key_list = []
    c = 1
    index = 1
    song_key = ''
    song_chord = ''
    for chord in graph_dict[song]:
        if chord[0] != song_chord:
            new_key = chord[1]
            if new_key != song_key:
                new_k = URIRef("file://onto.owl#" +song + '_'+ 'key_' + str(c) + '_' + chord[1])
                k = URIRef("file://onto.owl#" + chord[1])
                g.add ((new_k, RDF.type, k))
                song_key = chord[1]
            l = chord[0].replace(':','')
            if  index != len(graph_dict[song]):
                x = URIRef("file://onto.owl#" +song + '_'+ 'chord_' + str(c) + '_' + l) # instance URI
            else:
                x = URIRef("file://onto.owl#" +song + '_'+ 'LastChord' + '_' + l) # instance 
            c += 1
            y = URIRef("file://onto.owl#" + l) # class of instance URI
            g.add ((x, RDF.type, y))
            g.add ((x, hs, new_k))
            chord_list.append(x)
            key_list.append(new_k)
            song_chord = chord[0]
        index +=1
    for chord in range(len(chord_list) - 1):
        g.add( (chord_list[chord], nx, chord_list[chord+1]))
        g.add( (chord_list[chord+1], pr, chord_list[chord]))
    if chord_list:
        g.add( (chord_list[-1], nx, no))
    
    g.serialize(destination=# destination# + song + '_keys.owl', format='xml')
    for i in chord_list:
        g.remove((i,None,None))
    for i in key_list:
        g.remove((i,None,None))

    
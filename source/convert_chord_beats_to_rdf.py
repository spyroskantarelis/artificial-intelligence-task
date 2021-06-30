from rdflib import Namespace
from rdflib import Graph
from rdflib.namespace import RDF
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import XSD

n = Namespace("file://onto.owl#")
to = Namespace("http://purl.org/ontology/tonality/")
g = Graph()

hb = n.hasBars
ht = n.hasTimeSignature

from chords_beats_beatles import all_chords as all_chords

def namethesong(song):

    name = song['chord_id']
    name_list = name.split('_')
    new_name_list = name_list[:len(name_list)-3]
    
    new_name = ''
    for i in new_name_list:
        new_name = new_name + i + '_'

    new_name = new_name[:-1]
    print(new_name)
    return new_name

def fraction_to_float(first,second):
    
    a = float(first)
    b_new = second.split('/')
    b = int(b_new[0]) / int(b_new[1])
    c = a + b
    
    return c

for song in all_chords:

    songname = namethesong(song[0])
    list = []
    for j in song:
        x = URIRef("file://onto.owl#" + j['chord_id'])
        y = URIRef("file://onto.owl#" + j['chord'])
        g.add ((x, RDF.type, y))

        bars = fraction_to_float(j['m_duration'][0], j['m_duration'][1])
        g.add ((x, hb, Literal(bars,  datatype=XSD.decimal)))
        list.append(x)
    g.serialize(destination= # folder destination#  + songname + '_bars.owl', format='xml')
    for i in list:
        g.remove((i,None,None))

    

    
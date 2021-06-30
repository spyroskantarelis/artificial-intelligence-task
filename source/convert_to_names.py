from chords_dict_beatles import chords_dict as chords_dict

graph_dict = {}

for i in chords_dict:
    j = i.replace('.txt','')
    graph_dict[j] = chords_dict[i]

with open('chords_graph_dict_beatles.py', 'w') as f:
    f.write('graph_dict = %s' % graph_dict)
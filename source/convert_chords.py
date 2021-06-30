from chords_list_beatles import chords_list as chords_dict


for i in chords_dict:
    new_list = []
    for j in chords_dict[i]:
        spl = j[1].split(':')
        key = spl[0]
        key = key.replace('#','s')
        spl2 = j[0].split('/')
        new = spl2[0]
        new = new.replace('#','s')
        spl3 = new.split('(')
        new = spl3[0]
        if '6' in new:
            new = new.replace('6','')
        if '9' in new:
            y = new.replace('9','7')
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
        
        new_list.append((y,key)) 
        
    chords_dict[i] = new_list


with open('chords_dict_beatles.py', 'w') as f:
    f.write('chords_dict = %s' % chords_dict)
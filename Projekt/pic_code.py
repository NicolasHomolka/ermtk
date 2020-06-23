import xerml_einlesen

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout


import os
import graphviz
import xml.etree.ElementTree as et
from lxml import etree


def get_rel_names(path):
    root = xerml_einlesen.get_root(path)

    matrix = []
    for child in root:
        if child.tag == 'rel':
            matrix.append(child.get('to'))

    return(matrix)

def get_xmlfile(path):
    base_path = os.path.dirname(os.path.realpath(_file_))
    xml_file = os.path.join(base_path, path)
    return xml_file

def get_root(path):
    xml_file = get_xmlfile(path)
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return root

def check_string(rel):
    chars = {'ö':'oe','ä':'ae','ü':'ue', 'Ö':'Oe', 'Ä':'Ae', 'Ü':'Ue', 'ß':'ss'}
    temp = ""
    for i in range(len(rel)):
        for j in range(len(rel[i])):
            temp = rel[i][j]
            for (char,char_to_replace) in chars.items():
                temp = temp.replace(char,char_to_replace)
            rel[i][j] = temp
    return rel

def check_string_dict(dic):
    chars = {'ö':'oe','ä':'ae','ü':'ue', 'Ö':'Oe', 'Ä':'Ae', 'Ü':'Ue', 'ß':'ss'}
    new_dic = {}
    temp = ""
    for key, value in dic.items():
        temp = key
        for (char,char_to_replace) in chars.items():
            temp = temp.replace(char,char_to_replace)
        key = temp
        key = key[0].upper()+(key[1:]).lower()
        key = "".join(key.split())
        new_dic[key] = value
    return new_dic

def get_super_sub(path):
    root = xerml_einlesen.get_root(path)

    matrix = []
    first_level = 0
    for child in root:
        temp_matrix = []
        if child.tag == 'rel':
            temp_matrix.append(child.get('to'))

            for grandchild in child:
                if grandchild.tag == 'super':
                    temp_matrix.append(grandchild.get('ref'))
                    temp_matrix.append(grandchild.get('total'))
                    temp_matrix.append(grandchild.get('disjoint'))
                
                if grandchild.tag == 'sub':
                    temp_matrix.append(grandchild.get('ref'))


        if len(temp_matrix) > 0:
            matrix.insert(first_level, temp_matrix)
            first_level += 1

    return matrix

def get_lo(lo_root):
    lo_dict = {}
    for child in lo_root:
        if child.tag == 'entlo':
            lo_dict[child.get("entref")] = child.get("name-lo")
            for grandchild in child:
                if grandchild.tag == 'attr':
                    lo_dict[grandchild.get("name")] = grandchild.get("name-lo")
        if child.tag == 'rello':
            lo_dict[child.get("relref")] = child.get("name-lo")
            for grandchild in child:
                if grandchild.tag == 'attr':
                    lo_dict[grandchild.get("name")] = grandchild.get("name-lo")
    lo_dict = check_string_dict(lo_dict)
    return lo_dict

def get_rel_attr(path):
    root = xerml_einlesen.get_root(path)

    matrix = []
    first_level = 0
    for child in root:
        temp_matrix = []
        if child.tag == 'rel':
            temp_matrix.append(child.get('to'))

            for grandchild in child:
                if grandchild.tag == 'part':
                    temp_matrix.append(grandchild.get('ref'))

        if len(temp_matrix) > 0:
            matrix.insert(first_level, temp_matrix)
            first_level += 1

    return(matrix)


def get_rel(path):
    root = xerml_einlesen.get_root(path)

    matrix = []
    first_level = 0
    for child in root:
        temp_matrix = []
        if child.tag == 'rel':
            temp_matrix.append(child.get('to'))
            for grandchild in child:
                if grandchild.tag == 'part':
                    temp_matrix.append(grandchild.get('ref'))
                    temp_matrix.append(grandchild.get('min'))
                    temp_matrix.append(grandchild.get('max'))
        if len(temp_matrix) > 0:
            matrix.insert(first_level, temp_matrix)
            first_level += 1
    return matrix


def get_ent_attr(path):
    root = xerml_einlesen.get_root(path)

    matrix = []
    first_level = 0
    for child in root:
        temp_matrix = []
        if child.tag == 'ent':
            temp_matrix.append(child.get('name'))

            for grandchild in child:
                if grandchild.tag == 'attr':
                    temp_matrix.append(grandchild.get('name'))

        if len(temp_matrix) > 0:
            matrix.insert(first_level, temp_matrix)
            first_level += 1

    return(matrix)

def get_weak(path):
    root = xerml_einlesen.get_root(path)

    matrix = []
    first_level = 0
    for child in root:
        temp_matrix = []
        if child.tag == 'rel':
            temp_matrix.append(child.get('to'))

            for grandchild in child:
                if grandchild.tag == 'part':
                    if grandchild.get('weak') == 'true':
                        temp_matrix.append(grandchild.get('ref'))
        if len(temp_matrix) > 0:
            matrix.insert(first_level, temp_matrix)
            first_level += 1

    return matrix


def get_pk(path):
    root = xerml_einlesen.get_root(path)

    matrix = []
    first_level = 0
    for child in root:
        temp_matrix = []
        if child.tag == 'ent':
            temp_matrix.append(child.get('name'))

            for grandchild in child:
                if grandchild.tag == 'attr':
                    if grandchild.get('prime') == 'true':
                        temp_matrix.append(grandchild.get('name'))
        if len(temp_matrix) > 0:
            matrix.insert(first_level, temp_matrix)
            first_level += 1

    return matrix

def draw_diamond(pic_code, key, key_neu, x, y, relh, relw, name):

    pic_code += '\nboxwid=' + str(relw) + '; boxht=' + str(relh) + ';' + key_neu + ': box invis "' + name + '" at (' + str(x) + ", " + str(y) + ');'
    pic_code += '\nline from last box .n to last box .e then to last box .s then to last box .w then to last box .n'

    return pic_code

def draw_triangle(pic_code, key, x, y, sup, pos, sub, triw, trih):
  

    pic_code += '\nboxht=' + str(trih) + '; boxwid=' + str(triw) + ';' + key + ': box invis at (' + str(x) + ', ' + str(y) + ');'
    pic_code += '\nline from last box .n to last box .se then to last box .sw then to last box .n'
    sub = [x for x in sub if len(x) >  2]
    x1 = 0
    x2 = 0

    y1 = 0
    y2 = 0

    xmax = 0
    ymax = 0
    for curr in sub:
        super_keyf = curr[1]
        akt = super_keyf
        akt = akt[0].upper()+(akt[1:]).lower()
        akt = "".join(akt.split())
        super_key = akt
        if curr[2] == "true":
            mini = 1
        else:
            mini = 0
        if curr[3] == "true":
            maxi = 1
        else:
            maxi = len(curr) - 4
        for j in range(1, len(sup), 1):
            for keyf,(xf,yf) in pos.items():
                x1 = x * 0.6
                x2 = xf * 0.60

                if x1 > x2:
                    x_diff = x1 - x2
                else:
                    x_diff = x2 - x1

                y1 = y * 0.7
                y2 = yf * 0.7

                if y1 > y2:
                    y_diff = y1 - y2
                else:
                    y_diff = y2 - y1

                if sup[j] == super_key:
                    if sup[j] == keyf:

                        if x1 >= x2 and y1 >= y2:
                            pic_code += '\nline from ' + str(key) + ' .n to ' + sup[j] + ' .s;'
                        elif x1 <= x2 and y1 >= y2 and x_diff >= 50:
                            pic_code += '\nline from ' + str(key) + ' .n to ' + sup[j] + ' .w;'
                        elif x1 >= x2 and y1 <= y2 and x_diff <= 50:
                            pic_code += '\nline from ' + str(key) + ' .n to ' + sup[j] + ' .s;'
                        elif x1 >= x2 and y1 <= y2 and x_diff >= 50:
                            pic_code += '\nline from ' + str(key) + ' .n to ' + sup[j] + ' .e;'
                        elif x1 <= x2 and y1 <= y2 and x_diff <= 50:
                            pic_code += '\nline from ' + str(key) + ' .n to ' + sup[j] + ' .s;'
                        elif x1 <= x2 and y1 <= y2 and x_diff >= 50:
                            pic_code += '\nline from ' + str(key) + ' .n to ' + sup[j] + ' .w;' 
                            
                        pic_code += '\nbox invis at last line .center "(' + str(mini) + ', ' + str(maxi) + ')";'
                elif keyf == sup[j]:
                    if x1 >= x2 and y1 >= y2:
                        pic_code += '\nline from ' + str(key) + ' .sw to ' + sup[j] + ' .n;'
                    elif x1 <= x2 and y1 >= y2:
                        pic_code += '\nline from ' + str(key) + ' .se to ' + sup[j] + ' .n;'
                    elif x1 >= x2 and y1 <= y2:
                        pic_code += '\nline from ' + str(key) + ' .sw to ' + sup[j] + ' .s;'
                    elif x1 <= x2 and y1 <= y2:
                        pic_code += '\nline from ' + str(key) + ' .se to ' + sup[j] + ' .s;'

                    pic_code += '\nbox invis at last line .center "(1, 1)";'

    return pic_code

def draw_weak_ent(key, x, y, pic_code, color_ent, wboxh, wboxw, name):

    pic_code += '\nboxwid=' + str(wboxw) + ';boxht=' + str(wboxh) + '; box shaded "' + color_ent + '" at (' + str(x) + ", " + str(y) + ') "' + name + '";' 
    return pic_code

def draw_weak_rel(key, x, y, pic_code, wrelw, wrelh):

    pic_code += '\nboxwid=' + str(wrelw) + ';boxht=' + str(wrelh) + '; box invis at (' + str(x) + ", " + str(y) + ');'
    pic_code += '\nline from last box .n to last box .e then to last box .s then to last box .w then to last box .n'

    return pic_code

def draw_erd(pic_code, rel, relations, pos, super_sub, sup, weak, attr_1, attr_ent, color_ent, lo):
    attr = []
    for curr in attr_ent:
        attr.append(curr[1:])
    weak = [x for x in weak if len(x) > 1]
    rel = [a for a in rel if len(a) > 1]
    i = 0
    for curr in rel:
        if len(curr) <= 1:
            del(rel[i])
        i += 1
    xmax = 0
    ymax = 0
    for key,(x,y) in pos.items():
        if x > xmax:
            xmax = x
        if y > ymax:
            ymax = y
    if xmax > 3000:
        boxh = 200
        boxw = 400
        wboxh = 185
        wboxw = 385
        relh = 300
        relw = 300
        wrelh = 270
        wrelw = 270
        trih = 250
        triw = 270

    elif xmax <= 1250:
        boxh = 50
        boxw = 100
        wboxh = 40
        wboxw = 90
        relh = 80
        relw = 80
        wrelh = 65
        wrelw = 65
        triw = 80
        trih = 65

    elif xmax > 1250 and xmax <= 3000:
        boxh = 80
        boxw = 160
        wboxh = 60
        wboxw = 140
        relh = 140
        relw = 140
        wrelh = 115
        wrelw = 115
        triw = 140
        trih = 120

    
    for key,(x,y) in pos.items():
        
        x = int(x)
        y = int(y)
        
        if lo == "":
            name = key
        else:
            name = lo.get(key)
            if name is None:
                name = key
        key_neu = key[0].upper()+key[1:].lower()
        key_neu = "".join(key_neu.split())
        for akt in attr:
            if key not in akt:
                check1 = True
            else:
                check1 = False
                break
        if key not in relations:
            check = True
            for i in range(len(super_sub)):
                if key == super_sub[i][0]:
                    check = False
                    break
                else:
                    check = True
            if check and check1:
                pic_code += '\nboxwid=' + str(boxw) + ';boxht= ' + str(boxh) + ';' + str(key) + ': box shaded "' + color_ent + '" at (' + str(x) + ", " + str(y) + ') ' + '"' + str(name) + '";'
                for akt in weak:
                    for curr in akt:
                        if key == curr:
                            pic_code = draw_weak_ent(key, x, y, pic_code, color_ent, wboxh, wboxw, name)    
        else:
            check = True
            for i in range(len(super_sub)):
                if key == super_sub[i][0]:
                    check = False
                    break
                else:
                    check = True
            if check and check1:
                pic_code = draw_diamond(pic_code, key, key_neu, x, y, relh, relw, name)
                for akt in weak:
                    for curr in akt:
                        if key == curr:
                            pic_code = draw_weak_rel(key, x, y, pic_code, wrelw, wrelh)

    for curr in rel:
        if len(curr) > 7:
            for i in range(1, len(curr) - 2, 3):
                akt = curr
                akt[0] = curr[0][0].upper()+(curr[0][1:]).lower()
                akt[0] = "".join(akt[0].split())
                akt[i] = curr[i][0].upper()+(curr[i][1:]).lower()
                akt[i] = "".join(akt[i].split())
            
            for i in range(1, len(curr) - 2, 3):

                x1 = pos[curr[0]][0]
                x2 = pos[curr[i]][0]

                if x1 > x2:
                    x_diff = x1 - x2
                else:
                    x_diff = x2 - x1

                y1 = pos[curr[0]][1]
                y2 = pos[curr[i]][1]

                if y1 > y2:
                    y_diff = y1 - y2
                else:
                    y_diff = y2 - y1
                
                if x1 >= x2 and y1 >= y2 and y_diff <= 50 and x_diff <= 50:
                    pic_code += '\nline from ' + curr[0] + ' .s to ' + curr[i] + ' .n;'
                elif x1 >= x2 and y1 >= y2 and y_diff >= 50 and x_diff <= 50:
                    pic_code += '\nline from ' + curr[0] + ' .s to ' + curr[i] + ' .e;'
                elif x1 >= x2 and y1 >= y2 and y_diff <= 50: 
                    pic_code += '\nline from ' + curr[0] + ' .w to ' + curr[i] + ' .e;'
                elif x1 >= x2 and y1 >= y2 and y_diff >= 50:
                    pic_code += '\nline from ' + curr[0] + ' .s to ' + curr[i] + ' .n;'
                elif x1 >= x2 and y1 <= y2 and y_diff <= 50:
                    pic_code += '\nline from ' + curr[0] + '.w to ' + curr[i] + ' .e;'
                elif x1 >= x2 and y1 <= y2 and y_diff >= 50:
                    pic_code += '\nline from ' + curr[0] + '.n to ' + curr[i] + ' .s;'
                elif x1 <= x2 and y1 >= y2 and y_diff <= 50 and x_diff <= 50:
                    pic_code += '\nline from ' + curr[0] + ' .n to ' + curr[i] + ' .s;'
                elif x1 <= x2 and y1 >= y2 and y_diff >= 50 and x_diff <= 50:
                    pic_code += '\nline  from ' + curr[0] + ' .s to ' + curr[i] + ' .n;'
                elif x1 <= x2 and y1 >= y2 and y_diff <= 50:
                    pic_code += '\nline from ' + curr[0] + ' .n to ' + curr[i] + ' .s;'
                elif x1 <= x2 and y1 >= y2 and y_diff >= 50:
                    pic_code += '\nline from ' + curr[0] + ' .s to ' + curr[i] + ' .n;'
                elif x1 <= x2 and y1 <= y2 and y_diff <= 50:
                    pic_code += '\nline from ' + curr[0] + '.s to ' + curr[i] + ' .e;'
                elif x1 <= x2 and y1 <= y2 and y_diff >= 50:
                    pic_code += '\nline from ' + curr[0] + '.n to ' + curr[i] + ' .w;'
                elif x1 >= x2 and y1 <= y2 and x_diff <= 100:
                    pic_code += '\nline from ' + curr[0] + ' .n to ' + curr[i] + ' .s;'
                elif x1 <= x2 and y1 <= y2 and x_diff <= 100:
                    pic_code += '\nline from ' + curr[0] + ' .n to ' + curr[i] + ' .s;'
                elif x1 >= x2 and y1 <= y2 and x_diff >= 100:
                    pic_code += '\nline from ' + curr[0] + ' .n to ' + curr[i] + ' .e;'
                elif x1 <= x2 and y1 <= y2 and x_diff >= 100:
                    pic_code += '\nline from ' + curr[0] + ' .n to ' + curr[i] + ' .s;'

                pic_code += '\nbox invis at last line .center "( ' + str(curr[i + 1]) + ', ' + str(curr[i + 2]) + ')";' 
        else: 
            akt = curr
            akt[0] = curr[0][0].upper()+(curr[0][1:]).lower()
            akt[0] = "".join(akt[0].split())
            akt[1] = curr[1][0].upper()+(curr[1][1:]).lower()
            akt[1] = "".join(akt[1].split())
            akt[4] = curr[4][0].upper()+(curr[4][1:]).lower()
            akt[4] = "".join(akt[4].split())

            x1 = pos[akt[0]][0]
            x2 = pos[akt[1]][0]
            if x1 > x2:
                x_diff = x1 - x2
            else:
                x_diff = x2 - x1

            y1 = pos[akt[0]][1]
            y2 = pos[akt[1]][1]

            if y1 > y2:
                y_diff = y1 - y2
            else:
                y_diff = y2 - y1

            check = True
            if len(super_sub) == 0:
                check = True
            else:
                for i in range(len(super_sub)):
                    if akt[0] == super_sub[i][0]:
                        check = False
                        break
            if check:
                if pos[akt[1]][1] > pos[akt[0]][1] and y_diff > 50:
                    pic_code += '\nline from ' + akt[0] + ' .n to ' + akt[1] + ' .s;'
                elif pos[akt[1]][1] < pos[akt[0]][1] and y_diff > 50:
                    pic_code += '\nline from ' + akt[0] + ' .s to ' + akt[1] + ' .n;'
                elif pos[akt[1]][0] < pos[akt[0]][0] and x_diff > 50:
                    pic_code += '\nline from ' + akt[0] + ' .w to ' + akt[1] + ' .e;'
                elif pos[akt[1]][0] > pos[akt[0]][0] and x_diff > 50:
                    pic_code += '\nline from ' + akt[0] + ' .e to ' + akt[1] + ' .w;'
                pic_code += '\nbox invis at last line .center "' + '(' + akt[5] + ',' + akt[6] + ')";' 
                
                x1 = pos[akt[4]][0]
                x2 = pos[akt[0]][0]

                if x1 > x2:
                    x_diff = x1 - x2
                else:
                    x_diff = x2 - x1

                y1 = pos[akt[4]][1]
                y2 = pos[akt[0]][1]

                if y1 > y2:
                    y_diff = y1 - y2
                else:
                    y_diff = y2 - y1
                if pos[akt[4]][1] > pos[akt[0]][1] and y_diff > 50:
                    pic_code += '\nline from ' + akt[0] + ' .n to ' + akt[4] + ' .s;'
                elif pos[akt[4]][1] < pos[akt[0]][1] and y_diff > 50:
                    pic_code += '\nline from ' + akt[0] + ' .s to ' + akt[4] + ' .n;'
                elif pos[akt[4]][0] < pos[akt[0]][0] and x_diff > 50:
                    pic_code += '\nline from ' + akt[0] + ' .w to ' + akt[4] + ' .e;'
                elif pos[akt[4]][0] > pos[akt[0]][0] and x_diff > 50:
                    pic_code += '\nline from ' + akt[0] + ' .e to ' + akt[4] + ' .w;'
                pic_code += '\nbox invis at last line .center "' + '(' + akt[2] + ',' + akt[3] + ')";' 

    for curr in super_sub:
            for key,(x,y) in pos.items():
                x = int(x)
                y = int(y)
                if key == curr[0]:
                    key_neu = key[0].upper()+key[1:].lower()
                    key_neu = "".join(key_neu.split())
                    pic_code = draw_triangle(pic_code, key_neu, x, y, curr, pos, sup, trih, triw)
    return pic_code

def draw_attr(pic_code, pos, ent, pk, color_attr, ellw, ellh, lo):
    for curr in ent:
        label = curr[0]
        tmp = label
        for i in range(1, len(curr), 1):
            label += curr[i]
            for key,(x,y) in pos.items():
                if lo == "":
                    name = curr[i]
                else:
                    name = lo.get(curr[i])
                    if name is None:
                        name = curr[i]
                x = int(x)
                y = int(y)
                if key == label:
                    for current in pk:
                        if curr[i] in current:
                            check = True
                    if check:
                        unterstrich = "_"
                        faktor = len(curr[i])
                        unterstrich = unterstrich * faktor
                        pic_code += '\nellipseht=' + str(ellh) + ';ellipsewid=' + str(ellw) + ';' + label + ': ellipse shaded "' + color_attr + '" "' + unterstrich + '" at (' + str(x) + ',' + str(y) + ');'
                        pic_code += '\nellipseht=' + str(ellh) + ';ellipsewid=' + str(ellw) + '; ellipse invis at last ellipse "' + name + '";'
                    else:
                        pic_code += '\nellipseht=' + str(ellh) + ';ellipsewid=' + str(ellw) + ';' + label + ': ellipse shaded "' + color_attr + '" at (' + str(x) + ',' + str(y) + ') "' + name + '";'
                        ent = curr[0]

                    for keyf,(xf,yf) in pos.items():
                        if curr[0] == keyf:
                            x1 = x
                            x2 = xf

                            if x1 > x2:
                                x_diff = x1 - x2
                            else:
                                x_diff = x2 - x1

                            y1 = y
                            y2 = yf

                            if y1 > y2:
                                y_diff = y1 - y2
                            else:
                                y_diff = y2 - y1
                    if y1 >= y2 and x_diff >= 50 and y_diff >= 50:
                        pic_code += '\nline from ' + curr[0] + ' .n to ' + label + ' .s;'
                    elif y1 >= y2 and x1 <= x2 and x_diff >= 50 and y_diff <= 50:
                        pic_code += '\nline from ' + curr[0] + ' .w to ' + label + ' .e;'
                    elif y1 >= y2 and x1 >= x2 and x_diff >= 50 and y_diff <= 50:
                        pic_code += '\nline from ' + curr[0] + ' .e to ' + label + ' .w;'
                    elif y1 >= y2 and x_diff <= 50 and x1 >= x2:
                        pic_code += '\nline from ' + curr[0] + ' .n to ' + label + ' .s;'
                    elif y1 >= y2 and x_diff <= 50 and x1 <= x2: 
                        pic_code += '\nline from ' + curr[0] + ' .w to ' + label + ' .s;'
                    elif y1 <= y2 and x_diff >= 50:
                        pic_code += '\nline from ' + curr[0] + ' .s to ' + label + ' .n;'
                    elif y1 <= y2 and x_diff <= 50 and x1 >= x2:
                        pic_code += '\nline from ' + curr[0] + ' .e to ' + label + ' .n;'
                    elif y1 <= y2 and x_diff <= 50 and x1 <= x2: 
                        pic_code += '\nline from ' + curr[0] + ' .w to ' + label + ' .n;'      
                    check = False
                    label = tmp
    return pic_code

def write_erd_to_file(pic, inputfile):
    root = xerml_einlesen.get_root(inputfile)
    '''
    title = "output"
    for child in root:
        if child.tag == "title":
            if child.get('lang') is None:
                title = child.get('name')
    ''' 
    if os.path.exists("erd.pic"):
        os.remove("erd.pic")
    file = open("erd.pic", "w")
    file.write(pic)  
    file.close()
    print('Your file is created at: ' + os.getcwd() + '/erd.pic')


#INSTALL: pygraphviz, networkx

def nx_graph(rel):
    erd = nx.Graph()
    for curr in rel:
        if len(curr) > 1:
            for i in range(len(curr)):

                erd.add_edge(curr[0], curr[i])
        else:
            continue
    #-Goverlap=scale
    pos = graphviz_layout(erd, prog='neato', args="-Gsplines=true -Goverlap=scale -Gsize=0.19,0.285! -Gmaxiter=10000 -Gepsilon=0.00001 -Gdpi=1 -Gratio=fill" )
    return pos

def erd_pic(inputfile, args, lo_tree):

    ent = get_ent_attr(inputfile)
    pk = get_pk(inputfile)
    weak = get_weak(inputfile)
    super_sub = get_super_sub(inputfile)
    super_sub = [x for x in super_sub if len(x) >= 2]
    rel_min_max = get_rel(inputfile)
    rel_min_max = check_string(rel_min_max)
    rel = get_rel_attr(inputfile)
    rel = check_string(rel)

    ent = check_string(ent)

    if lo_tree is not None:
        lo_root = lo_tree.getroot()
        lo = get_lo(lo_root)
    else:
        lo = ""

    for curr in weak:
        for i in range(len(curr)):
                akt = curr
                akt[0] = curr[0][0].upper()+(curr[0][1:]).lower()
                akt[0] = "".join(akt[0].split())
                akt[i] = curr[i][0].upper()+(curr[i][1:]).lower()
                akt[i] = "".join(akt[i].split())


    for curr in rel:
        if len(curr) > 1:
            akt = curr
            akt[0] = curr[0][0].upper()+(curr[0][1:]).lower()
            akt[0] = "".join(akt[0].split())
            akt[1] = curr[1][0].upper()+(curr[1][1:]).lower()
            akt[1] = "".join(akt[1].split())
            akt[2] = curr[2][0].upper()+(curr[2][1:]).lower()
            akt[2] = "".join(akt[2].split())

    for curr in ent:
        for i in range(len(curr)):
                akt = curr
                akt[0] = curr[0][0].upper()+(curr[0][1:]).lower()
                akt[0] = "".join(akt[0].split())
                akt[i] = curr[i][0].upper()+(curr[i][1:]).lower()
                akt[i] = "".join(akt[i].split())

    for curr in pk:
        for i in range(len(curr)):
                akt = curr
                akt[0] = curr[0][0].upper()+(curr[0][1:]).lower()
                akt[0] = "".join(akt[0].split())
                akt[i] = curr[i][0].upper()+(curr[i][1:]).lower()
                akt[i] = "".join(akt[i].split())
    rel_t = []
    super_sub_only = super_sub
    for akt in super_sub_only:
        if len(akt) > 1:
            del(akt[3])
            del(akt[2])
            rel_t.append(akt)

    check = False
    for curr in rel:
        for akt in curr:
            if akt in rel_t:
                check = False
            else:
                check = True
        if check:
            rel_t.append(curr)
        check = False

    temp = rel_t

    rel_re = rel_t[::-1]
    rel_t = temp

    ent_for_layout = []
    for i in range(len(ent)):
        tmp = [ent[i][0]]
        for y in range(1, len(ent[i])):
            tmp.append(str(ent[i][0]) + str(ent[i][y]))
        ent_for_layout.append(tmp)

    for akt in ent_for_layout:
        rel_re.append(akt)

    for i in range (0,len(rel_t), 1):
        for j in range(len(rel_t[i])):
            temp = rel_t[i][j]
            temp = "".join(temp.split())
            temp = temp[0].upper() + temp[1:].lower()
            rel_t[i][j] = temp

    pos = nx_graph(rel_re)

    for i in range(len(super_sub)):
        for j in range(len(super_sub[i])):
                temp = super_sub[i][j]
                temp = "".join(temp.split())
                temp = temp[0].upper() + temp[1:].lower()
                super_sub[i][j] = temp


    rel_only = get_rel_names(inputfile)

    for i in range (0,len(rel_only), 1):
        temp = rel_only[i]
        temp = "".join(temp.split())
        temp = temp[0].upper() + temp[1:].lower()
        rel_only[i] = temp
    chars = {'ö':'oe','ä':'ae','ü':'ue', 'Ö':'Oe', 'Ä':'Ae', 'Ü':'Ue', 'ß':'ss'}
    temp = ""
    for i in range(len(rel_only)):
        temp = rel_only[i]
        for (char,char_to_replace) in chars.items():
            temp = temp.replace(char,char_to_replace)
        rel_only[i] = temp

    for i in range(0, len(super_sub) - 1, 1):
        super_sub[i].append('sub')
    super_sub = get_super_sub(inputfile)
    pic_code = ".PS"

    if args.color is True:
        pic_code += "\n.defcolor medblue rgb #89D8D6"
        color_ent = "medblue"
        color_attr = "lightblue"
    else:
        color_ent = "white"
        color_attr = "white"
    pic_erd = draw_erd(pic_code, rel_min_max, rel_only, pos, super_sub_only, super_sub, weak, ent, ent_for_layout, color_ent, lo)

    xmax = 0
    ymax = 0
    for key,(x,y) in pos.items():
        if x > xmax:
            xmax = x
        if y > ymax:
            ymax = y
    if xmax > 3000:
        ellh = 200
        ellw = 400

    elif xmax <= 1250:
        ellh = 60
        ellw = 100

    elif xmax > 1250 and xmax <= 3000:
        ellh = 100
        ellw = 180

    if args.attr is True:
        pic_erd = draw_attr(pic_erd, pos, ent, pk, color_attr, ellw, ellh, lo)
    pic_erd += "\n.PE"
    
    
    write_erd_to_file(pic_erd, inputfile)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#14.2.2019 09:06
#TODO: Bei Weak selbes wie bei Super Sub

import os
from lxml import etree as ET
import lod


page = ET.Element('svg')
page.attrib["xmlns"]="http://www.w3.org/2000/svg"
page.attrib["version"]="1.1"
page.attrib["viewBox"]="0 0 500 500"
page.attrib["width"]="1920"
page.attrib["height"]="1080"
page.attrib["id"]="svg"
doc = ET.ElementTree(page)


def get_pk(path):
    root = lod.get_root(path)

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

def cutpk(pk_list):

    new_pk_list = []

    for i in pk_list:
        del i[0]

    for i in range(len(pk_list)):
        for y in range(len(pk_list[i])):
            new_pk_list.append(pk_list[i][y])

    return new_pk_list

def cut_super_sub_and_weak(super_sub_list, weak_list, rel_list):
    tmp_super_sub_list = []
    for ii in range(len(super_sub_list)):
        for yy in range(4, len(super_sub_list[ii])):
            tmp_super_sub_list.append([super_sub_list[ii][1], super_sub_list[ii][yy]])

    for i in range(len(weak_list)):
        if len(weak_list[i]) > 1:
            for y in range(len(rel_list)):
                if weak_list[i][0] == rel_list[y][0]:
                    if weak_list[i][1] != rel_list[y][1]:
                        tmp_super_sub_list.append([rel_list[y][1], rel_list[y][4]])
                    else:
                        tmp_super_sub_list.append([rel_list[y][4], rel_list[y][1]])
                        

                    
    return tmp_super_sub_list


def create_ent(ent_list, pk_list, super_sub_list, tmp_super_sub_list, pk_list_full):
    
    y_coord = 30

    for i in range(len(ent_list)):
        
        
        x_coord = 20
        subsvg = ET.SubElement(page, 'svg')
        subsvg.attrib["id"]=str(ent_list[i][0])
        subsvg.attrib["width"]="100"
        subsvg.attrib["height"]="35"
        subsvg.attrib["x"]=str(x_coord)
        subsvg.attrib["y"]=str(y_coord)

        rect = ET.SubElement(subsvg, 'rect')
        rect.attrib["width"]='100'
        rect.attrib["height"]='35'
        rect.attrib["x"]="0"
        rect.attrib["y"]="0"
        rect.attrib["style"]='fill:rgb(255,255,255);stroke-width:0;stroke:rgb(0,0,0)'

        point = ET.SubElement(rect, 'point')
        point.attrib["id"]=str(ent_list[i][0])
        point.attrib["x"]="50%"
        point.attrib["y"]="100%"
        point.attrib["marker"]="url(#circle)"

        text = ET.SubElement(subsvg, 'text')
        text.attrib["x"]="50%"
        text.attrib["y"]="50%"
        text.attrib["alignment-baseline"]="middle"
        text.attrib["text-anchor"]="middle"
        text.attrib["font-size"]="8pt"
        text.text = ent_list[i][0]

        x_coord += 99

        #super_sub
        for ii in range(len(tmp_super_sub_list)):
            if ent_list[i][0] == tmp_super_sub_list[ii][1]:
                print(tmp_super_sub_list)
                print("------")
                for yy in range(len(pk_list_full)):
                    if pk_list_full[yy][0] == tmp_super_sub_list[ii][0]:
                        for zz in range(1, len(pk_list_full[yy])):
                            super_pk = ""
                            for ww in range(len(pk_list_full)):
                                if pk_list_full[ww][0] == tmp_super_sub_list[ii][0]:
                                    super_pk = str(pk_list_full[ww][0]) + str(pk_list_full[ww][1])


                            subsvg = ET.SubElement(page, 'svg')
                            subsvg.attrib["id"]=str(ent_list[i][0]) + str(pk_list_full[yy][zz])
                            subsvg.attrib["width"]="100"
                            subsvg.attrib["height"]="35"
                            subsvg.attrib["x"]=str(x_coord)
                            subsvg.attrib["y"]=str(y_coord)

                            pk_list_full.append([ent_list[i][0], pk_list_full[yy][zz]])

                            rect = ET.SubElement(subsvg, 'rect')
                            rect.attrib["width"]='100'
                            rect.attrib["height"]='35'
                            rect.attrib["x"]="0"
                            rect.attrib["y"]="0"
                            rect.attrib["style"]='fill:rgb(191,191,191);stroke-width:1;stroke:rgb(0,0,0)'

                            point = ET.SubElement(rect, 'point')
                            point.attrib["id"]=str(ent_list[i][0]) + str(pk_list_full[yy][zz])
                            point.attrib["x"]="50%"
                            point.attrib["y"]="100%"

                            text = ET.SubElement(subsvg, 'text')
                            text.attrib["x"]="50%"
                            text.attrib["y"]="50%"
                            text.attrib["alignment-baseline"]="middle"
                            text.attrib["text-anchor"]="middle"
                            text.attrib["font-size"]="8pt"
                            text.attrib["text-decoration"]="underline"

                            text.text = pk_list_full[yy][zz]

                            sstring_from = str(ent_list[i][0]) + str(pk_list_full[yy][zz])
                            results_from = doc.xpath("//svg[@id = '%s']" % sstring_from)
                            pos_from = doc.xpath("//point[@id = '%s']" % sstring_from)
                            pos_svg_from = pos_from[0]
                            from_svg = results_from[0]
                            from_x = int(from_svg.attrib['x'])
                            from_y = int(from_svg.attrib['y'])
                            from_width = int(from_svg.attrib['width'])
                            from_height = int(from_svg.attrib['height'])
                            from_x_pos = pos_svg_from.attrib['x']
                            from_x_pos = int(from_x_pos[:-1]) / 100
                            print(from_width)
                            print(from_height)
                            point_x_from = from_x + (from_width * from_x_pos)





                            sstring_to = str(tmp_super_sub_list[ii][0]) + str(pk_list_full[yy][zz])
                            results_to = doc.xpath("//svg[@id = '%s']" % sstring_to)
                            pos_to = doc.xpath("//point[@id = '%s']" % sstring_from)
                            to_svg = results_to[0]
                            pos_svg_to = pos_to[0]
                            to_x = int(to_svg.attrib['x'])
                            to_y = int(to_svg.attrib['y'])
                            to_width = int(to_svg.attrib['width'])
                            to_height = int(to_svg.attrib['height'])
                            to_x_pos = pos_svg_to.attrib['x']
                            to_x_pos = int(to_x_pos[:-1]) / 100
                            point_x_to = to_x + (to_width * to_x_pos)


                            polyline = ET.SubElement(page, 'polyline')
                            polyline.attrib["points"]=str(point_x_from) + "," + str(from_y) + " " + str(point_x_to) + "," + str(to_y)
                            polyline.attrib["style"]="fill:none;stroke:black;stroke-width:1"

                            x_coord += 99

        for y in range(1, len(ent_list[i])):



            subsvg = ET.SubElement(page, 'svg')
            subsvg.attrib["id"]=str(ent_list[i][0]) + str(ent_list[i][y])
            subsvg.attrib["width"]="100"
            subsvg.attrib["height"]="35"
            subsvg.attrib["x"]=str(x_coord)
            subsvg.attrib["y"]=str(y_coord)


            rect = ET.SubElement(subsvg, 'rect')
            rect.attrib["width"]='100'
            rect.attrib["height"]='35'
            rect.attrib["x"]="0"
            rect.attrib["y"]="0"
            rect.attrib["style"]='fill:rgb(255,255,255);stroke-width:1;stroke:rgb(0,0,0)'

            point = ET.SubElement(rect, 'point')
            point.attrib["id"]=str(ent_list[i][0]) + str(ent_list[i][y])
            point.attrib["x"]="50%"
            point.attrib["y"]="100%"


            text = ET.SubElement(subsvg, 'text')
            text.attrib["x"]="50%"
            text.attrib["y"]="50%"
            text.attrib["alignment-baseline"]="middle"
            text.attrib["text-anchor"]="middle"
            text.attrib["font-size"]="8pt"

            if (str(ent_list[i][0]) + str(ent_list[i][y])) in pk_list:
                text.attrib["text-decoration"]="underline"
                rect.attrib["style"]='fill:rgb(191,191,191);stroke-width:1;stroke:rgb(0,0,0)'

            text.text = ent_list[i][y]

            x_coord += 99

        y_coord += 60
    return x_coord, y_coord, pk_list_full


def create_rel(rel_list, pk_list_cut, rel_attr_list, super_sub_list, x_coord, y_coord, pk_list):


    for i in range(len(rel_list)):
        if len(rel_list[i]) >= 6:
            if rel_list[i][3] == 'n' and rel_list[i][6] == 'n':

                    
        
                x_coord = 20
                subsvg = ET.SubElement(page, 'svg')
                subsvg.attrib["id"]=str(rel_list[i][0])
                subsvg.attrib["width"]="100"
                subsvg.attrib["height"]="35"
                subsvg.attrib["x"]=str(x_coord)
                subsvg.attrib["y"]=str(y_coord)

                rect = ET.SubElement(subsvg, 'rect')
                rect.attrib["width"]='100'
                rect.attrib["height"]='35'
                rect.attrib["x"]="0"
                rect.attrib["y"]="0"
                rect.attrib["style"]='fill:rgb(255,255,255);stroke-width:0;stroke:rgb(0,0,0)'

                point = ET.SubElement(rect, 'point')
                point.attrib["id"]=str(rel_list[i][0])
                point.attrib["x"]="50%"
                point.attrib["y"]="100%"
                point.attrib["marker"]="url(#circle)"

                text = ET.SubElement(subsvg, 'text')
                text.attrib["x"]="50%"
                text.attrib["y"]="50%"
                text.attrib["alignment-baseline"]="middle"
                text.attrib["text-anchor"]="middle"
                text.attrib["font-size"]="8pt"
                text.text = rel_list[i][0]

                x_coord += 99
                

                for y in pk_list:
                    if len(y) > 1:
                        if y[0] == rel_list[i][1]:
                            print("y01:" + str(y[0]))
                            subsvg = ET.SubElement(page, 'svg')
                            subsvg.attrib["id"]=str(rel_list[i][0]) + str(rel_list[i][1])
                            subsvg.attrib["width"]="100"
                            subsvg.attrib["height"]="35"
                            subsvg.attrib["x"]=str(x_coord)
                            subsvg.attrib["y"]=str(y_coord)


                            rect = ET.SubElement(subsvg, 'rect')
                            rect.attrib["width"]='100'
                            rect.attrib["height"]='35'
                            rect.attrib["x"]="0"
                            rect.attrib["y"]="0"
                            rect.attrib["style"]='fill:rgb(191,191,191);stroke-width:1;stroke:rgb(0,0,0)'

                            point = ET.SubElement(rect, 'point')
                            point.attrib["id"]=str(rel_list[i][0]) + str(rel_list[i][1])
                            point.attrib["x"]="50%"
                            point.attrib["y"]="100%"


                            text = ET.SubElement(subsvg, 'text')
                            text.attrib["x"]="50%"
                            text.attrib["y"]="50%"
                            text.attrib["alignment-baseline"]="middle"
                            text.attrib["text-anchor"]="middle"
                            text.attrib["font-size"]="8pt"
                            text.attrib["text-decoration"]="underline"
                            
                            text.text = y[1]
                            x_coord += 99

                        if y[0] == rel_list[i][4]:
                            print("y0:" + str(y[0]))
                            print("--------------->" + str(rel_list[i][4]))
                            subsvg = ET.SubElement(page, 'svg')
                            subsvg.attrib["id"]=str(rel_list[i][0]) + str(rel_list[i][4])
                            subsvg.attrib["width"]="100"
                            subsvg.attrib["height"]="35"
                            subsvg.attrib["x"]=str(x_coord)
                            subsvg.attrib["y"]=str(y_coord)


                            rect = ET.SubElement(subsvg, 'rect')
                            rect.attrib["width"]='100'
                            rect.attrib["height"]='35'
                            rect.attrib["x"]="0"
                            rect.attrib["y"]="0"
                            rect.attrib["style"]='fill:rgb(191,191,191);stroke-width:1;stroke:rgb(0,0,0)'

                            point = ET.SubElement(rect, 'point')
                            point.attrib["id"]=str(rel_list[i][0]) + str(rel_list[i][4])
                            point.attrib["x"]="50%"
                            point.attrib["y"]="100%"


                            text = ET.SubElement(subsvg, 'text')
                            text.attrib["x"]="50%"
                            text.attrib["y"]="50%"
                            text.attrib["alignment-baseline"]="middle"
                            text.attrib["text-anchor"]="middle"
                            text.attrib["font-size"]="8pt"
                            text.attrib["text-decoration"]="underline"
                            
                            text.text = y[1]
                            x_coord += 99
                y_coord += 60







def main():

    inputfile = "../datenmodelle/weingut/xml/weingut.xerml.xml"
    root = lod.get_root(inputfile)
    tree = lod.get_tree(inputfile)


    ent = lod.get_ent_attr(inputfile)
    rel = lod.get_rel(inputfile)
    pk = lod.get_pk(inputfile)
    full_pk = get_pk(inputfile)



    rel_attr = lod.get_rel_attr(inputfile)
    super_sub = lod.get_super_sub(inputfile)
    weak = lod.get_weak(inputfile)
    rel_only = lod.get_rel_only(inputfile)
    super_sub_only = lod.get_super_sub_only(inputfile)

    cutpk_list = cutpk(pk)
    cutsupersub = cut_super_sub_and_weak(super_sub, weak, rel)


    x, y, full_pk = create_ent(ent, cutpk_list, super_sub, cutsupersub, full_pk)
    create_rel(rel, pk, rel_attr, super_sub, x, y, full_pk)


    print("weak")
    print(weak)
    print("rel")
    print(rel)
    print("fullpk")
    print(full_pk)
    print("pk")
    print(pk)
    print("pk_cut")
    print(cutpk_list)
    print("rel_attr")
    print(rel_attr)
    print("super_sub")
    print(super_sub)
    print("ent")
    print(ent)


    doc.write('blockdiagram.svg', xml_declaration=True)
    print("Saved to " + "'" + os.getcwd() + "/blockdiagram.svg'")



main()
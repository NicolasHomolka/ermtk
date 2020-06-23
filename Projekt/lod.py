#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# date:     25.04.19 15:00
# author:   Nicolas Homolka
# TODO:     Größe Relation, Min-Max falsche Seite?!

import networkx as nx 
from networkx.drawing.nx_agraph import graphviz_layout
import graphviz
import os
from lxml import etree as ET
from colorama import Fore
import subprocess
import time

def get_xmlfile(path):
    base_path = os.path.dirname(os.path.realpath(__file__))
    xml_file = os.path.join(base_path, path)
    return xml_file

def get_root(path):
    xml_file = get_xmlfile(path)
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return root

def get_tree(path):
    xml_file = get_xmlfile(path)
    tree = ET.parse(xml_file)
    return tree

def get_ent_attr(root):
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
    return matrix

def get_rel_attr(root):
    matrix = []
    first_level = 0
    for child in root:
        temp_matrix = []
        if child.tag == 'rel':
            temp_matrix.append(child.get('to'))
            for grandchild in child:
                if grandchild.tag == 'attr':
                    temp_matrix.append(grandchild.get('name'))
        if len(temp_matrix) > 0:
            matrix.insert(first_level, temp_matrix)
            first_level += 1
    return matrix

def get_pk(root):
    matrix = []
    first_level = 0
    for child in root:
        temp_matrix = []
        if child.tag == 'ent':
            temp_matrix.append(child.get('name'))
            for grandchild in child:
                if grandchild.tag == 'attr':
                    if grandchild.get('prime') == 'true':
                        temp_matrix.append(str(child.get('name') + grandchild.get('name')))
        if len(temp_matrix) > 0:
            matrix.insert(first_level, temp_matrix)
            first_level += 1
    return matrix

def get_weak(root):
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

def get_super_sub(root):
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

def get_super_sub_only(root):
    matrix = []
    first_level = 0
    for child in root:
        temp_matrix = []
        if child.tag == 'rel':
            temp_matrix.append(child.get('to'))
            for grandchild in child:
                if grandchild.tag == 'super':
                    temp_matrix.append(grandchild.get('ref'))
                if grandchild.tag == 'sub':
                    temp_matrix.append(grandchild.get('ref'))
        if len(temp_matrix) > 0:
            matrix.insert(first_level, temp_matrix)
            first_level += 1
    return matrix

def get_rel(root):
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
    return lo_dict

def get_rel_only(root):
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
    return matrix

def get_empty_doc():
    tree = get_tree("empty1.fodg")
    return tree

def nx_graph(rel, args):
    erd = nx.Graph()
    for curr in rel:
        if len(curr) > 1:
            for i in range(len(curr)):

                erd.add_edge(curr[0], curr[i])
        else:
            continue
    if args.dot:
        pos = graphviz_layout(erd, prog='dot', args="-Gsplines=true -Goverlap=scale -Gsize=350,175! -Gmaxiter=10000 -Gepsilon=0.00001 -Gdpi=1 -Gratio=fill" )
    else:
        pos = graphviz_layout(erd, prog='neato', args="-Gsplines=true -Goverlap=scale -Gsize=350,175! -Gmaxiter=10000 -Gepsilon=0.00001 -Gdpi=1 -Gratio=fill" )

    return pos

def resize_doc(tree, x_max, y_max):
    root = tree.getroot()
    el = root.xpath('.//style:page-layout-properties', namespaces=root.nsmap)
    el1 = el[0]
    el1.attrib["{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}page-width"]= str(x_max / 100 + 10) + "cm"
    el1.attrib["{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}page-height"]= str(y_max / 100 + 6) + "cm"

def create_ent(tree, ent_list, pk_list, weak_list, rel_list, rel_attr_list, super_sub_list, display_attr, display_color, pos, x_max, y_max, lo):
    root = tree.getroot()
    el = root.xpath('.//draw:page', namespaces=root.nsmap)
    el1 = el[0]
    x = 2.0
    y = 2.0

    templist = []
    for tmp in range(0, len(weak_list)):
        for tmp2 in range(1, len(weak_list[tmp])):
            templist.append(weak_list[tmp][tmp2])

    for i in range(len(ent_list)):

        if ent_list[i][0] not in templist:

            shape_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
            text_node = ET.SubElement(shape_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
            span_node = ET.SubElement(text_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")

            if display_color:
                
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr_ent'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P_ent'
                text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T6'
            else:

                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P8'
                text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'

            for key,(x,y) in pos.items():
                if key == ent_list[i][0]:
                    x_coord = x
                    y_coord = y
          
            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=ent_list[i][0]
            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='10cm'
            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='6cm'
            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]= str(x_coord / 100) + 'cm'
            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]= str(y_coord / 100) + 'cm'

            if lo == "":
                span_node.text = ent_list[i][0]
            else:
                span_node.text = lo.get(ent_list[i][0])

            geometry_node = ET.SubElement(shape_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
            geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
            geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}mirror-horizontal"]='false'
            geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}mirror-vertical"]='false'
            geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='rectangle'
            geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 0 0 L 21600 0 21600 21600 0 21600 0 0 Z N'
            float(x)
            float(y)
            y += 2.0

            if display_attr:

                for z in range(len(ent_list[i]) - 1):

                    pk = False
                    if str(ent_list[i][0] + ent_list[i][z+1]) in pk_list[i]:
                        pk = True

                    attr_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                    text_node = ET.SubElement(attr_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                    span_node = ET.SubElement(text_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")

                    if display_color:
                        
                        if pk:
                            attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr4'
                            attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P5'
                            text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                            span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T4'
                        else:
                            attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr4'
                            attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P19'
                            text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                            span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T6'
                    else:
                        if pk:
                            attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                            attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P7'
                            text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                            span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T4'
                        else:
                            attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                            attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P8'
                            text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                            span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'

                    for key,(x,y) in pos.items():
                        if key == str(ent_list[i][0]) + str(ent_list[i][z+1]):
                            x_coord = x
                            y_coord = y

                    attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=ent_list[i][0] + ent_list[i][z + 1]
                    attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                    attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='10cm'
                    attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='6cm'
                    attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]= str(x_coord / 100) + 'cm'
                    attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]= str(y_coord / 100) + 'cm'

                    if lo == "":
                        span_node.text = ent_list[i][z + 1]
                    else:
                        span_node.text = lo.get(ent_list[i][z + 1])

                    geometry_node = ET.SubElement(attr_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
                    geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
                    geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}glue-points"]='10800 0 3163 3163 0 10800 3163 18437 10800 21600 18437 18437 21600 10800 18437 3163'
                    geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='ellipse'
                    geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-areas"]='3163 3163 18437 18437'
                    geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='U 10800 10800 10800 10800 0 360 Z N'

                    connector_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}connector")
                    connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr4'
                    connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='T1'
                    connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                    connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='line'
                    connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-shape"]=ent_list[i][0]
                    connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}end-shape"]=ent_list[i][0] + ent_list[i][z + 1]
                    connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}d"]="M5889 5191v3810"
                    connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]="0 0 1 3811"
        else:

            group_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}g")
            group_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr7'
            group_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=ent_list[i][0]

            shape_node = ET.SubElement(group_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
            text_node = ET.SubElement(shape_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
            span_node = ET.SubElement(text_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")

            shape_node1 = ET.SubElement(group_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
            text_node1 = ET.SubElement(shape_node1, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
            span_node1 = ET.SubElement(text_node1, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")

            if display_color:
                
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P8'
                text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'      
                shape_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr_ent'
                shape_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P_ent'
                text_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                span_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T6'
            else:

                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P8'
                text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'
                shape_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                shape_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P8'
                text_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                span_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'

            x_coord = 1
            y_coord = 1
            factor_x = 15 / x_max
            factor_y = 15 / y_max

            for key,(x,y) in pos.items():
                if key == ent_list[i][0]:
                    x_coord = x 
                    y_coord = y 

            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='10cm'
            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='6cm'
            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]= str(x_coord / 100) + 'cm'
            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]= str(y_coord / 100) + 'cm'

            geometry_node = ET.SubElement(shape_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
            geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
            geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}mirror-horizontal"]='false'
            geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}mirror-vertical"]='false'
            geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='rectangle'
            geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 0 0 L 21600 0 21600 21600 0 21600 0 0 Z N'

            shape_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=ent_list[i][0]
            shape_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
            shape_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='9cm'
            shape_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='5cm'
            shape_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]= str(x_coord / 100 + 0.5) + 'cm'
            shape_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]= str(y_coord / 100 + 0.5) + 'cm'

            if lo == "":
                span_node1.text = ent_list[i][0]
            else:
                span_node1.text = lo.get(ent_list[i][0])

            geometry_node1 = ET.SubElement(shape_node1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
            geometry_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
            geometry_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}mirror-horizontal"]='false'
            geometry_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}mirror-vertical"]='false'
            geometry_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='rectangle'
            geometry_node1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 0 0 L 21600 0 21600 21600 0 21600 0 0 Z N'
            float(x)
            float(y)
            y += 2.0

            if display_attr:

                for z in range(len(ent_list[i]) - 1):

                    pk = False
                    if str(ent_list[i][0] + ent_list[i][z+1]) in pk_list[i]:
                        pk = True

                    attr_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                    text_node = ET.SubElement(attr_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                    span_node = ET.SubElement(text_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")

                    if display_color:
                        
                        if pk:
                            #passt
                            attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr4'
                            attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P19'
                            text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                            span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T5'
                        else:
                            #passt
                            attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr4'
                            attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P19'
                            text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                            span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T6'
                    else:
                        if pk:
                            #passt
                            attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                            attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P22'
                            text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                            span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T5'
                        else:
                            #passt
                            attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                            attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P8'
                            text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                            span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'

                    attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=ent_list[i][0] + ent_list[i][z + 1]

                    for key,(x,y) in pos.items():
                        if key == str(ent_list[i][0]) + str(ent_list[i][z+1]):
                            x_coord = x
                            y_coord = y

                    attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                    attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='10cm'
                    attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='6cm'
                    attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]= str(x_coord / 100) + 'cm'
                    attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]= str(y_coord / 100) + 'cm'
                    if lo == "":
                        span_node.text = ent_list[i][z + 1]
                    else:
                        span_node.text = lo.get(ent_list[i][z + 1])

                    geometry_node = ET.SubElement(attr_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
                    geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
                    geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}glue-points"]='10800 0 3163 3163 0 10800 3163 18437 10800 21600 18437 18437 21600 10800 18437 3163'
                    geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='ellipse'
                    geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-areas"]='3163 3163 18437 18437'
                    geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='U 10800 10800 10800 10800 0 360 Z N'

                    connector_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}connector")
                    connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr4'
                    connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='T1'
                    connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                    connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='line'
                    connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-shape"]=ent_list[i][0]
                    connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}end-shape"]=ent_list[i][0] + ent_list[i][z + 1]
                    connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}d"]="M5889 5191v3810"
                    connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]="0 0 1 3811"

def create_rel(tree, rel_list, rel_attr_list, super_sub_list, weak_list, display_attr, display_color, pos, x_max, y_max, lo):
    root = tree.getroot()
    el = root.xpath('.//draw:page', namespaces=root.nsmap)
    el1 = el[0]
    x = 10.0
    y = 2.0

    for i in range(len(rel_list)):
        if len(weak_list[i]) <= 1:
            if len(rel_list[i]) > 1:

                shape_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                text_node = ET.SubElement(shape_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                span_node = ET.SubElement(text_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")

                if display_color:
                    
                    shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr_rel'
                    shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P_rel'
                    text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                    span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T6'
                else:

                    shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                    shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P8'
                    text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                    span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'

                x_coord = 1
                y_coord = 1
                factor_x = 15 / x_max
                factor_y = 15 / y_max

                for key,(x,y) in pos.items():
                    if key == rel_list[i][0]:
                        x_coord = x 
                        y_coord = y 
                
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=rel_list[i][0]
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='10cm'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='6cm'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]= str(x_coord / 100) + 'cm'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]= str(y_coord / 100) + 'cm'

                if lo == "":
                    span_node.text = rel_list[i][0]
                else:
                    span_node.text = lo.get(rel_list[i][0])

                geometry_node = ET.SubElement(shape_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
                geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
                geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='diamond'
                geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}mirror-horizontal"]='false'
                geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}mirror-vertical"]='false'
                geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 10800 0 L 21600 10800 10800 21600 0 10800 10800 0 Z N'
                geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}glue-points"]='10800 0 0 10800 10800 21600 21600 10800'
                geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-areas"]='5400 5400 16200 16200'

                if len(rel_list[i]) > 7:

                    node_list_rel = []
                    for e in range(0, len(rel_list[i])):
                        node_list_rel.append(e)
                        
                    for rel_list_idx in range(1, len(rel_list[i]), 3):
                        if rel_list_idx + 2 <= len(rel_list[i]):
                            
                            connector_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}connector")
                            connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr2'
                            connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P3'
                            connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                            connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='line'
                            connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-shape"]=rel_list[i][0]
                            connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}end-shape"]=rel_list[i][rel_list_idx]
                            connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}d"]="M21575 3050l2125 750"
                            connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]="0 0 2126 751"
                            text_connector = ET.SubElement(connector_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                            text_connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                            span_node_ = ET.SubElement(text_connector, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                            span_node_.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'
                            span_node_.text = "(1, 1)"

                else:
                    connector1_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}connector")
                    connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr2'
                    connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P3'
                    connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                    connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='line'
                    connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-shape"]=rel_list[i][0]
                    connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}end-shape"]=rel_list[i][1]
                    connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}d"]="M21575 3050l2125 750"
                    connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]="0 0 2126 751"
                    text_connector1 = ET.SubElement(connector1_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                    text_connector1.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                    span_node = ET.SubElement(text_connector1, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                    span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'
                    span_node.text = "(" + rel_list[i][2] + ", " + rel_list[i][3] + ")"

                    connector2_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}connector")
                    connector2_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr4'
                    connector2_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='T1'
                    connector2_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                    connector2_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='line'
                    connector2_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-shape"]=rel_list[i][0]
                    connector2_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}end-shape"]=rel_list[i][4]
                    connector2_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}d"]="M21575 3050l2125 750"
                    connector2_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]="0 0 2126 751"
                    text_connector2 = ET.SubElement(connector2_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                    text_connector2.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                    span_node = ET.SubElement(text_connector2, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                    span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'
                    span_node.text = "(" + rel_list[i][5] + ", " + rel_list[i][6] + ")"

                float(x)
                float(y)
                y += 2.0

                if display_attr:

                    if len(rel_attr_list[i]) > 1:
                        for y in range(1, len(rel_attr_list[i])):

                            rel_attr_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                            rel_attr_text_node = ET.SubElement(rel_attr_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                            rel_attr_span_node = ET.SubElement(rel_attr_text_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")

                            if display_color:         
                                    rel_attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr4'
                                    rel_attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P19'
                                    rel_attr_text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                                    rel_attr_span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T6'
                            else:
                                    rel_attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                                    rel_attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P8'
                                    rel_attr_text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                                    rel_attr_span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T5'
                   
                            rel_attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=rel_attr_list[i][0] + rel_attr_list[i][y]

                            for key,(x_c,y_c) in pos.items():
                                if key == str(rel_attr_list[i][0]) + str(rel_attr_list[i][y]):
                                    x_coord = x_c
                                    y_coord = y_c
  
                            rel_attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                            rel_attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='10cm'
                            rel_attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='6cm'
                            rel_attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]= str(x_coord / 100) + 'cm'
                            rel_attr_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]= str(y_coord / 100) + 'cm'

                            if lo == "":
                                rel_attr_span_node.text = rel_attr_list[i][y]
                            else:
                                rel_attr_span_node.text = lo.get(rel_attr_list[i][y])

                            rel_attr_geometry_node = ET.SubElement(rel_attr_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
                            rel_attr_geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
                            rel_attr_geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}glue-points"]='10800 0 3163 3163 0 10800 3163 18437 10800 21600 18437 18437 21600 10800 18437 3163'
                            rel_attr_geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='ellipse'
                            rel_attr_geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-areas"]='3163 3163 18437 18437'
                            rel_attr_geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='U 10800 10800 10800 10800 0 360 Z N'

                            rel_attr_connector_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}connector")
                            rel_attr_connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr4'
                            rel_attr_connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='T1'
                            rel_attr_connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                            rel_attr_connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='line'
                            rel_attr_connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-shape"]=rel_list[i][0]
                            rel_attr_connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}end-shape"]=rel_attr_list[i][0] + rel_attr_list[i][y]
                            rel_attr_connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}d"]="M5889 5191v3810"
                            rel_attr_connector_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]="0 0 1 3811"
                
            if len(super_sub_list[i]) > 1:
                min = ""
                max = ""
                super_sub_shape_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                super_sub_shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr9'
                super_sub_shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=super_sub_list[i][0] + "super_sub"

                if super_sub_list[i][3] == "true":
                    super_sub_shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P2'
                    max = "1"
                else:
                    super_sub_shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P17'
                    max = str(len(super_sub_list[i]) - 4)

                x_coord = 1
                y_coord = 1
                factor_x = 15 / x_max
                factor_y = 15 / y_max

                for key,(x,y) in pos.items():
                    if key == rel_list[i][0]:
                        x_coord = x 
                        y_coord = y 

                super_sub_connector1_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}connector")
                
                if super_sub_list[i][2] == "false":
                    super_sub_connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='grarrow'
                    min = "0"
                else:
                    super_sub_connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr10'
                    min = "1"

                super_sub_connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P4'
                super_sub_connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                super_sub_connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='line'
                super_sub_connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-shape"]=super_sub_list[i][0] + "super_sub"
                x_triangle = x_coord
                y_triangle = y_coord
                for key,(x,y) in pos.items():
                    if key == super_sub_list[i][1]:
                        x_ent = x 
                        y_ent = y 
                if y_ent <= y_triangle:
                    super_sub_connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-glue-point"]="4"
                else:
                    if x_ent >= x_triangle:
                        super_sub_connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-glue-point"]="8"
                    else:
                        super_sub_connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-glue-point"]="6"

                super_sub_connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}end-shape"]=super_sub_list[i][1]
                super_sub_connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}d"]="M12112 5890l-4762-1906"
                super_sub_connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]="0 0 4763 1907"
                super_sub_connector1_node_text = ET.SubElement(super_sub_connector1_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                super_sub_connector1_node_text.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                super_sub_connector1_node_span = ET.SubElement(super_sub_connector1_node_text, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                super_sub_connector1_node_span.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'

                super_sub_connector1_node_span.text = "(" + min + ", " + max + ")"

                node_list = []

                for l in range(0, len(super_sub_list[i]) + 1):
                    node_list.append(l)

                for sub in range(4, len(super_sub_list[i])):
                    
                    node_list[sub - 4] = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}connector")
                    node_list[sub - 4].attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr2'
                    node_list[sub - 4].attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P4'
                    node_list[sub - 4].attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                    node_list[sub - 4].attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='line'
                    node_list[sub - 4].attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-shape"]=super_sub_list[i][0] + "super_sub"
                    node_list[sub - 4].attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}end-shape"]=super_sub_list[i][sub]
                    node_list[sub - 4].attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}d"]="M12112 5890l-4762-1906"
                    node_list[sub - 4].attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]="0 0 4763 1907"

                    x_triangle = x_coord
                    y_triangle = y_coord
                    for key,(x,y) in pos.items():
                        if key == super_sub_list[i][sub]:
                            x_ent = x 
                            y_ent = y 
                    if y_ent <= y_triangle:
                        node_list[sub - 4].attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-glue-point"]="4"
                    else:
                        if x_ent >= x_triangle:
                            node_list[sub - 4].attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-glue-point"]="8"
                        else:
                            node_list[sub - 4].attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-glue-point"]="6"

                    super_sub_connector_node_text = ET.SubElement(node_list[sub - 4], "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                    super_sub_connector_node_text.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                    super_sub_connector_node_span = ET.SubElement(super_sub_connector_node_text, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                    super_sub_connector_node_span.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'
                    super_sub_connector_node_span.text = "(1, 1)"

                float(x)
                float(y)
                y += 2.0


                super_sub_shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                super_sub_shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='10cm'
                super_sub_shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='6cm'
                super_sub_shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]= str(x_coord / 100) + 'cm'
                super_sub_shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]= str(y_coord / 100) + 'cm'

                super_sub_geometry_node = ET.SubElement(super_sub_shape_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
                super_sub_geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
                super_sub_geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='isosceles-triangle'
                super_sub_geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}mirror-horizontal"]='false'
                super_sub_geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}mirror-vertical"]='false'
                super_sub_geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M ?f0 0 L 21600 21600 0 21600 Z N'
                super_sub_geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}glue-points"]='?f0 0 ?f1 10800 0 21600 10800 21600 21600 21600 ?f7 10800'
                super_sub_geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}modifiers"]='10800'
                #super_sub_geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='isosceles-triangle'
                super_sub_geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-areas"]='?f1 10800 ?f2 18000 ?f3 7200 ?f4 21600'
                super_sub_equation_node_1 = ET.SubElement(super_sub_geometry_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}equation")
                super_sub_equation_node_1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}name"]='f0'
                super_sub_equation_node_1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}formula"]='$0 '
                super_sub_equation_node_2 = ET.SubElement(super_sub_geometry_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}equation")
                super_sub_equation_node_2.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}name"]='f1'
                super_sub_equation_node_2.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}formula"]='$0 /2'
                super_sub_equation_node_3 = ET.SubElement(super_sub_geometry_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}equation")
                super_sub_equation_node_3.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}name"]='f2'
                super_sub_equation_node_3.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}formula"]='?f1 +10800'
                super_sub_equation_node_4 = ET.SubElement(super_sub_geometry_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}equation")
                super_sub_equation_node_4.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}name"]='f3'
                super_sub_equation_node_4.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}formula"]='$0 *2/3'
                super_sub_equation_node_5 = ET.SubElement(super_sub_geometry_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}equation")
                super_sub_equation_node_5.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}name"]='f4'
                super_sub_equation_node_5.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}formula"]='?f3 +7200'
                super_sub_equation_node_6 = ET.SubElement(super_sub_geometry_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}equation")
                super_sub_equation_node_6.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}name"]='f5'
                super_sub_equation_node_6.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}formula"]='21600-?f0 '
                super_sub_equation_node_7 = ET.SubElement(super_sub_geometry_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}equation")
                super_sub_equation_node_7.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}name"]='f6'
                super_sub_equation_node_7.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}formula"]='?f5 /2'
                super_sub_equation_node_8 = ET.SubElement(super_sub_geometry_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}equation")
                super_sub_equation_node_8.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}name"]='f7'
                super_sub_equation_node_8.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}formula"]='21600-?f6 '
                super_sub_handle_node = ET.SubElement(super_sub_geometry_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}equation")
                super_sub_handle_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}handle-position"]='$0 top'
                super_sub_handle_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}handle-range-x-minimum"]='0'
                super_sub_handle_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}handle-range-x-maximum"]='21600'




        else:
            group_node_rel = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}g")
            group_node_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=rel_list[i][0]

            shape_node_weak_rel = ET.SubElement(group_node_rel, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
            text_node_weak_rel = ET.SubElement(shape_node_weak_rel, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
            span_node_weak_rel = ET.SubElement(text_node_weak_rel, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
            shape_node_weak_rel1 = ET.SubElement(group_node_rel, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
            text_node_weak_rel1 = ET.SubElement(shape_node_weak_rel1, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
            span_node_weak_rel1 = ET.SubElement(text_node_weak_rel1, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")

            if display_color:
                shape_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                shape_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P8'
                text_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                span_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'      
                shape_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr_rel'
                shape_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P_rel'
                text_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                span_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T6'
            else:

                shape_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                shape_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P8'
                text_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                span_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'
                shape_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                shape_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P8'
                text_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                span_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'

            x_coord = 1
            y_coord = 1
            factor_x = 15 / x_max
            factor_y = 15 / y_max

            for key,(x,y) in pos.items():
                if key == rel_list[i][0]:
                    x_coord = x 
                    y_coord = y

            shape_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
            shape_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='10cm'
            shape_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='6cm'
            shape_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]= str(x_coord / 100) + 'cm'
            shape_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]= str(y_coord / 100) + 'cm'

            geometry_node_weak_rel = ET.SubElement(shape_node_weak_rel, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
            geometry_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
            geometry_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='diamond'
            geometry_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}mirror-horizontal"]='false'
            geometry_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}mirror-vertical"]='false'
            geometry_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 10800 0 L 21600 10800 10800 21600 0 10800 10800 0 Z N'
            geometry_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}glue-points"]='10800 0 0 10800 10800 21600 21600 10800'
            geometry_node_weak_rel.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-areas"]='5400 5400 16200 16200'

            shape_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
            shape_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='9cm'
            shape_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='5cm'
            shape_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]= str(x_coord / 100 + 0.5) + 'cm'
            shape_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]= str(y_coord / 100 + 0.5) + 'cm'

            if lo == "":
                span_node_weak_rel1.text = rel_list[i][0]
            else:
                span_node_weak_rel1.text = lo.get(rel_list[i][0])

            geometry_node_weak_rel1 = ET.SubElement(shape_node_weak_rel1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
            geometry_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
            geometry_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='diamond'
            geometry_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}mirror-horizontal"]='false'
            geometry_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}mirror-vertical"]='false'
            geometry_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 10800 0 L 21600 10800 10800 21600 0 10800 10800 0 Z N'
            geometry_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}glue-points"]='10800 0 0 10800 10800 21600 21600 10800'
            geometry_node_weak_rel1.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-areas"]='5400 5400 16200 16200'

            connector1_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}connector")
            connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr2'
            connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P3'
            connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
            connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='line'
            connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-shape"]=rel_list[i][0]
            connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}end-shape"]=rel_list[i][1]
            connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}d"]="M21575 3050l2125 750"
            connector1_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]="0 0 2126 751"
            text_connector1 = ET.SubElement(connector1_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
            text_connector1.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
            span_node = ET.SubElement(text_connector1, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
            span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'
            span_node.text = "(" + rel_list[i][2] + ", " + rel_list[i][3] + ")"

            connector2_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}connector")
            connector2_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr4'
            connector2_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='T1'
            connector2_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
            connector2_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='line'
            connector2_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-shape"]=rel_list[i][0]
            connector2_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}end-shape"]=rel_list[i][4]
            connector2_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}d"]="M21575 3050l2125 750"
            connector2_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]="0 0 2126 751"
            text_connector2 = ET.SubElement(connector2_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
            text_connector2.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
            span_node = ET.SubElement(text_connector2, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
            span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'
            span_node.text = "(" + rel_list[i][5] + ", " + rel_list[i][6] + ")"

def main(tree, display_color, display_attr, lo_tree, args):

    starttime = time.time()
    
    root = tree.getroot()
    empty_doc_tree = get_empty_doc()

    if lo_tree is not None:
        lo_root = lo_tree.getroot()
        lo = get_lo(lo_root)
    else:
        lo = ""

    ent = get_ent_attr(root)
    rel = get_rel(root)
    pk = get_pk(root)
    rel_attr = get_rel_attr(root)
    super_sub = get_super_sub(root)
    weak = get_weak(root)
    rel_only = get_rel_only(root)
    super_sub_only = get_super_sub_only(root)

    #----------------------Layout--------------------------------------

    rel_t = []
    for akt in super_sub_only:
        if len(akt) > 1:
            rel_t.append(akt)

    for curr in rel_only:
        for akt in curr:
            if akt not in rel_t:
                rel_t.append(curr)

    ent_for_layout = []
    for i in range(len(ent)):
        tmp = [ent[i][0]]
        for y in range(1, len(ent[i])):
            tmp.append(str(ent[i][0]) + str(ent[i][y]))
        ent_for_layout.append(tmp)

    for curr in ent_for_layout:
        rel_t.append(curr)

    rel_attr_for_layout = []
    for i in range(len(rel_attr)):
        tmp = [rel_attr[i][0]]
        if len(rel_attr[i]) > 1:
            for y in range(1, len(rel_attr[i])):
                tmp.append(str(rel_attr[i][0]) + str(rel_attr[i][y]))
            rel_attr_for_layout.append(tmp)

    for curr in rel_attr_for_layout:
        rel_t.append(curr)

    pos = nx_graph(rel_t, args)
    
    xmax = 0
    ymax = 0

    for key,(x,y) in pos.items():
        if x > xmax:
            xmax = x
        if y > ymax:
            ymax = y

    resize_doc(empty_doc_tree, xmax, ymax)

    #-------------------End Layout----------------------------------------------

    create_ent(empty_doc_tree, ent, pk, weak, rel, rel_attr, super_sub, display_attr, display_color, pos, xmax, ymax, lo)
    create_rel(empty_doc_tree, rel, rel_attr, super_sub, weak, display_attr, display_color, pos, xmax, ymax, lo)


    title = "output"
    for child in root:
        if child.tag == "title":
            if child.get('lang') is None:
                title = child.get('name')



    try:
        if args.output is None:
            empty_doc_tree.write( title + '.fodg', xml_declaration=True)
            print("Saved to " + "'" + os.getcwd() + "/" + title + ".fodg'")

        else:
            path_and_nof = args.output.split('/')
            name_of_file = path_and_nof[-1] + ".fodg"
            empty_doc_tree.write( name_of_file, xml_declaration=True)
            print("Saved to " + "'" + os.getcwd() + "/" + args.output)
            if (len(path_and_nof) > 1):  
                subprocess.call('cp ' + name_of_file + ' ' + args.output, shell=True)
                subprocess.call('rm ' + name_of_file, shell=True)

    except IOError:
        print(Fore.RED + "There was a Problem creating the file. Please try again" + Fore.RESET)
        return

    endtime = time.time()
    

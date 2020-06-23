#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from lxml import etree as ET

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


def get_ent_attr(path):
    root = get_root(path)

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

def get_pk(path):
    root = get_root(path)

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



def get_rel_attr(path):
    root = get_root(path)

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

def get_empty_doc():
    tree = get_tree("empty_block.fodg")
    return tree



def create_ent(tree, ent_list, pk_list):
    root = tree.getroot()
    el = root.xpath('.//draw:page', namespaces=root.nsmap)
    el1 = el[0]
    y_coord = 2.0
    for i in range(len(ent_list)):
        x_coord = 2.0
        for y in range(len(ent_list[i])):
            if ent_list[i][y] == ent_list[i][0]:

                

                shape_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=ent_list[i][0]

                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='T1'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='0cm'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='0.75cm'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]= str(x_coord) + 'cm'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]= str(y_coord) + 'cm'
                text_node = ET.SubElement(shape_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                span_node = ET.SubElement(text_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                span_node.text = ent_list[i][y]
                text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P2'
                span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T2'
                x_coord += 2

            else:
                shape_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=ent_list[i][0] + ent_list[i][y]

                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='T1'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='2.0cm'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='0.75cm'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]= str(x_coord) + 'cm'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]= str(y_coord) + 'cm'
                text_node = ET.SubElement(shape_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                span_node = ET.SubElement(text_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P2'
                span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T2'
                span_node.text = ent_list[i][y]
                
                pk = False

                for a in pk_list:
                    if a[0] == ent_list[i][0]:
                        for b in range(1, len(a)):
                            if a[b] == ent_list[i][y]:
                                pk = True

                if pk:
                    text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P2'
                    span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T5'
                else:
                    text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'
                    span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T2'
                
                geometry_node = ET.SubElement(shape_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
                geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
                geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='rectangle'
                geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 0 0 L 21600 0 21600 21600 0 21600 0 0 Z N'
                float(x_coord)
                float(y_coord)
                x_coord += 2
        
        y_coord += 1.5
    return y_coord 

def create_rel(tree, ent_list, rel_list, pk_list, y_coord):
    root = tree.getroot()
    el = root.xpath('.//draw:page', namespaces=root.nsmap)
    el1 = el[0]
    for i in range(len(rel_list)):
        if len(rel_list[i]) >= 6:
            if rel_list[i][3] == 'n' and rel_list[i][6] == 'n':

                x_coord = 2.0
                shape_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=rel_list[i][0]

                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='T1'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='2.0cm'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='0.75cm'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]= str(x_coord) + 'cm'
                shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]= str(y_coord) + 'cm'
                text_node = ET.SubElement(shape_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                span_node = ET.SubElement(text_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                span_node.text = rel_list[i][0]
                text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P2'
                span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T2'
                x_coord += 2
                
                
                for y in pk_list:
                    if len(y) > 1:
                        if y[0] == rel_list[i][1]:
                            shape_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=rel_list[i][1]

                            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='T1'
                            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='2.0cm'
                            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='0.75cm'
                            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]= str(x_coord) + 'cm'
                            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]= str(y_coord) + 'cm'
                            text_node = ET.SubElement(shape_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                            span_node = ET.SubElement(text_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                            span_node.text = y[1]
                            text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P2'
                            span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T2'
                            geometry_node = ET.SubElement(shape_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
                            geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
                            geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='rectangle'
                            geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 0 0 L 21600 0 21600 21600 0 21600 0 0 Z N'
                            x_coord += 2

                        if y[0] == rel_list[i][4]:
                            shape_node = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=rel_list[i][4]

                            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='T1'
                            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='2.0cm'
                            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='0.75cm'
                            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]= str(x_coord) + 'cm'
                            shape_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]= str(y_coord) + 'cm'
                            text_node = ET.SubElement(shape_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                            span_node = ET.SubElement(text_node, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                            span_node.text = y[1]
                            text_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P2'
                            span_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T2'
                            geometry_node = ET.SubElement(shape_node, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
                            geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
                            geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='rectangle'
                            geometry_node.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 0 0 L 21600 0 21600 21600 0 21600 0 0 Z N'
                            x_coord += 2
                    else:
                        print("Kann keine Super-Sub Typen darstellen")

                y_coord += 1.5


def main():
    print("begin")
    inputfile = "../datenmodelle/weingut/xml/weingut.xerml.xml"
    root = get_root(inputfile)
    tree = get_tree(inputfile)
    empty_doc_tree = get_empty_doc()

    ent = get_ent_attr(inputfile)
    rel = get_rel_attr(inputfile)
    pk = get_pk(inputfile)

    y_coord = create_ent(empty_doc_tree, ent, pk)
    create_rel(empty_doc_tree, ent, rel, pk, y_coord)
    print(rel)
    print()
    print(ent)
    print()
    print(pk)


    empty_doc_tree.write('block.fodg', xml_declaration=True)

    print("finished")


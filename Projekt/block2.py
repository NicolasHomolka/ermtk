#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# date:     21.03.19 10:16
# author:   Nicolas Homolka
# TODO:     (mehrere PK zusammenfassen und umrahmen), 
#           Sprachfile, pk selber name = problem (tank)
#           mehrwertige Bez

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

def get_super_sub_and_weak(root):
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

def get_empty_doc():
    tree = get_tree("empty_block2.fodg")
    return tree

def resize_doc(tree, x_max, y_max):
    root = tree.getroot()
    el = root.xpath('.//style:page-layout-properties', namespaces=root.nsmap)
    el1 = el[0]
    el1.attrib["{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}page-width"]= str(x_max + 5) + "cm"
    el1.attrib["{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}page-height"]= str(y_max + 5) + "cm"


def create_norm_elem(tree, ent, pk, super_sub):
    root = tree.getroot()
    el = root.xpath('.//draw:page', namespaces=root.nsmap)
    el1 = el[0]
    x_coord = 2
    y_coord = 3
    coords_of_rows = []
    for dimout in range(len(ent)):
        frame = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}frame")
        frame.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
        frame.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P2'
        frame.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
        frame.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='3cm'
        frame.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='1cm'
        frame.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]=str(x_coord)+'cm'
        frame.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]=str(y_coord)+'cm'
        text_box = ET.SubElement(frame, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-box")
        text = ET.SubElement(text_box, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
        text.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
        span = ET.SubElement(text, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
        span.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'
        span.text = ent[dimout][0]
        x_coord += 3

        for ss_dimout in range(len(super_sub)):
            if len(super_sub[ss_dimout]) > 1:
                for ss_dimin in range(2, len(super_sub[ss_dimout])):
                    if ent[dimout][0] == super_sub[ss_dimout][ss_dimin]:
                        for pk_dimout in range(len(pk)):
                            if super_sub[ss_dimout][1] in pk[pk_dimout]:
                                for pk_dimin in range(1, len(pk[pk_dimout])):
                                    custom_shape = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                                    custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr2'
                                    custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P4'
                                    custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=ent[dimout][0] + pk[pk_dimout][pk_dimin]
                                    custom_shape.attrib["id"]=ent[dimout][0] + pk[pk_dimout][pk_dimin]
                                    custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                                    custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='3cm'
                                    custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='1cm'
                                    custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]=str(x_coord)+'cm'
                                    custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]=str(y_coord)+'cm'
                                    text = ET.SubElement(custom_shape, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                                    text.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P3'
                                    span = ET.SubElement(text, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                                    span.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T2'
                                    span.text = pk[pk_dimout][pk_dimin]
                                    to_app = pk[pk_dimout][pk_dimin]

                                    for i in range(len(pk)):
                                        if pk[i][0] == ent[dimout][0]:
                                            if to_app not in pk[i]:
                                                pk[i].append(to_app)
                                    
                                    enhanced_geometry = ET.SubElement(custom_shape, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
                                    enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
                                    enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='rectangle'
                                    enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 0 0 L 21600 21600 0 21600 0 0 Z N'
                                    x_coord += 3

                                    connector = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}connector")
                                    connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr4'
                                    connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P7'
                                    connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                                    connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='lines'
                                    connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-shape"]=ent[dimout][0] + pk[pk_dimout][pk_dimin]
                                    connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}end-shape"]=super_sub[ss_dimout][1] + pk[pk_dimout][pk_dimin]
                                    connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}d"]='M6500 4000v501 1198 501'
                                    connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 1 2201'      
        
        for dimin in range(1, len(ent[dimout])):
            if ent[dimout][dimin] in pk[dimout]:
                custom_shape = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr2'
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P4'
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr2'
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=ent[dimout][0] + ent[dimout][dimin]
                custom_shape.attrib["id"]=ent[dimout][0] + ent[dimout][dimin]
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='3cm'
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='1cm'
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]=str(x_coord)+'cm'
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]=str(y_coord)+'cm'
                text = ET.SubElement(custom_shape, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                text.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P3'
                span = ET.SubElement(text, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                span.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T2'
                span.text = ent[dimout][dimin]
                enhanced_geometry = ET.SubElement(custom_shape, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
                enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
                enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='rectangle'
                enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 0 0 L 21600 21600 0 21600 0 0 Z N'
                x_coord += 3
            else:
                custom_shape = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr3'
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P6'
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr2'
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=ent[dimout][0] + ent[dimout][dimin]
                custom_shape.attrib["id"]=ent[dimout][0] + ent[dimout][dimin]
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='3cm'
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='1cm'
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]=str(x_coord)+'cm'
                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]=str(y_coord)+'cm'
                text = ET.SubElement(custom_shape, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                text.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P5'
                span = ET.SubElement(text, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                span.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'
                span.text = ent[dimout][dimin]
                enhanced_geometry = ET.SubElement(custom_shape, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
                enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
                enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='rectangle'
                enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 0 0 L 21600 21600 0 21600 0 0 Z N'
  
                x_coord += 3
        coords_of_rows.append([ent[dimout][0], x_coord, y_coord])
        x_coord = 2
        y_coord += 2
    return y_coord, coords_of_rows, pk

def create_add_elem(tree, rel, y_coord, pk, rel_attr):
    root = tree.getroot()
    el = root.xpath('.//draw:page', namespaces=root.nsmap)
    el1 = el[0]
    x_coord = 2
    for dimout in range(len(rel)):
        if len(rel[dimout]) >= 7:
            if rel[dimout][3] == "n" and rel[dimout][6] == "n":
                frame = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}frame")
                frame.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr1'
                frame.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P2'
                frame.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                frame.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='3cm'
                frame.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='1cm'
                frame.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]=str(x_coord)+'cm'
                frame.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]=str(y_coord)+'cm'
                text_box = ET.SubElement(frame, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-box")
                text = ET.SubElement(text_box, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                text.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P1'
                span = ET.SubElement(text, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                span.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'
                span.text = rel[dimout][0]
                x_coord += 3
                
                for pk_dimout in range(len(pk)):
                    if rel[dimout][1] == pk[pk_dimout][0]:
                        for pk_dimin in range(1, len(pk[pk_dimout])):
                            custom_shape = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr2'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P4'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr2'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=rel[dimout][0] + pk[pk_dimout][0] + pk[pk_dimout][pk_dimin] + "add"
                            custom_shape.attrib["id"]=rel[dimout][0] + pk[pk_dimout][0] + pk[pk_dimout][pk_dimin] + "add"
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='3cm'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='1cm'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]=str(x_coord)+'cm'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]=str(y_coord)+'cm'
                            text = ET.SubElement(custom_shape, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                            text.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P3'
                            span = ET.SubElement(text, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                            span.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T2'
                            span.text = pk[pk_dimout][pk_dimin]
                            enhanced_geometry = ET.SubElement(custom_shape, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
                            enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
                            enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='rectangle'
                            enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 0 0 L 21600 21600 0 21600 0 0 Z N'
                            x_coord += 3

                            connector = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}connector")
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr4'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P7'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='lines'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-shape"]=rel[dimout][0] + pk[pk_dimout][0] + pk[pk_dimout][pk_dimin] + "add"
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}end-shape"]=rel[dimout][1] + pk[pk_dimout][pk_dimin]
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}d"]='M6500 4000v501 1198 501'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 1 2201'
                            
                    if rel[dimout][4] == pk[pk_dimout][0]:
                        for pk_dimin in range(1, len(pk[pk_dimout])):
                            custom_shape = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr2'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P4'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr2'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=rel[dimout][0] + pk[pk_dimout][0] + pk[pk_dimout][pk_dimin] + "add"
                            custom_shape.attrib["id"]=rel[dimout][0] + pk[pk_dimout][0] + pk[pk_dimout][pk_dimin] + "add"
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='3cm'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='1cm'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]=str(x_coord)+'cm'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]=str(y_coord)+'cm'
                            text = ET.SubElement(custom_shape, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                            text.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P3'
                            span = ET.SubElement(text, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                            span.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T2'
                            span.text = pk[pk_dimout][pk_dimin]
                            enhanced_geometry = ET.SubElement(custom_shape, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
                            enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
                            enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='rectangle'
                            enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 0 0 L 21600 21600 0 21600 0 0 Z N'
                            x_coord += 3
                            connector = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}connector")
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr4'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P7'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='lines'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-shape"]=rel[dimout][0] + pk[pk_dimout][0] + pk[pk_dimout][pk_dimin] + "add"
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}end-shape"]=rel[dimout][4] + pk[pk_dimout][pk_dimin]
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}d"]='M6500 4000v501 1198 501'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 1 2201'
                for rel_attr_dimout in range(len(rel_attr)):
                    if len(rel_attr[rel_attr_dimout]) > 1:
                        if rel_attr[rel_attr_dimout][0] == rel[dimout][0]:
                            for rel_attr_dimin in range(1, len(rel_attr[rel_attr_dimout])):
                                custom_shape = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr3'
                                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P6'
                                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr2'
                                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=rel[dimout][0] + rel_attr[rel_attr_dimout][rel_attr_dimin]
                                custom_shape.attrib["id"]=rel[dimout][0] + rel_attr[rel_attr_dimout][rel_attr_dimin]
                                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='3cm'
                                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='1cm'
                                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]=str(x_coord)+'cm'
                                custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]=str(y_coord)+'cm'
                                text = ET.SubElement(custom_shape, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                                text.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P5'
                                span = ET.SubElement(text, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                                span.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'
                                span.text = rel_attr[rel_attr_dimout][rel_attr_dimin]
                                enhanced_geometry = ET.SubElement(custom_shape, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
                                enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
                                enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='rectangle'
                                enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 0 0 L 21600 21600 0 21600 0 0 Z N'
                                x_coord += 3      
                x_coord = 2
                y_coord += 2
    return y_coord
                
def create_1n_rels(tree, rel, ent, coords_of_rows, pk):
    root = tree.getroot()
    el = root.xpath('.//draw:page', namespaces=root.nsmap)
    el1 = el[0]
    
    for dimout in range(len(rel)):
        if len(rel[dimout]) > 1:
            if rel[dimout][3] == "1":

                for pk_dimout in range(len(pk)):
                    if rel[dimout][4] == pk[pk_dimout][0]:
                        x_coord = 0
                        y_coord = 0
                        for coord_dimout in range(len(coords_of_rows)):
                            if rel[dimout][1] == coords_of_rows[coord_dimout][0]:
                                x_coord = coords_of_rows[coord_dimout][1]
                                y_coord = coords_of_rows[coord_dimout][2]
                        
                        for pk_dimin in range(1, len(pk[pk_dimout])):

                            custom_shape = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr3'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P6'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr2'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=rel[dimout][0] + pk[pk_dimout][pk_dimin]
                            custom_shape.attrib["id"]=rel[dimout][0] + pk[pk_dimout][pk_dimin]
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='3cm'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='1cm'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]=str(x_coord)+'cm'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]=str(y_coord)+'cm'
                            text = ET.SubElement(custom_shape, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                            text.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P5'
                            span = ET.SubElement(text, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                            span.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'
                            span.text = pk[pk_dimout][pk_dimin]
                            enhanced_geometry = ET.SubElement(custom_shape, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
                            enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
                            enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='rectangle'
                            enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 0 0 L 21600 21600 0 21600 0 0 Z N'
                            x_coord += 3

                            connector = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}connector")
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr4'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P7'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='lines'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-shape"]=rel[dimout][0] + pk[pk_dimout][pk_dimin]
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}end-shape"]=rel[dimout][4] + pk[pk_dimout][pk_dimin]
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}d"]='M6500 4000v501 1198 501'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 1 2201'
                            
            if rel[dimout][6] == "1":

                for pk_dimout in range(len(pk)):
                    if rel[dimout][1] == pk[pk_dimout][0]:
                        x_coord = 0
                        y_coord = 0
                        for coord_dimout in range(len(coords_of_rows)):
                            if rel[dimout][4] == coords_of_rows[coord_dimout][0]:
                                x_coord = coords_of_rows[coord_dimout][1]
                                y_coord = coords_of_rows[coord_dimout][2]
                        for pk_dimin in range(1, len(pk[pk_dimout])):

                            custom_shape = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}custom-shape")
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr3'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P6'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr2'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}id"]=rel[dimout][0] + pk[pk_dimout][pk_dimin]
                            custom_shape.attrib["id"]=rel[dimout][0] + pk[pk_dimout][pk_dimin]
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width"]='3cm'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height"]='1cm'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x"]=str(x_coord)+'cm'
                            custom_shape.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y"]=str(y_coord)+'cm'
                            text = ET.SubElement(custom_shape, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p")
                            text.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='P5'
                            span = ET.SubElement(text, "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span")
                            span.attrib["{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name"]='T1'
                            span.text = pk[pk_dimout][pk_dimin]
                            enhanced_geometry = ET.SubElement(custom_shape, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-geometry")
                            enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 21600 21600'
                            enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='rectangle'
                            enhanced_geometry.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}enhanced-path"]='M 0 0 L 21600 21600 0 21600 0 0 Z N'
                            x_coord += 3

                            connector = ET.SubElement(el1, "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}connector")
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name"]='gr4'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}text-style-name"]='P7'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}layer"]='layout'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}type"]='lines'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}start-shape"]=rel[dimout][0] + pk[pk_dimout][pk_dimin]
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}end-shape"]=rel[dimout][1] + pk[pk_dimout][pk_dimin]
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}d"]='M6500 4000v501 1198 501'
                            connector.attrib["{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}viewBox"]='0 0 1 2201'
    for i in range(len(coords_of_rows)):
        if x_coord < coords_of_rows[i][1]:
            x_coord = coords_of_rows[i][1]
    return x_coord

def main(tree):

    root = tree.getroot()
    empty_doc_tree = get_empty_doc()

    ent = get_ent_attr(root)
    rel = get_rel(root)
    pk = get_pk(root)
    super_sub = get_super_sub_and_weak(root)
    weak = get_weak(root)
    rel_attr = get_rel_attr(root)

    for weak_dimout in range(len(weak)):
        if len(weak[weak_dimout]) > 1:
            for rel_dimout in range(len(rel)):
                if weak[weak_dimout][0] == rel[rel_dimout][0]:
                    if rel[rel_dimout][1] == weak[weak_dimout][1]:
                        super_sub.append([weak[weak_dimout][0], rel[rel_dimout][4], rel[rel_dimout][1]])
                        del(rel[rel_dimout])
                        rel.append([""])
                    else:
                        super_sub.append([weak[weak_dimout][0], rel[rel_dimout][1], rel[rel_dimout][4]])
                        del(rel[rel_dimout])
                        rel.append([""])


    y_coord, coords_of_rows, pk_new = create_norm_elem(empty_doc_tree, ent, pk, super_sub)
    y_max = create_add_elem(empty_doc_tree, rel, y_coord, pk_new, rel_attr)
    x_max = create_1n_rels(empty_doc_tree, rel, ent, coords_of_rows, pk_new)
    resize_doc(empty_doc_tree, x_max, y_max)

    empty_doc_tree.write('block.fodg', xml_declaration=True)

    print("Saved to " + "'" + os.getcwd() + "/block.fodg'")

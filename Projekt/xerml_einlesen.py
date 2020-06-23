#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#5.12.18 11:36

from colorama import Fore, Back
import os
import xml.etree.ElementTree as et
from lxml import etree
import sys



def get_xmlgramma(path):
    base_path = os.path.dirname(os.path.realpath(__file__))
    xml_file = os.path.join(base_path, path)
    return xml_file

def get_xmlfile(path):
    xml_file = os.path.realpath(path)
    return xml_file

def get_root(path):
    base_path = os.path.dirname(os.path.realpath(__file__))
    xml_file = os.path.join(base_path, path)
    tree = et.parse(xml_file)
    root = tree.getroot()
    return root

def open(path):
    grammaTree = etree.ElementTree(file=get_xmlgramma("Grammatik/xerml.rng"))
    schemaInstance = etree.RelaxNG(grammaTree)
    try:
        print(path)
        print(get_xmlfile(path))
        fileTree = etree.ElementTree(file=get_xmlfile(path))
        if schemaInstance.validate(fileTree) == 1:
            print("-> XERML-File: " + str(path) + " sucessfully parsed")
            # return data.Data(path, 0)
            return fileTree
        else:
            print(schemaInstance.error_log)
            sys.exit()
            return False
    except OSError:
        print(Fore.RED + "-> XERML-File: " + str(path) + " not found." + Fore.RESET)
        sys.exit()

#Wenn man einmal NUR die inputfile ohne ty oder lo falsch einliest (Datei ist nicht vorhanden) dann
#funkitoniert das Einlesen der richtigen Datei (Datei ist vorhanden) auch nicht mehr!!!!

def openLang(path):
    grammaTree = etree.ElementTree(file=get_xmlgramma("Grammatik/xerml_loc.rng"))
    schemaInstance = etree.RelaxNG(grammaTree)
    try:
        fileTree = etree.ElementTree(file=get_xmlfile(path))
        if schemaInstance.validate(fileTree) == 1:
            print("-> XERML-Language-File: " + str(path) + " sucessfully parsed")
            # return data.Data(path, 1)
            return fileTree
        else:
            print(schemaInstance.error_log)
            sys.exit()
            return False
    except OSError:
        print(Fore.RED + "-> XERML-Language-File: " + str(path) + " not found" + Fore.RESET)
        sys.exit()

def openTyp(path):
    grammaTree = etree.ElementTree(file=get_xmlgramma("Grammatik/xerml_typ.rng"))
    schemaInstance = etree.RelaxNG(grammaTree)
    try:
        fileTree = etree.ElementTree(file=get_xmlfile(path))
        if schemaInstance.validate(fileTree) == 1:
            print("-> XERML-Typ-File: " + str(path) + " sucessfully parsed")
            # return data.Data(path, 2)
            return fileTree
        else:
            print(schemaInstance.error_log)
            sys.exit()
            return False
    except OSError:
        print(Fore.RED + "-> XERML-Typ-File: " + str(path) + " not found" + Fore.RESET)
        sys.exit()


def focus(completetree, ent_focus, relcounter):
    focusrootelem = etree.fromstring(etree.tostring(completetree.getroot()))
    focustree = etree.ElementTree(element=focusrootelem)
    entities = [ent_focus]
    relations = []
    root = focustree.getroot()

    ret = rek_search(ent_focus, int(relcounter), root)
    entities = entities + ret[0]
    relations = relations + ret[1]

    entities = list(dict.fromkeys(entities))
    relations = list(dict.fromkeys(relations))

    print(entities)
    print(relations)

    for ent in root.findall('ent'):
        remove_ent = False
        for needed_ent in entities:
            if not ent.get('name') == needed_ent:
                remove_ent = True
            else:
                remove_ent = False
                break
        if remove_ent:
            root.remove(ent)
    for rel in root.findall('rel'):
        remove_rel = False
        for needed_rel in relations:
            if not rel.get('to') == needed_rel:
                remove_rel = True
            else:
                remove_rel = False
                break
        if remove_rel:
            root.remove(rel)
    focustree.write(ent_focus + '.xerml.xml')
    return focustree


def rek_search(ent, relcounter, root):
    entities = [ent]
    relations = []
    temp_ent = [ent]
    temp_rel = []
    ret = ([], [])
    if relcounter > 1:
        ret = rek_search(ent, relcounter-1, root)
    entities = entities + ret[0]
    relations = relations + ret[1]
    for ent_focus in entities:
        for rel in root.findall('rel'):
            for part in rel:
                if part.get('ref') == ent_focus:
                    temp_rel.append(rel.get('to'))
                    for needed_part in rel:
                        if needed_part.get('ref') not in entities and not (needed_part.get('ref') == ent_focus):
                            temp_ent.append(needed_part.get('ref'))
    entities = temp_ent + entities
    relations = relations + temp_rel
    coll = (entities, relations)
    return coll


def get_ent(path):
    root = get_root(path)

    matrix = []
    for child in root:
        if child.tag == 'ent':
            matrix.append(child.get('name'))

    print_ent(matrix)


def get_rel(path):
    root = get_root(path)

    matrix = []
    for child in root:
        if child.tag == 'rel':
            matrix.append(child.get('to'))

    print_rel(matrix)


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

    print_ent_attr(matrix)


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

        if len(temp_matrix) > 0:
            matrix.insert(first_level, temp_matrix)
            first_level += 1

    print_rel_attr(matrix)


def print_ent(matrix):

    print(" \nEntity-Types:")
    print("--------------------------------------------------------------------------------\n")
    for elem in matrix:
        print(elem)
    print()


def print_rel(matrix):

    print(" \nRelationship-Types:")
    print("--------------------------------------------------------------------------------\n")
    for elem in matrix:
        print(elem)
    print()


def print_ent_attr(matrix):

    print(" \nEntity-Types and attributes:")
    print("--------------------------------------------------------------------------------\n")
    for list in matrix:
        print(list[0] + ": \n")
        for i in list:
            if i != list[0]:
                print("\t" + i)
        print()
    print()

def print_rel_attr(matrix):

    print(" \nRelationship-Types and attributes:")
    print("--------------------------------------------------------------------------------\n")
    temp = ""
    for list in matrix:
        from_to = 0
        print(list[0] + ": \n")
        for i in list:
            if i != list[0]:
                if from_to == 0:
                    temp = "\tfrom " + i
                    from_to += 1
                else:
                    print(temp + " to " + i)

        print()
    print()

def list_all(path, ent, rel, attr, all):

    if rel and ent and attr:
        get_ent_attr(path)
        get_rel_attr(path)

    elif ent and attr:
        get_ent_attr(path)

    elif rel and attr:
        get_rel_attr(path)

    elif rel and ent:
        get_ent(path)
        get_rel(path)

    elif all:
        get_ent_attr(path)
        get_rel_attr(path)

    elif ent:
        get_ent(path)

    elif rel:
        get_rel(path)
    else:
        print("Please write one of the following commands: -ent | -rel | -all | -inf | -ent -rel "
              "| -ent -attr | -rel -attr | -ent -rel -attr")


# ----------------------------------------------------------------------------------------------------------------------



def list_inf(path):
    root = get_root(path)
    entitys = 0
    relations = 0
    title = ""
    title_en = ""
    title_en2 = ""

    for child in root:
        if child.tag == "ent":
            entitys = entitys + 1
        elif child.tag == "rel":
            relations = relations + 1
        elif child.tag == "title":
            if child.get('lang') is None:
                title = child.get('name')
            elif child.get('lang') == 'en':
                title_en = child.get('name')
                if title_en != "":
                    title_en2 = " (" + title_en + ") "
    print("-> XERML-File Data:\n   " + title + title_en2 + "\n   Entity-Types: " + str(entitys) +
          "\n   Relationship-Types: " + str(relations))
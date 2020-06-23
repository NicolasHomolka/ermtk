#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import Datensatz
import datenbank
import column
import table
import re
import sys
from colorama import Fore


datenbank = datenbank.datenbank
relations = []

def createColumn(tab,name, ucol, col, prime, type, qoute):
    root = type.getroot()
    type = ""
    min = ""
    max = ""
    clas = ""
    for typdsc in root.findall("typdsc"):
        if typdsc.get("entref") == name:
            for val in typdsc.findall("val"):
                if val.get("attr") == col:
                    x = val.text
                    try:
                        int(x)
                        type = "integer"
                    except ValueError:
                        try:
                            float(x)
                            type = "rational"
                        except ValueError:
                            type = "string"
            for attr in typdsc.findall("attr"):
                if attr.get("name") == col:
                    type = attr.get("type")
                    if attr.get("min") == None:
                        min = ""
                    else:
                        min = attr.get("min")
                    if attr.get("max") == None:
                        max = ""
                    else:
                        max = attr.get("max")
                    if attr.get("class") == None:
                        clas = ""
                    else:
                        clas = attr.get("class")
    tab.addcolumn(ucol, col, prime, type, min, max, clas, qoute)

def urlify(s):

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '_', s)

    return s

def findInkonsistence(root):
    for rel in root.findall("rel"):
        count = 0
        for part in rel.findall("part"):
            count += 1
        if count >= 3:
            for part in rel.findall("part"):
                if part.get("max") is '1':
                    print(Fore.YELLOW + "-> max-values must all be n, otherwise a multi-valued"
                                        " relationship type is not necessary. In Relation -> " + rel.get('to') + Fore.RESET)



def saveLogic(data, type, loc, allTables):
    print("Generating Logical Model ...")
    root = data.getroot()
    rootlo = ""
    datenbank.__init__(datenbank)
    if not loc == None:
        rootlo = loc.getroot()
    for title in root.findall("title"):
        if not loc == None:
            if title.get("lang"):
                datenbank.settitle(datenbank, urlify(title.get("name")))
                datenbank.setlanguage(datenbank, title.get("lang"))
        else:
            if(not(title.get("lang"))):
                datenbank.settitle(datenbank, urlify(title.get("name")))

    for ent in root.findall("ent"):
        tab = table.Table()
        tab.name = ent.get("name")
        tab.setuname(ent.get("name"))
        tab.desc = "Created from <ent>"
        tab.qoute = ent.get("qoute")
        if not loc == None:
            for entlo in rootlo.findall("entlo"):
                if entlo.get("entref") == ent.get("name"):
                    tab.setuname(entlo.get("name-lo"))
        for attr in ent:
            col = attr.get("name")
            ucol = col
            prime = attr.get("prime")
            qoute = attr.get("qoute")
            if not loc == None:
                for entlo in rootlo.findall("entlo"):
                    if entlo.get("entref") == ent.get("name"):
                        for attrlo in entlo:
                            if col == attrlo.get("name"):
                                ucol = attrlo.get("name-lo")
            if type == None:
                tab.addcolumn(ucol, col, prime, "string", "", "", "", qoute)
            else:
                createColumn(tab, ent.get("name"), ucol, col, prime, type, qoute)
        datenbank.addtable(datenbank, tab)
    findInkonsistence(root)
    for rel in root.findall("rel"):
        counter = 0
        max = 0
        bsuper = False
        for part in rel:
            if part.tag == "part" or part.tag == "attr":
                max += 1
                if part.get("max") == "n":
                    counter += 1
                if part.tag == "attr":
                    counter += 1
            else:
                bsuper = True
        if bsuper == False:
            if (counter != max and allTables) or (max > 3 and allTables):
                maintable = ""
                for part in rel:
                    if part.get("max") == "n":
                        maintable = part.get("ref")
                primarys = datenbank.getprimarycolumns(datenbank, maintable)
                group = 0
                for part in rel:
                    if part.get("max") == "1":
                        group += 1
                        for prime in primarys:
                            if part.get("weak") == "true":
                                datenbank.addcolumn(datenbank, part.get("ref"),prime, 1)
                                datenbank.addrelation(datenbank, part.get("ref"), prime.uname, datenbank.tableuname(datenbank, maintable), group, len(primarys), datenbank.tabqoute(datenbank, part.get("ref")))
                                #print(maintable)
            if counter == max or max > 2 or allTables:
                tab = table.Table()
                tab.name = rel.get("to")
                tab.qoute = rel.get("qoute")
                tab.setuname(tab.name)
                tab.desc = "Created from a m:n relation"
                if not loc == None:
                    for rello in rootlo.findall("rello"):
                        if rello.get("relref") == tab.name:
                            tab.setuname(rello.get("name-lo"))
                group = 0
                for part in rel:
                    group += 1
                    if part.tag == "part":
                        primarys = datenbank.getprimarycolumns(datenbank, part.get("ref"))
                        for prime in primarys:
                            if tab.unique(datenbank.tableuname(datenbank, part.get("ref")) + "_" + prime.uname):
                                tab.addcolumn(datenbank.tableuname(datenbank, part.get("ref")) + "_" + prime.uname, prime.uname, prime.prime, prime.type, prime.min, prime.max, prime.clas, prime.qoute)
                                tab.addrelation(tab.name, datenbank.tableuname(datenbank, part.get("ref")) + "_" + prime.uname, datenbank.tableuname(datenbank, part.get("ref")), group, len(primarys), datenbank.tabqoute(datenbank, part.get("ref")))
                            else:
                                tab.addcolumn(datenbank.tableuname(datenbank, part.get("ref")) + "_" + prime.uname + str(group), prime.uname, prime.prime, prime.type, prime.min, prime.max, prime.clas, prime.qoute)
                                tab.addrelation(tab.name, datenbank.tableuname(datenbank, part.get("ref")) + "_" + prime.uname + str(group), datenbank.tableuname(datenbank, part.get("ref")), group,len(primarys), datenbank.tabqoute(datenbank, part.get("ref")))
                    else:
                        uname = part.get("name")
                        if not loc == None:
                            for rello in rootlo.findall("rello"):
                                for attr in rello:
                                    if part.get("name") == attr.get("name"):
                                        uname = attr.get("name-lo")
                        types = ""
                        min = ""
                        max = ""
                        clas = ""
                        qoute = ""
                        if not type == None:
                            root = type.getroot()
                            for typdsc in root.findall("reldsc"):
                                for attr in typdsc.findall("attr"):
                                    if attr.get("name") == part.get("name"):
                                        types = attr.get("type")
                                        min = attr.get("min")
                                        max = attr.get("max")
                                        clas = attr.get("class")
                                        qoute = attr.get("qoute")
                                        if min == None:
                                            min = ""
                                        if max == None:
                                            max = ""
                                        if clas == None:
                                            clas = ""
                                        if qoute == None:
                                            qoute = ""
                        tab.addcolumn(uname, uname, part.get("prime"), types, min, max, clas, qoute)
                datenbank.addtable(datenbank, tab)
            else:
                maintable = ""
                for part in rel:
                    if part.get("max") == "n":
                        maintable = part.get("ref")
                primarys = datenbank.getprimarycolumns(datenbank, maintable)
                group = 0
                pos = 0
                for part in rel:
                    if part.get("max") == "1":
                        group += 1
                        for prime in primarys:
                            if part.get("weak") == "true":
                                pos += 1
                                datenbank.addcolumn(datenbank, part.get("ref"),prime, pos)
                            datenbank.addrelation(datenbank, part.get("ref"), prime.uname, datenbank.tableuname(datenbank, maintable), group, len(primarys), datenbank.tabqoute(datenbank, maintable))
        else:
            maintable = ""
            for part in rel:
                if part.tag == "super":
                    maintable = part.get("ref")
            primarys = datenbank.getprimarycolumns(datenbank, maintable)
            group = 0
            for part in rel:
                if part.tag == "sub":
                    group += 1
                    for primary in primarys:
                        temp = column.Column(primary.uname, primary.name, primary.type, primary.prime, primary.min, primary.max, primary.clas, primary.qoute)
                        datenbank.addcolumn(datenbank, part.get("ref"), temp)
                        datenbank.addrelation(datenbank, datenbank.tableuname(datenbank, part.get("ref")), temp.name, maintable, group, len(primarys), datenbank.tabqoute(datenbank, part.get("ref")))

    for tablen in datenbank.tabellen:
        primarys = datenbank.getprimarycolumns(datenbank, tablen.name)
        if len(primarys) == 0:
            print(Fore.YELLOW + "->Primary key for the table " + tablen.name + " is not set." + Fore.RESET)
            #sys.exit()

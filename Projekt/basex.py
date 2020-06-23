#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import logicalModell
import xml.dom.minidom as minidom
from BaseXClient import BaseXClient
import random
import re
import os
import datetime
from colorama import Fore
import config
from datetime import timedelta

first = True
root2 = ET.Element(logicalModell.datenbank.name)

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t", newl="\n")

def changetyp(typ):
    types = {
        "string": "string",
        "float": "number",
        "date": "date",
        "int": "number",
        "char": "string",
        "integer": "number",
        "rational": "number",
        "boolean": "string",
        "double": "number",
        "percent": "number",
        "varchar": "string",
        "Datetime": "datetime",
        "Time": "time",
        "time": "time"

    }

    if typ == "":
        tester = "string"
    else:
        tester = types[typ]
    return tester

def changetyp2(typ):
    types = {
        "string": "xs:string",
        "float": "xs:decimal",
        "date": "xs:date",
        "int": "xs:integer",
        "char": "xs:string",
        "integer": "xs:integer",
        "rational": "xs:decimal",
        "boolean": "xs:string",
        "double": "xs:decimal",
        "percent": "xs:decimal",
        "varchar": "xs:string",
        "Datetime": "xs:dateTime",
        "Time": "xs:time",
        "time": "xs:time"
    }

    if typ == "":
        tester = "xs:string"
    else:
        tester = types[typ]
    return tester

def urlify(s):

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '_', s)

    return s


def write_to_file(str, out):
    if os.path.exists(out):
        os.remove(out)
    file = open(out, "w+")
    file.truncate()
    file.write(str)
    file.close()


def getDate(i):
    stri = ""
    stri = stri + datetime.datetime.now().strftime("%Y")
    stri = stri + "-" + datetime.datetime.now().strftime("%m")
    #stri = stri + "-" + str((int(datetime.datetime.now().strftime("%d")) + i))
    stri = stri + "-" + str((datetime.datetime.now() + timedelta(days=i)).strftime("%d"))
    return stri

def getDatetime(i):
    stri = getDate(i)
    stri = stri + "T" + datetime.datetime.now().strftime("%X")
    return stri


def ddlgenerate_gramma(outputfile):
    root = ET.Element('schema', xmlns="http://purl.oclc.org/dsdl/schematron")
    checkStruct = ET.SubElement(root, "pattern")
    for table in logicalModell.datenbank.tabellen:
        tab = ET.SubElement(checkStruct, "rule", context=str(table.name))
        i = 1
        for column in table.columns:
            ET.SubElement(tab, "assert", test="*[" + str(i) + "] = " + column.name).text = "Column " + column.name + \
                                                                                           " has to be on place " + str(
                i)
            if (column.prime):
                ET.SubElement(tab, "assert",
                              test="count(" + column.name + ") != count(distinct-values(ancestor::" + table.name +
                                   "/" + column.name + " ))").text = "A Primary Key has to be unique"
                prime = ET.SubElement(checkStruct, "rule", context=str(column.name))
                ET.SubElement(prime, "assert", test="@prime and @prime = 'true'").text = "A Primary Key has to have" \
                                                                                         " a prime attribute with " \
                                                                                         "the value 'true'"
                if (changetyp(column.type) == "string"):
                    ET.SubElement(tab, "assert", test="string(" + column.name
                                                      + ") = string(" + column.name + ")").text = str(
                        column.name) + " has to be a string"
                elif (changetyp(column.type) == "number"):
                    if (not (column.min == "" and column.max == "")):
                        ET.SubElement(tab, "assert", test="number(" + column.name + ") = number(" + column.name
                                                          + ") and number(" + column.name + ") >= " + column.min
                                                          + " and number(" + column.name + ") <= " + column.max).text = \
                            str(column.name) + " has to be a number between " + str(column.min) + " and " + str(
                                column.max)
                    elif (not (column.min == "")):
                        ET.SubElement(tab, "assert", test="number(" + column.name + ") = number(" + column.name
                                                          + ") and number(" + column.name + ") >= " + column.min).text = \
                            str(column.name) + " has to be a number bigger than " + str(column.min)
                    elif (not (column.max == "")):
                        ET.SubElement(tab, "assert", test="number(" + column.name + ") = number(" + column.name
                                                          + ") and number(" + column.name + ") <= " + column.max).text = \
                            str(column.name) + " has to be a number smaller than " + str(column.max)
                    else:
                        ET.SubElement(tab, "assert", test="number(" + column.name + ") = number(" + column.name
                                                          + ")").text = str(column.name) + " has to be a number"
            else:
                if (changetyp(column.type) == "string"):
                    ET.SubElement(tab, "assert", test="string(" + column.name
                                                      + ") = string(" + column.name + ")").text = str(
                        column.name) + " has to be a string"
                elif (changetyp(column.type) == "number"):
                    if (not (column.min == "" and column.max == "")):
                        ET.SubElement(tab, "assert", test="number(" + column.name + ") = number(" + column.name
                                                          + ") and number(" + column.name + ") >= " + column.min
                                                          + " and number(" + column.name + ") <= " + column.max).text = \
                            str(column.name) + " has to be a number between " + str(column.min) + " and " + str(
                                column.max)
                    elif (not (column.min == "")):
                        ET.SubElement(tab, "assert", test="number(" + column.name + ") = number(" + column.name
                                                          + ") and number(" + column.name + ") >= " + column.min).text = \
                            str(column.name) + " has to be a number bigger than " + str(column.min)
                    elif (not (column.max == "")):
                        ET.SubElement(tab, "assert", test="number(" + column.name + ") = number(" + column.name
                                                          + ") and number(" + column.name + ") <= " + column.max).text = \
                            str(column.name) + " has to be a number smaller than " + str(column.max)
                    else:
                        ET.SubElement(tab, "assert", test="number(" + column.name + ") = number(" + column.name
                                                          + ")").text = str(column.name) + " has to be a number"
            i += 1
    checkrel = ET.SubElement(root, "pattern")
    for relation in logicalModell.relations:
        rel = ET.SubElement(checkrel, "rule", context=str(relation.to))

    write_to_file(prettify(root), outputfile)
    print("Schematron generated in file " + outputfile)


def ddlgenerate_xml(outputfile, amount, auto):
    print("Generating XML Tree ...")
    try:
        amount = int(amount)
    except:
        print("amount has to be a number!")
    root = ET.Element(logicalModell.datenbank.name)
    for table in logicalModell.datenbank.tabellen:
        for i in range(1, amount):
            tab = ET.SubElement(root, urlify(table.uname))
            for column in table.columns:
                if (changetyp(column.type) == "string"):
                    ET.SubElement(tab, urlify(column.uname)).text = urlify(column.name) + str(i)
                elif (changetyp(column.type) == "date"):
                    ET.SubElement(tab, urlify(column.uname)).text = str(getDate(i))
                elif (changetyp(column.type) == "datetime"):
                    ET.SubElement(tab, urlify(column.uname)).text = str(getDatetime(i))
                elif(changetyp(column.type) == "time"):
                    ET.SubElement(tab, urlify(column.uname)).text = str(datetime.datetime.now().strftime("%X"))
                else:
                    ET.SubElement(tab, urlify(column.uname)).text = str(i)
    write_to_file(prettify(root), outputfile)
    print("XML generated in file " + outputfile)
    if auto:
        try:
            print("Connecting to BaseXServer")
            session = BaseXClient.Session(config.basexconf['Address'], int(config.basexconf['Port']), config.basexconf['User'], config.basexconf['Password'])
            print(logicalModell.datenbank.name)
            session.execute("create db " + logicalModell.datenbank.name)
            print(session.info())

            session.add(logicalModell.datenbank.name, prettify(root))
            print(session.info())

            session.close()
        except ConnectionRefusedError:
            print(Fore.RED + "BaseX Server not found" + Fore.RESET)
        except:
            print("other exception")

def ddlgenerate_schema(outputfile):
    print("Generate XML Schema ...")
    #id = 0
    primes = []
    refs = []
    root = minidom.Document()
    schema = root.createElement("xs:schema")
    schema.setAttribute("xmlns:xs", "http://www.w3.org/2001/XMLSchema")
    database = root.createElement("xs:element")
    database.setAttribute("name", str(logicalModell.datenbank.name))
    ctyper = root.createElement("xs:complexType")
    sequencer = root.createElement("xs:sequence")
    for table in logicalModell.datenbank.tabellen:
        tab = root.createElement("xs:element")
        tab.setAttribute("name", str(urlify(table.uname)))
        tab.setAttribute("maxOccurs", "unbounded")
        ctype = root.createElement("xs:complexType")
        sequence = root.createElement("xs:sequence")
        for column in table.columns:
            col = root.createElement("xs:element")
            col.setAttribute("name", str(urlify(column.uname)))
            col.setAttribute("type", str(changetyp2(column.type)))
            #if (not (column.min == "" and column.max == "")):
            #    col.setAttribute("minInclusive", str(column.min))
            #    col.setAttribute("maxInclusive", str(column.max))
            #elif (not (column.min == "")):
            #    col.setAttribute("minInclusive", str(column.min))
            #elif (not (column.max == "")):
            #    col.setAttribute("maxInclusive", str(column.max))
            if(column.prime):
                key = root.createElement("xs:key")
                keyname = "PK_" + str(urlify(column.uname)) + "_" + str(urlify(table.uname))
                key.setAttribute("name",  keyname)
                selector = root.createElement("xs:selector")
                selector.setAttribute("xpath", (urlify(table.uname) + "/" + urlify(column.uname)))
                field = root.createElement("xs:field")
                field.setAttribute("xpath", ".")
                key.appendChild(selector)
                key.appendChild(field)
                primes.append(key)
            if(not(column.reference == "")):
                if (table.desc == "Created from a m:n relation"):
                    keyref = root.createElement("xs:keyref")
                    keyref.setAttribute("name", "FK_" + str(urlify(table.name)) + "_" + str(urlify(column.uname)) + "_to_" + str(urlify(column.reference)))
                    keyref.setAttribute("refer", ("PK_" + str(urlify(column.name)) + "_" + str(urlify(column.reference))))
                    selector2 = root.createElement("xs:selector")
                    selector2.setAttribute("xpath", urlify(table.uname) + "/" + urlify(column.uname))
                    field2 = root.createElement("xs:field")
                    field2.setAttribute("xpath", ".")
                    keyref.appendChild(selector2)
                    keyref.appendChild(field2)
                    refs.append(keyref)
                else:
                    keyref = root.createElement("xs:keyref")
                    keyref.setAttribute("name",
                                        "FK_" + str(urlify(table.uname)) + "_" + str(urlify(column.uname)) + "_to_" + str(
                                            urlify(column.reference)))
                    keyref.setAttribute("refer", ("PK_" + str(urlify(column.uname)) + "_" + str(urlify(column.reference))))
                    selector2 = root.createElement("xs:selector")
                    selector2.setAttribute("xpath", urlify(table.uname) + "/" + urlify(column.uname))
                    field2 = root.createElement("xs:field")
                    field2.setAttribute("xpath", ".")
                    keyref.appendChild(selector2)
                    keyref.appendChild(field2)
                    refs.append(keyref)
            sequence.appendChild(col)
        ctype.appendChild(sequence)
        tab.appendChild(ctype)
        sequencer.appendChild(tab)
    ctyper.appendChild(sequencer)
    database.appendChild(ctyper)
    for key in primes:
        database.appendChild(key)
    for keyref in refs:
        database.appendChild(keyref)
    schema.appendChild(database)
    root.appendChild(schema)

    write_to_file(root.toprettyxml(indent="   "), outputfile)
    print("XML Schema generated in file " + outputfile)



def dmlgenerate(outputfile, amount, auto):
    print("Generating XML Tree ...")
    try:
        amount = int(amount)
    except:
        print("amount has to be a number!")
    root = ET.Element(logicalModell.datenbank.name)
    for table in logicalModell.datenbank.tabellen:
        for i in range(0, amount):
            tab = ET.SubElement(root, urlify(table.uname))
            for column in table.columns:
                ET.SubElement(tab, urlify(column.uname)).text = str(column.data[0])
                column.data.pop(0)
    write_to_file(prettify(root), outputfile)
    print("XML generated in file " + outputfile)
    if auto:
        try:
            print("Connecting to BaseXServer")
            session = BaseXClient.Session(config.basexconf['Address'], int(config.basexconf['Port']),
                                          config.basexconf['User'], config.basexconf['Password'])
            print(logicalModell.datenbank.name)
            session.execute("create db " + logicalModell.datenbank.name)
            print(session.info())

            session.add(logicalModell.datenbank.name, prettify(root))
            print(session.info())

            session.close()
        except ConnectionRefusedError:
            print(Fore.RED + "BaseX Server not found" + Fore.RESET)
        except:
            print("other exception")


def dmlgeneratefromform(outputfile, amount, tabl):
    print("Generating XML Tree ...")
    global first
    global root2
    try:
        amount = int(amount)
    except:
        print("amount has to be a number!")
    if first:
        root2 = ET.Element(logicalModell.datenbank.name)
        first = False
    for table in logicalModell.datenbank.tabellen:
        if table.name is tabl:
                tab = ET.SubElement(root2, urlify(table.uname))
                for column in table.columns:
                    ET.SubElement(tab, urlify(column.uname)).text = str(column.data[0])
                    column.data.pop(0)
    write_to_file(prettify(root2), outputfile)
    print("XML generated in file " + outputfile)



def toBaseX(outputfile):
    try:
        print("Connecting to BaseXServer")
        session = BaseXClient.Session(config.basexconf['Address'], int(config.basexconf['Port']),
                                      config.basexconf['User'], config.basexconf['Password'])
        print(logicalModell.datenbank.name)
        session.execute("create db " + logicalModell.datenbank.name)
        print(session.info())

        session.add(logicalModell.datenbank.name, prettify(root2))
        print(session.info())

        session.close()
    except ConnectionRefusedError:
        print(Fore.RED + "BaseX Server not found" + Fore.RESET)
    except:
        print("other exception")




            



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''

Generator for Rel by Mario Stavarache

'''

import logicalModell
import sys, string, os
import pyperclip
import keyboard
import time
import subprocess
import config

keywordCounter = 1
outputstring = ""
dropstring = ""
insertstring = ""

def ddlgenerate(outputfile, auto, format, drop):
    outputfilestring = str(outputfile)
    ka = outputfile.replace(".rel", "")
    dropout = open(ka + "DROP.rel", "w+")
    out = open(outputfilestring, "w+")
    out.writelines("//Database " + logicalModell.datenbank.name + "\n")
    out.writelines("\n")
    global outputstring
    outputstring += "//Database " + logicalModell.datenbank.name + "\r\n"
    outputstring += "\r\n"
    dropVars = []
    dropFKCons = []
    dropChecks = []
    global keywordCounter
    for table in logicalModell.datenbank.tabellen:
        primarys = table.getprimary()
        if len(primarys) == 0:
            print("Primary Key missing in " + str(table.uname))
    for table in logicalModell.datenbank.tabellen:
        primarys = table.getprimary()
        out.writelines("//" + table.desc + "\n")
        outputstring += "//" + table.desc + "\r\n"
        out.writelines("var " + repl(str(table.uname)) + " real relation" + "\n")
        outputstring += "var " + repl(str(table.uname)) + " real relation" + "\r\n"
        dropVars.append("drop " + "var " + repl(str(table.uname)) + ";")
        if(drop):
            print("Dropped Table " + repl(str(table.uname)))
        else:
            print("Created Table " + repl(str(table.uname)))
        out.writelines("{\n")
        outputstring += "{\r\n"
        i = 0
        j = 0
        helpkeys = True
        checks = []
        maxColumnLength = 0
        for column in table.columns:
            if len(column.uname) > maxColumnLength:
                maxColumnLength = len(column.uname)
        for column in table.columns:
            checks.append(column)
            if j != 0:
                out.writelines("\n,   ")
                outputstring += "\r\n,   "
            else:
                out.writelines("    ")
                outputstring += "    "
            #columnLength =  maxColumnLength - len(column.uname)
            out.writelines(repl(str(column.uname)) + " " + formating(maxColumnLength, column.uname, format) + reltyp(column.type))
            outputstring += repl(str(column.uname)) + " " + formating(maxColumnLength, column.uname, format) + reltyp(column.type)
            j += 1
        out.writelines("\n}")
        outputstring += "\r\n}"
        for column in table.columns:
            check(column.min, column.max, out, column, str(table.uname), dropChecks)
            i = i + 1
            if len(primarys) == 1:
                if column.prime == "true":
                    if len(primarys) == 1:
                        out.writelines(" key{" + repl(str(column.uname)) + "};\n\n")
                        outputstring += " key{" + repl(str(column.uname)) + "};\r\n\r\n"
            else:
                if helpkeys:
                    out.writelines("key{")
                    outputstring += "key{"
                    j = 1
                    for primary in primarys:
                        out.writelines(repl(str(primary)))
                        outputstring += repl(str(primary))
                        if j < len(primarys):
                            out.writelines(",")
                            outputstring += ","
                        j = j + 1
                    out.writelines("};\n\n")
                    outputstring += "};\r\n\r\n"
                    helpkeys = False
            foreigns = table.getforeigncolumns()

        for foreign in foreigns:
            if table.desc == "Erstellt aus einer m:n Beziehung" or table.desc == "Created from a m:n relation":
                for fore in foreign:
                    out.writelines("constraint fk_" + repl(str(table.uname)) + "_" + repl(str((foreign[0]).reference))
                                   + "_on_" + repl(str(fore.uname)) + " ("+ repl(str(table.uname))
                                   + " rename" + " {" + repl(str(fore.uname)) + " as " + repl(str(fore.name))+ "}) ")
                    outputstring += "constraint fk_" + repl(str(table.uname)) + "_" + repl(str((foreign[0]).reference)) +\
                                    "_on_" + repl(str(fore.uname)) + " ("+ repl(str(table.uname)) +\
                                    " rename" + " {" + repl(str(fore.uname)) + " as " + repl(str(fore.name))+ "}) "
                    dropFKCons.append("constraint fk_" + repl(str(table.uname)) + "_" + repl(str((foreign[0]).reference))
                                   + "_on_" + repl(str(fore.uname)))
                    if (drop):
                        print("Dropped Foreign Key Constraint: fk_" + repl(str(table.uname)) + "_" + repl(
                            str((foreign[0]).reference))
                              + "_on_" + repl(str(fore.uname)))
                    else:
                        print("Created Foreign Key Constraint: fk_" + repl(str(table.uname)) + "_" + repl(
                            str((foreign[0]).reference))
                              + "_on_" + repl(str(fore.uname)))

                    out.writelines("{" + repl(str(fore.name))
                                   + "} " + "<= " + repl(str((foreign[0]).reference))
                                   + " {"  + repl(str(fore.name)) + "};\n\n")
                    outputstring += "{" + repl(str(fore.name)) +\
                                    "} " + "<= " + repl(str((foreign[0]).reference)) +\
                                    " {"  + repl(str(fore.name)) + "};\r\n\r\n"
            elif table.desc == "Erstellt aus <ent>" or table.desc == "Created from <ent>":
                for fore in foreign:
                    out.writelines("constraint fk_" + repl(str(table.uname)) + "_" + repl(str((foreign[0]).reference))
                                   + "_on_" + repl(str(fore.uname)) + " " + repl(str(table.uname)))
                    outputstring += "constraint fk_" + repl(str(table.uname)) + "_" + repl(str((foreign[0]).reference)) +\
                                    "_on_" + repl(str(fore.uname)) + " " + repl(str(table.uname))
                    dropFKCons.append("constraint fk_" + repl(str(table.uname)) + "_" + repl(str((foreign[0]).reference))
                                   + "_on_" + repl(str(fore.uname)))
                    if(drop):
                        print("Dropped Foreign Key Constraint: fk_" + repl(str(table.uname)) + "_" + repl(
                            str((foreign[0]).reference))
                              + "_on_" + repl(str(fore.uname)))
                    else:
                        print("Created Foreign Key Constraint: fk_" + repl(str(table.uname)) + "_" + repl(str((foreign[0]).reference))
                                   + "_on_" + repl(str(fore.uname)))
                    out.writelines("{" + repl(str(fore.uname))
                                   + "} " + "<= " + repl(str((foreign[0]).reference))
                                   + " {"  + repl(str(fore.uname)) + "};\n\n")
                    outputstring += "{" + repl(str(fore.uname)) +\
                                    "} " + "<= " + repl(str((foreign[0]).reference)) +\
                                    " {"  + repl(str(fore.uname)) + "};\r\n\r\n"

    writeDropFile(dropout, dropVars, dropFKCons , dropChecks);
    keywordCounter += 1
    global dropstring

    if auto:
        outputstring += "\r\n\r\n <EOT> \r\n"
        os.chdir(config.relconf['Directory'])
        p = subprocess.Popen(["./RelDBMS.sh"], cwd=config.relconf['Directory'], stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        time.sleep(5)
        p.communicate(input=outputstring)
        print("Create Commands executed successfully.")

    if drop:
        dropstring += "\r\n\r\n <EOT> \r\n"
        os.chdir(config.relconf['Directory'])
        p = subprocess.Popen(["./RelDBMS.sh"], cwd=config.relconf['Directory'], stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        time.sleep(5)
        p.communicate(input=dropstring)
        print("Drop Commands executed successfully.")


def reltyp(typ):
    types = {
        "string": "char",
        "rational": "rational",
        "integer": "integer",
        "date": "char",
        "char": "char",
        "boolean": "char",
        "float": "rational",
        " ": "char",
        "": "char",
        "double": "rational",
        "percent": "char",
        "number": "rational",
        "time": "char",
        "varchar": "char",
        "Datetime": "char",
        "Time": "char",
        "datetime": "char"
    }



    if typ == "":
        tester = "char"
    else:
        tester = types[typ]
    return tester

def check(min, max, out, uname, table, dropChecks):
    global outputstring
    if (str(reltyp(uname.type)) == "rational"):
        if min != "":
            out.writelines("type check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " possrep {\n")
            outputstring += "type check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " possrep {\r\n"
            out.writelines("check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " " + reltyp(uname.type) + " constraint " +
                           "check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " > " + str(min) + ".0")
            outputstring += "check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " " + reltyp(uname.type) + " constraint " +\
                            "check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " > " + str(min) + ".0"
            dropChecks.append("type check_" + repl(str(table)) + "_" + repl(str(uname.uname)))
            if max != "":
                out.writelines( "\nand " + "check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " < " + str(max) + ".0" + "\n};\n\n")
                outputstring += "\r\nand " + "check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " < " + str(max) + ".0" + "\r\n};\r\n\r\n"
            else:
                out.writelines("};\n\n")
                outputstring += "};\r\n\r\n"
        else:
            if max!= "":
                out.writelines("check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " < " + str(max) + ".0" + "\n};\n\n")
                outputstring += "check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " < " + str(max) + ".0" + "\r\n};\r\n\r\n"
                dropChecks.append("type check_" + repl(str(table)) + "_" + repl(str(uname.uname)))
    elif (str(reltyp(uname.type)) == "integer"):
        if min != "":
            out.writelines("type check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " possrep {\n")
            outputstring += "type check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " possrep {\r\n"
            out.writelines("check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " " + reltyp(uname.type) + " constraint " +
                           "check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " > " + str(min))
            outputstring += "check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " " + reltyp(uname.type) + " constraint " +\
                            "check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " > " + str(min)
            dropChecks.append("type check_" + repl(str(table)) + "_" + repl(str(uname.uname)))
            if max != "":
                out.writelines( "\nand " + "check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " < " + str(max) + "\n};\n\n")
                outputstring += "\r\nand " + "check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " < " + str(max) + "\r\n};\r\n\r\n"
            else:
                out.writelines("};\n\n")
                outputstring += "\r\nand " + "check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " < " + str(max) + "\r\n};\r\n\r\n"
        else:
            if max!= "":
                out.writelines("check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " < " + str(max) + "\n};\n\n")
                outputstring += "check_" + repl(str(table)) + "_" + repl(str(uname.uname)) + " < " + str(max) + "\r\n};\r\n\r\n"
                dropChecks.append("type " + "check_" + repl(str(table)) + "_" + repl(str(uname.uname)))

def repl(ka):
    keywords = ["type", "begin", "operator", "var", "integer", "from", "to", "times", "constraint", "call", "real", "relation",
                "key", "possrep", "rename", "char", "rational", "times", "as", "tuple", "tup"]
    if str(ka).lower() in keywords:
        ka += str(keywordCounter)
    erg = ka.replace(" ", "_").replace("ä","ae").replace("ü","ue").replace("ö","oe").replace("ß", "ss")
    return erg

def dmlgenerate(outputfile, amount, auto):
    print("Generating inserts")
    global insertstring
    out = open(outputfile, "w")
    try:
        amount = int(amount)
    except:
        print("amount has to be a number!")


    for table in logicalModell.datenbank.tabellen:
        data = table.getdata()
        out.writelines(repl(table.uname) + " := relation {\n")
        insertstring += str(repl(table.uname)) + " := relation {\r\n"
        j = 0
        for datas in data:
            twice = " tuple { "
            out.writelines(twice)
            insertstring += twice
            i = 0
            for datases in datas:
                if i != 0:
                    out.writelines(", ")
                    insertstring += ", "
                if reltyp(table.columns[i].type) == "char":
                    if (str(datases) not in twice):
                        out.writelines(str(repl(table.columns[i].uname)) + " \'" + str(datases) + "\'")
                        insertstring += str(repl(table.columns[i].uname)) + " \'" + str(datases) + "\'"

                elif reltyp(table.columns[i].type) == "integer" or reltyp(table.columns[i].type) == "rational":
                    if (str(datases) not in twice):
                        out.writelines(str(repl(table.columns[i].uname)) + " " + str(datases))
                        insertstring += str(repl(table.columns[i].uname)) + " " + str(datases)
                i += 1
            j += 1
            if j < amount:
                out.writelines("},\n")
                insertstring += "},\r\n"
            else:
                out.writelines("}\n")
                insertstring += "}\r\n"
        out.writelines("};\n\n")
        insertstring += "};\r\n\r\n"

    if auto:
        insertstring += "\r\n\r\n <EOT> \r\n"
        os.chdir(config.relconf['Directory'])
        p = subprocess.Popen(["./RelDBMS.sh"], cwd=config.relconf['Directory'], stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        time.sleep(5)
        p.communicate(input=insertstring)
        print("Insert Commands executed successfully.")

def formating(max, current, format):
    length = len(repl(str(current)))

    difference = max - length
    if format:
        if difference == 0:
            return " "
        else:
            return " " * (difference + 1)
    else:
        return ""

def writeDropFile(dropout, dropVars, dropFKCons, dropChecks):
    global dropstring
    for check in dropChecks[::-1]:
        dropout.writelines("drop " + check + ";" + "\n")
        dropstring += "drop " + check + ";" + "\r\n"
    dropout.writelines("\n")
    dropstring += "\r\n"
    for con in dropFKCons[::-1]:
        dropout.writelines("drop " + con + ";" + "\n")
        dropstring += "drop " + con + ";" + "\r\n"
    dropout.writelines("\n")
    dropstring += "\r\n"
    for var in dropVars[::-1]:
        dropout.writelines(str(var) + "\n")
        dropstring += str(var) + "\r\n"

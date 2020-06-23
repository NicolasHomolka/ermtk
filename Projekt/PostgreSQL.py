#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logicalModell
import psycopg2
import re
import config

def ddlgenerate(outputfile, auto, format, notnull, constaft, consttabl):
    out = open(outputfile, "w")
    foreignnumber = 0
    maxcolumn = logicalModell.datenbank.maxcolumn(logicalModell.datenbank)
    maxtype = 0
    for table in logicalModell.datenbank.tabellen:
        for column in table.columns:
            if len(changetyp(column.type)) > maxtype:
                maxtype = len(changetyp(column.type))
    for table in logicalModell.datenbank.tabellen:
        primarys = table.getprimarycolumns(table.name)
        out.writelines("--" + table.desc + "\n")
        out.writelines("create table " + urlify(table.uname, table.qoute) + "\n")
        out.writelines("(\n")
        i = 0
        checks = []
        for column in table.columns:
            checks.append(column)
            if i != 0:
                out.writelines(",   ")
            else:
                out.writelines("    ")
            out.writelines(urlify(column.uname, column.qoute) + " " + formating(maxcolumn, urlify(column.uname, column.qoute), format) + changetyp(column.type) + formating(maxtype, changetyp(column.type), format))
            if not notnull:
                out.writelines(" not null")
            if column.prime == "true" and not constaft and not consttabl:
                if len(primarys) == 1:
                    out.writelines(" primary key")
            if column.count == 1 and not constaft and not consttabl:
                if table.desc == "Created from a m:n relation":
                    out.writelines(" references " + urlify(column.reference) + " (" + urlify(column.name, column.refqoute) + ")")
                else:
                    out.writelines(" references " + urlify(column.reference) + " (" + urlify(column.uname, column.refqoute) + ")")
            check(column.min, column.max, out, column.uname, column.qoute)
            out.writelines("\n")
            i = i + 1
        if (len(primarys) > 1 or consttabl) and not constaft:
            out.writelines(",   primary key(")
            j = 1
            for primary in primarys:
                out.writelines(urlify(primary.uname, primary.qoute))
                if j < len(primarys):
                    out.writelines(",")
                j = j + 1
            out.writelines(")\n")
        foreigns = table.getforeigncolumns()
        for foreign in foreigns:
            if (len(foreign) > 1 or (consttabl and len(foreign) > 0)) and not constaft:
                foreignnumber += 1
                out.writelines(",   foreign key(")
                current = 1
                for fore in foreign:
                    out.writelines(urlify(fore.uname, fore.qoute))
                    if current < fore.count:
                        current += 1
                        out.writelines(", ")
                out.writelines(")")
                out.writelines(" references " + urlify((foreign[0]).reference) + "(")
                current = 0
                for fore in foreign:
                    current += 1
                    if table.desc == "Created from a m:n relation":
                        out.writelines(urlify(fore.name, fore.qoute))
                    else:
                        out.writelines(urlify(fore.uname, fore.qoute))
                    if current < fore.count:
                        out.writelines(",")
                out.writelines(")\n")

        out.writelines(");\n\n")
    if constaft:
        for table in logicalModell.datenbank.tabellen:
            primarys = table.getprimarycolumns(table.name)
            foreigns = table.getforeigncolumns()
            if len(primarys) > 0:
                out.writelines("alter table " + table.uname + "\n")
                out.writelines("    add constraint pk_" + table.uname + " primary key(")
                j = 1
                for primary in primarys:
                    out.writelines(urlify(primary.uname, primary.qoute))
                    if j < len(primarys):
                        out.writelines(",")
                    j = j + 1
                out.writelines(");\n\n")
            for foreign in foreigns:
                if len(foreign) > 0:
                    foreignnumber += 1
                    out.writelines("alter table " +  table.uname + "\n")

                    out.writelines("    add constraint fk_" + urlify((foreign[0]).reference) + str(foreignnumber))
                    out.writelines("\n        foreign key(")
                    current = 0
                    for fore in foreign:
                        current += 1
                        out.writelines(urlify(fore.uname, fore.qoute))
                        if current < fore.count:
                            out.writelines(",")
                    out.writelines(")\n")
                    out.writelines("          references " + urlify((foreign[0]).reference) + "(")
                    current = 0
                    for fore in foreign:
                        current += 1
                        if table.desc == "Created from a m:n relation":
                            out.writelines(urlify(fore.name, fore.qoute))
                        else:
                            out.writelines(urlify(fore.uname, fore.qoute))
                        if current < fore.count:
                            out.writelines(",")
                    out.writelines(");\n\n")

    for table in reversed(logicalModell.datenbank.tabellen):
        out.writelines("drop table if exists " + urlify(table.uname, table.qoute) + ";\n")

    out.close()
    if auto:
        try:
            con = psycopg2.connect(host=config.postgresqlconf['Address'], database=config.postgresqlconf['Database'], user=config.postgresqlconf['User'], password=config.postgresqlconf['Password'])
            cur = con.cursor()
            f = open(outputfile)
            full_sql = f.read()
            sql_commands = full_sql.split(';')
            i = 0
            error = 0

            while i < len(sql_commands) - 1:
                try:
                    cur.execute(sql_commands[i])
                except:
                    error += 1
                i += 1
            cur.close()
            con.close()
            print(error)
        except:
            print("PostGreSQL Server not found")



def changetyp(typ):
    types = {
        "string": "varchar(300)",
        "float": "numeric",
        "date": "timestamp",
        "int": "integer",
        "char": "varchar(300)",
        "integer": "integer",
        "rational": "numeric",
        "boolean": "boolean",
        "double": "numeric",
        "percent": "numeric",
        "varchar": "varchar(300)",
        "Datetime": "timestamp",
        "Time": "timestamp",
        "time": "timestamp"
    }

    if typ == "":
        tester = "varchar(300)"
    else:
        tester = types[typ]
    return tester


def check(min, max, out, uname, qoute):
    if min != "":
        out.writelines(" check(" + urlify(uname, qoute) + " > " + min)
        if max != "":
            out.writelines(" and " + urlify(uname, qoute) + " < " + max + ")")
        else:
            out.writelines(")")
    else:
        if max!= "":
            out.writelines(" check(" + urlify(uname, qoute) + " < " + max + ")")

def formating(max, current, format):
    if format:
        return " " * (max - len(current))
    else:
        return ""

def urlify(s, qoute = "false"):

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '_', s)

    s = s.replace("ä", "ae")
    s = s.replace("Ä", "Äe")
    s = s.replace("ö", "oe")
    s = s.replace("Ö", "oe")
    s = s.replace("ü", "ue")
    s = s.replace("Ü", "ue")
    s = s.replace("ß", "ss")

    if len(s) > 30:
        i = len(s) - 30
        s = s[:-i]

    if qoute == "true":
        s = "\"" + s + "\""
    return s

def urlify2(s, qoute = "false"):

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    s = s.replace("ä", "ae")
    s = s.replace("Ä", "Äe")
    s = s.replace("ö", "oe")
    s = s.replace("Ö", "oe")
    s = s.replace("ü", "ue")
    s = s.replace("Ü", "ue")
    s = s.replace("ß", "ss")

    if qoute == "true":
        s = "\"" + s + "\""
    return s


def dmlgenerate(outputfile, amount, auto):
    print("Generating inserts")
    out = open(outputfile, "a+")
    try:
        amount = int(amount)
    except:
        print("amount has to be a number!")

    for table in logicalModell.datenbank.tabellen:
        data = table.getdata()
        base = 0
        for datas in data:
            if base == 0:
                out.writelines("insert into " + urlify(table.uname, table.qoute) + " values(")
            else:
                out.writelines(",\n(")
            i = 0
            count = 0
            for datases in datas:
                if i != 0:
                    out.writelines(", ")
                if changetyp((table.columns[count]).type) == "varchar(300)":
                    out.writelines("\'" + urlify2(datases) + "\'")
                else:
                    out.writelines(urlify2(datases))
                i += 1
                count += 1
            out.writelines(")")
            base += 1
        out.writelines(";\n")
    if auto:
        try:
            con = psycopg2.connect(host=config.postgresqlconf['Address'], database=config.postgresqlconf['Database'], user=config.postgresqlconf['User'], password=config.postgresqlconf['Password'])
            cur = con.cursor()
            f = open(outputfile)
            full_sql = f.read()
            sql_commands = full_sql.split(';')
            i = 0
            error = 0

            while i < len(sql_commands) - 1:
                try:
                    cur.execute(sql_commands[i])
                except:
                    error += 1
                i += 1
            cur.close()
            con.close()
            print(error)
        except:
            print("PostGreSQL Server not found")

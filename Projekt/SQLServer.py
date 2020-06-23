#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logicalModell
import sys
import pyodbc
import re
from pyodbc import Error
from colorama import Fore
import config
import config

def ddlgenerate(outputfile, auto, format, notnull, consttabl, keyword, constaft):
    out = open(outputfile, "w")
    foreignnumber = 0
    if constaft:
        print(Fore.BLUE + "-> SQL Server can only apply primary keys in the table! The constraints will be written in the tables! " + Fore.RESET)
    if auto:
        if logicalModell.datenbank.name == "Fluggesellschaften" or logicalModell.datenbank.name == "All_Airways_Association":
            database = "AAA"
        elif logicalModell.datenbank.name == "Fussball" or logicalModell.datenbank.name == "soccer":
            database = "fussball"
        elif logicalModell.datenbank.name == "Kinokette" or logicalModell.datenbank.name == "Cinema_Chain":
            database = "kinokette"
        elif logicalModell.datenbank.name == "Mondial_Datenbank" or logicalModell.datenbank.name == "Mondial_Database":
            database = "mondial"
        elif logicalModell.datenbank.name == "Tankstelle" or logicalModell.datenbank.name == "Fuel_Station":
            database = "tankstelle"
        elif logicalModell.datenbank.name == "Rettungsstelle" or logicalModell.datenbank.name == "emergency_room":
            database = "rettungsstelle"
        elif logicalModell.datenbank.name == "Schulungsfirma" or logicalModell.datenbank.name == "School_of_Music_Course_Database":
            database = "sf"
        elif logicalModell.datenbank.name == "Schoolinformationsystem" or logicalModell.datenbank.name == "School_Info-System":
            database = "sis"
        elif logicalModell.datenbank.name == "Weingut" or logicalModell.datenbank.name == "winery":
            database = "weingut"
        else:
            database = "mydatabase"
        try:
            #/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.2.so.0.1
            connection = pyodbc.connect("Driver={" + config.sqlserverconf['Driver'] + "};Server=" + config.sqlserverconf['Server'] + ";Database=" + database + ";uid=" + config.sqlserverconf['UserID'] + ";pwd=" + config.sqlserverconf['Password'])
            cursor = connection.cursor()
        except Error as e:
            print(e)
    drop = True
    sql_drop_tables = ""
    if drop:
        for table in reversed(logicalModell.datenbank.tabellen):
            if not keyword:
                out.writelines("drop table if exists " + check_name(str(table.uname), table.qoute) + ";\n")
                sql_drop_tables += "drop table if exists " + check_name(str(table.uname), table.qoute) + ";\n"
            else:
                out.writelines("DROP TABLE IF EXISTS " + check_name(str(table.uname), table.qoute) + ";\n")
                sql_drop_tables += "DROP TABLE IF EXISTS " + check_name(str(table.uname), table.qoute) + ";\n"
        if auto:
            try:
                cursor.execute(sql_drop_tables)
            except Error as e:
                print(e)
        if not keyword:
            out.writelines("go\n\n")
        else:
            out.writelines("GO\n\n")
        print(Fore.BLUE + "-> Creating Tables for " + logicalModell.datenbank.name + "-Database..." + Fore.RESET)
    for table in logicalModell.datenbank.tabellen:
        primarys = table.getprimarycolumns(table.name)
        sql_create_tables = ""
        out.writelines("--" + table.desc + "\n")
        if not keyword:
            out.writelines("create table " + check_name(str(table.uname), table.qoute) + "(\n")
            sql_create_tables += "create table " + check_name(str(table.uname), table.qoute) + "(\n"
        else:
            out.writelines("CREATE TABLE " + check_name(str(table.uname), table.qoute) + "(\n")
            sql_create_tables += "CREATE TABLE " + check_name(str(table.uname), table.qoute) + "(\n"
        checks = []
        maxColumnLength = 0
        maxTypeLenght = 0
        for column in table.columns:
            if len(column.uname) > maxColumnLength:
                maxColumnLength = len(column.uname)
            if len(sqlserver_type(column.type, keyword)) > maxTypeLenght:
                maxTypeLenght = len(sqlserver_type(column.type, keyword))
        i = 0
        for column in table.columns:
            checks.append(column)
            if i != 0:
                out.writelines(",   ")
                sql_create_tables += ",   "
            else:
                out.writelines("    ")
                sql_create_tables += "    "
            columnLength = maxColumnLength - len(check_name(column.uname, column.qoute))
            typeLength = maxTypeLenght - len(sqlserver_type(column.type, keyword))
            out.writelines(check_name(str(column.uname), column.qoute) + freeSpace(format, columnLength) + sqlserver_type(column.type, keyword) + freeSpace(format, typeLength))
            sql_create_tables += check_name(str(column.uname)) + freeSpace(format, columnLength) + sqlserver_type(column.type, keyword) + freeSpace(format, typeLength)
            if notnull:
                if not keyword:
                    out.writelines(" not null")
                    sql_create_tables += " not null"
                else:
                    out.writelines(" NOT NULL")
                    sql_create_tables += " NOT NULL"
            if column.prime == "true" and not consttabl:
                if len(primarys) == 1:
                    if not keyword:
                        out.writelines(" primary key")
                        sql_create_tables += " primary key"
                    else:
                        out.writelines(" PRIMARY KEY")
                        sql_create_tables += " PRIMARY KEY"
            if column.count == 1 and not consttabl:
                if table.desc == "Created from a m:n relation":
                    if not keyword:
                        out.writelines(" references " + check_name(str(column.reference), column.qoute) + "(" + check_name(str(column.name), column.qoute) + ")")
                        sql_create_tables += " references " + check_name(str(column.reference), column.qoute) + "(" + check_name(str(column.name), column.qoute) + ")"
                    else:
                        out.writelines(" REFERENCES " + check_name(str(column.reference), column.qoute) + "(" + check_name(
                            str(column.name), column.qoute) + ")")
                        sql_create_tables += " REFERENCES " + check_name(str(column.reference), column.qoute) + "(" + check_name(
                            str(column.name), column.qoute) + ")"
                else:
                    if not keyword:
                        out.writelines(" references " + check_name(str(column.reference), column.qoute) + "(" + check_name(str(column.uname), column.qoute) + ")")
                        sql_create_tables += " references " + check_name(str(column.reference), column.qoute) + "(" + check_name(str(column.uname), column.qoute) + ")"
                    else:
                        out.writelines(" REFERENCES " + check_name(str(column.reference), column.qoute) + "(" + check_name(
                            str(column.uname), column.qoute) + ")")
                        sql_create_tables += " REFERENCES " + check_name(str(column.reference), column.qoute) + "(" + check_name(
                            str(column.uname), column.qoute) + ")"
            if not consttabl:
                check(column.min, column.max, out, check_name(str(column.uname), column.qoute), keyword)
            out.writelines("\n")
            sql_create_tables += "\n"
            i = i + 1
        if len(primarys) > 1 or consttabl:
            if len(primarys) >= 1:
                if not keyword:
                    out.writelines(",   primary key(")
                    sql_create_tables += ",   primary key("
                else:
                    out.writelines(",   PRIMARY KEY(")
                    sql_create_tables += ",   PRIMARY KEY("
                j = 1
                for primary in primarys:
                    out.writelines(check_name(primary.uname, primary.qoute))
                    sql_create_tables += check_name(primary.uname, primary.qoute)
                    if j < len(primarys):
                        out.writelines(", ")
                        sql_create_tables += ", "
                    j = j + 1
                out.writelines(")\n")
                sql_create_tables += ")\n"
        foreigns = table.getforeigncolumns()
        for foreign in foreigns:
            if (len(foreign) > 1 or (consttabl and len(foreign) > 0)) and not constaft:
                foreignnumber += 1
                if not keyword:
                    out.writelines(",   constraint fk_" + check_name(str((foreign[1]).reference)) + str(foreignnumber))
                    out.writelines("\n      foreign key(")
                    sql_create_tables += ",   constraint fk_" + check_name(str((foreign[1]).reference)) + str(foreignnumber) + "\n      foreign key("
                else:
                    out.writelines(",   CONSTRAINT fk_" + check_name(str((foreign[1]).reference)) + str(foreignnumber))
                    out.writelines("\n      FOREIGN KEY(")
                    sql_create_tables += ",   CONSTRAINT fk_" + check_name(str((foreign[1]).reference)) + str(
                        foreignnumber) + "\n      FOREIGN KEY("
                current = 0
                for fore in foreign:
                    current += 1
                    out.writelines(check_name(str(fore.uname), fore.qoute))
                    sql_create_tables += check_name(str(fore.uname), fore.qoute)
                    if current < fore.count:
                        out.writelines(", ")
                        sql_create_tables += ", "
                out.writelines(")\n")
                sql_create_tables += ")\n"
                if not keyword:
                    out.writelines("      references " + check_name(str((foreign[0]).reference), (foreign[0]).refqoute) + "(")
                    sql_create_tables += "      references " + check_name(str((foreign[0]).reference), (foreign[0]).refqoute) + "("
                else:
                    out.writelines("      REFERENCES " + check_name(str((foreign[0]).reference), (foreign[0]).refqoute) + "(")
                    sql_create_tables += "      REFERENCES " + check_name(str((foreign[0]).reference), (foreign[0]).refqoute) + "("
                current = 0
                for fore in foreign:
                    current += 1
                    if table.desc == "Created from a m:n relation":
                        out.writelines(check_name(str(fore.name), fore.qoute))
                        sql_create_tables += check_name(str(fore.name), fore.qoute)
                    else:
                        out.writelines(check_name(str(fore.uname), fore.qoute))
                        sql_create_tables += check_name(str(fore.uname), fore.qoute)
                    if current < fore.count:
                        out.writelines(", ")
                        sql_create_tables += ", "
                out.writelines(")\n")
                sql_create_tables += ")\n"
        if consttabl:
            for column in table.columns:
                check_tablconst(column.min, column.max, out, check_name(str(column.uname)), keyword)
            out.writelines("\n")
        if not keyword:
            out.writelines(");\ngo\n\n")
            sql_create_tables += ");\n\n"
        else:
            out.writelines(");\nGO\n\n")
            sql_create_tables += ");\n\n"
        if auto:
            try:
                cursor.execute(sql_create_tables)
            except Error as e:
                print(Fore.RED + "-> Error while creating Table  " + check_name(table.uname) + ": " + str(e) + Fore.RESET)
    if constaft:
        for table in logicalModell.datenbank.tabellen:
            sql_create_tables = ""
            foreigns = table.getforeigncolumns()
            for foreign in foreigns:
                if len(foreign) > 0:
                    foreignnumber += 1
                    out.writelines("--Table " + check_name(table.uname) + " gets a foreign key constraint from " + check_name((foreign[0]).reference) + "\n\n")
                    if keyword:
                        out.writelines("ALTER TABLE " + check_name(table.uname, table.qoute) + "\n")
                        out.writelines("    ADD CONSTRAINT fk_" + check_name((foreign[0]).reference) + str(foreignnumber))
                        out.writelines("\n        FOREIGN KEY(")
                        sql_create_tables += "ALTER TABLE " + check_name(table.uname, table.qoute) + "\n    ADD CONSTRAINT fk_" + check_name((foreign[0]).reference) + str(foreignnumber)
                        sql_create_tables += "\n        FOREIGN KEY("
                    else:
                        out.writelines("alter table " +  check_name(table.uname, table.qoute) + "\n")
                        out.writelines("    add constraint fk_" + check_name((foreign[0]).reference) + str(foreignnumber))
                        out.writelines("\n        foreign key(")
                        sql_create_tables += "alter table " + check_name(table.uname, table.qoute) + "\n    add constraint fk_" + check_name((foreign[0]).reference) + str(foreignnumber)
                        sql_create_tables += "\n        foreign key("
                    current = 0
                    for fore in foreign:
                        current += 1
                        out.writelines(check_name(fore.uname, fore.qoute))
                        sql_create_tables += check_name(fore.uname, fore.qoute)
                        if current < fore.count:
                            out.writelines(", ")
                            sql_create_tables += ", "
                    out.writelines(")\n")
                    sql_create_tables += ")\n"
                    if keyword:
                        out.writelines("          REFERENCES " + check_name((foreign[0]).reference, (foreign[0]).refqoute) + "(")
                        sql_create_tables += "          REFERENCES " + check_name((foreign[0]).reference, (foreign[0]).refqoute) + "("
                    else:
                        out.writelines("          references " + check_name((foreign[0]).reference, (foreign[0]).refqoute) + "(")
                        sql_create_tables += "          references " + check_name((foreign[0]).reference, (foreign[0]).refqoute) + "("
                    current = 0
                    for fore in foreign:
                        current += 1
                        if table.desc == "Created from a m:n relation":
                            out.writelines(check_name(fore.name, fore.qoute))
                            sql_create_tables += check_name(fore.name, fore.qoute)
                        else:
                            out.writelines(check_name(fore.uname, fore.qoute))
                            sql_create_tables += check_name(fore.uname, fore.qoute)
                        if current < fore.count:
                            out.writelines(", ")
                            sql_create_tables += ", "
                    if keyword:
                        out.writelines(");\nGO\n\n")
                        sql_create_tables += ");\n\n"
                    else:
                        out.writelines(");\ngo\n\n")
                        sql_create_tables += ");\n\n"
                if auto:
                    try:
                        cursor.execute(sql_create_tables)
                    except Error as e:
                        print(Fore.RED + "-> Error while adding Foreign Key Constraints " + table.uname + ": " + str(e) + Fore.RESET)
    print(Fore.GREEN + "-> Finished creating Tables for " + logicalModell.datenbank.name + "-Database" + Fore.RESET)
    if auto:
        connection.commit()
        cursor.close()
        connection.close()
    print("-> SQL generated in file " + outputfile)
    out.close()

def freeSpace(format, length):
    freeSpace = ""
    if not format:
        while length > 0:
            freeSpace += " "
            length -= 1
        freeSpace += " "
    else:
        freeSpace += " "
    return freeSpace

def sqlserver_type(typ, keyword):
    if not keyword:
        types = {
            "percent": "char",
            "double": "float",
            "varchar": "varchar(132)",
            "Datetime": "datetime",
            "Time": "time",
            "string": "varchar(132)",
            "int": "int",
            "float": "float",
            "date": "datetime",
            "integer": "int",
            "char": "varchar(132)",
            "boolean": "int",
            "rational": "float",
            "time": "timestamp"
        }
    else:
        types = {
            "percent": "CHAR",
            "double": "FLOAT",
            "varchar": "VARCHAR(132)",
            "Datetime": "DATETIME",
            "Time": "TIME",
            "string": "VARCHAR(132)",
            "int": "INT",
            "float": "FLOAT",
            "date": "DATETIME",
            "integer": "INT",
            "char": "VARCHAR(132)",
            "boolean": "int",
            "rational": "FLOAT",
            "time": "TIMESTAMP"
        }
    if typ == "":
        if not keyword:
            tester = "varchar(132)"
        else:
            tester = "VARCHAR(132)"
    else:
        tester = types[typ]
    return tester

def check_name(name, qoute = "false"):
    erg = ""
    if type(name) == str:
        name = re.sub(r"[^\w\s]", '', name)
        name = re.sub(r"\s+", '_', name)
        erg = name.replace("ä", "ae").replace("ü", "ue").replace("ö", "oe").replace("ß", "ss").replace("Ä", "Ae").replace("Ü", "Ue").replace("Ö", "Oe")
    if qoute == "true":
        erg = "\"" + erg + "\""
    return erg

def check(min, max, out, uname, keyword):
    if min != "":
        if keyword:
            out.writelines(" CHECK(" + uname + " >= " + min + "")
            if max != "":
                out.writelines(" AND " + uname + " <= " + max + ")")
            else:
                out.writelines(")")
        else:
            out.writelines(" check(" + uname + " >= " + min + "")
            if max != "":
                out.writelines(" and " + uname + " <= " + max + ")")
            else:
                out.writelines(")")
    else:
        if keyword:
            if max != "":
                out.writelines(" CHECK(" + uname + " <= " + max + ")")
        else:
            if max != "":
                out.writelines(" check(" + uname + " <= " + max + ")")

def check_tablconst(min, max, out, uname, keyword):
    if min != "":
        if keyword:
            out.writelines(" CHECK(" + uname + " >= " + min + "")
            if max != "":
                out.writelines(" AND " + uname + " <= " + max + ")")
            else:
                out.writelines(")")
        else:
            out.writelines(" check(" + uname + " >= " + min + "")
            if max != "":
                out.writelines(" and " + uname + " <= " + max + ")")
            else:
                out.writelines(")")
    else:
        if keyword:
            if max != "":
                out.writelines(" CHECK(" + uname + " <= " + max + ")")
        else:
            if max != "":
                out.writelines(" check(" + uname + " <= " + max + ")")

def dmlgenerate(outputfile, amount, auto):
    print("Generating inserts")
    out = open(outputfile, "a+")
    try:
        amount = int(amount)
    except:
        print("amount has to be a number!")
    if auto:
        if logicalModell.datenbank.name == "Fluggesellschaften" or logicalModell.datenbank.name == "All_Airways_Association":
            database = "AAA"
        elif logicalModell.datenbank.name == "Fussball" or logicalModell.datenbank.name == "soccer":
            database = "fussball"
        elif logicalModell.datenbank.name == "Kinokette" or logicalModell.datenbank.name == "Cinema_Chain":
            database = "kinokette"
        elif logicalModell.datenbank.name == "Mondial_Datenbank" or logicalModell.datenbank.name == "Mondial_Database":
            database = "mondial"
        elif logicalModell.datenbank.name == "Tankstelle" or logicalModell.datenbank.name == "Fuel_Station":
            database = "tankstelle"
        elif logicalModell.datenbank.name == "Rettungsstelle" or logicalModell.datenbank.name == "emergency_room":
            database = "rettungsstelle"
        elif logicalModell.datenbank.name == "Schulungsfirma" or logicalModell.datenbank.name == "School_of_Music_Course_Database":
            database = "sf"
        elif logicalModell.datenbank.name == "Schoolinformationsystem" or logicalModell.datenbank.name == "School_Info-System":
            database = "sis"
        elif logicalModell.datenbank.name == "Weingut" or logicalModell.datenbank.name == "winery":
            database = "weingut"
        else:
            database = "mydatabase"
        try:
            # /opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.2.so.0.1
            connection = pyodbc.connect("Driver={" + config.sqlserverconf['Driver'] + "};Server=" + config.sqlserverconf['Server'] + ";Database=" + database + ";uid=" + config.sqlserverconf['UserID'] + ";pwd=" + config.sqlserverconf['Password'])
            cursor = connection.cursor()
        except Error as e:
            print(e)
    count_create = 0
    count_error = 0
    for table in logicalModell.datenbank.tabellen:
        data = table.getdata()
        for datas in data:
            sql_inserts = ""
            out.writelines("insert into " + check_name(table.uname, table.qoute) + "\n  (")
            sql_inserts += "insert into " + check_name(table.uname, table.qoute) + "\n  ("
            j = 0
            for column in table.columns:
                if j != 0:
                    out.writelines(", " + check_name(column.uname, column.qoute))
                    sql_inserts += ", " + check_name(column.uname, column.qoute)
                else:
                    out.writelines(check_name(column.uname, column.qoute))
                    sql_inserts += check_name(column.uname, column.qoute)
                j += 1
            out.writelines(")\nvalues\n (")
            sql_inserts += ")\nvalues\n ("
            i = 0
            for datases in datas:
                if i != 0:
                    out.writelines(", ")
                    sql_inserts += ", "
                if (sqlserver_type(table.columns[i].type, False) == 'char' or sqlserver_type(table.columns[i].type, False) == 'varchar(132)'):
                    out.writelines("\'" + check_name(datases) + "\'")
                    sql_inserts += "\'" + check_name(datases) + "\'"
                else:
                    out.writelines(str(datases))
                    sql_inserts += str(datases)
                i += 1
            out.writelines(");\n")
            sql_inserts += ");"
            if auto:
                try:
                    cursor = connection.cursor()
                    cursor.execute(sql_inserts)
                    connection.commit()
                    count_create += 1
                except Error as e:
                    print(Fore.RED + "-> Error while creating Inserts for table " + table.uname + ": " + str(e) + Fore.RESET)
                    count_error += 1
    if auto:
        print(Fore.GREEN + "-> Finished creating " + str(count_create) + " Inserts for " + logicalModell.datenbank.name + "-Database" + Fore.RESET)
        if count_error > 0:
            print(Fore.RED + "-> Could not create " + str(count_error) + " Inserts for " + logicalModell.datenbank.name + "-Database" + Fore.RESET)
    if auto:
        connection.close()



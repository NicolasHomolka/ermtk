#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import cmd2
import xerml_einlesen
import basex
import oracle
import rel
import PostgreSQL
import sqlite
import mySQL
#import SQLServer
import Graphml_converter
from colorama import Fore
import subprocess
import pic_code
import graphviz_converter
import logicalModell
import logischeDatensaetze
import config
import os
import block2
import lod
#import dmlform
import sys

vers = 'ermtk 0.0.0.1'

inputfile_global = ""
data_global = None
data_ty_global = None
data_lo_global = None
prompt_lo_global = ""
prompt_ty_global = ""
prompt_global = "ermtk> "


# create the top-level parser for the base command
ermtk_parser = argparse.ArgumentParser(prog='ermtk')
ermtk_parser.add_argument('-v', '--version', action='version', version=vers)
ermtk_subparsers = ermtk_parser.add_subparsers(title='sub-commands', help='sub-command help', dest='subparser')

# create the parser for the "erd" sub-command

parser_erdgenerate = ermtk_subparsers.add_parser('erdgenerate', help='Generate an ERD from XERML Modell')
parser_erdgenerate.add_argument('-i', '--inputfile', help='Inputfile')
parser_erdgenerate.add_argument('-o', '--output', help='Outputfile')
parser_erdgenerate.add_argument('-n', '--notation', help='Takes a value to define the notation \n'
                                                         'Example: --notation crowfoot')
parser_erdgenerate.add_argument('-t', '--typ', help='Attributes with types are displayed in the ERD')
parser_erdgenerate.add_argument('-a', '--attr', action='store_true', help='The ERD displays Attributes')
parser_erdgenerate.add_argument('-c', '--color', action='store_true', help='The ERD is colored')
parser_erdgenerate.add_argument('-g', '--graphml', action='store_true', help='The Output-Type is a GraphML File')
parser_erdgenerate.add_argument('-p', '--pic', action='store_true', help='The Output-Type is a Pic-File')
parser_erdgenerate.add_argument('-d', '--draw', action='store_true', help='The Output-Type is a LibreOffice Draw File')
parser_erdgenerate.add_argument('-v', '--viz', action='store_true', help='The Output-Type is a Graphviz File')
parser_erdgenerate.add_argument('-l', '--loc', help='Define the output language')
parser_erdgenerate.add_argument('-s', '--show', action='store_true', help='Shows generated Diagramm in Programm')
parser_erdgenerate.add_argument('--auto', action='store_true', help='ERD generated with default options')
parser_erdgenerate.add_argument('--dot', action='store_true', help='ERD generated with dot layout')

# create the parser for the "open" sub-command

parser_open = ermtk_subparsers.add_parser('open', help='Opens a XERML-File to use it in the Shell')
parser_open.add_argument('-i', '--inputfile', help='Inputfile')
parser_open.add_argument('-l', '--language', help='Laguagefile')
parser_open.add_argument('-t', '--type', help='Typefile')

# create the parser for the "close" sub-command

parser_close = ermtk_subparsers.add_parser('close', help='Closes a XERML-File if it is not needed anymore')
parser_close.add_argument('-t', '--type', action='store_true', help='Typefile')
parser_close.add_argument('-l', '--language', action='store_true', help='Languagefile')

# create the parser for the "exit" sub-command

parser_exit = ermtk_subparsers.add_parser('exit', help='Exit the shell')

parser_shell = ermtk_subparsers.add_parser('shell', help='Enters the shell')

# create the parser for the "bye" sub-command

parser_bye = ermtk_subparsers.add_parser('bye', help='Exit the shell')

# create the parser for the "list" sub-command

parser_list = ermtk_subparsers.add_parser('list', help='Generate an ERD from XERML Modell')
parser_list.add_argument('-all', action='store_true', help='List all Entity-Types and Relationship-Types')
parser_list.add_argument('-ent', action='store_true', help='List Entity-Types')
parser_list.add_argument('-rel', action='store_true', help='List Relationship-Types')
parser_list.add_argument('-attr', action='store_true', help='List Attributes')

# create the parser for the "focus" sub-command

parser_erdfocus = ermtk_subparsers.add_parser('erdfocus', help='Generate an ERD focusing on specified Entities')
parser_erdfocus.add_argument('-i', '--inputfile', help='Inputfile')
parser_erdfocus.add_argument('-o', '--output', help='Outputfile')
parser_erdfocus.add_argument('-f', '--filter', help='Takes a value to filter the ERD')
parser_erdfocus.add_argument('-r', '--relcounter', help='Takes a number to define how much you want to see.')
parser_erdfocus.add_argument('-n', '--notation', help='Takes a value to define the notation \n'
                                                      'Example: --notation crowfoot')
parser_erdfocus.add_argument('-t', '--typ', help='Attributes with types are displayed in the ERD')
parser_erdfocus.add_argument('-a', '--attr', action='store_true', help='Attributes are displayed in the ERD')
parser_erdfocus.add_argument('-c', '--color', action='store_true', help='The ERD is colored')
parser_erdfocus.add_argument('-g', '--graphml', action='store_true', help='The Output-Type is a GraphML File')
parser_erdfocus.add_argument('-p', '--pic', action='store_true', help='The Output-Type is a Pic-File')
parser_erdfocus.add_argument('-d', '--draw', action='store_true', help='The Output-Type is a LibreOffice Draw File')
parser_erdfocus.add_argument('-v', '--viz', action='store_true', help='The Output-Type is a Graphviz File')
parser_erdfocus.add_argument('-l', '--loc', help='Define the output language')
parser_erdfocus.add_argument('--auto', action='store_true', help='ERD generated with default options')

# create the parser for the "block" sub-command

parser_blockdiagram = ermtk_subparsers.add_parser('blockdiagram',
                                                  help='Generate an blockdiagram of the relational model')
parser_blockdiagram.add_argument('-i', '--inputfile', help='Inputfile')
parser_blockdiagram.add_argument('-l', '--language', help='Define the output language')
# parser_blockdiagram.add_argument('-c', '--color', help='The diagram is colored')

# create the parser for the "ddl" sub-command
parser_ddlgenerate = ermtk_subparsers.add_parser('ddlgenerate', help='Convert an XERML Modell into DDL-Commands')
parser_ddlgenerate.add_argument('-i', '--inputfile', help='Inputfile')
parser_ddlgenerate.add_argument('-o', "--output", help='Outputfile')
parser_ddlgenerate.add_argument("--amount", help='Amount of XML data (only availible for BaseX)')
parser_ddlgenerate.add_argument('databasetype',
                                help='Available Databasetype: basexml, basexschema, mysql, oracle, postgresql, rel, '
                                     'sqlserver, sqlite')
parser_ddlgenerate.add_argument('-t', "--typ", help='Typdescription')
parser_ddlgenerate.add_argument('-l', "--loc", help='Localisation')
parser_ddlgenerate.add_argument('--auto', action='store_true', help='Automatically run against database')
parser_ddlgenerate.add_argument('--alltables', action='store_true', help='All relationship types as tables')
parser_ddlgenerate.add_argument('--notnull', action='store_true', help='Deactivates the not null')
parser_ddlgenerate.add_argument('--format', action='store_true', help='Format for outputfile')
parser_ddlgenerate.add_argument('--constaft', action='store_true', help='Constraints after create Tables')
parser_ddlgenerate.add_argument('--consttabl', action='store_true', help='Constraints as Tableconstraints')
parser_ddlgenerate.add_argument('--keyword', action='store_true', help='Keywords as uppercase')
parser_ddlgenerate.add_argument('--drop', action='store_true', help='Execute Rel dropscript')

# create the parser for the "dml" sub-command
parser_dmlgenerate = ermtk_subparsers.add_parser('dmlgenerate', help='Generate example data in form of DML-Commands')
parser_dmlgenerate.add_argument('-i', "--inputfile", help='Inputfile')
parser_dmlgenerate.add_argument('-o', "--output", help='Outputfile')
parser_dmlgenerate.add_argument('--alltables', action='store_true', help='All relations as tables')
parser_dmlgenerate.add_argument('--auto', action='store_true', help='Automatically run against database')
parser_dmlgenerate.add_argument('database', help='Available Databases: baseX, mysql, '
                                                 'oracle, postgresql, rel, sqlserver')
parser_dmlgenerate.add_argument('-t', "--typ", help='Typdescription')
parser_dmlgenerate.add_argument('-l', "--loc", help='Localisation')
parser_dmlgenerate.add_argument('amount', help='Amount of Example Data')

parser_dmlform = ermtk_subparsers.add_parser('dmlform', help='Generate an entry form for typ in example data')
parser_dmlform.add_argument('-i', "--inputfile", help='Inputfile')
parser_dmlform.add_argument('-t', "--typ", help='Typdescription')
parser_dmlform.add_argument('-l', "--loc", help='Localisation')
parser_dmlform.add_argument('-o', "--output", help='Outputfile')
parser_dmlform.add_argument('database', help='Database')
parser_dmlform.add_argument("--alltables", action='store_true', help='All relations as tables')

# -------------------------- Config Parser ---------------------------------------
parser_configure = ermtk_subparsers.add_parser('config', help="Configure database connection attributes")
parser_configures = parser_configure.add_subparsers(title='config-commands', help='config-command help', dest='subparser')
parser_configure.add_argument('-s', '--save', action='store_true', help='Save current configuration')
# BaseX config
parser_basex = parser_configures.add_parser('basex', help="BaseX connection attributes")
parser_basex.add_argument('-a', '--address', help="Configure Address DEFAULT = Localhost")
parser_basex.add_argument('-por', '--port', help="Configure Port DEFAULT = 1984")
parser_basex.add_argument('-usr', '--user', help="Configure User DEFAULT = admin")
parser_basex.add_argument('-pwd', '--password', help="Configure Password DEFAULT = admin")
# Oracle config
parser_oracle = parser_configures.add_parser('oracle', help="Oracle connection attributes")
parser_oracle.add_argument('-a', '--address', help="Configure Address DEFAULT = 127.0.0.1")
parser_oracle.add_argument('-s', '--servicename', help="Configure ServiceName DEFAULT = XE")
parser_oracle.add_argument('-usr', '--user', help="Configure User DEFAULT = i13075")
parser_oracle.add_argument('-pwd', '--password', help="Configure Password DEFAULT = topsecret")
# Postgresql config
parser_postgre = parser_configures.add_parser('postgresql', help="PostgreSQL connection attributes")
parser_postgre.add_argument('-a', '--address', help="Configure Address DEFAULT = localhost")
parser_postgre.add_argument('-d', '--database', help="Configure Database DEFAULT = test")
parser_postgre.add_argument('-usr', '--user', help="Configure User DEFAULT = postgres")
parser_postgre.add_argument('-pwd', '--password', help="Configure Password DEFAULT = postgres")
# SQLite config
parser_sqlite = parser_configures.add_parser('sqlite', help="SQLite connection attributes")
parser_sqlite.add_argument('-d', '--directory', help="Configure Directory DEFAULT = "
                                                     "/home/christoph/GitCopy/Ermtk/SQLite_DB.db")
# SQLServer config
parser_sqlserver = parser_configures.add_parser('sqlserver', help="SQLServer connection attributes")
parser_sqlserver.add_argument('-dri', '--driver', help="Configure Driver DEFAULT = ODBC Driver 17 for SQL Server")
parser_sqlserver.add_argument('-ser', '--server', help="Configure Server DEFAULT = localhost")
parser_sqlserver.add_argument('-da', '--database', help="Configure Database DEFAULT = mydatabase")
parser_sqlserver.add_argument('-usr', '--userid', help="Configure UserID DEFAULT = sa")
parser_sqlserver.add_argument('-pwd', '--password', help="Configure Password DEFAULT = xX94Hugo")
# MYSQL config
parser_mysql = parser_configures.add_parser('mysql', help="MySQL connection attributes")
parser_mysql.add_argument('-a', '--address', help="Configure Address DEFAULT = Localhost")
parser_mysql.add_argument('-usr', '--user', help="Configure User DEFAULT = root")
parser_mysql.add_argument('-pwd', '--password', help="Configure Password DEFAULT = rootpasswordgiven")
parser_mysql.add_argument('-da', '--database', help="Configure Database DEFAULT = mydatabase")
# REL config
parser_rel = parser_configures.add_parser('rel', help="REL connection attributes")
parser_rel.add_argument('-d', '--directory', help="Configure Directory DEFAULT = "
                                                     "/home/mario/Downloads/Rel3.013.linuxDBMS")
#



def check_input(args):
    global data_ty_global
    global data_lo_global
    global data_global
    inputfile = args.inputfile or ""
    typ = args.typ or ""
    loc = args.loc or ""
    if inputfile == "" and data_global == None:
        raise NameError(Fore.RED + "Please select a inputfile" + Fore.RESET)
    elif not inputfile == "" or not(data_global == None):
        if data_global == None:
            print(inputfile)
            data_global = xerml_einlesen.open(inputfile)
        if not typ == "" and data_ty_global == None:
            data_ty_global = xerml_einlesen.openTyp(typ)
        if (not loc == "") and data_lo_global == None:
            data_lo_global = xerml_einlesen.openLang(loc)
    elif inputfile != "":
        data_global = xerml_einlesen.open(inputfile)


def do_ddlgenerate(args):
    database = args.databasetype
    database.lower()
    constaft = args.constaft
    consttabl = args.consttabl
    keyword = args.keyword
    outputfile = args.output or "test.sql"
    amount = args.amount or 3
    allTables = args.alltables
    notnull = args.notnull
    if constaft and consttabl:
        print("Constaft and Consttabl are not compatible. Just 1 of these Arguments can be used")
        sys.exit()
    check_input(args)
    logicalModell.saveLogic(data_global, data_ty_global, data_lo_global, allTables)
    if database == 'oracle':
        oracle.ddlgenerate(outputfile, args.auto, args.format, not notnull, constaft, consttabl)
    elif database == 'postgresql':
        PostgreSQL.ddlgenerate(outputfile, args.auto, args.format, not notnull, constaft, consttabl)
    elif database == 'basexml':
        basex.ddlgenerate_xml(outputfile, amount, args.auto)
    elif database == 'basexschema':
        basex.ddlgenerate_schema(outputfile)
    elif database == 'rel':
        rel.ddlgenerate(outputfile, args.auto, args.format, args.drop)
    elif database == 'sqlite':
        sqlite.ddlgenerate(outputfile, args.auto, args.format, not notnull, consttabl, keyword, constaft)
    elif database == 'mysql':
        mySQL.ddlgenerate(outputfile, args.auto, args.format, not notnull, consttabl, keyword, constaft)
    elif database == 'sqlserver':
        SQLServer.ddlgenerate(outputfile, args.auto, args.format, not notnull, consttabl, keyword, constaft)
    else:
        print(Fore.RED + "Datatype " + str(database) + " not found." + Fore.RESET)


def do_dmlform(args):
    #m
    inputfile = args.inputfile
    outputfile = args.output or "kein output"
    database = args.database
    database.lower()
    #logischeDatensaetze.dmlgenerate(amount)
    check_input(args)
    logicalModell.saveLogic(data_global, data_ty_global, data_lo_global, args.alltables)
    dmlform.dmlform(database, outputfile)


def do_dmlgenerate(args):
    inputfile = args.inputfile
    outputfile = args.output or "default"
    database = args.database
    database.lower()
    amount = args.amount
    check_input(args)
    allTables = args.alltables
    logicalModell.saveLogic(data_global, data_ty_global, data_lo_global, allTables)
    logischeDatensaetze.dmlgenerate(amount)
    if database == 'basex':
        basex.dmlgenerate(outputfile, amount, args.auto)
    if database == 'oracle':
        oracle.dmlgenerate(outputfile, amount, args.auto)
    if database == 'postgresql':
        PostgreSQL.dmlgenerate(outputfile, amount, args.auto)
    if database == 'sqlite':
        sqlite.dmlgenerate(outputfile, amount, args.auto)
    if database == 'mysql':
        mySQL.dmlgenerate(outputfile, amount, args.auto)
    if database == 'sqlserver':
        SQLServer.dmlgenerate(outputfile, amount, args.auto)
    if database == 'rel':
        rel.dmlgenerate(outputfile, amount, args.auto)



def do_blockdiagram(args):
    global inputfile_global
    if inputfile_global != "":
        block2.main(data_global)


def do_erdfocus(args):
    global data_global
    check_input(args)
    if args.graphml:
        entitys = args.filter.split(",")
        rels = args.relcounter.split(",")
        for indx in range(len(entitys)):
            data = data_global
            tree = xerml_einlesen.focus(data, entitys[indx], rels[indx] or 1)
            args.output = entitys[indx] + ".graphml"
            Graphml_converter.GraphmlConverter(args, tree, data_lo_global, data_ty_global)
    elif args.pic:
        entitys = args.filter.split(",")
        rels = args.relcounter.split(",")
        for indx in range(len(entitys)):
            data = data_global
            tree = xerml_einlesen.focus(data, entitys[indx], rels[indx] or 1)
            inputfile_f = entitys[indx] + ".graphml"
            pic_code.erd_pic(inputfile_f)
    elif args.draw:
        if inputfile_global != "":
            entitys = args.filter.split(",")
            rels = args.relcounter.split(",")
            for indx in range(len(entitys)):
                data = data_global
                tree = xerml_einlesen.focus(data, entitys[indx], rels[indx] or 1)
                if args.color:
                    if args.attr:
                        lod.main(tree, True, True, data_lo_global, args)
                    else:
                        lod.main(tree, True, False, data_lo_global, args)
                else:
                    if args.attr:
                        lod.main(tree, False, True, data_lo_global, args)
                    else:
                        lod.main(tree, False, False, data_lo_global, args)
        else:
            print(
                Fore.RED + "Before you want to draw an ERD you have to open a XERML-file with the following command:"
                           " open [filename]" + Fore.RESET)
    elif args.viz:
        entitys = args.filter.split(",")
        rels = args.relcounter.split(",")
        for indx in range(len(entitys)):
            data = data_global
            tree = xerml_einlesen.focus(data, entitys[indx], rels[indx] or 1)
            graphviz_converter.graphviz_converter(args, data_global, data_lo_global, data_ty_global)
    else:
        print(Fore.RED + "You need to choose a valid Output-Format!" + Fore.RESET)


def do_erdgenerate(args):
    check_input(args)
    global inputfile_global
    if args.inputfile:
        inputfile_global = args.inputfile
    if args.graphml:
        Graphml_converter.GraphmlConverter(args, data_global, data_lo_global, data_ty_global)
        if args.show:
            p = subprocess.Popen("locate -b yed.jar", stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            if args.output:
                o = args.output
            else:
                o = "output.graphml"
            command = 'java -jar ' + output.decode('utf-8').rstrip() + ' ' + o
            subprocess.call(command, shell=True)
    elif args.pic:

        pic_code.erd_pic(inputfile_global, args, data_lo_global)
        subprocess.call('groff -p ' + os.getcwd() + '/erd.pic > erd.pdf', shell=True)
    elif args.draw:
        if inputfile_global != "":
            if args.color:
                if args.attr:
                    lod.main(data_global, True, True, data_lo_global, args)
                else:
                    lod.main(data_global, True, False, data_lo_global, args)
            else:
                if args.attr:
                    lod.main(data_global, False, True, data_lo_global, args)
                else:
                    lod.main(data_global, False, False, data_lo_global, args) 
        else:
            print(Fore.RED + "Before you want to draw an ERD you have to open a XERML-file with the following command:"
                             " open [filename]" + Fore.RESET)
    elif args.viz:
        graphviz_converter.graphviz_converter(args, data_global, data_lo_global, data_ty_global)
    else:
        print(Fore.RED + "You need to choose a valid Output-Format!" + Fore.RESET)


def do_open(args):
    try:
        global inputfile_global
        global data_ty_global
        global data_lo_global
        global data_global
        global prompt_global
        global prompt_lo_global
        global prompt_ty_global
        lang = args.language or None
        typ = args.type or None
        data = args.inputfile or None
        if data is not None:
            if data_global is None:
                data_global = xerml_einlesen.open(data)
                inputfile_global = data
                if not data_global:
                    return
                prompt_global = "ermtk (" + inputfile_global[:15] + prompt_lo_global + prompt_ty_global + ")> "
            else:
                do_close(args)
                do_open(args)
        if typ is not None:
            if data_ty_global == None:
                if not (data_global is None):
                    data_ty_global = xerml_einlesen.openTyp(typ)
                    if not data_ty_global:
                        return
                    prompt_ty_global = "[T]"
                    prompt_global = "ermtk (" + inputfile_global[:15] + prompt_lo_global + prompt_ty_global + ")> "
                else:
                    print(Fore.RED + "An Error occured. This can have 2 reasons: \n\t1) Please open the mainfile before"
                                     " the typdescription\n\t2) File not found. Please check if you wrote "
                                     "the filename correct" + Fore.RESET)
            else:
                print(Fore.RED + "Please close current type description with the command: close -t" + Fore.RESET)
        if lang is not None:
            if data_lo_global == None:
                if not (data_global is None):
                    data_lo_global = xerml_einlesen.openLang(lang)
                    if not data_lo_global:
                        return
                    root = data_lo_global.getroot()
                    for child in root:
                        if child.tag == 'entlo':
                            prompt_lo_global = "[" + child.get('lang') + "]"
                    prompt_global = "ermtk (" + inputfile_global[:15] + prompt_lo_global + prompt_ty_global + ")> "
                else:
                    print(Fore.RED + "An Error occured. This can have 2 reasons: \n\t1) Please open the mainfile before"
                                     " the localisation\n\t2) File not found. Please check if you wrote "
                                     "the filename correct" + Fore.RESET)
            else:
                print(Fore.RED + "Please close current Localisation with the command: close -l" + Fore.RESET)
    except OSError:
        print(Fore.RED + "File not found. Please check if you wrote the filename correct" + Fore.RESET)


def do_close(args):
    global data_ty_global
    global data_lo_global
    global data_global
    global prompt_global
    global prompt_lo_global
    global prompt_ty_global
    global inputfile_global
    lang = args.language
    typ = args.type
    if typ:
        if data_ty_global != None:
            data_ty_global = None
            prompt_ty_global = ""
            print(Fore.RED + "Type-File has been closed" + Fore.RESET)
            prompt_global = "ermtk (" + inputfile_global[:15] + prompt_lo_global + prompt_ty_global + ")> "
        else:
            print(Fore.RED + "There is no Type-File opened" + Fore.RESET)
    elif lang:
        if data_lo_global != None:
            data_lo_global = None
            prompt_lo_global = ""
            print(Fore.RED + "Language-File has been closed" + Fore.RESET)
            prompt_global = "ermtk (" + inputfile_global[:15] + prompt_lo_global + prompt_ty_global + ")> "
        else:
            print(Fore.RED + "There is no Language-File opened" + Fore.RESET)
    else:
        print("All opened Files have been closed")
        data_global = None
        data_lo_global = None
        data_ty_global = None
        inputfile_global = ""
        prompt_ty_global = ""
        prompt_lo_global = ""
        prompt_global = "ermtk> "
    

def do_list(args):
    global inputfile_global
    if inputfile_global == "":
        print(Fore.RED + "Please open first a file with the command: open [input_file]" + Fore.RESET)
    else:
        all_l = args.all
        rel_l = args.rel
        ent = args.ent
        attr = args.attr
        xerml_einlesen.list(inputfile_global, ent, rel_l, attr, all_l)


def do_exit():
    print("Bye Bye")
    exit()


def do_shell():
    # Just a placeholder, please don't delete
    return


def do_config(args):
    func = getattr(args, 'subparser', None)
    if func is not None:
        if func == 'basex':
            do_basexconf(args)
        elif func == 'oracle':
            do_oracleconf(args)
        elif func == 'postgresql':
            do_postgreconf(args)
        elif func == 'sqlite':
            do_sqliteconf(args)
        elif func == 'sqlserver':
            do_sqlserverconf(args)
        elif func == 'mysql':
            do_mysqlconf(args)
        elif func == 'rel':
            do_relconf(args)
    else:
        if args.save:
            config.update_config()
        else:
            config.print_config()


def do_basexconf(args):
    address = args.address or None
    port = args.port or None
    user = args.user or None
    pwd = args.password or None
    if address is not None:
        config.basexconf['Address'] = address
    elif port is not None:
        config.basexconf['Port'] = port
    elif user is not None:
        config.basexconf['User'] = user
    elif pwd is not None:
        config.basexconf['Password'] = pwd
    else:
        config.print_basex()


def do_oracleconf(args):
    address = args.address or None
    servicename = args.servicename or None
    user = args.user or None
    pwd = args.password or None
    if address is not None:
        config.oracleconf['Address'] = address
    elif servicename is not None:
        config.oracleconf['Port'] = servicename
    elif user is not None:
        config.oracleconf['User'] = user
    elif pwd is not None:
        config.oracleconf['Password'] = pwd
    else:
        config.print_oracle()


def do_postgreconf(args):
    address = args.address or None
    database = args.database or None
    user = args.user or None
    pwd = args.password or None
    if address is not None:
        config.postgresqlconf['Address'] = address
    elif database is not None:
        config.postgresqlconf['Database'] = database
    elif user is not None:
        config.postgresqlconf['User'] = user
    elif pwd is not None:
        config.postgresqlconf['Password'] = pwd
    else:
        config.print_postgre()


def do_sqliteconf(args):
    directory = args.directory or None
    if not (directory == None):
        config.sqliteconf['Directory'] = sqlite
    else:
        config.print_sqlite()


def do_sqlserverconf(args):
    driver = args.driver or None
    server = args.server or None
    database = args.database or None
    userid = args.userid or None
    pwd = args.password or None
    if driver is not None:
        config.sqlserverconf['Driver'] = driver
    elif server is not None:
        config.sqlserverconf['Server'] = server
    elif database is not None:
        config.sqlserverconf['Database'] = database
    elif userid is not None:
        config.sqlserverconf['UserID'] = userid
    elif pwd is not None:
        config.sqlserverconf['Password'] = pwd
    else:
        config.print_sqlserver()


def do_mysqlconf(args):
    address = args.address or None
    database = args.database or None
    user = args.user or None
    pwd = args.password or None
    if address is not None:
        config.postgresqlconf['Address'] = address
    elif database is not None:
        config.postgresqlconf['Database'] = database
    elif user is not None:
        config.postgresqlconf['User'] = user
    elif pwd is not None:
        config.postgresqlconf['Password'] = pwd
    else:
        config.print_mysql()


def do_relconf(args):
    directory = args.directory or None
    if not (directory == None):
        config.relconf['Directory'] = directory
    else:
        config.print_rel()

class ermtk(cmd2.Cmd):
    prompt = 'ermtk> '

    CMD_CAT_DDL = 'DDL Commands'
    CMD_CAT_ERD = 'ERD Commands'
    CMD_CAT_DML = 'DML Commands'
    CMD_CAT_GEN = 'General Commands'
    CMD_CAT_PRE = 'Pre-defined Commands'

    def __init__(self):
        super().__init__()
        self.prompt = Fore.CYAN + "ermtk> " + Fore.RESET

    def _set_prompt(self):
        global prompt_global
        self.prompt = Fore.CYAN + prompt_global + Fore.RESET

    @cmd2.with_category(CMD_CAT_ERD)
    @cmd2.with_argparser(parser_erdgenerate)
    def do_erdgenerate(self, args):
        """Generates ERD Diagram"""
        do_erdgenerate(args)

    @cmd2.with_category(CMD_CAT_GEN)
    @cmd2.with_argparser(parser_open)
    def do_open(self, args):
        """Opens the Inputfile and displays the amount of Entities and Relations it contains"""
        do_open(args)
        self._set_prompt()

    @cmd2.with_category(CMD_CAT_GEN)
    @cmd2.with_argparser(parser_close)
    def do_close(self, args):
        """Closes the Inputfile after it is opened with the open Command"""
        do_close(args)
        self._set_prompt()

    @cmd2.with_category(CMD_CAT_GEN)
    @cmd2.with_argparser(parser_list)
    def do_list(self, args):
        """Lists all Entities and Relations that the Inputfile contains"""
        do_list(args)

    @cmd2.with_category(CMD_CAT_ERD)
    @cmd2.with_argparser(parser_erdfocus)
    def do_erdfocus(self, args):
        """I dont know"""
        do_erdfocus(args)

    @cmd2.with_category(CMD_CAT_ERD)
    @cmd2.with_argparser(parser_blockdiagram)
    def do_blockdiagram(self, args):
        """Generates ERD in Block-Format"""
        do_blockdiagram(args)

    @cmd2.with_category(CMD_CAT_DDL)
    @cmd2.with_argparser(parser_ddlgenerate)
    def do_ddlgenerate(self, args):
        """Generates DDL Expressions"""
        do_ddlgenerate(args)

    @cmd2.with_category(CMD_CAT_DML)
    @cmd2.with_argparser(parser_dmlgenerate)
    def do_dmlgenerate(self, args):
        """Generates DML Expressions"""
        do_dmlgenerate(args)

    @cmd2.with_category(CMD_CAT_DML)
    @cmd2.with_argparser(parser_dmlform)
    def do_dmlform(self, args):
        """Generates DML Form"""
        do_dmlform(args)

    @cmd2.with_category(CMD_CAT_GEN)
    @cmd2.with_argparser(ermtk_parser)
    def do_ermtk(self, args):
        """Runs Help Command"""
        self.do_help('ermtk')

    @cmd2.with_category(CMD_CAT_GEN)
    @cmd2.with_argparser(parser_exit)
    def do_exit(self, args):
        """Exits the Shell"""
        do_exit()

    @cmd2.with_category(CMD_CAT_GEN)
    @cmd2.with_argparser(parser_shell)
    def do_shell(self, args):
        """Exits the Shell"""
        do_shell()

    @cmd2.with_category(CMD_CAT_GEN)
    def do_quit(self, args):
        print("Bye Bye")
        return True

    @cmd2.with_category(CMD_CAT_GEN)
    @cmd2.with_argparser(parser_bye)
    def do_bye(self, args):
        """Exits the Shell"""
        do_exit(args)

    @cmd2.with_argparser(parser_configure)
    def do_config(self, args):
        do_config(args)


parser_blockdiagram.set_defaults(func=do_blockdiagram)
parser_erdfocus.set_defaults(func=do_erdfocus)
parser_erdgenerate.set_defaults(func=do_erdgenerate)
parser_ddlgenerate.set_defaults(func=do_ddlgenerate)
parser_dmlform.set_defaults(func=do_dmlform)
parser_dmlgenerate.set_defaults(func=do_dmlgenerate)
parser_open.set_defaults(func=do_open)
parser_list.set_defaults(func=do_list)
parser_close.set_defaults(func=do_close)
parser_exit.set_defaults(func=do_exit)
parser_shell.set_defaults(func=do_shell)
parser_configure.set_defaults(func=do_config)


def main():
    config.load_config()
    app = ermtk()
    app.quit_on_sigint = True
    args = ermtk_parser.parse_args()
    # if args.shell:
    #    app.cmdloop()
    func = getattr(args, 'func', None)
    if func is not None:
        if func.__name__ == "do_shell":
            app.cmdloop()
        else:
            func(args)
    else:
        app.do_help("ermtk")


if __name__ == '__main__':
    main()

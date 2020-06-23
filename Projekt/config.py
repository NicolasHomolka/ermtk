#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
import os
from colorama import Fore

config = configparser.ConfigParser()
basexconf = ""
oracleconf = ""
postgresqlconf = ""
sqliteconf = ""
sqlserverconf = ""
mysqlconf = ""
relconf = ""

def write_config():
    config['BASEX'] = {'Address': 'localhost',
                       'Port': '1984',
                       'User': 'admin',
                       'Password': 'admin'}

    config['ORACLE'] = {'Address': '127.0.0.1',
                        'ServiceName': 'XE',
                        'User': 'i13075',
                        'Password': 'topsecret'}

    config['POSTGRESQL'] = {'Address': 'localhost',
                            'Database': 'test',
                            'User': 'postgres',
                            "Password": 'postgres'}

    config['SQLITE'] = {'Directory': '/home/christoph/GitCopy/Ermtk/SQLite_DB.db'}

    config['SQLSERVER'] = {'Driver': 'ODBC Driver 17 for SQL Server',
                           'Server': 'localhost',
                           'Database': 'mydatabase',
                           'UserID' : 'sa',
                           'Password': 'xX94Hugo'}

    config['MYSQL'] = {'Address': 'localhost',
                       'User': 'root',
                       'Password': 'rootpasswordgiven',
                       'Database': 'mydatabase'}

    config['REL'] = {'Directory': '/home/mario/Downloads/Rel3.013.linuxDBMS'}

    with open(os.path.abspath('.') + "/ermtk.ini", 'wt') as configfile:
        config.write(configfile)

def load_config():
    if os.path.exists("/etc/ermtk.ini"):
        config.read("/etc/ermtk.ini")
    if os.path.exists(os.environ.get('HOME') + "/ermtk.ini"):
        config.read(os.environ.get('HOME') + "/ermtk.ini")
    if os.path.exists(os.path.abspath('.') + "/ermtk.ini"):
        config.read(os.path.abspath('.') + "/ermtk.ini")

    global basexconf
    global oracleconf
    global postgresqlconf
    global sqliteconf
    global sqlserverconf
    global mysqlconf
    global relconf

    try:
        basexconf = config['BASEX']
        oracleconf = config['ORACLE']
        postgresqlconf = config['POSTGRESQL']
        sqliteconf = config['SQLITE']
        sqlserverconf = config['SQLSERVER']
        mysqlconf = config['MYSQL']
        relconf = config['REL']
    except KeyError:
        print(Fore.RED + "No configuration file found" + Fore.RESET)

def update_config():
    try:
        basexconf = config['BASEX']
        with open(os.path.abspath('.') + "/ermtk.ini", 'wt') as configfile:
            config.write(configfile)
    except KeyError:
        write_config()



def print_basex():
    print('BaseX config:')
    print('Address: ' + basexconf['Address'])
    print('Port: ' + basexconf['Port'])
    print('User: ' + basexconf['User'])
    print('Password: ' + basexconf['Password'])

def print_oracle():
    print('Oracle config:')
    print('Address: ' + oracleconf['Address'])
    print('ServiceName: ' + oracleconf['ServiceName'])
    print('User: ' + oracleconf['User'])
    print('Password: ' + oracleconf['Password'])

def print_postgre():
    print('PostgreSQL config:')
    print('Address: ' + postgresqlconf['Address'])
    print('Database: ' + postgresqlconf['Database'])
    print('User: ' + postgresqlconf['User'])
    print('Password: ' + postgresqlconf['Password'])

def print_sqlite():
    print('SQLite config:')
    print('Directory: ' + sqliteconf['Directory'])

def print_sqlserver():
    print('SQLServer config:')
    print('Driver: ' + sqlserverconf['Driver'])
    print('Server: ' + sqlserverconf['Server'])
    print('Database: ' + sqlserverconf['Database'])
    print('UserID: ' + sqlserverconf['UserID'])
    print('Password: ' + sqlserverconf['Password'])

def print_mysql():
    print('MySQL config:')
    print('Address: ' + mysqlconf['Address'])
    print('User: ' + mysqlconf['User'])
    print('Password: ' + mysqlconf['Password'])
    print('Database: ' + mysqlconf['Database'])

def print_rel():
    print("REL")
    print("Directory: " + relconf['Directory'])

def print_config():
    print("Configuration ----------")
    print_basex()
    print("------------------------")
    print_oracle()
    print("------------------------")
    print_postgre()
    print("------------------------")
    print_sqlite()
    print("------------------------")
    print_sqlserver()
    print("------------------------")
    print_mysql()
    print("------------------------")
    print_rel()




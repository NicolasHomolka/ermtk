#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class datenbank:
    name = ""
    tabellen = []
    language = ""

    def __init__(self):
        self.name = ""
        self.tabellen = []
        self.language = ""

    def settitle(self, title):
        self.name = title

    def addtable(self, table):
        self.tabellen.append(table)

    def setlanguage(self, lang):
        self.language = lang

    def getprimarycolumns(self,table):
        for tables in self.tabellen:
            primarys = tables.getprimarycolumns(table)
            if len(primarys) > 0:
                return primarys
        return []

    def addcolumn(self,table, column, pos=0):
        for tables in self.tabellen:
            if tables.name == table:
                tables.addcolumn(column.uname, column.name, column.prime, column.type, column.min, column.max, column.clas, column.qoute, pos)

    def addrelation(self, tablename, name, reference, group, count, refqoute):
        for table in self.tabellen:
            table.addrelation(tablename, name, reference, group, count, refqoute)

    def tableuname(self, tablename):
        for table in self.tabellen:
            if tablename == table.name:
                return table.uname
        return tablename

    def tablename(self, tablename):
        for table in self.tabellen:
            if tablename == table.uname:
                return table.name

    def columnuname(self, tablename, columnname):
        for table in self.tabellen:
            if tablename == table.name:
                return table.columnname(columnname)
        return columnname

    def maxcolumn(self):
        current = 0
        for table in self.tabellen:
            for column in table.columns:
                if len(column.uname) > current:
                    current = len(column.uname)
        return current

    def tabqoute(self, tablename):
        for table in self.tabellen:
            if table.name == tablename:
                return table.qoute
        return ""

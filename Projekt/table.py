#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import column
import re

class Table:
    name = ""
    columns = []
    rows = []

    def __init__(self, name, columns, rows):
        self.desc = ""
        self.qoute = "false"
        self.name = name
        self.uname = name
        self.columns = columns
        self.rows = rows

    def __init__(self):
        self.name = ""
        self.desc = ""
        self.uname = ""
        self.qoute = "false"
        self.columns = []
        self.rows = []

    def setuname(self, uname):
        temp = re.sub(r"[^\w\s]", '', uname)
        temp = re.sub(r"\s+", '_', temp)
        self.uname = temp

    def addcolumn(self, uname, col, prime, type="string", min="", max="", clas="", qoute="",pos=0):
        if pos == 0:
            self.columns.append(column.Column(uname, col, type, prime, min, max, clas, qoute))
        else:
            self.columns.insert(pos-1, column.Column(uname, col, type, prime, min, max, clas, qoute))

    def addcolumnsub(self, col):
        self.columns.append(col)

    def addrelation(self, tablename, uname, reference, group, count, refqoute):
        if tablename == self.name:
            for column in self.columns:
                column.addrelation(uname, reference, group, count, refqoute)

    def getprimary(self):
        primarys = []
        for columne in self.columns:
            if columne.prime == "true":
                primarys.append(columne.uname)
        return primarys

    def getprimarycolumns(self,name):
        primarys = []
        if self.name == name:
            for columne in self.columns:
                if columne.prime == "true":
                    primarys.append(columne)
        return primarys

    def unique(self, name):
        for columne in self.columns:
            if columne.uname == name:
                return False
        return True

    def getforeigncolumns(self):
        all = []
        i = 0
        for outer in self.columns:
            i += 1
            foreign = []
            for column in self.columns:
                if column.group == i:
                    foreign.append(column)
            all.append(foreign)
        return all

    def getdata(self):
        data = []
        max = 0
        if len(self.columns) > 0:
            max = len(self.columns[0].data)
        i = 0
        while i < max:
            data.append([])
            i += 1
        for column in self.columns:
            i = 0
            while i < len(column.data):
                data[i].append(column.data[i])
                i += 1
        return data

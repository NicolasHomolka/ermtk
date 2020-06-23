#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Column:

    def __init__(self, uname, name, typ, prime, min, max, clas, qoute):
        self.name = name
        self.type = typ
        self.prime = prime
        self.uname = uname
        self.data = []
        self.reference = ""
        self.group = 0
        self.count = 0
        self.qoute = qoute
        self.clas = clas
        self.refqoute = ""
        if min == None:
            self.min = ""
        else:
            self.min = min
        if max == None:
            self.max = ""
        else:
            self.max = max

    def addrelation(self, uname, reference, group, count, refqoute):
        if self.uname == uname:
            self.reference = reference
            self.group = group
            self.count = count
            self.refqoute = refqoute

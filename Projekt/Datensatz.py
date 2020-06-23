#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

class Datensatz:
    data = {}

    def add(self, column, value):
        self.data.update({column:value})

    def __init__(self, column, value):
        self.add(column,value)

    def drop(self):
        self.data.clear()

    
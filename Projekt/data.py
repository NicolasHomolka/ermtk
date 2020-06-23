#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Data:

    def __init__(self, root, typ):
        self.root = root
        self.typ = typ

    def get_lang(self):
        for child in self.root:
            if child.tag == 'entlo':
                return child.get('lang')

    def get_ent(self):
        matrix = []
        for child in self.root:
            if child.tag == 'ent':
                matrix.append(child.get('name'))
        return matrix

    def get_rel(self):
        matrix = []
        for child in self.root:
            if child.tag == 'rel':
                matrix.append(child.get('to'))
        return matrix

    def get_ent_attr(self):
        matrix = []
        first_level = 0
        for child in self.root:
            temp_matrix = []
            if child.tag == 'ent':
                temp_matrix.append(child.get('name'))

                for grandchild in child:
                    if grandchild.tag == 'attr':
                        temp_matrix.append(grandchild.get('name'))

            if len(temp_matrix) > 0:
                matrix.insert(first_level, temp_matrix)
                first_level += 1
        return matrix

    def get_rel_attr(self):
        matrix = []
        first_level = 0
        for child in self.root:
            temp_matrix = []
            if child.tag == 'rel':
                temp_matrix.append(child.get('to'))

                for grandchild in child:
                    if grandchild.tag == 'part':
                        temp_matrix.append(grandchild.get('ref'))

            if len(temp_matrix) > 0:
                matrix.insert(first_level, temp_matrix)
                first_level += 1
        return matrix
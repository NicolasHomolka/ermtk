#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from graphviz import Graph
import os


class graphviz_converter:

    _erd = None
    out = None
    _tree = None
    _tree_lo = None
    _tree_ty = None
    _root = None

    def __init__(self, args, tree, tree_lo, tree_ty):
        if not(args.loc == "") or args.loc is not False:
            self._tree_lo = tree_lo
        if not(args.typ == "") or args.typ is not False:
            self._tree_ty = tree_ty
        self._tree = tree
        _root = self._tree.getroot()
        name = "erd"
        set = False
        for child in _root:
            if child.tag == "title":
                name = child.get("name")
                set = True
            if set:
                break
        _erd = Graph(name, filename=name, engine="sfdp")
        self.create_erd(args, _erd, _root)

    def create_erd(self, args, erd, root):
        s = False

        for child in root:
            sup = False
            prime = False
            disjoint = False
            total = False
            weak = False

            # Creating Entities
            if child.tag == "title":
                if not s:
                    erd.attr(label=child.get("name"))
                    erd.attr(fontsize="20")
                    s = True
            elif child.tag == "ent":
                for rel in root:
                    for relPart in rel:
                        if relPart.get("ref") == child.get("name") and relPart.get("weak") == "true":
                            weak = True
                            break
                self.create_ent(erd, child.get("name"), weak)
                weak = False
            # Creating Attributes
                if args.attr:
                    for entPart in child:
                        if entPart.tag == "attr" and entPart.get("prime") == "true":
                            prime = True
                        elif entPart.tag == "attr":
                                self.create_attr(erd, child.get("name") +"."+ entPart.get("name"), weak, prime, entPart.get("name"))
                                self.create_edge(erd, child.get("name"), child.get("name") +"."+ entPart.get("name"))

            # Creating Relations
            elif child.tag == "rel":
                rela = child.get("to")
                sup = False
                disjoint = False
                total = False
                weak = False
                for relPart in child:
                    if relPart.get("weak") == "true":
                        weak = True
                    elif relPart.tag == "super":
                        sup = True
                        if relPart.get("disjoint") == "true":
                            disjoint = True
                        elif relPart.get("total") == "true":
                            total = True
                self.create_rel(erd, rela, weak, sup, disjoint)

                # Creating Edges
                for par in child:
                    if par.tag == "part":
                        self.create_edgeRel(erd, rela, par.get("ref"), par.get("min"), par.get("max"))
                    elif par.tag == "super":
                        if total:
                            self.create_edgeTotal(erd, rela, par.get('ref'))
                        else:
                            self.create_edge(erd, rela, par.get("ref"))
                    elif par.tag == "sub":
                        self.create_edge(erd, rela, par.get("ref"))

        erd.render(format="pdf")
        cwd = os.getcwd()
        print("Your ERD is sucessfully created in:" + cwd)

    def create_ent(self, erd, name, weak):
        if not weak:
            erd.attr("node", shape="box", peripheries="1")
            erd.node(name)
        else:
            erd.attr("node", shape="box", peripheries="2")
            erd.node(name)

    def create_attr(self, erd, name, weak, prime, label):
        if weak and prime:
            erd.attr("node", shape="circle", style="dashed", label=label)
            erd.node(name)
        elif prime:
            erd.attr("node", shape="circle", style="bold", label=label)
            erd.node(name)
        else:
            erd.attr("node", shape="circle", label=label)
            erd.node(name)

    def create_rel(self, erd, name, weak, sup, disjoint):
        if weak:
            erd.attr("node", shape="diamond", peripheries="2")
            erd.node(name)
        elif sup:
            if disjoint:
                erd.attr("node", shape="triangle", color="black")
                erd.node(name=name, style="filled")
            else:
                erd.attr("node", shape="triangle", color="white")
                erd.node(name=name, style="filled")
        else:
            erd.attr("node", shape="diamond", peripheries="1")
            erd.node(name)

    def create_edgeTotal(self, erd, ent1, ent2):
        s = "(" + 1 + ", " + "n)"
        erd.edge(ent1, ent2, peripheries="2")

    def create_edgeRel(self, erd, ent1, ent2, mini, maxi):
        s = "(" + mini + ", " + maxi + ")"
        erd.edge(ent1, ent2, label=s, peripheries="1")

    def create_edge(self, erd, ent1, ent2):
        erd.edge(ent1, ent2, peripheries="1")
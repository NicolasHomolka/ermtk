#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from colorama import Fore
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout



class GraphmlConverter:
    out = None
    _tree = None
    _tree_lo = None
    node_counter = 0
    rel_counter = 0
    ent_map = {}
    rel_map = {}
    node_layout_map = {}
    rel_layout_map = {}
    positions = None
    color = False
    edge_types = {"0,1": "crows_foot_one_optional", "0,n": "crows_foot_many_optional",
                  "1,1": "crows_foot_one_mandatory", "1,n": "crows_foot_many_mandatory",
                  "sub": "none", "super": "none", "attr": "none"}

    def __init__(self, args, tree, tree_lo, tree_ty):
        if args.loc is not None:
            self._tree_lo = tree_lo
        else:
            self._tree_lo = None
        if args.color:
            self.color = True
        self._tree = tree
        self.get_layout(args)
        self.create_erd(args)

    def get_layout(self, args):
        erd = nx.Graph()
        root = self._tree.getroot()
        for rel in root.findall('rel'):
            erd.add_node(rel.get('to'), size=100)
            for child in rel.findall('part'):
                erd.add_node(child.get('ref'), size=100)
                erd.add_edge(rel.get('to'), child.get('ref'))
            for child in rel.findall('super'):
                erd.add_node(child.get('ref'), size=100)
                erd.add_edge(rel.get('to'), child.get('ref'))
            for child in rel.findall('sub'):
                erd.add_node(child.get('ref'), size=100)
                erd.add_edge(rel.get('to'), child.get('ref'))
            if args.attr:
                for child in rel.findall('attr'):
                    erd.add_node(child.get('ref'), size=100)
                    erd.add_edge(rel.get('to'), child.get('name'))
        if args.attr:
            for ent in root.findall('ent'):
                for child in ent.findall('attr'):
                    erd.add_node(child.get('name'), size=100)
                    erd.add_edge(ent.get('name'), child.get('name'))
        self.positions = graphviz_layout(erd, prog='dot')

    def create_erd(self, args):
        try:
            if args.output is None:
                if os.path.exists("output.graphml"):
                    os.remove("output.graphml")
                self.out = open("output.graphml", "w+")
            else:
                if os.path.exists(os.getcwd() + "/" + args.output):
                    os.remove("./" + args.output)
                self.out = open(os.getcwd() + "/" + args.output, "w+")
            self.init_file()
        except IOError:
            print(Fore.RED + "There was a Problem creating the file. Please try again" + Fore.RESET)
            return
        root = self._tree.getroot()
        self.node_counter = 0
        # ------------------------------------------------------------------------------------------------------
        for child in root:
            if child.tag == "ent":
                key = "n" + str(self.node_counter)
                self.ent_map[key] = child.get("name")
                weak = False
                for rel in root.findall("rel"):
                    for relPart in rel:
                        if relPart.get("ref") == child.get("name") and relPart.get("weak") == "true":
                            weak = True
                self.create_node(key, child.get("name"), "small_entity", weak)
                self.node_counter += 1
                if args.attr:
                    for attr in child:
                        self.create_attribute(attr, key)
            # --------------------------------------------------------------------------------------------------
            elif child.tag == "rel":
                key = "n" + str(self.node_counter)
                self.rel_map[key] = child.get("to")
                self.node_counter += 1
                generalization_node = False
                weak = False
                for part in child:
                    if part.tag == "part":
                        for mayWeak in child:
                            if mayWeak.get("weak") == "true":
                                weak = True
                        self.create_node(key, child.get("to"), "relationship", weak)
                        # --------------------------------------------------------------------------------------
                        if args.notation == "crowfoot":
                            if part.get("max") != "n":
                                if int(part.get("max")) > 1:
                                    edge_type_key = str(part.get("min")) + "," + str(1)
                                else:
                                    edge_type_key = str(part.get("min")) + "," + str(part.get("max"))
                            else:
                                edge_type_key = str(part.get("min")) + "," + str(part.get("max"))
                            part_name = part.get("ref")
                            key_e = ""
                            for k in self.ent_map:
                                if self.ent_map[k] == part_name:
                                    key_e = k
                            r_id = "e" + str(self.rel_counter)
                            if key_e != "" and key != "":
                                self.create_edge(r_id, key_e, key, edge_type_key)
                            else:
                                print(Fore.RED + "There was an entity missing for a relationship" + Fore.RESET)
                            self.rel_counter += 1
                        # --------------------------------------------------------------------------------------
                        elif args.notation == "chen":
                            edge_description = str(part.get("min")) + "," + str(part.get("max"))
                            part_name = part.get("ref")
                            key_e = ""
                            for k in self.ent_map:
                                if self.ent_map[k] == part_name:
                                    key_e = k
                            r_id = "e" + str(self.rel_counter)
                            if key_e != "" and key != "":
                                self.create_chen_edge(r_id, key_e, key, edge_description)
                            else:
                                print(Fore.RED + "There was an entity missing for a relationship" + Fore.RESET)
                            self.rel_counter += 1
                        else:
                            edge_description = str(part.get("min")) + "," + str(part.get("max"))
                            part_name = part.get("ref")
                            key_e = ""
                            for k in self.ent_map:
                                if self.ent_map[k] == part_name:
                                    key_e = k
                            r_id = "e" + str(self.rel_counter)
                            if key_e != "" and key != "":
                                self.create_chen_edge(r_id, key_e, key, edge_description)
                            else:
                                print(Fore.RED + "There was an entity missing for a relationship" + Fore.RESET)
                            self.rel_counter += 1
                    # ------------------------------------------------------------------------------------------
                    elif part.tag == "super":
                        if not generalization_node:
                            generalization_node = True
                            total = False
                            min = "0"
                            max = "n"
                            disjoint = False
                            if part.get("total") == "true":
                                total = True
                                min = "1"
                            if part.get("disjoint") == "true":
                                disjoint = True
                                max = "1"
                            self.create_generalization_node(key, disjoint, child.get('to'))
                            part_name = part.get("ref")
                            key_e = ""
                            for k in self.ent_map:
                                if self.ent_map[k] == part_name:
                                    key_e = k
                            r_id = "e" + str(self.rel_counter)
                            if key_e != "" and key != "":
                                if args.notation == "chen":
                                    desc = min + "," + max
                                    self.create_chen_edge(r_id, key_e, key, "super", desc)

                                else:
                                    self.create_edge(r_id, key_e, key, "super")
                                    if total:
                                        self.rel_counter += 1
                                        r_id = "e" + str(self.rel_counter)
                                        self.create_edge(r_id, key_e, key, "super")
                            else:
                                print(Fore.RED + "There was an entity missing for a relationship" + Fore.RESET)
                            self.rel_counter += 1
                    # ------------------------------------------------------------------------------------------
                    elif part.tag == "sub":
                        part_name = part.get("ref")
                        key_e = ""
                        for k in self.ent_map:
                            if self.ent_map[k] == part_name:
                                key_e = k
                        r_id = "e" + str(self.rel_counter)
                        if key_e != "" and key != "":
                            if args.notation == "chen":
                                self.create_chen_edge(r_id, key_e, key, "sub", "1,1")
                            else:
                                self.create_edge(r_id, key_e, key, "sub")
                        else:
                            print(Fore.RED + "There was an entity missing for a relationship" + Fore.RESET)
                        self.rel_counter += 1
                    elif part.tag == "attr" and args.attr:
                        self.create_attribute(part, key)

        self.close_file()
        if args.output is None:
            print("Your file is created at: " + os.getcwd() + "/output.graphml")
        else:
            print("Your file is created at: " + os.getcwd() + "/" + args.output)

    def init_file(self):
        self.out.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        self.out.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" '
                       'xmlns:java="http://www.yworks.com/xml/yfiles-common/1.0/java" '
                       'xmlns:sys="http://www.yworks.com/xml/yfiles-common/markup/primitives/2.0" '
                       'xmlns:x="http://www.yworks.com/xml/yfiles-common/markup/2.0" '
                       'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                       'xmlns:y="http://www.yworks.com/xml/graphml" '
                       'xmlns:yed="http://www.yworks.com/xml/yed/3" '
                       'xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns '
                       'http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd">\n')
        self.out.write('\t<key for="node" id="d1" yfiles.type="nodegraphics"/>\n')
        self.out.write('\t<key for="edge" id="d2" yfiles.type="edgegraphics"/>\n')
        self.out.write('\t<graph edgedefault="directed" id="G">\n')

    def create_attribute(self, attr, key):
        key_attr = "n" + str(self.node_counter)
        if attr.get("prime") == "true":
            self.create_prime_node(key_attr, attr.get("name"), "attribute")
            self.node_counter += 1
        else:
            self.create_node(key_attr, attr.get("name"), "attribute", False)
            self.node_counter += 1
        e_id = "e" + str(self.rel_counter)
        self.create_edge(e_id, key, key_attr, "attr")
        self.rel_counter += 1

    def create_node(self, key, name_std, type_desc, weak):
        x_pos = str(self.positions[name_std][0] * 1.5)
        y_pos = str(self.positions[name_std][1] * 1.5)
        name = name_std
        search_element_name = None
        if type_desc == "small_entity":
            search_element_name = "entref"
        elif type_desc == "relationship":
            search_element_name = "relref"
        if not (self._tree_lo is None):
            root = self._tree_lo.getroot()
            if type_desc == "attribute":
                for ent in root:
                    for attr in ent:
                        if attr.get("name") == name_std:
                            name = attr.get("name-lo")
            else:
                for ent in root:
                    if ent.get(search_element_name) == name_std:
                        name = ent.get("name-lo")
        self.out.write('\t\t<node id="' + key + '">\n')
        self.out.write('\t\t\t<data key="d1">\n')
        self.out.write('\t\t\t\t<y:GenericNode configuration="com.yworks.entityRelationship.' + type_desc + '">\n')
        if len(name) > 10:
            self.out.write('\t\t\t\t\t<y:Geometry height="90.0" width="130.0" x="' + x_pos + '" y="' + y_pos + '"/>\n')
        else:
            self.out.write('\t\t\t\t\t<y:Geometry height="50.0" width="90.0" x="' + x_pos + '" y="' + y_pos + '"/>\n')
        if not self.color:
            self.out.write('\t\t\t\t\t<y:Fill hasColor="false" transparent="false"/>\n')
        else:
            if type_desc == "small_entity":
                self.out.write('\t\t\t\t\t<y:Fill color="#89D8D6" transparent="false"/>\n')
            elif type_desc == "attribute":
                self.out.write('\t\t\t\t\t<y:Fill color="#89BED8" transparent="false"/>\n')
            elif type_desc == "relationship":
                self.out.write('\t\t\t\t\t<y:Fill color="#93D889" transparent="false"/>\n')
        self.out.write('\t\t\t\t\t<y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" '
                       'fontSize="12" fontStyle="plain" height="17.96875" horizontalTextPosition="center" '
                       'iconTextGap="4" modelName="internal" modelPosition="c" textColor="#000000" '
                       'verticalTextPosition="bottom" visible="true">' + name + '</y:NodeLabel>\n')
        if weak:
            self.out.write('\t\t\t\t\t<y:StyleProperties>\n')
            self.out.write('\t\t\t\t\t\t<y:Property class="java.lang.Boolean" name="doubleBorder" value="true"/>\n')
            self.out.write('\t\t\t\t\t</y:StyleProperties>\n')
        self.out.write('\t\t\t\t</y:GenericNode>\n')
        self.out.write('\t\t\t</data>\n')
        self.out.write('\t\t</node>\n')

    def create_prime_node(self, key, name, type_desc):
        x_pos = str(self.positions[name][0] * 1.5)
        y_pos = str(self.positions[name][1] * 1.5)
        self.out.write('\t\t<node id="' + key + '">\n')
        self.out.write('\t\t\t<data key="d1">\n')
        self.out.write('\t\t\t\t<y:GenericNode configuration="com.yworks.entityRelationship.' + type_desc + '">\n')
        if len(name) > 10:
            self.out.write('\t\t\t\t\t<y:Geometry height="90.0" width="130.0" x="' + x_pos + '" y="' + y_pos + '"/>\n')
        else:
            self.out.write('\t\t\t\t\t<y:Geometry height="50.0" width="90.0" x="' + x_pos + '" y="' + y_pos + '"/>\n')
        if not self.color:
            self.out.write('\t\t\t\t\t<y:Fill hasColor="false" transparent="false"/>\n')
        else:
            self.out.write('\t\t\t\t\t<y:Fill color="#89BED8" transparent="false"/>\n')
        self.out.write('\t\t\t\t\t<y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" '
                       'fontSize="12" fontStyle="plain" height="17.96875" horizontalTextPosition="center" '
                       'iconTextGap="4" modelName="custom" textColor="#000000" underlinedText="true" '
                       'verticalTextPosition="bottom" visible="true">' + name + '</y:NodeLabel>\n')
        self.out.write('\t\t\t\t</y:GenericNode>\n')
        self.out.write('\t\t\t</data>\n')
        self.out.write('\t\t</node>\n')

    def create_generalization_node(self, key, disjoint, name):
        x_pos = str(self.positions[name][0] * 1.5)
        y_pos = str(self.positions[name][1] * 1.5)
        mode = 'hasColor="false"'
        if not disjoint:
            mode = 'color="#000000"'
        self.out.write('\t\t<node id="' + key + '">\n')
        self.out.write('\t\t\t<data key="d1">\n')
        self.out.write('\t\t\t\t<y:ShapeNode>\n')
        self.out.write('\t\t\t\t\t<y:Geometry height="50.0" width="90.0" x="' + x_pos + '" y="' + y_pos + '"/>\n')
        self.out.write('\t\t\t\t\t<y:Fill ' + mode + ' transparent="false"/>\n')
        self.out.write('\t\t\t\t\t<y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" '
                       'fontSize="12" fontStyle="plain" height="17.96875" horizontalTextPosition="center" '
                       'iconTextGap="4" modelName="custom" textColor="#000000" '
                       'verticalTextPosition="bottom" visible="true"/>\n')
        self.out.write('\t\t\t\t\t<y:Shape type="triangle"/>\n')
        self.out.write('\t\t\t\t</y:ShapeNode>\n')
        self.out.write('\t\t\t</data>\n')
        self.out.write('\t\t</node>\n')

    def create_edge(self, e_id, key_source, key_target, edge_type_key):
        self.out.write('\t\t<edge id="' + e_id + '" source="' + key_source + '" target="' + key_target + '">\n')
        self.out.write('\t\t\t<data key="d2">\n')
        self.out.write('\t\t\t\t<y:PolyLineEdge>\n')
        self.out.write('\t\t\t\t\t<y:LineStyle color="#000000" type="line" width="1.0"/>\n')
        self.out.write('\t\t\t\t\t<y:Arrows source="' + self.edge_types[edge_type_key] + '" target="none"/>\n')
        self.out.write('\t\t\t\t</y:PolyLineEdge>\n')
        self.out.write('\t\t\t</data>\n')
        self.out.write('\t\t</edge>\n')

    def create_chen_edge(self, e_id, key_source, key_target, edge_description):
        self.out.write('\t\t<edge id="' + e_id + '" source="' + key_source + '" target="' + key_target + '">\n')
        self.out.write('\t\t\t<data key="d2">\n')
        self.out.write('\t\t\t\t<y:PolyLineEdge>\n')
        self.out.write('\t\t\t\t\t<y:LineStyle color="#000000" type="line" width="1.0"/>\n')
        self.out.write('\t\t\t\t\t<y:Arrows source="none" target="none"/>\n')
        self.out.write('\t\t\t\t\t<y:EdgeLabel alignment="center" configuration="AutoFlippingLabel" distance="2.0" '
                       'fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" '
                       'hasLineColor="false" height="17.96875" horizontalTextPosition="center" iconTextGap="4" '
                       'modelName="custom" preferredPlacement="source_right" ratio="0.5" textColor="#000000" '
                       'verticalTextPosition="bottom" visible="true" width="90.3203125" x="-15.16015625" '
                       'xml:space="preserve" y="-22.94091796875003">' + '(' + edge_description + ')' +
                       '<y:LabelModel><y:SmartEdgeLabelModel autoRotationEnabled="false" defaultAngle="0.0" '
                       'defaultDistance="10.0"/></y:LabelModel><y:ModelParameter><y:SmartEdgeLabelModelParameter '
                       'angle="0.0" distance="30.0" distanceToCenter="true" position="right" ratio="0.0" segment="0"/>'
                       '</y:ModelParameter><y:PreferredPlacementDescriptor angle="0.0" angleOffsetOnRightSide="0" '
                       'angleReference="absolute" angleRotationOnRightSide="co" distance="-1.0" placement="source" '
                       'side="right" sideReference="relative_to_edge_flow"/></y:EdgeLabel>\n')
        self.out.write('\t\t\t\t</y:PolyLineEdge>\n')
        self.out.write('\t\t\t</data>\n')
        self.out.write('\t\t</edge>\n')

    def close_file(self):
        self.out.write('\t</graph>\n')
        self.out.write('</graphml>')
        self.out.close()

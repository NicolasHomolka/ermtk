/*
* Author:       Nicolas Homolka
* Last Solved:  PK unterstrichen, Beziehung mit 1 Entity-Typen darstellbar
* Last Problem: 
* TODO:         Super - Subtypen, Abhängige Entity-Typen, Mehrwertige Beziehungen, Layout  
*/

//Libre Office Draw API Stuff

import com.sun.star.uno.UnoRuntime;

import com.sun.star.drawing.*;
import com.sun.star.uno.UnoRuntime;
import com.sun.star.lang.XComponent;

import com.sun.star.awt.Point;
import com.sun.star.awt.Size;

import com.sun.star.beans.PropertyValue;
import com.sun.star.beans.XPropertySet;
import com.sun.star.container.XNamed;

import com.sun.star.drawing.PolygonFlags;
import com.sun.star.drawing.PolyPolygonBezierCoords;
import com.sun.star.drawing.XShape;
import com.sun.star.drawing.XShapes;
import com.sun.star.drawing.XShapeGrouper;
import com.sun.star.drawing.XDrawPage;
import com.sun.star.drawing.ShapeCollection;

import com.sun.star.lang.XMultiServiceFactory;
import com.sun.star.container.XIndexAccess;
import com.sun.star.text.XText;

import com.sun.star.style.XStyle;

import com.sun.star.uno.*;
import com.sun.star.lang.*;
import com.sun.star.frame.*;

import com.sun.star.text.*;
import com.sun.star.style.*;
import com.sun.star.container.*;
import com.sun.star.beans.*;
import com.sun.star.table.*;

//Java Stuff

import java.util.Random;
import java.util.HashMap;
import java.util.Map;
import java.util.Iterator;
import java.util.Set;
import java.util.LinkedHashMap;
import java.util.*;

//XML Stuff

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Element;
import java.io.File;
import java.util.ArrayList;

class Entity {
    int x;
    int y;
    int width;
    int height;
    String name;

    Entity(String name, int width, int height, int x, int y) {
        this.name = name;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }

    void print() {
        System.out.println(name);
        System.out.println(width);
        System.out.println(height);
        System.out.println(x);
        System.out.println(y);
    }
}

class Relation {
    String name;
    String from;
    String to;
    String max_to;
    String max_from;

    Relation(String name, String from, String max_from, String to, String max_to) {
        this.name = name;
        this.from = from;
        this.to = to;
        this.max_from = max_from;
        this.max_to = max_to;
    }

    void print() {
        System.out.println(name);
        System.out.println(from);
        System.out.println(max_from);
        System.out.println(to);
        System.out.println(max_to);
    }
}

// --------------------------------------------------------------------------------------------------
// ---------------------- Class SDraw
// ---------------------------------------------------------------
// --------------------------------------------------------------------------------------------------

public class SDraw {

    public static void main(String args[]) {
        long start = new Date().getTime();



        String inputfile = new String();

        inputfile = "../datenmodelle/weingut/xml/weingut.xerml.xml";
        String display_attr = "0";
        String display_color = "0";

        System.out.println(display_attr);

        int color = getCol(255, 255, 255);

        if (display_color.equals("1")) {
            color = 16711680;
        }

        com.sun.star.uno.XComponentContext xContext = null;

        try {
            // get the remote office component context
            xContext = com.sun.star.comp.helper.Bootstrap.bootstrap();
            System.out.println("Connected to a running office ...");
        } catch (java.lang.Exception e) {
            e.printStackTrace(System.err);
            System.exit(1);
        }
        com.sun.star.lang.XComponent xDrawDoc = null;
        com.sun.star.drawing.XDrawPage xDrawPage = null;
        System.out.println("Opening an empty Draw document ...");
        xDrawDoc = openDraw(xContext);
        try {
            System.out.println("getting Drawpage");
            com.sun.star.drawing.XDrawPagesSupplier xDPS = UnoRuntime
                    .queryInterface(com.sun.star.drawing.XDrawPagesSupplier.class, xDrawDoc);
            com.sun.star.drawing.XDrawPages xDPn = xDPS.getDrawPages();
            com.sun.star.container.XIndexAccess xDPi = UnoRuntime
                    .queryInterface(com.sun.star.container.XIndexAccess.class, xDPn);
            xDrawPage = UnoRuntime.queryInterface(com.sun.star.drawing.XDrawPage.class, xDPi.getByIndex(0));
        } catch (java.lang.Exception e) {
            System.err.println("Couldn't create document" + e);
            e.printStackTrace(System.err);
        }
        // put something on the drawpage
        System.out.println("inserting some Shapes");
        com.sun.star.drawing.XShapes xShapes = UnoRuntime.queryInterface(com.sun.star.drawing.XShapes.class, xDrawPage);

        ArrayList<ArrayList<String>> ent = get_ent(inputfile);
        System.out.println(ent);
        System.out.println("");
        ArrayList<ArrayList<String>> rel = get_rel(inputfile);
        System.out.println(rel);
        System.out.println(rel.size());
        System.out.println("");
        ArrayList<ArrayList<String>> rel_attr = get_rel_attr(inputfile);
        System.out.println(rel_attr);
        System.out.println("");
        ArrayList<ArrayList<String>> PK = getPK(inputfile);
        System.out.println(PK);
        System.out.println("");
        ArrayList<ArrayList<String>> SuperSub = getSuperSub(inputfile);
        System.out.println(SuperSub);

        for (int i = 0; i < SuperSub.size(); i++) {
            if (SuperSub.get(i).size() <= 1) {
                SuperSub.remove(i);
                i--;
            }
        }

        System.out.println("--------------------------------------------------");
        System.out.println(SuperSub);
        System.out.println("--------------------------------------------------");

        for (int i = 0; i < rel.size(); i++) {
            if (rel.get(i).size() <= 1) {
                rel.remove(i);
            }
        }

        Relation[] rel_list = new Relation[rel.size()];

        for (int i = 0; i < rel.size(); i++) {
            if (rel.size() >= 2) {
                rel_list[i] = new Relation(rel.get(i).get(0), rel.get(i).get(1), rel.get(i).get(2), rel.get(i).get(3),
                        rel.get(i).get(4));
                // beim öffnen von sis.passet.xerml.xml wird ein fehler geworfen, wegen
                // super/sub typ

            }
        }
        System.out.println("neu rel:" + rel);
        int x = 2000;
        int y = 2500;

        Entity[] ent_list = new Entity[ent.size()];

        for (int i = 0; i < ent.size(); i++) {
            ent_list[i] = new Entity(ent.get(i).get(0), 2500, 1900, x, y);
            y += 4000;
            if (y >= 16000) {
                y = 2500;
                x += 4000;
            }
        }
        HashMap<String, XShape> hmap_ent = new HashMap<String, XShape>();
        HashMap<String, XShape> hmap_rel = new HashMap<String, XShape>();
        HashMap<String, XShape> hmap_attr = new HashMap<String, XShape>();

        int x_rel = 125;
        int y_rel = 20;

        for (int i = 0; i < ent_list.length; i++) {
            hmap_ent.put(ent.get(i).get(0),
                    createEntity(xDrawDoc, 1800, 900, ent_list[i].x, ent_list[i].y, ent.get(i).get(0), color));
        }

        for (int i = 0; i < SuperSub.size(); i++) {
            hmap_rel.put(SuperSub.get(i).get(0), createSuperSub(xDrawDoc, hmap_ent, SuperSub.get(i), 100, 100, color));

        }

        for (int i = 0; i < rel_list.length; i++) {
            for (int idx = 0; idx < ent_list.length; idx++) {
                if (rel_list[i].from.equals(ent_list[idx].name)) {

                    for (int idx1 = 0; idx1 < ent_list.length; idx1++) {
                        if (rel_list[i].to.equals(ent_list[idx1].name)) {
                            if (rel.get(i).size() <= 5) {
                                if (rel_list[i].from == rel_list[i].to) {
                                    hmap_rel.put(rel.get(i).get(0),
                                            createRelation(xDrawDoc, hmap_ent.get(ent.get(idx1).get(0)),
                                                    hmap_ent.get(ent.get(idx1).get(0)), rel_list[i].name,
                                                    rel_list[i].max_from, rel_list[i].max_to, x_rel, y_rel, true,
                                                    color));
                                } else {
                                    hmap_rel.put(rel.get(i).get(0),
                                            createRelation(xDrawDoc, hmap_ent.get(ent.get(idx1).get(0)),
                                                    hmap_ent.get(ent.get(idx).get(0)), rel_list[i].name,
                                                    rel_list[i].max_from, rel_list[i].max_to, x_rel, y_rel, false,
                                                    color));
                                }
                            } else {
                                ArrayList<XShape> shape_array = new ArrayList<XShape>();
                                for (int pos = 1; pos + 2 <= rel.get(idx).size(); pos += 2) {

                                    shape_array.add(hmap_ent.get(rel.get(idx).get(pos)));
                                }
                                hmap_rel.put(rel.get(i).get(0),
                                        createMoreRelation(xDrawDoc, shape_array, rel.get(idx), 100, 100, color));
                            }
                            y_rel += 20;
                        }
                    }
                }
            }
        }

        if (display_attr.equals("1")) {
            for (int i = 0; i < rel_attr.size(); i++) {
                if (rel_attr.get(i).size() > 1) {
                    for (int y_attr = 1; y_attr < rel_attr.get(i).size(); y_attr++) {
                        hmap_attr.put(rel_attr.get(i).get(0) + rel_attr.get(i).get(y_attr),
                                createAttr(xDrawDoc, 1800, 900, 5000, 5000, rel_attr.get(i).get(y_attr),
                                        hmap_rel.get(rel_attr.get(i).get(0)), false, color));
                    }
                }
            }

            for (int i = 0; i < ent.size(); i++) {
                for (int y_attr = 1; y_attr < ent.get(i).size(); y_attr++) {
                    if (PK.get(i).get(y_attr) != "") {
                        hmap_attr.put(ent.get(i).get(0) + ent.get(i).get(y_attr), createAttr(xDrawDoc, 1800, 900, 5000,
                                5000, ent.get(i).get(y_attr), hmap_ent.get(ent.get(i).get(0)), true, color));
                    } else {
                        hmap_attr.put(ent.get(i).get(0) + ent.get(i).get(y_attr), createAttr(xDrawDoc, 1800, 900, 5000,
                                5000, ent.get(i).get(y_attr), hmap_ent.get(ent.get(i).get(0)), false, color));
                    }
                }
            }
        } else {
            System.out.println("Without attr");
        }

        System.out.println("done");
        long runningTime = new Date().getTime() - start;
        System.out.println("time: " + runningTime);
        System.exit(0);
    }

    // ----------------------------End of
    // Main--------------------------------------------------------------

    public static com.sun.star.drawing.XShape createSuperSub(com.sun.star.lang.XComponent xDocComp,
            HashMap<String, XShape> hmap_ent, ArrayList<String> SuperSubList, int x, int y, int col) {

        com.sun.star.drawing.XShape xDrawShape = null;
        com.sun.star.frame.XDesktop xDesktop = null;
        com.sun.star.lang.XComponent xComponent = null;
        xDesktop = getDesktop();
        try {
            ArrayList<Object> connectors = new ArrayList<Object>();
            xComponent = xDesktop.getCurrentComponent();
            XDrawPagesSupplier xDrawPagesSupplier = (XDrawPagesSupplier) UnoRuntime
                    .queryInterface(XDrawPagesSupplier.class, xComponent);
            Object drawPages = xDrawPagesSupplier.getDrawPages();
            XIndexAccess xIndexedDrawPages = (XIndexAccess) UnoRuntime.queryInterface(XIndexAccess.class, drawPages);
            Object drawPage = xIndexedDrawPages.getByIndex(0);
            XMultiServiceFactory xDrawFactory = (XMultiServiceFactory) UnoRuntime
                    .queryInterface(XMultiServiceFactory.class, xComponent);

            XDrawPage xDrawPage = (XDrawPage) UnoRuntime.queryInterface(XDrawPage.class, drawPage);

            XShapes xShapes = (XShapes) UnoRuntime.queryInterface(XShapes.class, xDrawPage);
            XMultiServiceFactory xMsf = UnoRuntime.queryInterface(XMultiServiceFactory.class, xComponent);

            Object diamond = drawPolygon(xDrawPage, x, y, 8, 3, "");
            XText xShapeText = UnoRuntime.queryInterface(XText.class, diamond);
            xDrawShape = UnoRuntime.queryInterface(XShape.class, diamond);
            XPropertySet xShapeProps = UnoRuntime.queryInterface(XPropertySet.class, diamond);

            xShapeProps.setPropertyValue("FillColor", Integer.valueOf(col));

            com.sun.star.text.XTextCursor xTCursor = xShapeText.createTextCursor();
            com.sun.star.beans.XPropertySet xTCPS = UnoRuntime.queryInterface(com.sun.star.beans.XPropertySet.class,
                    xTCursor);
            xTCPS.setPropertyValue("CharHeight", 6.0f);

            int tmp = 0;
            for (int i = 3; i < SuperSubList.size(); i++) {
                connectors.add(xMsf.createInstance("com.sun.star.drawing.ConnectorShape"));
                xShapes.add(UnoRuntime.queryInterface(XShape.class, connectors.get(tmp)));
                XPropertySet xConnectorPropSet = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class,
                        connectors.get(tmp));
                xConnectorPropSet.setPropertyValue("StartShape", diamond);
                xConnectorPropSet.setPropertyValue("EndShape", hmap_ent.get(SuperSubList.get(i)));
                tmp++;
            }

            xDrawPage.add(xDrawShape);

        } catch (java.lang.Exception e) {
            System.err.println("Couldn't create instance " + e);
            e.printStackTrace(System.err);
        }

        return xDrawShape;
    }

    public static com.sun.star.drawing.XShape createMoreRelation(com.sun.star.lang.XComponent xDocComp,
            ArrayList<XShape> shape_array, ArrayList<String> rel_list, int x, int y, int col) {

        com.sun.star.drawing.XShape xDrawShape = null;
        com.sun.star.frame.XDesktop xDesktop = null;
        com.sun.star.lang.XComponent xComponent = null;
        xDesktop = getDesktop();
        try {
            ArrayList<Object> connectors = new ArrayList<Object>();
            xComponent = xDesktop.getCurrentComponent();
            XDrawPagesSupplier xDrawPagesSupplier = (XDrawPagesSupplier) UnoRuntime
                    .queryInterface(XDrawPagesSupplier.class, xComponent);
            Object drawPages = xDrawPagesSupplier.getDrawPages();
            XIndexAccess xIndexedDrawPages = (XIndexAccess) UnoRuntime.queryInterface(XIndexAccess.class, drawPages);
            Object drawPage = xIndexedDrawPages.getByIndex(0);
            XMultiServiceFactory xDrawFactory = (XMultiServiceFactory) UnoRuntime
                    .queryInterface(XMultiServiceFactory.class, xComponent);

            XDrawPage xDrawPage = (XDrawPage) UnoRuntime.queryInterface(XDrawPage.class, drawPage);

            XShapes xShapes = (XShapes) UnoRuntime.queryInterface(XShapes.class, xDrawPage);
            XMultiServiceFactory xMsf = UnoRuntime.queryInterface(XMultiServiceFactory.class, xComponent);

            Object diamond = drawPolygon(xDrawPage, x, y, 8, 4, "");
            XText xShapeText = UnoRuntime.queryInterface(XText.class, diamond);
            xDrawShape = UnoRuntime.queryInterface(XShape.class, diamond);
            XPropertySet xShapeProps = UnoRuntime.queryInterface(XPropertySet.class, diamond);

            xShapeProps.setPropertyValue("FillColor", Integer.valueOf(col));

            com.sun.star.text.XTextCursor xTCursor = xShapeText.createTextCursor();
            com.sun.star.beans.XPropertySet xTCPS = UnoRuntime.queryInterface(com.sun.star.beans.XPropertySet.class,
                    xTCursor);
            xTCPS.setPropertyValue("CharHeight", 6.0f);
            xShapeText.insertString(xTCursor, rel_list.get(0), false);

            for (int i = 0; i < shape_array.size(); i++) {
                connectors.add(xMsf.createInstance("com.sun.star.drawing.ConnectorShape"));
                xShapes.add(UnoRuntime.queryInterface(XShape.class, connectors.get(i)));
                XPropertySet xConnectorPropSet = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class,
                        connectors.get(i));
                xConnectorPropSet.setPropertyValue("StartShape", diamond);
                xConnectorPropSet.setPropertyValue("EndShape", shape_array.get(i));
            }

            xDrawPage.add(xDrawShape);

        } catch (java.lang.Exception e) {
            System.err.println("Couldn't create instance " + e);
            e.printStackTrace(System.err);
        }

        return xDrawShape;
    }

    public static com.sun.star.drawing.XShape createAttr(com.sun.star.lang.XComponent xDocComp, int width, int height,
            int x, int y, String text, com.sun.star.drawing.XShape ent, boolean is_PK, int col) {
        com.sun.star.drawing.XShape xDrawShape = null;
        com.sun.star.frame.XDesktop xDesktop = null;
        com.sun.star.lang.XComponent xComponent = null;
        xDesktop = getDesktop();

        try {
            xComponent = xDesktop.getCurrentComponent();
            XDrawPagesSupplier xDrawPagesSupplier = (XDrawPagesSupplier) UnoRuntime
                    .queryInterface(XDrawPagesSupplier.class, xComponent);
            Object drawPages = xDrawPagesSupplier.getDrawPages();
            XIndexAccess xIndexedDrawPages = (XIndexAccess) UnoRuntime.queryInterface(XIndexAccess.class, drawPages);
            Object drawPage = xIndexedDrawPages.getByIndex(0);
            XMultiServiceFactory xDrawFactory = (XMultiServiceFactory) UnoRuntime
                    .queryInterface(XMultiServiceFactory.class, xComponent);
            Object drawShape = xDrawFactory.createInstance("com.sun.star.drawing.EllipseShape");
            XDrawPage xDrawPage = (XDrawPage) UnoRuntime.queryInterface(XDrawPage.class, drawPage);
            xDrawShape = UnoRuntime.queryInterface(XShape.class, drawShape);
            xDrawShape.setSize(new Size(width, height));
            xDrawShape.setPosition(new Point(x, y));

            xDrawPage.add(xDrawShape);
            XMultiServiceFactory xMsf = UnoRuntime.queryInterface(XMultiServiceFactory.class, xComponent);
            XShapes xShapes = (XShapes) UnoRuntime.queryInterface(XShapes.class, xDrawPage);

            XText xShapeText = UnoRuntime.queryInterface(XText.class, drawShape);
            XPropertySet xShapeProps = UnoRuntime.queryInterface(XPropertySet.class, drawShape);

            xShapeProps.setPropertyValue("FillColor", Integer.valueOf(col));

            com.sun.star.text.XTextCursor xTCursor = xShapeText.createTextCursor();
            com.sun.star.beans.XPropertySet xTCPS = UnoRuntime.queryInterface(com.sun.star.beans.XPropertySet.class,
                    xTCursor);

            xTCPS.setPropertyValue("CharHeight", 6.0f);
            if (is_PK) {

                xTCPS.setPropertyValue("CharUnderline", 1);
            }
            xShapeText.insertString(xTCursor, text, false);
            com.sun.star.beans.XPropertySet xText = UnoRuntime.queryInterface(com.sun.star.beans.XPropertySet.class,
                    xShapeProps);

            Object connector1 = xMsf.createInstance("com.sun.star.drawing.ConnectorShape");
            xShapes.add(UnoRuntime.queryInterface(XShape.class, connector1));
            XPropertySet xConnector1PropSet = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class, connector1);
            xConnector1PropSet.setPropertyValue("StartShape", drawShape);
            xConnector1PropSet.setPropertyValue("EndShape", ent);

        } catch (java.lang.Exception e) {
            System.err.println("Couldn't create instance " + e);
            e.printStackTrace(System.err);
        }
        com.sun.star.beans.XPropertySet xSPS = UnoRuntime.queryInterface(com.sun.star.beans.XPropertySet.class,
                xDrawShape);
        return xDrawShape;

    }

    public static com.sun.star.drawing.XShape createEntity(com.sun.star.lang.XComponent xDocComp, int width, int height,
            int x, int y, String text, int col) {

        com.sun.star.drawing.XShape xDrawShape = null;
        com.sun.star.frame.XDesktop xDesktop = null;
        com.sun.star.lang.XComponent xComponent = null;
        xDesktop = getDesktop();

        try {
            xComponent = xDesktop.getCurrentComponent();
            XDrawPagesSupplier xDrawPagesSupplier = (XDrawPagesSupplier) UnoRuntime
                    .queryInterface(XDrawPagesSupplier.class, xComponent);
            Object drawPages = xDrawPagesSupplier.getDrawPages();
            XIndexAccess xIndexedDrawPages = (XIndexAccess) UnoRuntime.queryInterface(XIndexAccess.class, drawPages);
            Object drawPage = xIndexedDrawPages.getByIndex(0);
            XMultiServiceFactory xDrawFactory = (XMultiServiceFactory) UnoRuntime
                    .queryInterface(XMultiServiceFactory.class, xComponent);
            Object drawShape = xDrawFactory.createInstance("com.sun.star.drawing.RectangleShape");
            XDrawPage xDrawPage = (XDrawPage) UnoRuntime.queryInterface(XDrawPage.class, drawPage);
            xDrawShape = UnoRuntime.queryInterface(XShape.class, drawShape);
            xDrawShape.setSize(new Size(width, height));
            xDrawShape.setPosition(new Point(x, y));
            xDrawPage.add(xDrawShape);

            XText xShapeText = UnoRuntime.queryInterface(XText.class, drawShape);
            XPropertySet xShapeProps = UnoRuntime.queryInterface(XPropertySet.class, drawShape);

            xShapeProps.setPropertyValue("FillColor", Integer.valueOf(col));

            com.sun.star.text.XTextCursor xTCursor = xShapeText.createTextCursor();
            com.sun.star.beans.XPropertySet xTCPS = UnoRuntime.queryInterface(com.sun.star.beans.XPropertySet.class,
                    xTCursor);
            xTCPS.setPropertyValue("CharHeight", 6.0f);
            xShapeText.insertString(xTCursor, text, false);
            com.sun.star.beans.XPropertySet xText = UnoRuntime.queryInterface(com.sun.star.beans.XPropertySet.class,
                    xShapeProps);

        } catch (java.lang.Exception e) {
            System.err.println("Couldn't create instance " + e);
            e.printStackTrace(System.err);
        }
        com.sun.star.beans.XPropertySet xSPS = UnoRuntime.queryInterface(com.sun.star.beans.XPropertySet.class,
                xDrawShape);
        return xDrawShape;
    }

    public static com.sun.star.drawing.XShape createRelation(com.sun.star.lang.XComponent xDocComp,
            com.sun.star.drawing.XShape start_shape, com.sun.star.drawing.XShape end_shape, String text,
            String from_max, String to_max, int x, int y, boolean same, int col) {
        com.sun.star.drawing.XShape xDrawShape = null;
        com.sun.star.frame.XDesktop xDesktop = null;
        com.sun.star.lang.XComponent xComponent = null;
        xDesktop = getDesktop();
        try {
            xComponent = xDesktop.getCurrentComponent();
            XDrawPagesSupplier xDrawPagesSupplier = (XDrawPagesSupplier) UnoRuntime
                    .queryInterface(XDrawPagesSupplier.class, xComponent);
            Object drawPages = xDrawPagesSupplier.getDrawPages();
            XIndexAccess xIndexedDrawPages = (XIndexAccess) UnoRuntime.queryInterface(XIndexAccess.class, drawPages);
            Object drawPage = xIndexedDrawPages.getByIndex(0);
            XMultiServiceFactory xDrawFactory = (XMultiServiceFactory) UnoRuntime
                    .queryInterface(XMultiServiceFactory.class, xComponent);
            // Object connector = xDrawFactory.createInstance(
            // "com.sun.star.drawing.ConnectorShape");
            XDrawPage xDrawPage = (XDrawPage) UnoRuntime.queryInterface(XDrawPage.class, drawPage);

            XShapes xShapes = (XShapes) UnoRuntime.queryInterface(XShapes.class, xDrawPage);
            XMultiServiceFactory xMsf = UnoRuntime.queryInterface(XMultiServiceFactory.class, xComponent);
            Object connector1 = xMsf.createInstance("com.sun.star.drawing.ConnectorShape");
            Object connector2 = xMsf.createInstance("com.sun.star.drawing.ConnectorShape");
            xShapes.add(UnoRuntime.queryInterface(XShape.class, connector1));
            xShapes.add(UnoRuntime.queryInterface(XShape.class, connector2));
            XPropertySet xConnector1PropSet = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class, connector1);
            XPropertySet xConnector2PropSet = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class, connector2);
            Object diamond = drawPolygon(xDrawPage, x, y, 8, 4, text);
            XText xShapeText = UnoRuntime.queryInterface(XText.class, diamond);
            xDrawShape = UnoRuntime.queryInterface(XShape.class, diamond);
            XPropertySet xShapeProps = UnoRuntime.queryInterface(XPropertySet.class, diamond);

            xShapeProps.setPropertyValue("FillColor", Integer.valueOf(col));

            com.sun.star.text.XTextCursor xTCursor = xShapeText.createTextCursor();
            com.sun.star.beans.XPropertySet xTCPS = UnoRuntime.queryInterface(com.sun.star.beans.XPropertySet.class,
                    xTCursor);
            xTCPS.setPropertyValue("CharHeight", 6.0f);
            xShapeText.insertString(xTCursor, text, false);

            com.sun.star.beans.XPropertySet xText = UnoRuntime.queryInterface(com.sun.star.beans.XPropertySet.class,
                    xShapeProps);
            if (same) {
                xConnector1PropSet.setPropertyValue("StartShape", diamond);
                xConnector1PropSet.setPropertyValue("EndShape", start_shape);
            } else {
                xConnector1PropSet.setPropertyValue("StartShape", diamond);
                xConnector1PropSet.setPropertyValue("EndShape", start_shape);
                xConnector2PropSet.setPropertyValue("StartShape", diamond);
                xConnector2PropSet.setPropertyValue("EndShape", end_shape);
            }

            // Connector1 Text

            XText xConnextor1Text = UnoRuntime.queryInterface(XText.class, connector1);
            XPropertySet LineText1 = UnoRuntime.queryInterface(XPropertySet.class, connector1);

            com.sun.star.text.XTextCursor xTCursorstart = xConnextor1Text.createTextCursor();
            com.sun.star.beans.XPropertySet xTCPSstart = UnoRuntime
                    .queryInterface(com.sun.star.beans.XPropertySet.class, xTCursorstart);
            xTCPSstart.setPropertyValue("CharHeight", 6.0f);
            xConnextor1Text.insertString(xTCursorstart, from_max, false);

            com.sun.star.beans.XPropertySet xLineText1 = UnoRuntime
                    .queryInterface(com.sun.star.beans.XPropertySet.class, LineText1);

            // Connecor2 Text

            XText xConnector2Text = UnoRuntime.queryInterface(XText.class, connector2);
            XPropertySet LineText2 = UnoRuntime.queryInterface(XPropertySet.class, connector2);

            com.sun.star.text.XTextCursor xTCursorend = xConnector2Text.createTextCursor();
            com.sun.star.beans.XPropertySet xTCPSend = UnoRuntime.queryInterface(com.sun.star.beans.XPropertySet.class,
                    xTCursorend);
            xTCPSend.setPropertyValue("CharHeight", 6.0f);
            xConnector2Text.insertString(xTCursorend, to_max, false);

            com.sun.star.beans.XPropertySet xLineText2 = UnoRuntime
                    .queryInterface(com.sun.star.beans.XPropertySet.class, LineText2);

            xDrawPage.add(xDrawShape);

        } catch (java.lang.Exception e) {
            System.err.println("Couldn't create instance " + e);
            e.printStackTrace(System.err);
        }

        return xDrawShape;
    }

    // ----------------------------------------------------------------------
    // --------------------------------------------------------------------------------------
    // -----------------------------------------------------------------------------------------
    // ---------------------------drunter
    // passt------------------------------------------------------------------------------------
    // ----------------------------------------------------------------------------------

    public static com.sun.star.frame.XDesktop getDesktop() {
        com.sun.star.frame.XDesktop xDesktop = null;
        com.sun.star.lang.XMultiComponentFactory xMCF = null;

        try {
            com.sun.star.uno.XComponentContext xContext = null;

            // get the remote office component context
            xContext = com.sun.star.comp.helper.Bootstrap.bootstrap();

            // get the remote office service manager
            xMCF = xContext.getServiceManager();
            if (xMCF != null) {
                System.out.println("Connected to a running office ...");

                Object oDesktop = xMCF.createInstanceWithContext("com.sun.star.frame.Desktop", xContext);
                xDesktop = (com.sun.star.frame.XDesktop) UnoRuntime.queryInterface(com.sun.star.frame.XDesktop.class,
                        oDesktop);
            } else
                System.out.println("Can't create a desktop. No connection, no remote office servicemanager available!");
        } catch (java.lang.Exception e) {
            e.printStackTrace(System.err);
            System.exit(1);
        }

        return xDesktop;
    }

    public static com.sun.star.lang.XComponent openDraw(com.sun.star.uno.XComponentContext xContext) {
        com.sun.star.frame.XComponentLoader xCLoader;
        com.sun.star.lang.XComponent xComp = null;

        try {
            // get the remote office service manager
            com.sun.star.lang.XMultiComponentFactory xMCF = xContext.getServiceManager();

            Object oDesktop = xMCF.createInstanceWithContext("com.sun.star.frame.Desktop", xContext);

            xCLoader = UnoRuntime.queryInterface(com.sun.star.frame.XComponentLoader.class, oDesktop);
            com.sun.star.beans.PropertyValue szEmptyArgs[] = new com.sun.star.beans.PropertyValue[0];
            String strDoc = "private:factory/sdraw";
            xComp = xCLoader.loadComponentFromURL(strDoc, "_blank", 0, szEmptyArgs);

        } catch (java.lang.Exception e) {
            System.err.println(" Exception " + e);
            e.printStackTrace(System.err);
        }

        return xComp;
    }

    public static int getCol(int r, int g, int b) {
        return r * 65536 + g * 256 + b;
    }

    public static ArrayList<ArrayList<String>> getPK(String inputfile) {

        ArrayList<ArrayList<String>> PKarray = new ArrayList<>();

        try {
            File inputFile = new File(inputfile);
            DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
            Document doc = dBuilder.parse(inputFile);
            doc.getDocumentElement().normalize();

            NodeList nList = doc.getElementsByTagName("ent");

            for (int temp = 0; temp < nList.getLength(); temp++) {
                ArrayList<String> nodes = new ArrayList<>();
                Node nNode = nList.item(temp);

                if (nNode.getNodeType() == Node.ELEMENT_NODE) {
                    Element eElement = (Element) nNode;
                    nodes.add(eElement.getAttribute("name"));
                    NodeList attrList = eElement.getElementsByTagName("attr");

                    for (int count = 0; count < attrList.getLength(); count++) {
                        Node node1 = attrList.item(count);

                        if (node1.getNodeType() == node1.ELEMENT_NODE) {
                            Element eElement1 = (Element) node1;
                            nodes.add(eElement1.getAttribute("prime"));
                        }
                    }
                }
                PKarray.add(nodes);

            }
        } catch (java.lang.Exception e) {
            e.printStackTrace();
        }

        return PKarray;
    }

    public static ArrayList<ArrayList<String>> get_ent(String inputfile) {

        ArrayList<ArrayList<String>> entarray = new ArrayList<>();

        try {
            File inputFile = new File(inputfile);
            DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
            Document doc = dBuilder.parse(inputFile);
            doc.getDocumentElement().normalize();

            NodeList nList = doc.getElementsByTagName("ent");

            for (int temp = 0; temp < nList.getLength(); temp++) {
                ArrayList<String> nodes = new ArrayList<>();
                Node nNode = nList.item(temp);

                if (nNode.getNodeType() == Node.ELEMENT_NODE) {
                    Element eElement = (Element) nNode;
                    nodes.add(eElement.getAttribute("name"));
                    NodeList attrList = eElement.getElementsByTagName("attr");

                    for (int count = 0; count < attrList.getLength(); count++) {
                        Node node1 = attrList.item(count);

                        if (node1.getNodeType() == node1.ELEMENT_NODE) {
                            Element eElement1 = (Element) node1;
                            nodes.add(eElement1.getAttribute("name"));
                        }
                    }
                }
                entarray.add(nodes);

            }
        } catch (java.lang.Exception e) {
            e.printStackTrace();
        }

        return entarray;
    }

    public static ArrayList<ArrayList<String>> getSuperSub(String inputfile) {

        ArrayList<ArrayList<String>> super_sub_array = new ArrayList<>();

        try {
            File inputFile = new File(inputfile);
            DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
            Document doc = dBuilder.parse(inputFile);
            doc.getDocumentElement().normalize();

            NodeList nList = doc.getElementsByTagName("rel");

            for (int temp = 0; temp < nList.getLength(); temp++) {
                ArrayList<String> nodes = new ArrayList<>();
                Node nNode = nList.item(temp);

                if (nNode.getNodeType() == Node.ELEMENT_NODE) {
                    Element eElement = (Element) nNode;
                    nodes.add(eElement.getAttribute("to"));
                    NodeList superlist = eElement.getElementsByTagName("super");

                    for (int count = 0; count < superlist.getLength(); count++) {
                        Node node1 = superlist.item(count);

                        if (node1.getNodeType() == node1.ELEMENT_NODE) {
                            Element eElement1 = (Element) node1;
                            nodes.add(eElement1.getAttribute("total"));
                            nodes.add(eElement1.getAttribute("disjoint"));
                            nodes.add(eElement1.getAttribute("ref"));
                        }
                    }

                    NodeList sublist = eElement.getElementsByTagName("sub");

                    for (int count = 0; count < sublist.getLength(); count++) {
                        Node node1 = sublist.item(count);

                        if (node1.getNodeType() == node1.ELEMENT_NODE) {
                            Element eElement1 = (Element) node1;
                            nodes.add(eElement1.getAttribute("ref"));
                        }
                    }
                }
                super_sub_array.add(nodes);

            }
        } catch (java.lang.Exception e) {
            e.printStackTrace();
        }

        return super_sub_array;

    }

    public static ArrayList<ArrayList<String>> get_rel_attr(String inputfile) {

        ArrayList<ArrayList<String>> rel_attr_array = new ArrayList<>();

        try {
            File inputFile = new File(inputfile);
            DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
            Document doc = dBuilder.parse(inputFile);
            doc.getDocumentElement().normalize();

            NodeList nList = doc.getElementsByTagName("rel");

            for (int temp = 0; temp < nList.getLength(); temp++) {
                ArrayList<String> nodes = new ArrayList<>();
                Node nNode = nList.item(temp);

                if (nNode.getNodeType() == Node.ELEMENT_NODE) {
                    Element eElement = (Element) nNode;
                    nodes.add(eElement.getAttribute("to"));
                    NodeList attrList = eElement.getElementsByTagName("attr");

                    for (int count = 0; count < attrList.getLength(); count++) {
                        Node node1 = attrList.item(count);

                        if (node1.getNodeType() == node1.ELEMENT_NODE) {
                            Element eElement1 = (Element) node1;
                            nodes.add(eElement1.getAttribute("name"));
                        }
                    }
                }
                rel_attr_array.add(nodes);

            }
        } catch (java.lang.Exception e) {
            e.printStackTrace();
        }

        return rel_attr_array;

    }

    public static ArrayList<ArrayList<String>> get_rel(String inputfile) {

        ArrayList<ArrayList<String>> entarray = new ArrayList<>();

        try {
            File inputFile = new File(inputfile);
            DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
            Document doc = dBuilder.parse(inputFile);
            doc.getDocumentElement().normalize();

            NodeList nList = doc.getElementsByTagName("rel");

            for (int temp = 0; temp < nList.getLength(); temp++) {
                ArrayList<String> nodes = new ArrayList<>();
                Node nNode = nList.item(temp);

                if (nNode.getNodeType() == Node.ELEMENT_NODE) {
                    Element eElement = (Element) nNode;
                    nodes.add(eElement.getAttribute("to"));
                    NodeList partList = eElement.getElementsByTagName("part");

                    for (int count = 0; count < partList.getLength(); count++) {
                        Node node1 = partList.item(count);

                        if (node1.getNodeType() == node1.ELEMENT_NODE) {
                            Element eElement1 = (Element) node1;
                            nodes.add(eElement1.getAttribute("ref"));
                            nodes.add(eElement1.getAttribute("max"));
                        }
                    }
                }
                entarray.add(nodes);
            }
        } catch (java.lang.Exception e) {
            e.printStackTrace();
        }

        return entarray;
    }

    public static XShape drawPolygon(XDrawPage slide, int x, int y, int radius, int nSides, String text) {
        XShape polygon = addShape(slide, "PolyPolygonShape", 0, 0, 0, 0, text);

        Point[] pts = genPolygonPoints(x, y, radius, nSides);
        Point[][] polys = new Point[][] { pts };
        setProperty(polygon, "PolyPolygon", polys);
        return polygon;
    }

    public static XShape addShape(XDrawPage slide, String shapeType, int x, int y, int width, int height, String text) {
        XShape shape = makeShape(shapeType, x, y, width, height, text);
        if (shape != null)
            slide.add(shape);
        return shape;
    }

    public static XShape makeShape(String shapeType, int x, int y, int width, int height, String text) {
        XShape shape = null;
        try {
            shape = createInstanceMSF(XShape.class, "com.sun.star.drawing." + shapeType);
            shape.setPosition(new Point(x * 100, y * 100));
            shape.setSize(new Size(width * 100, height * 100));
        } catch (java.lang.Exception e) {
            System.out.println("Unable to create shape: " + shapeType);
        }
        return shape;
    }

    public static <T> T createInstanceMSF(Class<T> aType, String serviceName) {
        com.sun.star.drawing.XShape xDrawShape = null;
        com.sun.star.frame.XDesktop xDesktop = null;
        com.sun.star.lang.XComponent xComponent = null;
        xDesktop = getDesktop();
        try {
            xComponent = xDesktop.getCurrentComponent();
            XDrawPagesSupplier xDrawPagesSupplier = (XDrawPagesSupplier) UnoRuntime
                    .queryInterface(XDrawPagesSupplier.class, xComponent);
            Object drawPages = xDrawPagesSupplier.getDrawPages();
            XIndexAccess xIndexedDrawPages = (XIndexAccess) UnoRuntime.queryInterface(XIndexAccess.class, drawPages);
            Object drawPage = xIndexedDrawPages.getByIndex(0);
            XMultiServiceFactory xDrawFactory = (XMultiServiceFactory) UnoRuntime
                    .queryInterface(XMultiServiceFactory.class, xComponent);

            if (xDrawFactory == null) {
                System.out.println("No document found");
                return null;
            }

            T interfaceObj = null;
            try {
                Object o = xDrawFactory.createInstance(serviceName);
                interfaceObj = qi(aType, o);
            } catch (java.lang.Exception e) {
                System.out.println("Couldn't create interface for \"" + serviceName + "\": " + e);
            }
            return interfaceObj;
        } catch (java.lang.Exception e) {
            System.out.println("test");
        }

        T interfaceObj = null;
        return interfaceObj;

    }

    private static Point[] genPolygonPoints(int x, int y, int radius, int nSides) {
        if (nSides < 3) {
            System.out.println("Too f   ew sides; must be 3 or more");
            nSides = 3;
        } else if (nSides > 30) {
            System.out.println("Too many sides; must be 30 or less");
            nSides = 30;
        }

        Point[] pts = new Point[nSides];
        double angleStep = Math.PI / nSides;
        for (int i = 0; i < nSides; i++) {
            pts[i] = new Point((int) Math.round(x * 100 + radius * 100 * Math.cos(i * 2 * angleStep)),
                    (int) Math.round(y * 100 + radius * 100 * Math.sin(i * 2 * angleStep)));
        }
        return pts;
    }

    public static <T> T qi(Class<T> aType, Object o) {
        return UnoRuntime.queryInterface(aType, o);
    }

    public static void setProperty(Object obj, String propName, Object value) {
        XPropertySet propSet = qi(XPropertySet.class, obj);
        setProperty(propSet, propName, value);
    }

    public static void setProperty(XPropertySet propSet, String propName, Object value) {
        if (propSet == null) {
            System.out.println("Property set is null; cannot set \"" + propName + "\"");
            return;
        }
        try {
            propSet.setPropertyValue(propName, value);
        } catch (com.sun.star.lang.IllegalArgumentException e) {
            System.out.println("Property \"" + propName + "\" argument is illegal");
        } catch (java.lang.Exception e) {
            System.out.println("Could not set property \"" + propName + "\": " + e);
        }
    }

}

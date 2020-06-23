#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logicalModell
from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from collections import defaultdict
import basex
import mySQL
import oracle
import SQLServer
import sqlite
import PostgreSQL
import rel


def dmlform(database, outputfile):
    table_count = 1
    row_count = 0
    root = Tk()
    root.title("Eingabeformular")
    listoflist = []
    listidx = 0
    # root.geometry('500x600')
    scroll = Scrollbar(root)
    scroll.grid(row=5, column=2, sticky=E)
    nb = ttk.Notebook(root)
    nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')
    frames = {}
    frame = 0
    for table in logicalModell.datenbank.tabellen:
        frames[frame] = ttk.Frame(nb)
        nb.add(frames[frame], text=str(table.uname))
        frame += 1
    pages = defaultdict(list)
    frame = 0
    for table in logicalModell.datenbank.tabellen:
        for column in table.columns:
            label = Label(frames[frame], text=str(column.uname) + " (" + str(column.type) + ")")
            label.grid(row=row_count)
            name = StringVar()
            pages[frame].append(Entry(frames[frame], textvariable=name))
            entry = Entry(frames[frame], textvariable=name)
            entry.grid(row=row_count, column=1)
            row_count += 1
        row_count += 1
        but_confirm = Button(frames[frame], text="Insert", command=lambda frame=frame: confirm(frame, pages, database, outputfile, listoflist, listidx))
        but_confirm.grid(row=row_count)
        row_count += 1
        if (database == 'basex'):
            but_send = Button(frames[frame], text="To Database",
                                 command=lambda frame=frame: send(database, outputfile))
            but_send.grid(row=row_count)
        row_count += 1
        listbox = Listbox(frames[frame], heigh=10, width=100)
        listbox.grid(row=row_count, columnspan=2)
        listoflist.append(listbox)
        row_count += 1
        frame += 1
    root.mainloop()

def confirm(count, pages, database, outputfile, listoflist, listidx):
    right = False
    for i in range(0, len(pages)):
        if (count == i):
            for j in range(0, len(pages[i])):
                if (pages[i][j].get() == ""):
                    right = False
                    break
                else:
                    right = True
            if (right == True):
                table = logicalModell.datenbank.tabellen[i]
                text = ""
                for col in range(0, len(table.columns)):
                    table.columns[col].data.append(pages[i][col].get())
                    text += pages[i][col].get() + "; "
                listoflist[listidx].insert(END, text)

                if database == 'basex':
                    basex.dmlgeneratefromform("test.xml", 1, table.name)
                if database == 'oracle':
                    oracle.dmlgenerate(outputfile, 1, False)
                if database == 'postgresql':
                    PostgreSQL.dmlgenerate(outputfile, 1, False)
                if database == 'sqlite':
                    sqlite.dmlgenerate(outputfile, 1, True)
                if database == 'mysql':
                    mySQL.dmlgenerate(outputfile, 1, True)
                if database == 'sqlserver':
                    SQLServer.dmlgenerate(outputfile, 1, True)
                if database == 'rel':
                    rel.dmlgenerate(outputfile, 1, False, True)
                if (database == 'sqlserver' or database == 'mysql' or database == 'sqlite' or database == 'rel'):
                    for col in range(0, len(table.columns)):
                        table.columns[col].data.clear()
            else:
                tkinter.messagebox.showinfo("Missing Values", "There are some columns which have no values!")

def send(database, outputfile):
    if database == 'basex':
        basex.toBaseX(outputfile)
    if database == 'oracle':
        oracle.dmlgenerate(outputfile, 1, False)
    if database == 'postgresql':
        PostgreSQL.dmlgenerate(outputfile, 1, False)
    if database == 'sqlite':
        sqlite.dmlgenerate(outputfile, 1, False)
    if database == 'mysql':
        mySQL.dmlgenerate(outputfile, 1, False)
    if database == 'sqlserver':
        SQLServer.dmlgenerate(outputfile, 1, False)




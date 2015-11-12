#*********************************************************************
# File    : GUImain.py
# Date    : 10/20/2015
# Author  : Allen Kirby
# Purpose : The main app for the GUI 
#*********************************************************************

from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
import tkinter.font as font
import locale

from Constants import printConstants as PC
from Constants import config
from Constants import commands
from GUI import TableHeader as TH
from GUI import TableRow as TR
from GUI import ScrollFrame as SF
import CheckbookTransaction as CBT
import Checkbook as CB

def setRowText(row, cbt):
    counter = 0
    for i in range(len(CBT.KEYS)):
        value = cbt.getValue(CBT.KEYS[i])
        if type(value) is float:
            value = locale.currency(value, grouping=config.THOUSAND_SEP)
        elif type(value) is str:
            value = value.capitalize()
        row.setText(i, value)

def populateNewEntry(frame):
    for i in range(len(PC.SIZELIST) - 1):
        ttk.Entry(frame, width=PC.SIZELIST[i]).grid(row=0, column=i)
    btn = ttk.Button(frame, text="Add New", command=addNewEntry)
    btn.grid(row=0, column=len(PC.SIZELIST))

    frame.grid_forget()

def addNewEntry():
    counter = 0
    cbt = CBT.CheckbookTransaction()
    for child in newEntryContainer.winfo_children():
        if type(child) is ttk.Entry:
            cbt.setValue(CBT.KEYS[counter], child.get())
            counter += 1
    checkbook.addSingleTrans(cbt)
    populateScrollFrame(registerFrame.frame, checkbook)
    newEntryContainer.grid_forget()

def showAdd():
    newEntryContainer.grid(sticky=(W))
    for child in newEntryContainer.winfo_children():
        if type(child) is ttk.Entry:
            child.delete(0, END)

def hideAdd():
    newEntryContainer.grid_forget()

def closeWindow():
    if checkbook.isEdited():
        save = messagebox.askyesno("Save Dialog", "Do you wish to save?")
        if save:
            checkbook.save()
    root.destroy()

def populateScrollFrame(frame, cb):
    # destroy children of frame
    for child in frame.winfo_children():
        child.destroy()

    # add header to frame
    header = TH.TableHeader(frame, CBT.KEYS, PC.SIZELIST)

    # Populate table
    totalRowCount = 1
    for j in range(len(checkbook.checkRegister)):
        row = TR.TableRow(frame, PC.SIZELIST)
        for i in range(len(PC.SIZELIST)):
            header.setGrid(i, i + 1, 1)
            setRowText(row, checkbook.checkRegister[j])
            row.setGrid(i, i + 1 , j + 2)
            totalRowCount += 1

    # add total line
    ttk.Label(frame, text="Total:", width=PC.SIZELIST[3], anchor=E).grid(row=totalRowCount, column=4)
    ttk.Label(frame, text=str(locale.currency(checkbook.getTotal(), grouping=config.THOUSAND_SEP))).grid(row=totalRowCount, column=5)


checkbook = CB.Checkbook()
checkbook.load(config.FILE_NAME)

# set main window
root = Tk()
root.title("Checkbook Program")
root.minsize(width=1024, height=768)
# root.configure(background="green")
root.columnconfigure(0, weight=75)
root.columnconfigure(1, weight=25)
root.rowconfigure(0, weight=80)
root.rowconfigure(1, weight=20)

# set the frame to contain the register
s1 = Style()
s1.configure('headerStyle.TFrame', background="red")
registerContainer = ttk.Frame(root, padding="3 3 3 3")
registerContainer.grid(column=0, row=0, sticky=(W, E, S, N))
registerContainer.columnconfigure(0, weight=1)
registerContainer.rowconfigure(0, weight=1)

# button container
s2 = Style()
s2.configure('regStyle.TFrame', background="blue")
buttonContainer = ttk.Frame(root, padding="3 3 3 3")
buttonContainer.grid(column=1, row=0, sticky=(E, W, N, S))
buttonContainer.columnconfigure(0, weight=1)

for row in range(len(commands.EXIT_LIST[:1])):
    currBtn = ttk.Button(buttonContainer, text=commands.EXIT_LIST[row],
        command=closeWindow)
    currBtn.grid(row=row, column=0)
    currBtn.columnconfigure(0, weight=1)
    currBtn.rowconfigure(0, weight=1)
currBtn = ttk.Button(buttonContainer, text="Add", command=showAdd)
currBtn.grid(row=1, column=0)
currBtn.columnconfigure(0, weight=1)
currBtn.rowconfigure(0, weight=1)
currBtn = ttk.Button(buttonContainer, text="Hide", command=hideAdd)
currBtn.grid(row=2, column=0)
currBtn.columnconfigure(0, weight=1)
currBtn.rowconfigure(0, weight=1)

# New entry row
s3 = Style()
s3.configure('entStyle.TFrame', background="yellow")
newEntryContainer = ttk.Frame(root, padding="3 3 3 3")
newEntryContainer.grid(row=1, column=0)
newEntryContainer.rowconfigure(0, weight=1)
populateNewEntry(newEntryContainer)

# Scroll Frame
registerFrame = SF.ScrollFrame(registerContainer)

# populate scroll window
populateScrollFrame(registerFrame.frame, checkbook)

# start display
root.mainloop()

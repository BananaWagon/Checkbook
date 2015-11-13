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
from functools import partial
import tkinter.font as font
import locale

from Constants import printConstants as PC
from Constants import config
from Constants import commands
from GUI import TableHeader as TH
from GUI import TableRow as TR
from GUI import ScrollFrame as SF
import GUIProcessingFunctions as GPF
import CheckbookTransaction as CBT
import Checkbook as CB

def addAndPopulate(addFrame, populateFrame, cb):
    """Adds new values to the specified checkbook and populates the scroll frame
    Parameters:
        addFrame (Frame)      : the frame to gather new values from
        populateFrame (Frame) : the frame to populate with the specified checkbook
        cb (Checkbook)        : the checkbook to add to and populate from
    """
    GPF.processAddCommand(addFrame, cb)
    GPF.populateScrollFrame(populateFrame, cb)

def populateNewEntry(addFrame, populateFrame):
    """Fills the specified add frame with Entries to be used to add to the checkbook
    Parameters:
        addFrame (Frame)      : the frame to place Entries in
        populateFrame (Frame) : the frame to populate with the specified checkbook
    """

    for child in addFrame.winfo_children():
        print("destroy child")
        child.destroy()

    for i in range(len(PC.SIZELIST) - 1):
        ttk.Entry(addFrame, width=PC.SIZELIST[i]).grid(row=0, column=i)
    btn = ttk.Button(addFrame, text="Add New", command=partial(addAndPopulate, 
        addFrame, populateFrame, checkbook))
    btn.grid(row=0, column=len(PC.SIZELIST))

    addFrame.grid_forget()

def hideAdd():
    """Hides the new entry frame"""
    newEntryContainer.grid_forget()

if __name__ == '__main__':
    # init checkbook obj
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
    root.protocol("WM_DELETE_WINDOW", partial(GPF.processExitCommand, root, checkbook))

    # set the frame to contain the register
    s1 = Style()
    s1.configure('headerStyle.TFrame', background="red")
    registerContainer = ttk.Frame(root, padding="3 3 3 3")
    registerContainer.grid(column=0, row=0, sticky=(W, E, S, N))
    registerContainer.columnconfigure(0, weight=1)
    registerContainer.rowconfigure(0, weight=1)

    # Scroll Frame
    registerFrame = SF.ScrollFrame(registerContainer)

    # New entry row
    s3 = Style()
    s3.configure('entStyle.TFrame', background="yellow")
    newEntryContainer = ttk.Frame(root, padding="3 3 3 3")
    newEntryContainer.grid(row=1, column=0)
    newEntryContainer.rowconfigure(0, weight=1)
    populateNewEntry(newEntryContainer, registerFrame.frame)

    # map frames to functions
    commDict = {}
    for comm in GPF.COMMAND_FUNCTIONS:
        if comm is not None:
            if "exit" in comm.__name__.lower():
                commDict[comm.__name__] = root
            elif "load" in comm.__name__.lower():
                commDict[comm.__name__] = registerFrame.frame
            else:
                commDict[comm.__name__] = newEntryContainer

    # button container
    s2 = Style()
    s2.configure('regStyle.TFrame', background="blue")
    buttonContainer = ttk.Frame(root, padding="3 3 3 3")
    buttonContainer.grid(column=1, row=0, sticky=(E, W, N, S))
    buttonContainer.columnconfigure(0, weight=1)

    # populate buttons
    for row in range(len(commands.GUI_COMMAND_LIST)):
        currBtn = ttk.Button(buttonContainer, text=commands.GUI_COMMAND_LIST[row].capitalize())
        if GPF.COMMAND_FUNCTIONS[row] is not None:
            currBtn.config(command=partial(GPF.COMMAND_FUNCTIONS[row], commDict[GPF.COMMAND_FUNCTIONS[row].__name__], checkbook))
        currBtn.grid(row=row, column=0)
        currBtn.columnconfigure(0, weight=1)
        currBtn.rowconfigure(0, weight=1)

    # populate scroll window
    GPF.populateScrollFrame(registerFrame.frame, checkbook)

    # start display
    root.mainloop()

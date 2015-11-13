from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
import locale

from GUI import TableHeader as TH
from GUI import TableRow as TR
from Constants import printConstants as PC
from Constants import config
import CheckbookTransaction as CBT
import checkbookReport as CR

def processExitCommand(frame, cb):
    """Asks the user to save and then closes the frame
    Parameters:
        frame (frame)  : the frame to close
        cb (Checkbook) : the checkbook to save
    """
    processSaveCommand(frame, cb)
    frame.destroy()

def processShowAddCommand(frame, cb):
    """Shows the specified frame and clears Entries
    Parameters:
        frame (Frame) : the frame to display
    """
    frame.grid(sticky=(W))
    for child in frame.winfo_children():
        if type(child) is ttk.Entry:
            child.delete(0, END)

def processAddCommand(frame, cb):
    """Adds values contained in the specified frame into the specified checkbook
    Parameters:
        frame (Frame)  : the frame to gather values from
        cb (Checkbook) : the checkbook to add to
    """
    counter = 0
    cbt = CBT.CheckbookTransaction()
    for child in frame.winfo_children():
        if type(child) is ttk.Entry:
            cbt.setValue(CBT.KEYS[counter], child.get())
            counter += 1
    cb.addSingleTrans(cbt)
    frame.grid_forget()

def processSaveCommand(frame, cb):
    if cb.isEdited():
        save = messagebox.askyesno("Save Dialog", "Do you wish to save?")
        if save:
            cb.save()

def processLoadCommand(frame, cb):
    processSaveCommand(frame, cb)
    fileName = filedialog.askopenfilename(filetypes=[("xml files", ".xml")])
    if fileName:
        cb.clear()
        cb.load(fileName)
        populateScrollFrame(frame, cb)

def processReportCommand(frame, cb):
    print("processReportCommand")

def processEditCommand(frame, cb):
    print("processEditCommand")

def populateScrollFrame(frame, cb):
    """Populates the specified frames with values from the specified checkbook
    Parameters:
        frame (Frame)  : the frame to populate
        cb (Checkbook) : the checkbook used to populate
    """
    # destroy children of frame
    for child in frame.winfo_children():
        child.destroy()

    # add header to frame
    header = TH.TableHeader(frame, CBT.KEYS, PC.SIZELIST)

    # Populate table
    totalRowCount = 1
    for j in range(len(cb.checkRegister)):
        row = TR.TableRow(frame, PC.SIZELIST)
        for i in range(len(PC.SIZELIST)):
            header.setGrid(i, i + 1, 1)
            setRowText(row, cb.checkRegister[j])
            row.setGrid(i, i + 1 , j + 2)
            totalRowCount += 1

    # add total line
    ttk.Label(frame, text="Total:", width=PC.SIZELIST[3], anchor=E).grid(row=totalRowCount, column=4)
    ttk.Label(frame, text=str(locale.currency(cb.getTotal(), 
        grouping=config.THOUSAND_SEP))).grid(row=totalRowCount, column=5)

def setRowText(row, cbt):
    """Populates the specified row with the values in the specified CheckbookTransaction
    Parameters:
        row (TableRow)             : the row to populate
        cbt (CheckbookTransaction) : the CheckbookTransaction to get the values from
    """
    counter = 0
    for i in range(len(CBT.KEYS)):
        value = cbt.getValue(CBT.KEYS[i])
        if type(value) is float:
            value = locale.currency(value, grouping=config.THOUSAND_SEP)
        elif type(value) is str:
            value = value.capitalize()
        row.setText(i, value)



COMMAND_FUNCTIONS = [processShowAddCommand, processEditCommand, processReportCommand, 
                     processLoadCommand, processSaveCommand, processExitCommand]

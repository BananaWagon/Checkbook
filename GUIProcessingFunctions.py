from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
from functools import partial
import locale

from GUI import TableHeader as TH
from GUI import TableRow as TR
from Constants import printConstants as PC
from Constants import config
import CheckbookTransaction as CBT
import checkbookReport as CR

month = 0

def ok(frame):
    """Processes the month dialog
    Parameters:
        frame (Frame) : the frame to gather the month data from
    """
    global month
    for elem in frame.winfo_children():
        if type(elem) is ttk.Entry:
            month = int(elem.get())
    frame.destroy()

def _displayReport(frame, repText):
    """Displays the given report text in the specified frame
    Parameters:
        frame (Frame) : the frame to display the text
        repText (str) : the text to display
    """
    for elem in frame.winfo_children():
        elem.destroy()
    ttk.Label(frame, text=repText).pack()
    ttk.Button(frame,text="Ok", command=partial(ok, frame)).pack()


def processMonthlyReport(frame, cr, index):
    """Handles gathering the data for the Monthly report
    Parameters:
        frame (Frame)        : the frame to display the text
        cr (CheckbookReport) : the report generator
        index (int)          : used to select the report method
    """
    global month
    newTop = Toplevel()
    newTop.transient(frame)
    ttk.Label(newTop, text="Choose the month:").pack(side=LEFT, padx=5, pady=5)
    ttk.Entry(newTop, width=10).pack(side=LEFT, padx=5, pady=5)
    ttk.Button(newTop, text="Ok", command=partial(ok, newTop)).pack(
        side=LEFT, padx=5, pady=5)
    newTop.winfo_children()[1].focus_set()
    newTop.wait_window(newTop)
    repMethod = CR.CheckbookReport.dispatcher[CR.REPORT_TYPES[index]]
    _displayReport(frame, repMethod(cr, month))

def processTotalReport(frame, cr, index):
    """Handles displaying the total report
    Parameters:
        frame (Frame)        : the frame to display the text
        cr (CheckbookReport) : the report generator
        index (int)          : used to select the report method
    """
    repMethod = CR.CheckbookReport.dispatcher[CR.REPORT_TYPES[index]]
    _displayReport(frame, repMethod(cr))

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

    frame.winfo_children()[0].focus_set()

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
    cr = CR.CheckbookReport(cb)
    top = Toplevel()
    top.transient(frame)
    repTypeFrame = ttk.Frame(top)
    ttk.Label(repTypeFrame, text="Pick your report type:").pack(padx=5, pady=10)
    repTypeFrame.pack()
    for i in range(len(CR.REPORT_TYPES)):
        repMethod = CR.CheckbookReport.dispatcher[CR.REPORT_TYPES[i]]
        ttk.Button(repTypeFrame, text=CR.REPORT_TYPES[i],
            command=partial(REPORT_PROCESSORS[i], top, cr, i)).pack(side=LEFT, padx=5)
    top.geometry("+500+1")

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

REPORT_PROCESSORS = [processMonthlyReport, processTotalReport]

from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

class TableRow:
    """A class that represents a row in a table.
    Attribute:
        tableRow (list)     : a list of tkinter Entries
    """
    def __init__(self, parentFrame, sizeList):
        """Create a content row with the specified sizes
        Parameters:
            parentFrame (Frame) : a tkinter frame to hold the header
            sizeList (list)     : a list of ints to be the size of the entries
        """
        self.tableRow = []
        for i in range(len(sizeList)):
            currentEntry = ttk.Entry(parentFrame, width=sizeList[i], 
                state="readonly")
            self.tableRow.append(currentEntry)

    def setGrid(self, elemIndex, colNum, rowNum):
        """Sets the grid location for the specified element index
        Parameters:
            elemIndex (int) : the index of the element to edit
            colNum (int)    : the column number for the element
            rowNum (int)    : the row number for the element
        """
        self.tableRow[elemIndex].grid(column=colNum, row=rowNum)

    def setText(self, elemIndex, text):
        """Set the text for the specified element index
        Parameters:
            elemIndex (int) : the index of the element to edit
            text (string)   : the text to be displayed in the element
        """
        self.tableRow[elemIndex].configure(state="normal")
        self.tableRow[elemIndex].delete(0, END)
        self.tableRow[elemIndex].insert(0, text)
        self.tableRow[elemIndex].configure(state="readonly")

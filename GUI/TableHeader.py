from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

class TableHeader():
    """A class that represents the header for a table
    Attribute:
        headerRow (list)    : a list of tkinter Labels
    """
    def __init__(self, parentFrame, textList, sizeList):
        """Create the header row with the text in the given list.
        NOTE: The given lists should be the same size
        Parameters:
            parentFrame (Frame) : a tkinter frame to hold the header
            textList (list)     : a list of strings to be the text in the header
            sizeList (list)     : a list of ints to be the size of the labels
        """
        self.headerRow = []
        for i in range(len(textList)):
            currentLabel = ttk.Label(parentFrame, anchor="center", 
                text=textList[i], width=sizeList[i])
            self.headerRow.append(currentLabel)

    def setGrid(self, elemIndex, colNum, rowNum):
        """Sets the grid location for the specified element index
        Parameters:
            elemIndex (int) : the index of the element to edit
            colNum (int)    : the column number for the element
            rowNum (int)    : the row number for the element
        """
        self.headerRow[elemIndex].grid(column=colNum, row=rowNum)

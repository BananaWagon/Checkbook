from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

class TableHeader():
	"""A class that represents the header for a table"""
	def __init__(self, parentFrame, textList, sizeList):
		"""Create the header row with the text in the given list.
		NOTE: The given lists should be the same size
		Parameter:
			parentFrame (Frame) : a tkinter frame to hold the header
			textList (list)     : a list of strings to be the text in the header
			sizeList (list)     : a list of ints to be the size of the labels
		"""
		self.headerRow = []

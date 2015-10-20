#*********************************************************************
# File    : GUImain.py
# Date    : 10/20/2015
# Author  : Allen Kirby
# Purpose : The main app for the GUI 
#*********************************************************************




from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.font as font

from Constants import printConstants as PC
from Constants import config
import CheckbookTransaction as CBT
import Checkbook as CB

checkbook = CB.Checkbook()
checkbook.load(config.FILE_NAME)

# set window
root = Tk()
root.title("Checkbook Program")
root.minsize(width=768, height=432)

# font
# font.nametofont('TkDefaultFont').configure(size=12)
# myFont = font.Font(weight='normal')

# set content frame
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# s1 = Style()
# s1.configure('headerStyle.TFrame', background="red")
# header = ttk.Frame(mainframe, padding="3 1 3 1", style="headerStyle.TFrame",
#                    width=sum(PC.SIZELIST))
# header.grid(column=0, row=1, sticky=(W))
# header.columnconfigure(0, weight=1)
# header.rowconfigure(0, weight=1)

s2 = Style()
s2.configure('registerStyle.TFrame', background="blue")
register = ttk.Frame(mainframe, padding="3 1 3 1", style="registerStyle.TFrame")
register.grid(column=0, row=2, columnspan=len(PC.SIZELIST))
register.columnconfigure(0, weight=1)
register.rowconfigure(0, weight=1)


for j in range(len(checkbook.checkRegister)):
    for i in range(len(PC.SIZELIST)):
        formatString = "{:*^" + str(PC.SIZELIST[i]) + "}"
        ttk.Label(register, anchor="center", text=CBT.KEYS[i],
                  width=PC.SIZELIST[i]).grid(column=i + 1, row=1) # 
        ttk.Entry(register, width=PC.SIZELIST[i]).grid(column=i + 1, row=j+2)

# start display
root.mainloop()

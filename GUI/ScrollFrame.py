import tkinter as tk

class ScrollFrame(tk.Frame):
    """A class that creates a vertiacl scrolling frame
    Attributes:
        canvas (Canvas) : a canvas that will hold the frame 
                            and the scrollbar
        frame (Frame)   : the frame that will hold contents
        vsb (Scrollbar) : the scrollbar for the canvas
    """
    def __init__(self, root):
        """Creates a ScrollFrame object to be contained within the 
        specified root
        Parameter:
            root (Tk obj) : a Tkinter object that can contain frames
        """
        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(root, borderwidth=0)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(root, orient="vertical", 
            command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, 
            anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

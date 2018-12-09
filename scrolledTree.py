try:
    import tkinter as tk
    from tkinter import ttk
except: # Python 2.x
    import Tkinter as tk
    import Ttk as ttk


class scrolledTree(tk.Frame):

    def __init__(self, master=None, **kw):
        tk.Frame.__init__(self, master)

        self.frameOne = tk.Frame(self)

        self.tree = ttk.Treeview(self.frameOne, **kw)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.scrollX = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.scrollY = tk.Scrollbar(self.frameOne, orient=tk.VERTICAL, command=self.tree.yview)

        self.tree.config(xscrollcommand=self.scrollX.set)
        self.tree.config(yscrollcommand=self.scrollY.set)

        self.scrollY.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.frameOne.pack(fill=tk.BOTH, expand=True)
        
        self.scrollX.pack(fill=tk.BOTH)

try:
    import tkinter as tk
    from tkinter import tix
    from tkinter import messagebox as msgBox
except: # Python 2.x
    import Tkinter as tk
    import Tix as tix
    import tkMessageBox as msgBox

import statusBar

statusTxts = statusBar.getTxts(["toolBar.py"])


class toolBar(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.master = master

        self._loadImgs()
        self._createWidgets()

    def _loadImgs(self):
        self.openImg = tk.PhotoImage(file="data/open.png")
        self.openURLImg = tk.PhotoImage(file="data/openURL.png")
        self.saveImg = tk.PhotoImage(file="data/save.png")
        self.closeImg = tk.PhotoImage(file="data/close.png")
        self.dirImg = tk.PhotoImage(file="data/folder.gif")
        self.regImg = tk.PhotoImage(file="data/reg.png")
        self.exitImg = tk.PhotoImage(file="data/exit.png")

    def _createWidgets(self):
        self.balloon = tix.Balloon(self)
        
        self.openBtn = tk.Button(self, image=self.openImg, command=lambda: self.do("openFile"))
        self.openURL = tk.Button(self, image=self.openURLImg, command=lambda: self.do("openURL"))
        self.saveBtn = tk.Button(self, image=self.saveImg, command=lambda: self.do("save"))
        self.closeBtn = tk.Button(self, image=self.closeImg, command=lambda: self.do("onClose"))
        self.pathBtn = tk.Button(self, image=self.dirImg, command=lambda: self.do("pathBrowser"))
        self.regBtn = tk.Button(self, image=self.regImg, command=lambda: self.do("regBrowser"),
                                state=tk.NORMAL if self.master.regAvailable else tk.DISABLED)
        self.exitBtn = tk.Button(self, image=self.exitImg, command=lambda: self.do("onExit"))

        self.openBtn.pack(side=tk.LEFT)
        self.openURL.pack(side=tk.LEFT)
        self.saveBtn.pack(side=tk.LEFT)
        self.closeBtn.pack(side=tk.LEFT)
        self.pathBtn.pack(side=tk.LEFT)
        self.regBtn.pack(side=tk.LEFT)
        self.exitBtn.pack(side=tk.LEFT)

        statusBar.bindBalloon(self.balloon, statusTxts, self.__dict__)

    def do(self, cmd, *args, **kwargs):
        if hasattr(self.master, cmd):
            return getattr(self.master, cmd)(*args, **kwargs)
        else:
            msgBox.showerror("yangEdit Error", "Function '{}' not available.". \
                             format(cmd), master=self.master)

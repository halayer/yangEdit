try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox as msgBox
    from tkinter import filedialog as fileDialog
    from tkinter import simpledialog as dialog
    from tkinter import tix
    from tkinter import scrolledtext as tkst
except: # Python 2.x
    import Tkinter as tk
    import Ttk as ttk
    import tkMessageBox as msgBox
    import tkFileDialog as fileDialog
    import Tix as tix
    import ScrolledText as tkst
    import tkSimpleDialog as dialog

import os
import sys
import json
import editFrame
import settings
import refTypes
import pathBrowser
import toolBar
from urllib.request import urlopen
import traceback
import notebook
import updater
import dict2robot

getExc = traceback.format_exc

regAvailable = True

if sys.platform != "win32":
    regAvailable = False
else:
    import regBrowser


class yangEditApp(tix.Tk):

    def __init__(self, toOpen=list()):
        tix.Tk.__init__(self)
        self.title("yangEdit")
        self.iconbitmap("data/icon.ico")
        self.geometry("600x600")

        self.protocol("WM_DELETE_WINDOW", self.onExit)

        self.fileTypes = (("JSON files", ".json"), ("All files", "*.*"))
        self.tabDict = refTypes.refDict({})
        self.jsonData = None
        self.toOpen = list(toOpen)
        self.fileDict = dict()
        self.widgets = dict()
        self.regAvailable = regAvailable

        self._loadImgs()
        self._createWidgets()

        self.loadSession()

    def onClose(self, event=None, index=None): # 'event' is not used
        if not index:
            try:
                index = self.tabView.index(self.tabView.select())
            except:
                return

        del self.tabDict[self.tabView.tab(index, "text")]
        
        try:
            del self.fileDict[index]
        except:
            msgBox.showerror("yangEdit", getExc(), master=self)

            return

        self.tabView.forget(index)

    def loadSession(self, sessionFile="data/JSON/lastSession.json"):
        with open(sessionFile) as file:
            try:
                data = json.loads(file.read())
            except:
                msgBox.showerror("yangEdit", "Can't restore last session.")
                return

        for file in data["files"]:
            if os.path.isfile(file):
                self._createEditFrame(file)
            else:
                msgBox.showerror("yangEdit", f"The file {file} doesnt " \
                                 "exists anymore.")

        if len(self.tabView.tabs()) >= data["sel"] + 1:
            self.tabView.select(data["sel"])

        for file in self.toOpen:
            self._createEditFrame(file)

    def onExit(self, sessionFile="data/JSON/lastSession.json"):
        data = {"files": list(), "sel": int()}

        data["files"] = list(self.fileDict.values())

        try:
            data["sel"] = self.tabView.index(self.tabView.select())
        except tk.TclError:
            data["sel"] = 0

        with open(sessionFile, "w") as file:
            file.write(json.dumps(data, indent=4))

        self.destroy()

    def update(self, event=None): # 'event' is not used
        sel = self.tabView.select()
        
        try:
            self.tabDict[self.tabView.tab(sel, "text")].update()
        except:
            return

    def openFile(self):
        fileName = fileDialog.askopenfilename(filetypes=self.fileTypes,
                                              title="Choose a file to open.")

        if not fileName:
            return

        self._createEditFrame(fileName)

    def openURL(self):
        url = dialog.askstring("yangEdit", "Open the URL you want to open:",
                               parent=self)

        if not url:
            return

        try:
            data = json.loads(urlopen(url).read().decode())
        except:
            msgBox.showerror("Error opening the URL.", getExc(),
                             master=self)

            return

        self._createEditFrame(url, data, True)

    def _createEditFrame(self, file=None, data=None, url=False):
        if not url:
            fileName = os.path.split(file)[1]
        else:
            fileName = file

        if fileName in self.tabDict:
            d = self.fileDict.copy()
            d = {v: k for k, v in d.items()}

            self.tabView.select(d[fileName])

            return
        
        frame = editFrame.editFrame(file, data, self.tabView)
        self.tabDict.update({fileName: frame})

        h = self.tabView.insert(tk.END, frame, text=fileName)

        self.fileDict.update({self.tabView.index(tk.END) - 1: fileName})

        self.tabView.select(self.tabView.index(tk.END) - 1)

        frame.focus_set()

    def _loadImgs(self):
        self.closeImg = tk.PhotoImage(file="data/close.png")
        self.triImg = tk.PhotoImage(file="data/triangle.png")

        self.openImg = tk.PhotoImage(file="data/open.png")
        self.openURLImg = tk.PhotoImage(file="data/openURL.png")
        self.saveImg = tk.PhotoImage(file="data/save.png")

        self.dirImg = tk.PhotoImage(file="data/folder.gif")
        self.regImg = tk.PhotoImage(file="data/reg.png")

    def save(self, event=None): # 'event' is not used
        sel = self.tabView.select()

        if not sel: return

        try:
            self.tabDict[self.tabView.tab(sel, "text")].save()
        except:
            return
        
    def search(self):
        sel = self.tabView.select()

        if not sel: return

        try:
            self.tabDict[self.tabView.tab(sel, "text")].search()
        except:
            return

    def pathBrowser(self):
        path = fileDialog.askdirectory(title="Select a directory")

        if os.path.isdir(path):
            root = tk.Toplevel(self)
            root.title("Path Browser")
            root.iconbitmap("data/folder.ico")

            pB = pathBrowser.pathBrowser(root, path, self._createEditFrame)
            pB.pack(expand=True, fill=tk.BOTH)

            root.mainloop()

    def changeTab(self, event=None): # 'event' is not used
        try:
            tab = self.tabView.select()
            file = self.tabView.tab(tab, "text")

            self.title("yangEdit [{}]".format(file))
        except:
            self.title("yangEdit")

    def regBrowser(self):
        root = tk.Toplevel(self)
        root.title("Registry Browser")
        root.iconbitmap("data/reg.ico")

        frame = regBrowser.regBrowser(root)
        frame.pack(expand=True, fill=tk.BOTH)

        root.mainloop()

    def data2Dict(self):
        def copyToClip():
            root.clipboard_clear()
            root.clipboard_append(data)
            
        sel = self.tabView.select()
        
        try:
            data = json.dumps(
                self.tabDict[self.tabView.tab(sel, "text")].jsonObj,
                indent=4
            )
        except:
            return

        root = tk.Toplevel(self)
        root.title("data2dict")
        root.iconbitmap("data/icon.ico")

        st = tkst.ScrolledText(root)

        st.insert(tk.END, data)
        st.pack(fill=tk.BOTH,expand=True)

        copyBtn = ttk.Button(root, text="Copy",
                             command=copyToClip)
        copyBtn.pack(fill=tk.BOTH)

    def robotSnippet(self):
        def copyToClip():
            root.clipboard_clear()
            root.clipboard_append(data)
            
        sel = self.tabView.select()
        
        try:
            data = json.dumps(
                self.tabDict[self.tabView.tab(sel, "text")].jsonObj,
                indent=4
            )
        except:
            return

        data = dict2robot.dict2robot(data)

        root = tk.Toplevel(self)
        root.title("data2dict")
        root.iconbitmap("data/icon.ico")

        st = tkst.ScrolledText(root)

        st.insert(tk.END, data)
        st.pack(fill=tk.BOTH,expand=True)

        copyBtn = ttk.Button(root, text="Copy",
                             command=copyToClip)
        copyBtn.pack(fill=tk.BOTH)
        
    def _tabMenu(self, event):
        ID = self.tabView.identify(event.x, event.y)

        if ID.upper() == "LABEL":
            menu = tk.Menu(self.tabView, tearoff=False)
            index = self.tabView.index("@%d,%d" % (event.x, event.y))

            menu.add_command(label="Close", command=
                             lambda: self.onClose(index=index),
                             image=self.closeImg, compound=tk.LEFT)

            menu.tk_popup(event.x_root, event.y_root)

    def _createMenu(self):
        self.menu = tk.Menu(self, tearoff=False)

        self.fileMenu = tk.Menu(self.menu, tearoff=False)

        self.fileMenu.add_command(label="Open", command=self.openFile,
                                  image=self.openImg, compound=tk.LEFT,
                                  underline=0)
        self.fileMenu.add_command(label="Open from URL", command=self.openURL,
                                  image=self.openURLImg, compound=tk.LEFT,
                                  underline=10)
        self.fileMenu.add_command(label="Save", command=self.save,
                                  image=self.saveImg, compound=tk.LEFT,
                                  underline=0)
        self.fileMenu.add_separator()

        self.fileMenu.add_command(label="Exit", command=self.destroy,
                                  image=self.triImg, compound=tk.LEFT)

        self.editMenu = tk.Menu(self.menu, tearoff=False)

        self.editMenu.add_command(label="Search", command=self.search,
                                  image=self.triImg, compound=tk.LEFT)
        
        self.optMenu = settings.optMenu(self.menu, self.tabDict)

        self.extraMenu = tk.Menu(self.menu, tearoff=False)

        self.extraMenu.add_command(label="Data2Dict", command=self.data2Dict,
                                   image=self.triImg, compound=tk.LEFT,
                                   underline=0)
        self.extraMenu.add_command(label="Path Browser", command=self.pathBrowser,
                                   image=self.dirImg, compound=tk.LEFT,
                                   underline=0)
        self.extraMenu.add_command(label="Registry Browser", command=self.regBrowser,
                                   state=tk.DISABLED if not regAvailable else tk.NORMAL,
                                   image=self.regImg, compound=tk.LEFT,
                                   underline=0)
        self.extraMenu.add_command(label="Robot Snippet", command=self.robotSnippet)

        self.menu.add_cascade(label="File", menu=self.fileMenu)
        self.menu.add_cascade(label="Edit", menu=self.editMenu)
        self.menu.add_cascade(label="Extras", menu=self.extraMenu)
        self.menu.add_cascade(label="Options", menu=self.optMenu)

        self.config(menu=self.menu)

    def _bindings(self):
        self.bind("<Control-w>", self.onClose)
        self.bind("<Control-s>", self.save)
        self.bind("<F5>", self.update)
        self.bind("<Control-o>", lambda i: self.openFile())
        self.bind("<Control-u>", lambda i: self.openURL())
        self.tabView.bind("<Button-3>", self._tabMenu)
        self.bind("<Control-d>", lambda i: self.data2Dict())
        self.bind("<Control-p>", lambda i: self.pathBrowser())
        self.bind("<Control-r>", lambda i: self.regBrowser())
        self.bind("<Control-f>", lambda i: self.search())

    def _createWidgets(self):
        self.toolBar = toolBar.toolBar(self)
        self.toolBar.pack(fill=tk.Y, anchor=tk.W)
        
        self.tabView = notebook.customNotebook(self)
        self.tabView.pack(fill=tk.BOTH, expand=True)

        self.tabView.bind("<<NotebookTabChanged>>", self.changeTab)
        self.tabView.bind("<<NotebookTabClosed>>", self.onClose)

        self._createMenu()
        self._bindings()


if __name__ == "__main__":
    app = yangEditApp(sys.argv[1:])

    try:
        import getpass

        if getpass.getuser() == "Henning":
            with open("TODO.txt") as file:
                msgBox.showinfo("TODO list", file.read(), master=app)
    except:
        pass

    updater.main(app)
    
    app.mainloop()

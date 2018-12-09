import sys

if sys.platform != "win32":
    quit()

try:
    import winreg
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox as msgBox
except: # Python 2.x
    import _winreg as winreg
    import Tkinter as tk
    import Ttk as ttk
    import tkMessageBox as msgBox

import regTools


class regBrowser(tk.LabelFrame):

    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master, text="Registry Browser")

        self.roots = {"HKCR": "HKEY_CLASSES_ROOT", "HKCU": "HKEY_CURRENT_USER",
                      "HKLM": "HKEY_LOCAL_MACHINE", "HKU": "HKEY_USERS",
                      "HKCC": "HKEY_CURRENT_CONFIG"}

        self._loadImgs()
        self._createWidgets()
        self._createRoots()

    def _loadImgs(self):
        self.dirImg = tk.PhotoImage(file="data/folder.gif")

    def _createWidgets(self):
        self.dataCols = ("key", "subKey", "valueNum", "type")
##        msgBox.showerror("Registry Browser", "NotImplementedError", master=self)
##        
##        self.label = tk.Label(self, text="TODO: Complete registry browser")
##        self.label.pack()

        self.tree = ttk.Treeview(self, columns=self.dataCols,
                                 displaycolumns="")

        self.tree.heading("#0", text="Registry Structure")
        
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<<TreeviewOpen>>", self._updateTree)

        self.focus_set()

    def _permError(self, msg, title="Registry Browser"):
        msgBox.showerror(title, msg, master=self)

    def _createRoots(self):
        for k, v in self.roots.items():
            setattr(self, k, self.tree.insert("", tk.END, text=v,
                                              values=[v, "", -1, "key"],
                                              image=self.dirImg))

            self.tree.insert(getattr(self, k), tk.END, text="dummy")

    def _insert(self, parent, regKey, key, subKey):
        if regTools.hasValues(regKey) or regTools.hasSubKeys(regKey):
            for _key in regTools.getKeys(regKey):
                _parent = self.tree.insert(parent, tk.END, text=_key,
                                           values=[key, subKey + "\\" + _key, -1,
                                                   "key"],
                                           image=self.dirImg)
                
                if not subKey:
                    newKey = winreg.OpenKey(key, _key)
                else:
                    newKey = winreg.OpenKey(int(key), subKey + "\\" + _key)

                if regTools.hasValues(newKey) or regTools.hasSubKeys(newKey):
                    self.tree.insert(_parent, tk.END, text="dummy")

            for i, item in enumerate(regTools.getValues(regKey).items()):
                _parent = self.tree.insert(parent, tk.END, text=item[0],
                                           values=[key, subKey, i, "valueName"])

                self.tree.insert(_parent, tk.END, text=item[1],
                                 values=[key, subKey, i, "value"])

    def _updateTree(self, event):
        sel = self.tree.focus()

        try:
            topChild = self.tree.get_children(sel)[0]
        except:
            return

        if self.tree.item(topChild, option="text") == "dummy":
            self.tree.delete(topChild)

            key = self.tree.set(sel, "key")
            subKey = self.tree.set(sel, "subKey")

            print(key, subKey)

            if len(subKey) >= 1:
                if subKey[0] == "\\":
                    subKey = subKey[1:]

            print(key, subKey)

            if hasattr(winreg, key):
                regKey = winreg.OpenKey(getattr(winreg, key), subKey)
            else:
                regKey = winreg.OpenKey(int(key), subKey)

            if hasattr(winreg, key):
                self._insert(sel, regKey, getattr(winreg, key), subKey)
            else:
                self._insert(sel, regKey, key, subKey)

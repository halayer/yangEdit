try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox as msgBox
    from tkinter import simpledialog as simpleDialog
except: # Python 2.x
    import Tkinter as tk
    import ttk
    import tkMessageBox as msgBox
    import tkSimpleDialog as simpleDialog

import os
import shutil
import imgViewer

KB = 1024.0
MB = KB * KB
GB = MB * KB


class pathBrowser(tk.LabelFrame):

    def __init__(self, master=None, path=None, onFileClick=None):
        tk.LabelFrame.__init__(self, master, text="Path Browser")

        if path is None:
            path = os.getcwd()

        self.path = path.replace("\\", "/")
        self.imgDict = {}
        self.onFileClick = onFileClick

        self._loadImgs()
        self._createWidgets()

    def _loadImgs(self):
        self.dirImg = tk.PhotoImage(file="data/folder.gif")
        self.pyImg = tk.PhotoImage(file="data/python.gif")
        self.jsonImg = tk.PhotoImage(file="data/json.png")
        self.cImg = tk.PhotoImage(file="data/c.png")
        self.cppImg = tk.PhotoImage(file="data/cpp.png")
        self.pydImg = tk.PhotoImage(file="data/pyd.png")
        self.txtImg = tk.PhotoImage(file="data/txt.png")
        self.exeImg = tk.PhotoImage(file="data/exe.png")
        self.fileImg = tk.PhotoImage(file="data/file.png")
        self.dllImg = tk.PhotoImage(file="data/dll.png")

        self.triImg = tk.PhotoImage(file="data/triangle.png")

        self.imgDict.update({".PY": self.pyImg, ".JSON": self.jsonImg,
                             ".C": self.cImg, ".CPP": self.cppImg,
                             ".PYD": self.pydImg, ".TXT": self.txtImg,
                             ".EXE": self.exeImg, ".DLL": self.dllImg,
                             ".SYS": self.dllImg})

    def _createWidgets(self):
        self.dataCols = ("fullPath", "type", "size")

        xFrame = tk.Frame(self, relief=tk.FLAT)
        mainFrame = tk.Frame(self, relief=tk.FLAT)
        
        self.tree = ttk.Treeview(mainFrame, columns=self.dataCols,
                                 displaycolumns="size")

        scrollY = ttk.Scrollbar(mainFrame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollX = ttk.Scrollbar(xFrame, orient=tk.HORIZONTAL, command=self.tree.xview)

        self.tree.heading("#0", text="Directory Structure", anchor=tk.W)
        self.tree.heading("size", text="File Size", anchor=tk.W)

        self.tree.config(yscroll=scrollY.set)
        self.tree.config(xscroll=scrollX.set)

        self.tree.column("size", stretch=False, width=70)
        
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollY.pack(fill=tk.Y, side=tk.LEFT)
        scrollX.pack(fill=tk.X)

        mainFrame.pack(fill=tk.BOTH, expand=True)
        xFrame.pack(fill=tk.X)

        self.tree.bind("<<TreeviewOpen>>", self._updateTree)
        self.tree.bind("<Button-3>", self._openMenu)

        self._createRoot()

    def _permError(self, path, title="Path Browser"):
        msgBox.showerror(title, f"Access denied: {path}", master=self)

    def _createRoot(self):
        parent = self.parent = self.tree.insert("", tk.END, text=self.path,
                                                values=[self.path, "dir"],
                                                image=self.dirImg)
        try:
            self._insert(parent, self.path, os.listdir(self.path))
        except PermissionError:
            self._permError(self.path)

    def _insert(self, parent, fullPath, children):
        for child in children:
            cPath = os.path.join(fullPath, child).replace("\\", "/")

            if os.path.isdir(cPath):
                cid = self.tree.insert(parent, tk.END, text=child,
                                       values=[cPath, "dir"],
                                       image=self.dirImg)

                isEmpty = False

                try:
                    if len(os.listdir(cPath)) == 0:
                        isEmpty = True
                except:
                    pass

                if not isEmpty:
                    self.tree.insert(cid, tk.END, text="dummy")
            else:
                size = self._formatSize(os.stat(cPath).st_size)
                ext = os.path.splitext(child)[1].upper()
                img = None
                
                for k, v in self.imgDict.items():
                    if ext == k:
                        img = v

                        break

                if img:
                    self.tree.insert(parent, tk.END, text=child,
                                     values=[cPath, "file", size],
                                     image=img)
                else:
                    self.tree.insert(parent, tk.END, text=child,
                                     values=[cPath, "file", size],
                                     image=self.fileImg)

    def _formatSize(self, size):
        if size >= GB:
            return '{:,.1f} GB'.format(size / GB)
        if size >= MB:
            return '{:,.1f} MB'.format(size / MB)
        if size >= KB:
            return '{:,.1f} KB'.format(size / KB)
        return '{} Bytes'.format(size)

    def _updateTree(self, event=None): # 'event' is unused
        nodeID = self.tree.focus()

        if self.tree.parent(nodeID):
            try:
                topChild = self.tree.get_children(nodeID)[0]
            except:
                topChild = None
                
            if topChild:
                if self.tree.item(topChild, option="text") == "dummy":
                    self.tree.delete(topChild)
                    path = self.tree.set(nodeID, "fullPath")

                    try:
                        self._insert(nodeID, path, os.listdir(path))
                    except PermissionError:
                        self._permError(path)
            else:
                if self.onFileClick:
                    self.onFileClick(self.tree.set(nodeID, "fullPath"))

    def rename(self, path, item):
        parentDir, fileName = os.path.split(path)

        newFileName = simpleDialog.askstring("Path Browser", "Type the new name:")

        os.rename(parentDir + os.sep + fileName,
                  parentDir + os.sep + newFileName)

        self.tree.set(item, "fullPath", parentDir + os.sep + newFileName)
        self.tree.item(item, text=newFileName)

        self.focus_set()

    def delete(self, path, item):
        quest = msgBox.askyesno("Path Browser", "Do you really want to delete" \
                                f" {path}?", master=self)

        self.focus_set()

        if not quest:
            return

        if os.path.isdir(path):
            try:
                shutil.rmtree(path)
            except Exception as e:
                msgBox.showerror("Path Browser", f"Error:\n{e}", master=self)
                return

            if path == self.path:
                self.destroy()

                if self.master.title() == "Path Browser":
                    self.master.destroy()
            else:
                self.tree.delete(item)
        else:
            os.unlink(path)

            self.tree.delete(item)

        self.focus_set()

    def new(self, path, item):
        fullPath = self.tree.item(item)["values"][0]

        if os.path.isdir(fullPath):
            treeMaster = item
        else:
            treeMaster = self.tree.parent(item)
        
        def OK():
            typ = newType.get()
            name = nameEntry.get()

            root.destroy()

            if typ == "DIR":
                os.mkdir(os.path.join(path, name))

                self.tree.insert(treeMaster, tk.END, text=name, values=[
                    os.path.join(path, name), "dir"], image=self.dirImg)
            else:
                open(os.path.join(path, name), "w").close()

                img = None
                ext = os.path.splitext(os.path.join(path, name))[1].upper()

                for k, v in self.imgDict.items():
                    if ext == k:
                        img = v

                        break

                self.tree.insert(treeMaster, tk.END, text=name, values=[
                    os.path.join(path, name), "file", "0 Bytes"], image=img)
        
        if os.path.isfile(path):
            path = os.path.dirname(path)

        root = tk.Toplevel(self)
        root.title("New")

        newType = tk.StringVar(value="DIR")

        typeDir = ttk.Radiobutton(root, variable=newType, value="DIR",
                                  text="Directory")
        typeFile = ttk.Radiobutton(root, variable=newType, value="FILE",
                                   text="File")

        typeDir.grid()
        typeFile.grid()

        nameLabel = ttk.Label(root, text="Name: ")
        nameEntry = ttk.Entry(root)

        nameLabel.grid(row=2, column=0)
        nameEntry.grid(row=2, column=1)

        okBtn = ttk.Button(root, text="OK", command=OK)
        okBtn.grid()

        root.mainloop()

    def _openMenu(self, event=None):
        sel = self.tree.identify("item", event.x, event.y)
        
        path = self.tree.set(sel, "fullPath")

        menu = tk.Menu(self, tearoff=False)

        ext = None

        if os.path.isfile(path):
            ext = os.path.splitext(path)[-1].upper()

        if os.path.isfile(path) or os.path.isdir(path):
            menu.add_command(label="Rename", command=lambda: self.rename(path, sel),
                             image=self.triImg, compound=tk.LEFT)
            menu.add_command(label="Delete", command=lambda: self.delete(path, sel),
                             image=self.triImg, compound=tk.LEFT)
            menu.add_command(label="New...", command=lambda: self.new(path, sel),
                             image=self.triImg, compound=tk.LEFT)

            if ext:
                if ext == ".PNG" or ext == ".BMP":
                    menu.add_command(label="View Image", command=lambda: imgViewer.
                                     viewImg(path, self), image=self.triImg, compound=
                                     tk.LEFT)
                else:
                    menu.add_command(label="View Image", image=self.triImg,
                                     compound=tk.LEFT, state=tk.DISABLED)
                
        else:
            menu.add_command(label="Rename", command=lambda: self.rename(path, sel),
                             image=self.triImg, compound=tk.LEFT, state=tk.DISABLED)
            menu.add_command(label="Delete", command=lambda: self.delete(path, sel),
                             image=self.triImg, compound=tk.LEFT, state=tk.DISABLED)

        menu.tk_popup(event.x_root, event.y_root)

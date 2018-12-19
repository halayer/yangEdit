try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox as msgBox
    from tkinter import font
    from tkinter import scrolledtext as tkst
except: # Python 2.x
    import Tkinter as tk
    import Ttk as ttk
    import tkMessageBox as msgBox
    import tkFont as font
    import ScrolledText as tkst

import json
import scrolledTree
import yangTools
import propPanel
import pathBrowser
import refTypes
import settings
import dict2robot
import os

NoneType = type(None)


class editFrame(tk.Frame):

    def __init__(self, file=None, data=None, master=None):
        tk.Frame.__init__(self, master)

        self.loaded = False
        
        if not data:
            if file:
                self.file = file
        else:
            self.jsonObj = data; self.loaded = True

##        self.name = dict(); self.nameCounter = 0
##        self.prefix = dict(); self.prefixCounter = 0
##        self.mandatory = dict(); self.mandatoryCounter = 0
##        self.type = dict(); self.typeCounter = 0
##        self.key = dict(); self.keyCounter = 0
##        self.keys = dict(); self.keysCounter = 0
##        self.value_type = dict(); self.value_typeCounter = 0
        self.props = {"name": [], "prefix": [], "mandatory": [], \
                      "type": [], "key": [], "keys": [], "value_type": []}

        self.cProps = None
        self.realNames = dict()

        self._loadImgs()
        self._loadData()
        self._createWidgets()

    def _loadImgs(self):
        # value_type images
        self.intImg = tk.PhotoImage(file="data/int.png")
        self.strImg = tk.PhotoImage(file="data/str.png")
        self.floatImg = tk.PhotoImage(file="data/float.png")
        self.emptyImg = tk.PhotoImage(file="data/none.png")

        # yang type images
        self.containerImg = tk.PhotoImage(file="data/container.png")
        self.leafImg = tk.PhotoImage(file="data/leaf.png")
        self.leafListImg = tk.PhotoImage(file="data/leaf-list.png")
        self.choiceImg = tk.PhotoImage(file="data/choice.png")
        self.caseImg = tk.PhotoImage(file="data/case.png")
        self.outputImg = tk.PhotoImage(file="data/output.png")
        self.inputImg = tk.PhotoImage(file="data/input.png")
        self.bellImg = tk.PhotoImage(file="data/notification.png")
        self.anyXmlImg = tk.PhotoImage(file="data/anyxml.png")
        self.keyLeafImg = tk.PhotoImage(file="data/keyLeaf.png")
        self.arrayImg = tk.PhotoImage(file="data/array.png")

        self.triImg = tk.PhotoImage(file="data/triangle.png")
        self.robotImg = tk.PhotoImage(file="data/robot.png")

        self.typeImgs = {"container": self.containerImg, "leaf": self.leafImg,
                         "leaf-list": self.leafListImg, "choice": self.choiceImg,
                         "case": self.caseImg, "output": self.outputImg,
                         "input": self.inputImg, "notification": self.bellImg,
                         "anyxml": self.anyXmlImg, "leaf (key)": self.keyLeafImg,
                         "list": self.arrayImg, "leaflist": self.leafListImg}

        self.valueTypeImgs = {"string": self.strImg, "uint64": self.intImg,
                              "uint32": self.intImg, "uint16": self.intImg,
                              "union": self.floatImg, "empty": self.emptyImg}

    def _crawlList(self, aList):
        retList = refTypes.refList(aList)

        for i in range(len(retList)):
            if isinstance(retList[i], dict):
                retList[i] = self._crawlDict(retList[i])
            elif isinstance(retList[i], list):
                retList[i] = self._crawlList(retList[i])

        return retList
    
    def _crawlDict(self, aDict):
        retDict = refTypes.refDict(aDict)

        for k in retDict.keys():
            if isinstance(retDict[k], dict):
                retDict[k] = self._crawlDict(retDict[k])
            elif isinstance(retDict[k], list):
                retDict[k] = self._crawlList(retDict[k])

        return retDict

    def _loadData(self):
        if not self.loaded:
            with open(self.file, "r") as file:
                try:
                    jsonObj = json.loads(file.read())

                    self.modules = jsonObj.get("modules", dict())
                    self.namespaces = jsonObj.get("namespaces", dict())

                    if "tree" in jsonObj:
                        jsonObj["tree"] = self._crawlDict(jsonObj["tree"])

                        self.jsonObj = jsonObj

                        return

                    for obj in jsonObj.keys():
                        if isinstance(obj, dict):
                            jsonObj[obj] = self._crawlDict(jsonObj[obj])
                        elif isinstance(obj, list):
                            jsonObj[obj] = self._crawlList(jsonObj[obj])
                            
                    self.jsonObj = jsonObj
                except:
                    msgBox.showerror("Error", "File is not a valid JSON file.")

                    raise

    def _hasOnlyNode(self, aDict):
        if len(aDict) == 1:
            if "__node__" in aDict:
                return True

        return False

    def YANGImg(self, yangType):
        if yangType in self.typeImgs:
            return self.typeImgs[yangType]
        else:
            return tk.PhotoImage(width=16, height=16)

    def search(self):
        pass
##        index = 0
##        
##        def searchBtn():
##            d = self.__dict__[toSearch.get()]
##
##            found = False
##            value = None
##
##            for k, v in d.items():
##                if k.split("\x00")[0] == entry.get():
##                    found = True
##                    value = v
##
##            if found:
##                self.tree.tree.selection_set(value)
##                self.tree.tree.see(value)
##
##                if len(self
##
##            foundNum
##
##        toSearch = tk.StringVar(value="name")
##        radios = ["name", "prefix", "type", "key", "keys", "mandatory", "value_type"]
##        gridColumn = 0
##        
##        root = tk.Toplevel(self)
##        root.title(f"Search [{self.file}]")
##        root.iconbitmap("data/icon.ico")
##
##        entry = ttk.Entry(root)
##        entry.grid()
##
##        searchBtn = ttk.Button(root, text="Search", command=searchBtn)
##        searchBtn.grid(row=0, column=1)
##
##        for radio in radios:
##            widget = ttk.Radiobutton(root, variable=toSearch, value=radio,
##                                     text=radio)
##            widget.grid(row=1, column=gridColumn)
##
##            gridColumn += 1
##
##        root.mainloop()

    def insertProps(self, nodeDict, item):
        if "name" in nodeDict:
            self.props["name"].append(item)
        if "prefix" in nodeDict:
            self.props["prefix"].append(item)
        if "type" in nodeDict:
            self.props["type"].append(item)
        if "key" in nodeDict:
            self.props["key"].append(item)
        if "keys" in nodeDict:
            self.props["keys"].append(item)
        if "mandatory" in nodeDict:
            self.props["mandatory"].append(item)
        if "value_type" in nodeDict:
            self.props["value_type"].append(item)

    def _advancedInsert(self, var, parent="", name="", lastPrefix="", opened=False):
        if isinstance(var, dict):
            if not name:
                if settings.showPrefix:
                    treeName = yangTools.name(var, False)
                else:
                    treeName = yangTools.name(var)
            else:
                if not settings.showPrefix:
                    treeName = yangTools.removePrefix(name)
                else:
                    treeName = name

            tag = ""

            if "__node__" in var:
                if "name" in var["__node__"]:
                    if settings.showPrefix and "prefix" in var["__node__"]:
                        if not var["__node__"]["prefix"] == lastPrefix:
                            treeName = var["__node__"]["prefix"] + ":" + var["__node__"]["name"]
                    else:
                        treeName = var["__node__"]["name"]

            yangType = yangTools.type(var)

            if var.get("__node__", {}).get("mandatory", "").lower() == "true":
                tag = "mandatory"
                
            if var.get("__node__", {}).get("key", "").lower() == "true":
                tag = "keyLeaf"

                yangType = "leaf (key)"

            prt = self.tree.tree.insert(parent, tk.END, text=treeName,
                                        values=[yangType], image=self.YANGImg(yangType),
                                        open=opened, tag=tag)

            if "__node__" in var:
                self.insertProps(var["__node__"], prt)

            if name:
                self.realNames.update({prt: name})
            else:
                self.realNames.update({prt: yangTools.name(var, False)})

            keyLeafList = list()
            mandatoryList = list()
            insList = list()

            for k, v in var.items():
                if k == "__node__":
                    if settings.show__node__:
                        self.insList.append([[v, prt], {"name": k, "lastPrefix":
                                                        var.get("__node__", {}).get("prefix", "")}])
                else:
                    if isinstance(v, dict):
                        if v.get("__node__", {}).get("key", "").upper() == "TRUE":
                            keyLeafList.append([[v, prt], {"name": k, "lastPrefix":
                                                           var.get("__node__", {}).get("prefix", "")}])

                            continue
                        elif v.get("__node__", {}).get("mandatory", "").upper() == "TRUE":
                            mandatoryList.append([[v, prt], {"name": k, "lastPrefix":
                                                             var.get("__node__", {}).get("prefix", "")}])

                            continue
                        
                    insList.append([[v, prt], {"name": k, "lastPrefix":
                                               var.get("__node__", {}).get("prefix", "")}])

            for i in keyLeafList:
                self._advancedInsert(*i[0], **i[1])
                
            for i in mandatoryList:
                self._advancedInsert(*i[0], **i[1])
                
            for i in insList:
                self._advancedInsert(*i[0], **i[1])
        elif isinstance(var, str):
            if name:
                self.tree.tree.insert(parent, tk.END, text=name)
            else:
                self.tree.tree.insert(parent, tk.END, text=var)

    def _insertValues(self):
        if type(self.jsonObj) == list:
            for obj in self.jsonObj:
                self._advancedInsert(obj)

            return
        elif type(self.jsonObj) == dict:
            for k, v in self.jsonObj.items():
                if k == "__node__": continue
                
                self._advancedInsert(v, name=k)

            return

        self._advancedInsert(self.jsonObj)

    def _hasParent(self, index):
        return bool(self.tree.tree.parent(index))

    def _getParent(self, index):
        parentIndex = self.tree.tree.parent(index)
        
        return self.tree.tree.item(parentIndex), parentIndex

    def _getIndex(self, index):
        item = self.tree.tree.item(index)

        if not index: return

        retList = [self.realNames[index]]

        while self._hasParent(index):
            item, index = self._getParent(index)
            
            retList.append(self.realNames[index])

        return retList

    def _getAt(self, indexList):
        indexList = indexList[::-1]

        item = self.jsonObj
        
        for i in indexList:
            item = item[i]

        return item

    def _setAt(self, indexList, key, value):
        indexList = indexList[::-1]

        item = self.jsonObj

        for i in indexList:
            item = item[yangTools.removePrefix(i)]

        item[key] = value

    def _delAt(self, indexList, key):
        indexList = indexList[::-1]

        item = self.jsonObj

        indexLen = len(indexList)

        if indexLen == 0:
            del item[key]

            return

        for j, i in enumerate(indexList):
            if j == len(indexList) - 1:
                item = item[yangTools.removePrefix(i)]
                del item[key]
            else:
                item = item[yangTools.removePrefix(i)]

    def _treeMenu(self, event):
        sel = self.tree.tree.identify("item", event.x, event.y)

        index = self._getIndex(sel)
        propsIndex = index.copy()
        propsIndex.insert(0, "__node__")

        menu = tk.Menu(self, tearoff=0)

        if not index or not self._hasProps(index):
            menu.add_command(label="YANG Properties",
                             state=tk.DISABLED,
                             image=self.triImg, compound=tk.LEFT)
            menu.add_command(label="Set YANG Properties",
                             command=lambda: self._setProps(index, sel, event),
                             image=self.triImg, compound=tk.LEFT, state=tk.DISABLED)
            menu.add_command(label="container2dict",
                             command=lambda: self.container2dict(index),
                             image=self.containerImg, compound=tk.LEFT,
                             state=tk.DISABLED)
            menu.add_command(label="Robot Snippet",
                             command=lambda: self.robotSnippet(index),
                             image=self.robotImg, compound=tk.LEFT,
                             state=tk.DISABLED)
        else:
            props = self._getAt(propsIndex)
            
            menu.add_command(label="YANG Properties",
                             command=lambda: self._openProps(index),
                             image=self.triImg, compound=tk.LEFT)
            menu.add_command(label="Set YANG Properties",
                             command=lambda: self._setProps(index, sel, event),
                             image=self.triImg, compound=tk.LEFT)
            menu.add_command(label="container2dict",
                             command=lambda: self.container2dict(index),
                             image=self.containerImg, compound=tk.LEFT,
                             state=tk.NORMAL if props.get("type", "").upper() \
                             == "CONTAINER" else tk.DISABLED)
            menu.add_command(label="Robot Snippet",
                             command=lambda: self.robotSnippet(index),
                             image=self.robotImg, compound=tk.LEFT)

        menu.tk_popup(event.x_root, event.y_root)

    def container2dict(self, index):
        data = self._getAt(index)

        def copyToClip():
            root.clipboard_clear()
            root.clipboard_append(data)
        
        try:
            data = json.dumps(data, indent=4)
        except:
            return

        root = tk.Toplevel(self)
        root.title("container2dict")
        root.iconbitmap("data/icon.ico")

        st = tkst.ScrolledText(root)

        st.insert(tk.END, data)
        st.pack(fill=tk.BOTH,expand=True)

        st.config(state=tk.DISABLED)

        copyBtn = ttk.Button(root, text="Copy All",
                             command=copyToClip)
        copyBtn.pack(fill=tk.BOTH)

    def robotSnippet(self, index):
        data = dict2robot.dict2robot(self._getAt(index))

        def copyToClip():
            root.clipboard_clear()
            root.clipboard_append(data)
        
        root = tk.Toplevel(self)
        root.title("Robot Snippet")
        root.iconbitmap("data/robot.ico")

        st = tkst.ScrolledText(root)

        st.insert(tk.END, data)
        st.pack(fill=tk.BOTH,expand=True)

        st.config(state=tk.DISABLED)

        copyBtn = ttk.Button(root, text="Copy All",
                             command=copyToClip)
        copyBtn.pack(fill=tk.BOTH)

    def _changeSel(self, event=None): # 'event' is unused
        sel = self.tree.tree.selection()

        if sel:
            sel = sel[0]
        else:
            if hasattr(self, "propPanel"):
                self.propPanel.update("", None)

                return

        index = self._getIndex(sel)

        if self._hasProps(index):
            props = self._getAt(index)
            self.cProps = refTypes.refDict(props["__node__"])
            
            self.updateProps(sel)

    def _hasProps(self, index):
        data = self._getAt(index)

        if isinstance(data, dict):
            if "__node__" in data:
                return True

        return False

    def getModuleName(self, prefix):
        return self.namespaces.get(prefix)

    def updateProps(self, item):
        props = self.cProps.copy()
        
        if settings.propPanel:
            module = self.getModuleName(self.cProps.get("prefix", ""))
                
            self.propPanel.update(item, props, module=module)

    def changeProp(self, indexOrItem, value, key):
        if isinstance(indexOrItem, int):
            item = self.tree.tree.item(indexOrItem)
        else:
            item = indexOrItem

        index = self._getIndex(item)
        index2 = index[1:]
        oldName = index[0]

        prefix = ""

        if "__node__" in self._getAt(index):
            if "prefix" in self._getAt(index)["__node__"]:
                prefix = self._getAt(index)["__node__"]["prefix"]
            
        if self._hasProps(index):
            if value == "name":
                self.realNames.update({item: prefix + ":" + key})

                oldVal = self._getAt(index)
                
                self._delAt(index2, oldName)

                self._setAt(index2, key, oldVal)

                index[0] = key

                if settings.showPrefix and prefix:
                    self.tree.tree.item(item, text=prefix + ":" + key)
                else:
                    self.tree.tree.item(item, text=key)
            
            index.insert(0, "__node__")
            
            self._setAt(index, value, key)

    def hasProp(self, indexOrItem, propName):
        if isinstance(indexOrItem, int):
            item = self.tree.tree.item(indexOrItem)
        else:
            item = indexOrItem

        index = self._getIndex(item)

        if self._hasProps(index):
            props = self._getAt(index)["__node__"]

            if propName in props:
                return True

        return False

    def delProp(self, indexOrItem, propName):
        if isinstance(indexOrItem, int):
            item = self.tree.tree.item(indexOrItem)
        else:
            item = indexOrItem

        index = self._getIndex(item)

        if self.hasProp(item, propName):
            index.insert(0, "__node__")
            self._delAt(index, propName)
        
    def update(self):
        self.tree.destroy()

        if hasattr(self, "propPanel"):
            self.propPanel.destroy()

        if hasattr(self, "pathBrowser"):
            self.pathBrowser.destroy()

        self._loadData()
        self._createWidgets()

    def save(self):
        with open(self.file, "w") as file:
            file.write(json.dumps(self.jsonObj, indent=4))
        
    def _setProps(self, index, item, event):
        def OK():
            newVal = entry.get()
            index.insert(0, "__node__")

            if optType.get() == "keys":
                try:
                    newVal = refTypes.refList(json.loads(newVal))
                except:
                    msgBox.showerror("yangEdit", "The value has to be list-like.")
                    root.focus_set()

                    return

            self._setAt(index, optType.get(), newVal)

            root.destroy()

            self.tree.tree.selection_set(item)

        def onRadioChange(event=None): # 'event' is unused
            entry.delete(0, tk.END)

            if optType.get() in list(__node__.keys()):
                entry.insert(tk.END, __node__[optType.get()])
        
        __node__ = self._getAt(index)["__node__"]
        doc = __node__["doc"] if "doc" in __node__ else ""
        optType = tk.StringVar(value="doc")
        gridNum = 0

        root = tk.Toplevel(self)
        root.title("Set Props")
        root.iconbitmap("data/icon.ico")

        radio = ["doc", "key", "keys", "mandatory", "name", "prefix",
                 "type", "value_type"]

        for i in radio:
            btn = ttk.Radiobutton(root, variable=optType, value=i,
                                  text=i)
            btn.grid(row=gridNum)

            btn.bind("<Button-1>", onRadioChange)

            gridNum += 1

        label = ttk.Label(root, text="Value: ")
        entry = ttk.Entry(root)

        entry.insert(tk.END, doc)

        okBtn = ttk.Button(root, text="OK", command=OK)

        label.grid(row=gridNum)
        entry.grid(row=gridNum, column=1)

        entry.focus_set()

        okBtn.grid(row=gridNum + 1)

        root.mainloop()

    def _openProps(self, index):
        props = self._getAt(index)

        root = tk.Toplevel(self)
        root.title("YANG Properties")
        root.iconbitmap("data/icon.ico")

        panel = propPanel.propPanel(root, props["__node__"], tree=self.tree.tree)

        panel.pack()

    def _createWidgets(self):
        self.tree = scrolledTree.scrolledTree(self, columns=("type",),
                                              selectmode="extended")
        
        self.tree.tree.heading("#0", text="Name")
        self.tree.tree.heading("type", text="Type")

        boldFont = font.Font(weight=font.BOLD, size=8)

        self.tree.tree.tag_configure("mandatory", font=boldFont)
        self.tree.tree.tag_configure("keyLeaf", foreground="blue", font=boldFont)

        self.tree.tree.bind("<<TreeviewSelect>>", self._changeSel)
        self.tree.tree.bind("<Button-3>", self._treeMenu)

        if settings.pathBrowser:
            self.pathBrowser = pathBrowser.pathBrowser(self, os.path.dirname(
                self.file), self.master.master._createEditFrame)
            self.pathBrowser.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        if settings.propPanel:
            self.propPanel = propPanel.propPanel(self, tree=self.tree.tree)
            self.propPanel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._insertValues()

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

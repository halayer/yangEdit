try:
    import tkinter as tk
except: # Python 2.x
    import Tkinter as tk

STD_PROPS = {"doc": "", "key": "", "mandatory": "", "name": "",
             "prefix": "", "type": "", "value_type": ""}


class propPanel(tk.LabelFrame):

    def __init__(self, master=None, props=None, **kw):
        tk.LabelFrame.__init__(self, master, width=250, text="YANG Properties")

        if props is None:
            self.props = dict()
        else:
            self.props = props

        self.tree = None

        if "tree" in kw:
            self.tree = kw["tree"]
            
        self.widgets = list()
        self.item = None
        self.master = master
        self.module = None

        self._createWidgets()

    def update(self, item, newProps=STD_PROPS, module=None):
        for widget in self.widgets:
            widget.destroy()

        if newProps is None:
            self.props = dict()
            self._createWidgets()

            return

        self.item = item

        self.widgets = list()

        self.props = newProps
        self.module = module

        self._createWidgets()

    def changeProp(self, event):
        def OK():
            self.props[prop] = entry.get()

            if self.master and hasattr(self.master, "changeProp"):
                self.master.changeProp(self.item, prop, entry.get())

            root.destroy()

            self.update(self.item, self.props)

        def delProp():
            del self.props[prop]
            
            self.master.delProp(self.item, prop)

            root.destroy()

            self.update(self.item, self.props)
        
        prop = event.widget.cget('text').split(":")[0]

        root = tk.Toplevel(self)
        root.title(f"Change {prop}")
        root.iconbitmap("data/icon.ico")

        label = tk.Label(root, text=prop + ":")
        entry = tk.Entry(root)
        entry.bind("<Return>", lambda i: OK())
        okBtn = tk.Button(root, text="OK", command=OK)
        delBtn = tk.Button(root, text="Delete property", command=delProp,
                           state=tk.DISABLED if prop == "name" or prop == "type" \
                           else tk.NORMAL)

        label.grid()
        entry.grid(row=0, column=1)

        okBtn.grid()
        delBtn.grid(row=1, column=1)

        entry.focus_set()

        root.mainloop()

    def _createWidgets(self):
        gridNum = 0
        changeProp = self.changeProp

        if len(self.props) == 0:
            widget = tk.Label(self, text="Select a YANG Object in the YANG tree.\n" \
                              "By double-clicking on a YANG Property, you can change/delete it.")
            widget.pack(fill=None, expand=True)

            self.widgets.append(widget)

            return
        
        for k, v in self.props.items():
            widget = tk.Label(self, text=k + ":")
            widget.grid(row=gridNum, column=0, sticky=tk.W)
            widget.bind("<Double-1>", self.changeProp)
            
            self.widgets.append(widget)

            widget = tk.Label(self, text=v)
            widget.grid(row=gridNum, column=1, sticky=tk.W)
            widget.bind("<Double-1>", self.changeProp)
            
            self.widgets.append(widget)

            gridNum += 1

        if self.module:
            widget = tk.Label(self, text="module:")
            widget.grid(row=gridNum, column=0, sticky=tk.W)

            self.widgets.append(widget)

            widget = tk.Label(self, text=self.module)
            widget.grid(row=gridNum, column=1, sticky=tk.W)

            self.widgets.append(widget)

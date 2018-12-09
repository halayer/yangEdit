try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter.simpledialog import Dialog
except: # Python 2.x
    import Tkinter as tk
    import Ttk as ttk
    from tkSimpleDialog import Dialog

import entrys


class _queryString(Dialog):

    def __init__(self, title="", prompt="", parent=tk._default_root):
        self.prompt = str(prompt)

        Dialog.__init__(self, parent, title)

    def body(self, root):
        self.label = tk.Label(root, text=self.prompt)
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        return self.entry

    def apply(self):
        self.result = self.entry.get()


def askString(title="", prompt="", **kw):
    dialog = _queryString(title, prompt, **kw)

    return dialog.result

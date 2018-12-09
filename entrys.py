try:
    import tkinter as tk
except: # Python 2.x
    import Tkinter as tk


class validatingEntry(tk.Entry):
    # base class for validating entry widgets

    def __init__(self, master, value="", **kw):
        tk.Entry.__init__(self, master, kw)
        self.__value = value
        self.__variable = tk.StringVar()
        self.__variable.set(value)
        self.__variable.trace("w", self.__callback)
        self.config(textvariable=self.__variable)

    def __callback(self, *dummy):
        value = self.__variable.get()
        newvalue = self.validate(value)
        if newvalue is None:
            self.__variable.set(self.__value)
        elif newvalue != value:
            self.__value = newvalue
            self.__variable.set(self.newvalue)
        else:
            self.__value = value

    def validate(self, value):
        # override: return value, new value, or None if invalid
        return value


class intEntry(validatingEntry):

    def __init_(self, master=None, value="", range=(None, None), callback=None, **kw):
        validatingEntry.__init__(self, master, **kw)

        self.max, self.min = range
        self.callback = callback

    def validate(self, value):
        try:
            val = int(value)

            if self.max and self.min:
                if val >= self.min and val <= self.max:
                    if self.callback: self.callback(value)
                    return value
            else:
                if self.callback: self.callback(value)
                return value

            return None
        except:
            return None

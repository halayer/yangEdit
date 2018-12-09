try:
    import tkinter as tk
except: # Python 2.x
    import Tkinter as tk

import json
import refTypes

SETTINGS_FILE = "data/JSON/settings.json"


class optMenu(tk.Menu):

    def __init__(self, master=None, tabs=refTypes.refDict(), tearoff=False):
        tk.Menu.__init__(self, master, tearoff=tearoff)

        self.show__node__ = tk.BooleanVar()
        self.propPanel = tk.BooleanVar()
        self.showPrefix = tk.BooleanVar()
        self.pathBrowser = tk.BooleanVar()

        if not isinstance(tabs, refTypes.refDict):
            raise TypeError("'tabs' has to be a instance of refTypes.refDict.")

        self.all = {"show__node__": self.show__node__, "propPanel": self.propPanel,
                    "showPrefix": self.showPrefix, "pathBrowser": self.pathBrowser}

        self.texts = {"Show '__node__' (senseless)": self.show__node__,
                      "Show YANG property panel": self.propPanel,
                      "Show prefix": self.showPrefix,
                      "Show path browser": self.pathBrowser}

        self.tabs = tabs
        print(self.tabs)

        self.getSettings()
        self._insertBtns()

    def getSettings(self):
        for k, v in self.all.items():
            v.set(getSetting(k))

    def updateSettings(self):
        for k, v in self.all.items():
            changeSetting(k, v.get())

        for v in self.tabs.values():
            v.update()

    def _insertBtns(self):
        for k, v in self.texts.items():
            self.add_checkbutton(label=k, variable=v,
                             command=self.updateSettings)


def loadSettings(fileName=SETTINGS_FILE):
    global show__node__
    global propPanel
    global showPrefix
    global pathBrowser
    global __data
    
    with open(fileName) as file:
        __data = json.loads(file.read())

    show__node__ = __data["show__node__"]
    propPanel = __data["propPanel"]
    showPrefix = __data["showPrefix"]
    pathBrowser = __data["pathBrowser"]

def changeSetting(key, value, fileName=SETTINGS_FILE):
    __data[key] = value

    with open(fileName, "w") as file:
        file.write(json.dumps(__data))

    loadSettings()

def getSetting(key):
    return __data[key]

loadSettings()

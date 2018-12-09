try:
    import tkinter as tk
except: # Python 2.x
    import Tkinter as tk

import os
import json

def getTxts(sysArgv):
    fileName = os.path.split(sysArgv[0])[-1]
    with open("statusTxts.json") as file:
        return json.loads(file.read())[fileName]

def bindBalloon(balloon, txts, widgets):
    for k, v in txts.items():
        if k in widgets:
            balloon.bind_widget(widgets[k],
                                balloonmsg=v.get("balloonMsg", ""),
                                statusmsg=v.get("statusMsg", ""))


class statusBar(tk.Label):

    def __init__(self, master=None):
        tk.Label.__init__(self, master, bd=1)

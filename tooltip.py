try:
    import tkinter as tk
except: # Python 2.x
    import Tkinter as tk

class createToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, treeWidget):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = treeWidget
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Motion>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.item = None
        self.tw = None
        self.showing = False
        self.allMaster = treeWidget.master.master.master

    def enter(self, event=None):
        if not self.showing:
            self.schedule(event)
        else:
            item = self.widget.identify("item", event.x, event.y)

            if not item == self.item:
                self.leave()
                self.schedule(event)
##        else:
##            x, y = self.widget.winfo_pointerxy()
##            
##            self.tw.geometry("+{}+{}".format(x, y))

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self, event=None):
        self.unschedule()
        self.hidetip()

        self.showtip(event)

    def unschedule(self):
        self.showing = False

    def showtip(self, event=None):
        if self.showing:
            return

        txt = ""
        item = self.widget.identify("item", event.x, event.y)

        if not item:
            self.unschedule()
            return

        self.item = item

        index = self.allMaster._getIndex(item)

        if index:
            props = self.allMaster._getAt(index)

            for k, v in props.get("__node__", dict()).items():
                txt += k + ": " + v + "\n"

        x, y = self.widget.winfo_pointerxy()
        
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_attributes("-topmost", True)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=txt, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

        self.showing = True

        self.tw.update()
        self.widget.update()

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

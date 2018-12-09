try:
    import tkinter as tk
    from tkinter import messagebox as msgBox
except: # Python 2.x
    import Tkinter as tk
    import tkMessageBox as msgBox

import os

def viewImg(imgPath, master=None):
    root = tk.Toplevel(master)

    img = tk.PhotoImage(file=imgPath)

    width, height = str(img.width()), str(img.height())
    
    root.title(os.path.split(imgPath)[-1] + " (" + \
               width + "x" + height + ")")

    label = tk.Label(root, image=img)
    label.pack()

    root.mainloop()

try:
    from tkinter import filedialog as fileDialog
except: # Pyrhon 2.x
    import tkFileDialog as fileDialog

def saveAs(data, title="Save As...", initDir="/",
           fileTypes=(("TXT file", "*.txt"), ("All files", "*.*"),
                      ("JSON file", "*.json")), **args):
    args.update({"title": title, "initialdir": initDir,
                 "filetypes": fileTypes})
    fileName = fileDialog.asksaveasfilename(**args)

    if isinstance(data, bytes):
        file = open(fileName, "wb")
    else:
        file = open(fileName, "w")

    file.write(data)
    file.close()

    return fileName

def saveAsFilename(**args):
    fileName = fileDialog.asksaveasfilename(**args)

    return fileName

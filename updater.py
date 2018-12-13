try:
    from urllib.request import urlopen
    import tkinter as tk
    from tkinter import messagebox as msgBox
    from tkinter import ttk
except: # Python 2.x
    from urllib2 import urlopen
    import Tkinter as tk
    import tkMessageBox as msgBox
    import Ttk as ttk

import zipfile
import shutil
import os
import subprocess

def getCurrentVersion():
    with open("version.txt") as file:
        return file.read()

def getNewestVersion():
    with urlopen(versionURL) as file:
        data = file.read()

        if hasattr(data, "decode"):
            return data.decode()

def copyFiles(src, dest):
    for file in os.listdir(src):
        fileName = os.path.join(src, file)

        if os.path.isfile(fileName): shutil.copy(fileName, dest)
        else: shutil.copytree(fileName, os.path.join(dest, file))

class yangEditUpdater(tk.Tk):

    def __init__(self, master=None):
        tk.Tk.__init__(self)
        self.title("yangEdit updater")

        self.prgrBar = ttk.Progressbar(self, orient=tk.HORIZONTAL,
                                       length=200, mode="determinate")
        self.prgrBar.pack()

        self.download()

    def download(self):
        shutil.copytree("data/JSON", "JSON")
        
        inFile = open("yangEdit.zip", "wb")
        outFile = urlopen(yangEditURL)

        html = outFile.info()
        cl = html["Content-Length"]

        progress = 0
        self.prgrBar.start()

        while True:
            data = outFile.read(1024)
            progress += len(data)

            self.prgrBar.update()

            self.title("%s %s" % (progress * 100 / int(cl), "%"))

            self.prgrBar.config(maximum=100)
            self.prgrBar.config(value=progress * 100 / int(cl))

            inFile.write(data)

            if not data: break
            del data

        inFile.close()
        self.prgrBar.stop()

        for i in os.listdir():
            if not i == "yangEdit.zip" and not i == "JSON" \
            and not i == "updater.py":
                if os.path.isfile(i): os.unlink(i)
                else: shutil.rmtree(i)

        zipFile = zipfile.ZipFile("yangEdit.zip")
        zipFile.extractall()
        zipFile.close()

        copyFiles("yangEdit-master", ".")

        shutil.rmtree("yangEdit-master")

        shutil.rmtree("data/JSON")
        shutil.copytree("JSON", "data/JSON")

        shutil.rmtree("JSON")

        os.unlink("yangEdit.zip")

        self.destroy()

versionURL = "https://raw.githubusercontent.com/letsCodeMyLife/yangEdit/master/version.txt"
yangEditURL = "https://github.com/letsCodeMyLife/yangEdit/archive/master.zip"

def main(master=None):
    cMajor, cMinor = getCurrentVersion().split(".")

    try:
        nMajor, nMinor = getNewestVersion().split(".")
    except Exception as e:
        print(str(e))
        return

    download = False

    if int(nMajor) > int(cMajor):
        download = True
    elif int(nMinor) > int(cMinor):
        download = True

    print(download, getCurrentVersion(), getNewestVersion())

    if not download: return

    download = msgBox.askyesno("yangEdit", "yangEdit version {} is available. " \
                               "Do you want to download it?".format(getNewestVersion()),
                               master=master)

    if not download: return

    if hasattr(master, "onExit"):
        master.onExit()

    app = yangEditUpdater()
    app.mainloop()

    os.system("python main.py")

if __name__ == "__main__":
    main()

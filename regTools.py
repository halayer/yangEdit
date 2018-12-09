try:
    import winreg
except: # Python 2.x
    import _winreg as winreg

from collections import namedtuple

keyInfo = namedtuple("keyInfo", ["subKeys", "values", "lastModification"])

def getKeys(key):
    i = 0
    retList = tuple()

    while True:
        try:
            retList += (winreg.EnumKey(key, i),)

            i += 1
        except WindowsError:
            return retList

def getValues(key):
    keyDict = {}
    i = 0
    
    while True:
        try:
            subValue = winreg.EnumValue(key, i)
        except WindowsError as e:
            break
        
        keyDict[subValue[0]] = subValue[1]

        i += 1
        
    return keyDict

def setValue(key, valueName, type, value):
    winreg.SetValueEx(key, valueName, 0, type, value)

def delValue(key, valueName):
    winreg.DeleteValue(key, valueName)

def delKey(key, subKey):
    winreg.DeleteKey(key, subKey)

def getValue(key, valueName):
    return winreg.QueryValueEx(key, valueName)[0]

def getType(key, valueName):
    return winreg.QueryValueEx(key, valueName)[1]

def getKeyInfo(key):
    return keyInfo(*winreg.QueryInfoKey(key))

def hasSubKeys(key):
    return not len(getKeys(key)) == 0

def hasValues(key):
    return not len(getValues(key)) == 0

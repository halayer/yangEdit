import yangTools
import json

WS = "    "
EMPTY = "${EMPTY}"
EMPTY_LIST = "${EMPTY_LIST}"

def crawlDict(aDict, robotString, varName, type=None):
    rawVarName = varName
    varName = "${" + varName + "}"

    if type is None:
        type = yangTools.type(aDict).upper()

    if type in ["CONTAINER", "CHOICE", "CASE"]:
        robotString.append(varName + WS + "Create Dictionary")

        for k, v in aDict.items():
            if k == "__node__": continue
                
            if yangTools.type(v).upper() == "LEAF":                    
                robotString.append(WS.join(["Set To Dictionary", varName,
                                            k, EMPTY]))
            elif yangTools.type(v).upper() == "LEAFLIST":
                robotString.append(WS.join(["Set To Dictionary", varName,
                                            k, EMPTY_LIST]))
            else:
                _varName = k + "_" + yangTools.type(v)

                crawlDict(v, robotString, _varName)
                    
                robotString.append(WS.join(["Set To Dictionary", varName,
                                            k, "${" + _varName + "}"]))
    elif type == "LIST":
        robotString.append(varName + WS + "Create List")

        crawlDict(aDict, robotString, rawVarName + "_item", "CONTAINER")

        robotString.append("Append To List" + WS + varName + WS + "${" + rawVarName + "_item}")
    
##    for k, v in aDict.items():
##        _type = yangTools.type(v).upper()
##        
##        if _type in ["CONTAINER", "CHOICE", "CASE"]:
##            dictName = "${" + k + "_" + _type + "}"
##            robotString.append(dictName + WS + "Create Dictionary")
##
##            for _k, _v in v.items():
##                if _k == "__node__": continue
##                
##                if yangTools.type(_v).upper() == "LEAF":                    
##                    robotString.append(WS.join(["Set To Dictionary", dictName,
##                                                _k, EMPTY]))
##                else:
##                    _varName = _k + "_" + yangTools.type(_v)
##                    
##                    robotString.append(WS.join(["Set To Dictionary", dictName,
##                                                _k, "${" + _varName + "}"]))
##        else:
##           pass
##
##        for dictName in dictNames:
##            robotString.append("Set To Dictionary" + WS + "

def dict2robot(aDict):
    robotString = list()

    robotString.append("${EMTPY_LIST}" + WS + "Create List")

    crawlDict(aDict, robotString, "master_dict")

    return "\n".join(robotString)

def read(fileName):
    with open(fileName) as file:
        return json.loads(file.read())

if __name__ == "__main__":
    print(dict2robot(read("YSON.json")))

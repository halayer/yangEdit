YANG_VALUE_TYPES = frozenset({"string", "uint64", "uint32", "uint16", "union",
                              "empty", "bits"})

YANG_TYPES = frozenset({"leaf", "leaf-list", "choice", "container", "case",
                        "output", "input", "notification"})

IMG_TRANS_DICT = {"string": "data/str.png", "uint64": "data/int.png",
                  "uint32": "data/int.png", "uint16": "data/int.png",
                  "union": "data/float.png", "empty": "data/none.png",
                  "choice": "data/choice.png", "container": "data/container.png",
                  "leaf": "data/leaf.png", "leaf-list": "data/leaf-list.png",
                  "case": "data/case.png", "output": "data/output.png",
                  "input": "data/input.png", "notification": "data/notification.png",
                  "bits": "data/bits.png"}

def imgFromString(string):
    return IMG_TRANS_DICT[string]

def removePrefix(name):
    if ":" in name:
        return "".join(name.split(":")[1:])

    return name

def type(aDict):
    if isinstance(aDict, dict):
        if "__node__" in aDict:
            if "type" in aDict["__node__"]:
                return aDict["__node__"]["type"]

    return ""

def valueType(aDict):
    if isinstance(aDict, dict):
        if "__node__" in aDict:
            if "value_type" in aDict["__node__"]:
                return aDict["__node__"]["value_type"]

    return ""

def prefix(aDict):
    if isinstance(aDict, dict):
        if "__node__" in aDict:
            if "prefix" in aDict["__node__"]:
                return aDict["__node__"]["prefix"]

    return ""

def name(aDict, withoutPrefix=True):
    if isinstance(aDict, dict):
        if "__node__" in aDict:
            if "name" in aDict["__node__"]:
                name = aDict["__node__"]["name"]

                if withoutPrefix:
                    if prefix(aDict):
                        return name.strip(prefix(aDict))
                    else:
                        return removePrefix(aDict)
                else:
                    return name
                
    return ""

def mandatory(aDict):
    if isinstance(aDict, dict):
        if "__node__" in aDict:
            if "mandatory" in aDict["__node__"]:
                if aDict["__node__"]["mandatory"] == "false":
                    return False
                else:
                    return True

    return ""

def key(aDict):
    if isinstance(aDict, dict):
        if "__node__" in aDict:
            if "key" in aDict["__node__"]:
                if aDict["__node__"]["key"] == "false":
                    return False
                else:
                    return True

    return ""

def doc(aDict):
    if isinstance(aDict, dict):
        if "__node__" in aDict:
            if "doc" in aDict["__node__"]:
                return aDict["__node__"]["doc"]

    return ""

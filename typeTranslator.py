TRANS_DICT = {"String": str, "Integer": int,
              "Array": list, "Dictionary": dict,
              "None": type(None), "Boolean": bool, "Float": float}
REV_TRANS_DICT = {v: k for k, v in TRANS_DICT.items()}

IMG_TRANS_DICT = {"String": "data/str.png", "Integer": "data/int.png",
                  "Array": "data/array.png", "Dictionary": "data/dict.png",
                  "None": "data/none.png", "Boolean": "data/bool.png",
                  "Float": "data/float.png"}

def fromString(string):
    return TRANS_DICT[string]

def fromType(type):
    return REV_TRANS_DICT[type]

def imgFromString(string):
    return IMG_TRANS_DICT[string]

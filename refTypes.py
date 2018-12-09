class refDict(dict):

    def __init__(self, aDict=dict()):
        self.__dict = aDict

        dict.__init__(self, self.__dict)


class refList(list):

    def __init__(self, aList=list()):
        self.__list = aList

        list.__init__(self, self.__list)

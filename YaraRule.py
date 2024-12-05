class YaraRule:
    def __init__(self, name, meta, strings, condition):
        self.name = name
        self.meta = meta
        self.strings = strings
        self.condition = condition
    def print_rule(self):
        print(self.name)
        print(self.meta)
        print(self.strings)
        print(self.condition)
    def getName(self):
        return self.name
    def getMeta(self):
        return self.meta
    def getStrings(self):
        return self.strings
    def getCondition(self):
        return self.condition
    
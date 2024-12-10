import YaraCompiler
class YaraEvaluator:
    #Evaulates only AND and OR 

    def __init__(self, rules):
        self.rules = rules
        self.regex = self.compileRegex()
        self.regex = self.regex[:-1]

    def compileRegex(self):
        regex = r""
        stack = []
        for rule in self.rules:
            regex += "(?<" + rule.getName() + ">"
            postfix = rule.getCondition()
            postfix = YaraCompiler().shunting_yard(postfix)
            while(len(postfix) > 0):
                token = postfix.pop(0)
                if token == "or":
                    regex += "|"
                elif token == "and":
                    regex += "&"
                else:
                    regex += token

            regex += ")|"




from YaraCompiler import YaraCompiler
import YaraParser
pars = YaraParser.YaraLoader('.')
sycomp = YaraCompiler()
for rule in pars.load_rules():
    print(rule.print_rule())
    print()
    print(sycomp.tokenize(rule.getCondition()))
    print(sycomp.shunting_yard(rule.getCondition()))
from SYCOMPILER import SYCOMPILER
import parser
pars = parser.YaraLoader('.')
sycomp = SYCOMPILER()
for rule in pars.load_rules():
    print(rule.print_rule())
    print()
    print(sycomp.tokenize(rule.getCondition()))
    print(sycomp.shunting_yard(rule.getCondition()))

class YaraCompiler:
    def __init__(self):
        pass
    def tokenize(self,condition_string):
        tokens = []
        for token in condition_string.split():
            if token[0] == '(':
                tokens.append(token[0])
                tokens.append(token[1:])
            elif token[-1] == ')':
                tokens.append(token[:-1])
                tokens.append(token[-1])
            else:
                tokens.append(token)


        return tokens
        
        

    def precedence(self,operator):
        match (operator):
            case '[]':
                return 1
            case  '.':
                return 1
            case '-':
                return 2
            case '~':
                return 2
            case '*':
                return 3
            case '/':
                return 3
            case '%':
                return 3
            case '+':
                return 4
            case '-':
                return 4
            case '<<':
                return 5
            case '>>':
                return 5
            case '&':
                return 6
            case '^':
                return 7
            case '|':
                return 8
            case '<':
                return 9
            case '>':
                return 9
            case '<=':
                return 9
            case '>=':
                return 9
            case '==':
                return 10
            case '!=':
                return 10
            case 'contains':
                return 10
            case 'icontains':
                return 10
            case 'startswith':
                return 10
            case 'istartswith':
                return 10
            case 'endswith':
                return 10
            case 'iendswith':
                return 10
            case 'iequals':
                return 10
            case 'matches':
                return 10
            case 'not defined':
                return 11
            case 'and':
                return 12
            case 'or':
                return 13
            case _:
                return 0
    def shunting_yard(self, condition_string):
        output_queue = []
        operator_stack = []


        for token in self.tokenize(condition_string):
            if self.precedence(token) > 0:
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       self.precedence(operator_stack[-1]) >= self.precedence(token)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()
            elif '$' == token[0]: #če je spremenljivka ga pošlje takoj v output stack
                output_queue.append(token)
            else:
                operator_stack.append(token)

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())

        return output_queue

    
            






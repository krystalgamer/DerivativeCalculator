import re
from sys import argv

operatorList = ['+', '-', '*', '/']

class Converter(object):

    opPrecedence = { '+' : 1, '-' : 1, '*' : 2, '/' : 2 }

    def SetExpression(self, expression):
        self.expression = expression

    def __init__(self, expression):
        self.SetExpression(expression)
        return

    def ValidateInput(self):

        foundX = False
        foundDCase = False
        foundDigit = False
        newTerm = True

        if self.expression[0] in operatorList:
            print('Expressions can\'t start with operators')
            return False
        elif self.expression[-1] in operatorList:
            print('Expression can\'t end with operators')
            return False
        elif self.expression[-1] is '.':
            print('Experssion can\'t end with decimal case')
            return False

        for c in self.expression:

            if c in operatorList:
                if newTerm:
                    print('Two operators in a row is not allowed')
                    return False
                if foundDCase and not foundDigit:
                    print('Found decimal case but no digit was found')
                    return False
                foundX = False
                foundDCase = False
                newTerm = True
                continue

            newTerm = False
            if c is '.':
                if foundDCase:
                    print('A term can\'t have multiple decimal points')
                    return False
                if foundX:
                    print('A term can\'t have decimal cases after the variable')
                    return False
                foundDCase = True
            elif c.isdigit():
                if foundX:
                    print('Numbers can\'t come after variables')
                    return False
                foundDigit = True
            elif c is 'x':
                if foundX:
                    print('A term can\'t have multiple variables')
                    return False
                foundX = True
            else: 
                print('Unknown char ' + c)
                return False

        return True

    def InfixToRpn(self):

        if not self.ValidateInput():
            print('Quitting')
            return
            
        numberList = re.split('[\+\-\*\/]', self.expression)
        opList = re.findall('[\+\-\*\/]', self.expression)
        tokens = []

        if len(numberList) != (len(opList) + 1):
            print('Wrong number of operators')
            return None

        opStack = []
        output = []

        for n in numberList:
            output.append(n)

            if not opList:
                continue
            if not opStack:
                opStack.append(opList.pop(0))
                continue

            for op in opStack:
                if opPrecedence[opList[0]] <= opPrecedence[op]:
                    #it's always the top one 
                    output.append(opStack.pop(0))
                else:
                   opStack.insert(0, opList.pop(0)) 
                   break
        
        for op in opStack:
            output.append(op)

        return output

OPERAND_CONSTANT = 0
OPERAND_VARIABLE = 1

class Operand(object):

    def __init__(self, operand):
        self.type = (OPERAND_VARIABLE if 'x' in operand else OPERAND_CONSTANT) 
        self.value = float(operand.replace('x', ''))

class Branch(object):

    def __init__(self, operand1=None, operand2=None, operator=None):
        self.operand1 = operand1
        self.operand2 = operand2
        self.operator = operator
        
class Derivator(object):

    def SetupDerivation(self):

        for entry in self.expression:
        
            if entry in operatorList:
                if len(self.branch) < 2:
                    print('Not enough operands to work with, quitting')
                    return False
                operand2 = self.branch.pop()
                operand1 = self.branch.pop()

                if isinstance(operand2, str):
                    operand2 = Operand(operand2)
                if isinstance(operand1, str):
                    operand1 = Operand(operand1)
        
                self.branch.append(Branch(operand1, operand2, entry))
            else:
                self.branch.append(entry)
        
        return True

    def __init__(self, rpnExpression):
        self.expression = rpnExpression
        self.branch = []
        
def main():

    if len(argv) < 2:
        print('I need to take at least two arguments')
        return

    expression = ''
    for arg in argv[1:]:
        expression+=arg
    expression.replace(' ', '')

    print('Derivating ' + expression)
    converter = Converter(expression)
    rpnExpression = converter.InfixToRpn()

    if rpnExpression == None:
        return
    derivator = Derivator(rpnExpression)
    if not derivator.SetupDerivation():
        print('NOO')
        return
    print('YAS')
    
    return


if __name__ == '__main__':
    main()

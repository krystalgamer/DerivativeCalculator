import re
from sys import argv

printn = lambda x : print(x, end='')

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
                if Converter.opPrecedence[opList[0]] <= Converter.opPrecedence[op]:
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

    def Print(self):
        printn(str(self.value) + ('x ' if self.type == OPERAND_VARIABLE else ' '))
        return True


class Branch(object):

    def __init__(self, operand1=None, operand2=None, operator=None):
        self.operand = [operand1, operand2]
        self.operator = operator

    def Print(self):
        for i in range(2):
            if isinstance(self.operand[i], Branch) or isinstance(self.operand[i], Operand):
                if not self.operand[i].Print():
                    print('Error printing operand')
                    return False
            elif isinstance(self.operand[i], None):
                continue
            else:
                print('Unknwon operand type')
                return False

        printn(self.operator)
        return True
        
class Derivator(object):

    def SetupDerivation(self):

        #Creates basic output queue
        for entry in self.expression:
            if entry in operatorList:
                if len(self.output) < 2:
                    print('Not enough operands to work with, quitting')
                    return False

                operand2, operand1 = self.output.pop(), self.output.pop()

                if isinstance(operand2, str):
                    operand2 = Operand(operand2)
                if isinstance(operand1, str):
                    operand1 = Operand(operand1)
        
                self.output.append(Branch(operand1, operand2, entry))
            else:
                #is a number move to the queue
                self.output.append(entry)
        
        if len(self.output) != 1:
            print('Error creating ouput queue')
            return False

        self.branch = self.output.pop()
        return True


    def Derivate(self, branch=None):
       
        return self.derivateFunc[branch[0].operator if branch != None else self.branch.operator](branch)
        
    def __init__(self, rpnExpression):
        self.expression = rpnExpression
        self.output = []
        self.branch = None
        self.derivateFunc = {'+' : self.DerivateSum, '-' : self.DerivateSum}
    
    def Print(self):
        self.branch.Print()
        print('')
        
    def DerivateSum(self, branch):
        
        workingBranch = (branch[0] if branch != None else self.branch)

        for i in range(2):
            if isinstance(workingBranch.operand[i], Operand):
                if workingBranch.operand[i].type == OPERAND_CONSTANT:
                    workingBranch.operand[i].value = 0
                elif workingBranch.operand[i].type == OPERAND_VARIABLE:
                    workingBranch.operand[i].type = OPERAND_CONSTANT
                else:
                    print('Unknown operand type')
                    return False
        return True

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

    derivator.Print()
    if not derivator.Derivate():
        print('NAYE')
        return

    derivator.Print()
    return


if __name__ == '__main__':
    main()

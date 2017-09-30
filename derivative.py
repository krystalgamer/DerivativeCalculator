import re
from sys import argv


def ValidateInput(expression):

    operatorList = ['+', '-', '*', '/']
    foundX = False
    foundDCase = False
    foundDigit = False
    newTerm = True

    if expression[0] in operatorList:
        print('Expressions can\'t start with operators')
        return False
    elif expression[-1] in operatorList:
        print('Expression can\'t end with operators')
        return False

    for c in expression:

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


def InfixToRpn(expression):

    if not ValidateInput(expression):
        print('Quitting')
        return
        
    return



def main():

    if len(argv) < 2:
        print('I need to take at least two arguments')
        return

    expression = ''
    for arg in argv[1:]:
        expression+=arg
    expression.replace(' ', '')

    print('Derivating ' + expression)
    InfixToRpn(expression)
    return


if __name__ == '__main__':
    main()

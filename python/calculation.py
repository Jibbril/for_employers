# This is a small program for my pseudo-ai Winston. I simply wanted to try building a basic calculator
# that could resolve simple arithmetic. Functionality is mostly self-evident.

import string
from abilities.utilities.speak import speak


class Calculation:
    """
    This module does basic calculation for Winston. 
    
    It does not handle more complex math but statements with several numbers including exponents are allowed. 
    Accepts statements in both written ('what is 2 plus 2 times 5?') and mathematical form ('2+2*5')
    """
    def __init__(self, statement):
        self.statement = statement
        self.clean_statement = 'Resolved in interpret()'
        self.answer = 1234
        self.interpret(self.statement)
        self.evaluate(self.clean_statement)
        self.response = f'{self.clean_statement} is {self.answer} :)'
        speak(self.response)
        

    def interpret(self, statement):
        operators = {
            'added': '+',
            'plus': '+',
            'subtracted': '-',
            'minus': '-',
            'times': '*',
            'divided': '/',
            'power': '^'
        }

        for key, value in operators.items():
            if key in statement.lower():
                statement = statement.replace(key, value)
        
        for letter in statement:
            if letter.lower() in string.ascii_lowercase or letter.lower() in '?!':
                statement = statement.replace(letter, '')
            
        self.clean_statement = ' '.join(statement.strip().split())
        
    def evaluate(self, statement):
        statement = statement.split()
        operators = '^ * / -'.split()
        
        for operator in operators:
            indexes = [index for index, value in enumerate(statement) if value == operator]
            new_values = []
            
            index = 0
            offset = 0
            while index < len(indexes):
                res = self.operator_choice(operator, float(statement[indexes[index]-1]), float(statement[indexes[index]+1]))
                new_values.append((indexes[index]-offset,res))
                offset += 2
                index += 1
            
            for value in new_values:
                statement[value[0]] = value[1]
                statement.pop(value[0]-1)
                statement.pop(value[0])
        
        statement = [float(item) for item in statement if item != '+']
        statement = self.add(statement)

        self.answer = statement

    def operator_choice(self, operator, a, b):
        if operator == '^':
            return self.ttp(a, b)

        if operator == '*':
            return self.multiply([a, b])

        if operator == '/':
            return self.divide(a, b)

        if operator == '+':
            return self.add([a, b])

        if operator == '-':
            return self.subtract(a, [b])

        else:
            return 0
    
    def add(self, numbers):
        return sum(numbers)
    
    def subtract(self, base, subtractors=[]):
        return base - sum(subtractors)
    
    def multiply(self, numbers=[]):
        product = numbers.pop()
        for value in numbers:
            product *= value
        return product
    
    def divide(self, dividend, divisor):
        return float(dividend)/float(divisor)

    def ttp(self, base, exp):
        return pow(base, exp)






import sys

class TwosComplement:

    def __init__(self, expression):
        if isinstance(expression, str):
            if expression[-3:] == '_10':
                # base 10
                self.value = int(expression[:-3])
            else:
                # base 2c
                if expression[0] == '0':
                    # positive
                    self.value = int(expression, 2)
                else:
                    n = len(expression) - 1
                    self.value = -1 * (2 ** n - int(expression[1:], 2))
                    # print(f'{expression} = {self.value}')
        else:
            self.value = expression

    def __add__(self, o):
        return TwosComplement(self.value + o.value)

    def __subtract__(self, o):
        return TwosComplement(self.value - o.value)

    def __neg__(self):
        return TwosComplement(-self.value)

    def __str__(self):
        return f'{self.toBase("2c")}_2c    {self.toBase("10")}_10'

    def toBase(self, print_base='10'):
        if print_base == '10':
            return self.value
        
        elif print_base == '2c':
            if self.value >= 0:
                # return 2s complement and base 10
                return '0' + '{0:b}'.format(self.value)
            n = 0
            while -self.value >= 2 ** n:
                n += 1
            # return 2s complement and base 10
            return '1' + '{0:b}'.format(2 ** n + self.value)

def main():
    calc_expression = input('')
    calc_expression = ''.join(calc_expression.split(' '))
    print('base 10: ', end='')
    
    result = calculate(calc_expression, "10")
    print('\nbase 2c: ', end='')
    
    # print base 2c calculations
    calculate(calc_expression, "2c")
    print('')
    
    print(f'{result}')
    

def calculate(expression, print_base=''):
    # print(f'calculate {expression}')
    if expression[0] == '(':
        if print_base != '':
            print('( ', end='')
            
        res = calculate(expression[1:-1], print_base)
        
        if print_base != '':
            print(') ', end='')
            
        return res
    cur_start = 0
    cur_end = cur_start + 1
    total = TwosComplement(0)
    net_parenthesis = 0
    while cur_end < len(expression):
        if expression[cur_end] == '(':
            net_parenthesis += 1
        elif expression[cur_end] == ')':
            net_parenthesis -= 1
        elif expression[cur_end] in set(('+', '-')) and net_parenthesis == 0:
            # calculate
            total += calculate(expression[cur_start:cur_end], print_base)
            cur_start = cur_end
        cur_end += 1
    if expression[cur_start] == '+':
        if print_base != '':
            print('+ ', end='')
        total += calculate(expression[cur_start+1:cur_end], print_base)
    elif expression[cur_start] == '-':
        if print_base != '':
            print('- ', end='')
        total += (-calculate(expression[cur_start+1:cur_end], print_base))
    else:
        total += TwosComplement(expression)
        if print_base != '':
            print(f'({total.toBase(print_base)}) ', end='')
    # print(f'  returning {total.value}')
    return total
            
                
if __name__ == '__main__':
    # do forever until user escapes
    while True:
        main()

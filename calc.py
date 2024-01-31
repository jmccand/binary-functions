import sys

class TwosComplement:

    def __init__(self, expression):
        if isinstance(expression, str):
            if expression[-3:] == '_10':
                self.value = float(expression[:-3])
                return
            try:
                # base 2c
                decimal_point_loc = expression.find('.')
                if decimal_point_loc == -1:
                    decimal_point_loc = len(expression)
                # handle integer
                if expression[0] == '0':
                    # positive
                    self.value = int(expression[:decimal_point_loc], 2)
                else:
                    n = len(expression) - 1
                    self.value = -1 * (2 ** n - int(expression[1:decimal_point_loc], 2))
                    # print(f'{expression} = {self.value}')
                if decimal_point_loc < len(expression) - 1:
                    self.value += int(expression[decimal_point_loc + 1:], 2) * 2 ** (decimal_point_loc - len(expression) + 1)
            except ValueError:
                if expression[-3:] == '_10':
                    self.value = float(expression[:-3])
                else:
                    self.value = float(expression)
                    
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
            if self.value > int(self.value):
                return self.value
            else:
                return int(self.value)
        
        elif print_base == '2c':
            # return 2s complement

            # whole part
            whole_part = '{0:b}'.format(int(abs(self.value)))
            whole_part = '0' + whole_part

            # decimal
            decimal_part = ''
            remaining = self.value - int(self.value)
            # while there's still remaining
            while remaining != 0 and len(decimal_part) < 4:
                remaining *= 2
                decimal_part += str(int(remaining))
                remaining -= int(remaining)

            if self.value < 0:
                whole_part = '{0:b}'.format(((2 ** len(whole_part) - 1) ^ int(whole_part, 2)) + 1)
                if len(decimal_part) > 0:
                    decimal_part = '{0:b}'.format((2 ** len(decimal_part) - 1) ^ int(decimal_part, 2))
                    return f'{whole_part}.{decimal_part}'
            if len(decimal_part) > 0:
                return f'{whole_part}.{decimal_part}'
            return f'{whole_part}'

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

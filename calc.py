import sys

class TwosComplement:

    def __init__(self, expression):
        if isinstance(expression, str):
            if expression[-3:] == '_10':
                self.value = float(expression[:-3])
                return
            try:
                # base 2c

                # find decimal point
                decimal_point_loc = expression.find('.')
                if decimal_point_loc == -1:
                    decimal_point_loc = len(expression)

                decimal_length = len(expression) - decimal_point_loc - 1
                if decimal_length < 0:
                    decimal_length = 0
                integer_length = decimal_point_loc - 1
                
                self.value = int(expression[1:].replace('.', ''), 2) * 2 ** -(decimal_length)
                
                if expression[0] == '1':
                    # negative
                    self.value = -(2 ** integer_length - self.value)

                # print(f'{expression} -> {self.value}')

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
            if abs(self.value) > int(abs(self.value)):
                return self.value
            else:
                return int(self.value)
        
        elif print_base == '2c':
            # return 2s complement

            shift = 0
            while abs(self.value) * 2**shift - int(abs(self.value) * 2**shift) != 0 and shift < 4:
                shift += 1

            shifted = ''
            if self.value >= 0:
                shifted = '0{0:b}'.format(int(self.value * 2**shift))
            else:
                n = 0
                while 2 ** n <= abs(self.value):
                    n += 1
                fm = f'1{{0:0{n + shift}b}}'
                shifted = fm.format(2**(n + shift) - int(abs(self.value) * 2**shift))
            if shift != 0:
                return shifted[:-shift] + '.' + shifted[-shift:]
            return shifted

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

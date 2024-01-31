import sys

class TwosComplement:

    def __init__(self, expression):
        if isinstance(expression, str):
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
        if self.value >= 0:
            # return 2s complement and base 10
            return '0' + '{0:b}'.format(self.value) + '    ' + str(self.value) + '_10'
        n = 0
        while -self.value >= 2 ** n:
            n += 1
        # return 2s complement and base 10
        return '{0:b}'.format(2 ** n + self.value) + '_2c    ' + str(self.value) + '_10'

def main():
    calc_expression = input('')
    calc_expression = ''.join(calc_expression.split(' '))
    print(calculate(calc_expression))

def calculate(expression):
    # print(f'calculate {expression}')
    cur_start = 0
    cur_end = cur_start + 1
    total = TwosComplement(0)
    net_parenthesis = 0
    while cur_end < len(expression):
        if expression[cur_end] == '(':
            net_parenthesis += 1
        elif expression[cur_end] == ')':
            net_parenthesis -= 1
        elif expression[cur_end] in set(('+', '-')):
            # calculate
            total += calculate(expression[cur_start:cur_end])
            cur_start = cur_end
        cur_end += 1
    if expression[cur_start] == '+':
        total += calculate(expression[cur_start+1:cur_end])
    elif expression[cur_start] == '-':
        total += (-calculate(expression[cur_start+1:cur_end]))
    else:
        total += TwosComplement(expression)
    # print(f'  returning {total.value}')
    return total
            
                
if __name__ == '__main__':
    # do forever until user escapes
    while True:
        main()

from calculator.BinaryOperation import Add, Multiply, Divide, Subtract, Power, NoOp

# env variables
debug = False  # set this True to enable debug level logging
open_bracket = '('
closed_bracket = ')'
addition_sign = '+'
subtraction_sign = '-'
multiplication_sign = '*'
division_sign = '/'
exponent_sign = '^'

#  all supported mathematical operations
#  todo support '% (modulo)' operations
supported_operations = {addition_sign,
                        subtraction_sign,
                        multiplication_sign,
                        division_sign,
                        exponent_sign}

#  includes all supported characters excluding numbers
supported_operators = supported_operations.union(open_bracket, closed_bracket)


def evaluate(o):
    validate_brackets(o)

    numbers = parse_numbers(o)
    operations = parse_operators(o)

    log_start(numbers, operations)

    return calculate_helper(numbers, operations)


def log_start(numbers, operations):
    log('-------')
    log('looking for:')
    log('-------')
    log(numbers)
    log(operations)
    log('-------')


#  todo
#   1. investigate binary tree approach
#   2. dynamic programming variant for the current approach
#   function needs refactoring
#  function recursively evaluates the expression
def calculate_helper(numbers, operations):

    if len(numbers) == 1 and len(operations) != 0:
        raise RuntimeError

    if len(numbers) == 1:
        return int(numbers[0])

    if operations[0] == open_bracket:
        result = handle_bracket_operation(numbers, operations, 0, NoOp())

    elif operations[0] == exponent_sign:
        power = Power(int(numbers[0]))
        result = handle_operation_with_potential_precedence(numbers, operations, power)

    elif operations[0] == multiplication_sign:
        multiply = Multiply(int(numbers[0]))
        result = handle_operation_with_potential_precedence(numbers, operations, multiply)

    elif operations[0] == division_sign:
        divide = Divide(int(numbers[0]))
        result = handle_operation_with_potential_precedence(numbers, operations, divide)

    elif operations[0] == addition_sign:
        add = Add(int(numbers[0]))
        result = add.apply(calculate_helper(numbers[1:], operations[1:]))

    elif operations[0] == subtraction_sign:
        subtract = Subtract(int(numbers[0]))
        result = subtract.apply(calculate_helper(numbers[1:], operations[1:]))

    else:
        raise RuntimeError

    log_result(numbers, operations, result)

    return result


def log_result(numbers, operations, result):
    log(operations)
    log(numbers)
    log(result)
    log('-----')


def handle_operation_with_potential_precedence(numbers, operations, binary_operation):
    if len(operations) > 1 and operations[1] == '(':  # if bracket is coming up it takes higher precedence
        result = handle_bracket_operation(numbers, operations, 1, binary_operation)
    else:
        result = high_precedence_operation(numbers, operations, binary_operation)
    return result


def high_precedence_operation(numbers, operations, binary_operation):
    n = [binary_operation.apply(int(numbers[1]))] + numbers[2:]
    result = calculate_helper(n, operations[1:])
    return result


def handle_bracket_operation(numbers, operations, offset, binary_operation):

    i = find_index_of_closing_bracket(operations[offset:]) + offset
    j = find_operations_in_operators(operations[offset:], i) + offset

    n = binary_operation.apply(calculate_helper(numbers[offset:j + 1], operations[1+offset:i]))

    result = calculate_helper([n] + numbers[j + 1:len(numbers)], operations[i + 1:len(operations)])

    return result


def find_index_of_closing_bracket(operations):
    stack = []
    index = 0
    to_return = index
    for i in operations:
        if len(stack) == 0 and to_return != 0:
            return to_return
        if i == open_bracket:
            stack.append('x')
        if i == closed_bracket:
            stack.pop()
            to_return = index
        index = index + 1

    return to_return


def parse_numbers(o):
    result = []
    while len(o) != 0:
        n = ''
        if o[0] == ' ':
            o = o[1:]
            continue

        while len(o) != 0 and o[0].isdigit():
            n = n + o[0]
            o = o[1:]
        if len(o) != 0:
            o = o[1:]

        if n.isdigit():
            result.append(n)

    return result


def find_operations_in_operators(o, w):
    j = 0
    for i in range(0, w):
        x = o[i]
        if x in supported_operations:
            j = j + 1
    return j


def parse_operators(o):
    r = []
    for i in o:
        if i == ' ':
            continue
        if i in supported_operators:
            r.append(i)
        elif not i.isdigit():
            raise RuntimeError('Unsupported symbol ' + i)

    return r


def validate_brackets(o):
    index = 0
    stack = []
    index_of_opened = index
    fault = False
    for i in o:
        if i == open_bracket:
            stack.append('x')
            index_of_opened = index
        if i == closed_bracket:
            if len(stack) == 0:
                fault = True
                break
            stack.pop()
        index += 1

    if len(stack) > 0 or fault:
        m = 'Unbalanced bracket at ''\n' \
            + o[:index_of_opened] + '' + o[index_of_opened] + '' + o[index_of_opened + 1:len(o)] \
            + '\n' + (' ' * index_of_opened + '^')
        raise RuntimeError(m)


def log(message):
    if debug:
        print(message)


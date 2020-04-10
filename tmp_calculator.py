from calculator.binary_operation import Add, Multiply, Divide, Subtract, Exponent, NoOp

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

    numbers = __parse_numbers(o)
    operations = __parse_operators(o)

    return __calculate_helper(numbers, operations)


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


#  todo
#   1. investigate binary tree approach
#   2. dynamic programming variant for the current approach
#   function needs refactoring
#  function recursively evaluates the expression
def __calculate_helper(numbers, operations):

    if len(numbers) == 1 and len(operations) != 0:
        raise RuntimeError

    if len(numbers) == 1:
        return int(numbers[0])

    if operations[0] == open_bracket:
        result = __handle_bracket_operation(numbers, operations, 0, NoOp())

    elif operations[0] == exponent_sign:
        power = Exponent(int(numbers[0]))
        result = __handle_operation_with_potential_precedence(numbers, operations, power)

    elif operations[0] == multiplication_sign:
        multiply = Multiply(int(numbers[0]))
        result = __handle_operation_with_potential_precedence(numbers, operations, multiply)

    elif operations[0] == division_sign:
        divide = Divide(int(numbers[0]))
        result = __handle_operation_with_potential_precedence(numbers, operations, divide)
    elif operations[0] == addition_sign:
        add = Add(int(numbers[0]))
        # result = __handle_operation_with_potential_precedence(numbers, operations, add)
        result = add.apply(__calculate_helper(numbers[1:], operations[1:]))
    elif operations[0] == subtraction_sign:
        subtract = Subtract(int(numbers[0]))
        # result = __handle_operation_with_potential_precedence(numbers, operations, subtract)
        if len(operations) > 1 and operations[1] == '+':
            result = __high_precedence_operation(numbers, operations, subtract)
        else:
            result = subtract.apply(__calculate_helper(numbers[1:], operations[1:]))
        return result

    else:
        raise RuntimeError

    __log_result(numbers, operations, result)

    return result


def __log_result(numbers, operations, result):
    __log(operations)
    __log(numbers)
    __log(result)


def __handle_operation_with_potential_precedence(numbers, operations, binary_operation):
    if len(operations) > 1 and operations[1] == '(':  # if bracket is coming up it takes higher precedence
        result = __handle_bracket_operation(numbers, operations, 1, binary_operation)
    else:
        result = __high_precedence_operation(numbers, operations, binary_operation)
    return result


def __high_precedence_operation(numbers, operations, binary_operation):
    n = [binary_operation.apply(int(numbers[1]))] + numbers[2:]
    result = __calculate_helper(n, operations[1:])
    return result


def __handle_bracket_operation(numbers, operations, offset, binary_operation):

    i = __find_index_of_closing_bracket(operations[offset:]) + offset
    j = __find_operations_in_operators(operations[offset:], i) + offset

    n = binary_operation.apply(__calculate_helper(numbers[offset:j + 1], operations[1 + offset:i]))

    result = __calculate_helper([n] + numbers[j + 1:len(numbers)], operations[i + 1:len(operations)])

    return result


def __find_index_of_closing_bracket(operations):
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


def __parse_numbers(o):
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


def __find_operations_in_operators(o, w):
    j = 0
    for i in range(0, w):
        x = o[i]
        if x in supported_operations:
            j = j + 1
    return j


def __parse_operators(o):
    r = []
    for i in o:
        if i == ' ':
            continue
        if i in supported_operators:
            r.append(i)
        elif not i.isdigit():
            raise RuntimeError('Unsupported symbol ' + i)

    return r


def __log(message):
    if debug:
        print(message)


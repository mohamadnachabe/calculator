from calculator.binary_operation import Add, Multiply, Divide, Subtract, Exponent, NoOp

# env variables
from calculator.config import open_bracket, exponent_sign, multiplication_sign, division_sign, \
    addition_sign, subtraction_sign
from calculator.utils import __find_index_of_closing_bracket, __parse_numbers, __find_operations_in_operators, \
    __parse_operators, validate_brackets

debug = False  # set this True to enable debug level logging


def evaluate(o):
    validate_brackets(o)

    numbers = __parse_numbers(o)
    operations = __parse_operators(o)

    return __calculate_helper(numbers, operations)


#  todo
#   1. investigate binary tree approach
#   2. dynamic programming variant for the current approach
#   function needs refactoring
#  function recursively evaluates the expression
def find_operation_up_to_next_add(operations):
    i = 0
    while i != len(operations):
        if operations[i] == '+' or operations == '-':
            return i
        if operations[i] == '(':
            i = __find_index_of_closing_bracket(operations[i:])
        else:
            i += 1

    return i


def __calculate_helper(numbers, operations):
    if len(numbers) == 1 and len(operations) != 0:
        raise RuntimeError

    if len(numbers) == 1:
        return int(numbers[0])

    if operations[0] == open_bracket:
        result = __handle_bracket_operation(numbers, operations, 0, NoOp())

    elif operations[0] == exponent_sign:
        exponent = Exponent(int(numbers[0]))
        result = __handle_operation_with_potential_precedence(numbers, operations, exponent)

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

        if len(operations) > 1 and operations[1] == '+' or operations[1] == '-':
            n = [subtract.apply(int(numbers[1]))] + numbers[2:]
            result = __calculate_helper(n, operations[1:])

        else:

            i = find_operation_up_to_next_add(operations[1:]) + 1
            j = __find_operations_in_operators(operations[1:], 0, i) + 1

            n = subtract.apply(__calculate_helper(numbers[1:j], operations[1:i]))
            result = __calculate_helper([n]+numbers[j:], operations[i:])

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
    j = __find_operations_in_operators(operations[offset:], 0, i) + offset

    n = binary_operation.apply(__calculate_helper(numbers[offset:j + 1], operations[1 + offset:i]))

    result = __calculate_helper([n] + numbers[j + 1:len(numbers)], operations[i + 1:len(operations)])

    return result


def __log(message):
    if debug:
        print(message)

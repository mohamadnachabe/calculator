from calculator.binary_operation import Add, Multiply, Divide, Subtract, Exponent, NoOp

from calculator.config import open_bracket, exponent_sign, multiplication_sign, division_sign, \
    addition_sign, subtraction_sign
from calculator.utils import find_index_of_closing_bracket, parse_numbers, find_operations_in_operators, \
    parse_operators, validate_brackets, find_operation_up_to_next_add_or_sub

debug = False  # set this True to enable debug level logging


def evaluate(o):
    validate_brackets(o)

    numbers = parse_numbers(o)
    operations = parse_operators(o)

    return __calculate_helper__(numbers, operations)


def __calculate_helper__(numbers, operations):
    if len(numbers) == 1 and len(operations) != 0:
        raise RuntimeError

    if len(numbers) == 1:
        return numbers[0]

    if operations[0] == open_bracket:
        result = __handle_bracket_operation__(numbers, operations, 0, NoOp())

    elif operations[0] == exponent_sign:
        exponent = Exponent((numbers[0]))
        result = __handle_operation_with_potential_precedence__(numbers, operations, exponent)

    elif operations[0] == multiplication_sign:
        multiply = Multiply((numbers[0]))
        result = __handle_operation_with_potential_precedence__(numbers, operations, multiply)

    elif operations[0] == division_sign:
        divide = Divide((numbers[0]))
        result = __handle_operation_with_potential_precedence__(numbers, operations, divide)

    elif operations[0] == addition_sign:
        add = Add((numbers[0]))
        result = add.apply(__calculate_helper__(numbers[1:], operations[1:]))

    elif operations[0] == subtraction_sign:
        result = __handle_subtraction__(numbers, operations)

    else:
        raise RuntimeError

    __log_result__(numbers, operations, result)

    return result


def __handle_subtraction__(numbers, operations):
    subtract = Subtract((numbers[0]))
    if len(operations) > 1 and (operations[1] == '+' or operations[1] == '-'):
        n = [subtract.apply((numbers[1]))] + numbers[2:]
        result = __calculate_helper__(n, operations[1:])

    elif len(operations) == 1:
        result = subtract.apply((numbers[1]))

    else:
        i = find_operation_up_to_next_add_or_sub(operations[1:], 0)
        j = find_operations_in_operators(operations[1:], 0, i) + 1

        n = subtract.apply(__calculate_helper__(numbers[1:j + 1], operations[1:i + 1]))
        result = __calculate_helper__([n] + numbers[j + 1:], operations[i + 1:])
    return result


def __log_result__(numbers, operations, result):
    __log__(operations)
    __log__(numbers)
    __log__(result)


def __handle_operation_with_potential_precedence__(numbers, operations, binary_operation):
    if len(operations) > 1 and operations[1] == '(':  # if bracket is coming up it takes higher precedence
        result = __handle_bracket_operation__(numbers, operations, 1, binary_operation)
    else:
        result = __high_precedence_operation__(numbers, operations, binary_operation)
    return result


def __high_precedence_operation__(numbers, operations, binary_operation):
    n = [binary_operation.apply((numbers[1]))] + numbers[2:]
    result = __calculate_helper__(n, operations[1:])
    return result


def __handle_bracket_operation__(numbers, operations, offset, binary_operation):
    i = find_index_of_closing_bracket(operations[offset:], 0) + offset
    j = find_operations_in_operators(operations[offset:], 0, i) + offset

    n = binary_operation.apply(__calculate_helper__(numbers[offset:j + 1], operations[1 + offset:i]))

    result = __calculate_helper__([n] + numbers[j + 1:len(numbers)], operations[i + 1:len(operations)])

    return result


def __log__(message):
    if debug:
        print(message)

from calculator.binary_operation import Add, Multiply, Divide, Subtract, Exponent, NoOp
from calculator.calculator import __log
from calculator.config import open_bracket, closed_bracket, exponent_sign, multiplication_sign, division_sign, \
    addition_sign, subtraction_sign
from calculator.utils import parse_numbers, parse_operators, find_index_of_closing_bracket, \
    find_operations_in_operators, validate_brackets, find_operation_up_to_next_add_or_sub

debug = True  # set this True to enable debug level logging


def evaluate_opt(o):
    validate_brackets(o)

    numbers = parse_numbers(o)
    operations = parse_operators(o)

    return __calculate_helper(None, numbers, 0, len(numbers)-1, operations, 0, len(operations)-1)


def __calculate_helper(carry, numbers, ns, ne, operations, os, oe):
    if ne == ns and os >= oe:
        return carry if carry is not None else int(numbers[ns])

    if ne == ns:
        return int(numbers[ns])

    operation_ = operations[os]

    if carry is None:
        number_ = int(numbers[ns])
    else:
        number_ = carry

    if operation_ == open_bracket:
        result = __handle_bracket_operation(carry, numbers, ns, ne, operations, os, oe, NoOp())

    elif operation_ == exponent_sign:
        power = Exponent(number_)
        n = power.apply(int(numbers[ns+1]))
        result = __calculate_helper(n, numbers, ns + 1, ne, operations, os + 1, oe)

    elif operation_ == multiplication_sign:
        multiply = Multiply(number_)
        result = __handle_operation_with_potential_precedence(carry, numbers, ns, ne, operations, os, oe, multiply)

    elif operation_ == division_sign:
        divide = Divide(number_)
        result = __handle_operation_with_potential_precedence(carry, numbers, ns, ne, operations, os, oe, divide)

    elif operation_ == addition_sign:
        add = Add(number_)
        result = __handle_operation_with_potential_precedence(carry, numbers, ns, ne, operations, os, oe, add)

        # n = __calculate_helper(None, numbers, ns + 1, ne, operations, os + 1, oe)
        # result = add.apply(n)

    elif operation_ == subtraction_sign:
        subtract = Subtract(number_)

        if os != oe and operations[os] == '+' or operations[os] == '-':
            n = subtract.apply(int(numbers[ns+1]))
            result = __calculate_helper(n, numbers, ns+1, ne, operations, os+1, oe)

        else:
            i = find_operation_up_to_next_add_or_sub(operations, os) + 1
            j = find_operations_in_operators(operations, 1, i) + 1

            n = subtract.apply(__calculate_helper(None, numbers, ns+1, j, operations, os+1, i))
            result = __calculate_helper(n, numbers, j, ne, operations, i, oe)

    else:
        raise RuntimeError

    # __log_result(numbers, operations, result)

    return result


def __log_result(numbers, operations, result):
    __log(result)


def __handle_operation_with_potential_precedence(carry, numbers, ns, ne, operations, os, oe, binary_operation):
    if oe - os > 1 and operations[os] == '(':
        return __handle_bracket_operation(carry, numbers, ns, ne, operations, os, oe, binary_operation)
    else:
        return __high_precedence_operation(numbers, ns, ne, operations, os, oe, binary_operation)


def __high_precedence_operation(numbers, ns, ne, operations, os, oe, binary_operation):
    # n = binary_operation.apply(int(numbers[ns]))
    # if ns + 2 >= len(numbers):
    #     return n
    # else:
    #     return __calculate_helper(n, numbers, ns + 1, ne, operations, os, oe)

    n = binary_operation.apply(int(numbers[ns + 1]))
    return __calculate_helper(n, numbers, ns + 1, ne, operations, os + 1, oe)


def __handle_bracket_operation(carry, numbers, ns, ne, operations, os, oe, binary_operation):
    i = find_index_of_closing_bracket(operations, 0)
    j = find_operations_in_operators(operations, os, i)

    n = binary_operation.apply(
        __calculate_helper(carry, numbers, ns, ns + j, operations, os + 1, i - 1)
    )

    return __calculate_helper(n, numbers, ns + j, ne, operations, i + 1, oe)


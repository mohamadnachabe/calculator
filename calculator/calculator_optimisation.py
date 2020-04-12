from calculator.binary_operation import Add, Multiply, Divide, Subtract, Exponent, NoOp
from calculator.config import open_bracket, exponent_sign, multiplication_sign, division_sign, \
    addition_sign, subtraction_sign
from calculator.utils import parse_numbers, parse_operators, find_index_of_closing_bracket, \
    find_operations_in_operators, validate_brackets, find_operation_up_to_next_add_or_sub


def evaluate_opt(o):
    validate_brackets(o)

    numbers = parse_numbers(o)
    operations = parse_operators(o)

    return __calculate_helper(None, numbers, 0, len(numbers)-1, operations, 0, len(operations)-1)


def __calculate_helper(carry, numbers, ns, ne, operations, os, oe):
    """

    :param carry: if this number happens to be not None it replaces numbers[ns]
    :param numbers: all numbers required to compute equation
    :param ns: starting index for numbers
    :param ne: ending index for numbers (highest index should be len(numbers)-1)
    :param operations: all operations required to compute equation
    :param os: starting index for operations
    :param oe: ending index for operations
    :return: equation result between [ns, ne] and [os, oe]
    """

    # printing out current operation
    numbs1 = numbers[ns:ne+1] # need to add one because of nature of python splitting operation
    ops1 = operations[os:oe+1] # upped bound is exclusive

    if ns == ne and os >= oe:
        return carry if carry is not None else int(numbers[ns])
    elif ns > ne and os >= oe:
        return carry

    if ne == ns:
        return int(numbers[ns])

    operation_ = operations[os]

    if carry is None:
        number_ = int(numbers[ns])
    else:
        number_ = carry

    if operation_ == open_bracket:
        result = __handle_bracket_operation(numbers, ns, ne, operations, os, oe, NoOp())

    elif operation_ == exponent_sign:
        power = Exponent(number_)
        n = power.apply(int(numbers[ns+1]))
        result = __calculate_helper(n, numbers, ns + 1, ne, operations, os + 1, oe)

    elif operation_ == multiplication_sign:
        multiply = Multiply(number_)
        result = __handle_operation_with_potential_precedence(numbers, ns, ne, operations, os, oe, multiply)

    elif operation_ == division_sign:
        divide = Divide(number_)
        result = __handle_operation_with_potential_precedence(numbers, ns, ne, operations, os, oe, divide)

    elif operation_ == addition_sign:
        add = Add(number_)

        n = __calculate_helper(None, numbers, ns + 1, ne, operations, os + 1, oe)
        result = add.apply(n)

    elif operation_ == subtraction_sign:
        subtract = Subtract(number_)

        if os + 1 < len(operations) and (operations[os+1] == '+' or operations[os+1] == '-'):
            n = subtract.apply(int(numbers[ns+1]))
            result = __calculate_helper(n, numbers, ns+1, ne, operations, os+1, oe)

        elif os + 1 >= len(operations) or os == oe:
            result = subtract.apply(int(numbers[ns + 1]))

        else:
            i = find_operation_up_to_next_add_or_sub(operations, os) + 1
            j = find_operations_in_operators(operations, 1, i) + 1

            n = subtract.apply(__calculate_helper(carry, numbers, ns+1, j+1, operations, os+1, i))
            result = __calculate_helper(n, numbers, j+2, ne, operations, i+1, oe)

    else:
        raise RuntimeError('operation ' + operation_)

    return result


def __handle_operation_with_potential_precedence(numbers, ns, ne, operations, os, oe, binary_operation):
    if oe != os and operations[os+1] == '(':
        return __handle_bracket_operation(numbers, ns+1, ne, operations, os+1, oe, binary_operation)
    else:
        n = binary_operation.apply(int(numbers[ns + 1]))
        return __calculate_helper(n, numbers, ns + 1, ne, operations, os + 1, oe)


def __handle_bracket_operation(numbers, ns, ne, operations, os, oe, binary_operation):
    i = find_index_of_closing_bracket(operations, os)
    j = find_operations_in_operators(operations, os, i) + ns

    n = binary_operation.apply(
        __calculate_helper(None, numbers, ns, j, operations, os+1, i-1)
    )

    return __calculate_helper(n, numbers, j, ne, operations, i + 1, oe)


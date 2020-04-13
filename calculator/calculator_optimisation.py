from calculator.binary_operation import Add, Multiply, Divide, Subtract, Exponent, NoOp
from calculator.config import open_bracket, exponent_sign, multiplication_sign, division_sign, \
    addition_sign, subtraction_sign
from calculator.utils import parse_numbers, parse_operators, find_index_of_closing_bracket, \
    validate_brackets, find_numbers_between_operators, find_operation_up_to_next_add_or_sub_plus


def evaluate_opt(o):
    validate_brackets(o)

    numbers = parse_numbers(o)
    operations = parse_operators(o)

    return __calculate_helper(None, numbers, 0, len(numbers) - 1, operations, 0, len(operations) - 1)


def __calculate_helper(replacing_numb, numbers, ns, ne, operations, os, oe):
    """

    :param replacing_numb: if this number happens to be not None it replaces numbers[ns]
    :param numbers: all numbers required to compute equation
    :param ns: starting index for numbers
    :param ne: ending index for numbers (highest index should be len(numbers)-1)
    :param operations: all operations required to compute equation
    :param os: starting index for operations
    :param oe: ending index for operations
    :return: equation result between [ns, ne] and [os, oe]
    """

    if ne - ns == 1 and os > oe:
        return replacing_numb if replacing_numb is not None else int(numbers[ns])

    if ns == ne:
        return replacing_numb if replacing_numb is not None else int(numbers[ns])

    elif os > oe:
        return replacing_numb

    operation_ = operations[os]

    if replacing_numb is None:
        number_ = int(numbers[ns])
    else:
        number_ = replacing_numb

    if operation_ == open_bracket:
        result = __handle_bracket_operation(numbers, ns, ne, operations, os, oe, NoOp())

    elif operation_ == exponent_sign:
        power = Exponent(number_)
        result = __handle_operation_with_potential_precedence(numbers, ns, ne, operations, os, oe, power)

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

        if oe - os >= 1 and (operations[os + 1] == '+' or operations[os + 1] == '-'):
            n = subtract.apply(int(numbers[ns + 1]))
            result = __calculate_helper(n, numbers, ns + 1, ne, operations, os + 1, oe)

        elif oe - os == 0:
            result = subtract.apply(int(numbers[ns + 1]))

        else:
            i = find_operation_up_to_next_add_or_sub_plus(operations, os + 1, oe)
            j = find_numbers_between_operators(operations, 1, i) + ns

            n = subtract.apply(__calculate_helper(None, numbers, ns + 1, j, operations, os + 1, i))

            result = __calculate_helper(n, numbers, j, ne, operations, i + 1, oe)

    else:
        raise RuntimeError('operation ' + operation_)

    return result


def __handle_operation_with_potential_precedence(numbers, ns, ne, operations, os, oe, binary_operation):
    if oe != os and operations[os + 1] == '(':
        return __handle_bracket_operation(numbers, ns + 1, ne, operations, os + 1, oe, binary_operation)
    else:
        n = binary_operation.apply(int(numbers[ns + 1]))
        return __calculate_helper(n, numbers, ns + 1, ne, operations, os + 1, oe)


def __handle_bracket_operation(numbers, ns, ne, operations, os, oe, binary_operation):
    i = find_index_of_closing_bracket(operations, os)
    j = find_numbers_between_operators(operations, os, i) + ns - 1

    n = binary_operation.apply(
        __calculate_helper(None, numbers, ns, j, operations, os + 1, i - 1)
    )

    return __calculate_helper(n, numbers, j, ne, operations, i + 1, oe)

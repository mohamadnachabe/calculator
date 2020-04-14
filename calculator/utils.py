from calculator.config import open_bracket, closed_bracket, supported_operations, supported_operators


def find_index_of_closing_bracket(operations, start_index):
    stack = []
    index = start_index
    to_return = index

    for i in range(start_index, len(operations)):
        op = operations[i]
        if len(stack) == 0 and to_return != start_index:
            return to_return
        if op == open_bracket:
            stack.append('x')
        if op == closed_bracket:
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

        while len(o) != 0 and (o[0].isdigit() or o[0] == '.'):
            n = n + o[0]
            o = o[1:]

        if len(o) != 0:
            o = o[1:]

        if n not in supported_operators and len(n) > 0:
            result.append(float(n))

    return result


def find_operations_in_operators(operations, lower_bound, upper_bound):
    j = 0
    for i in range(lower_bound, upper_bound):
        if i >= len(operations):
            break
        x = operations[i]
        if x in supported_operations:
            j = j + 1
    return j


def find_numbers_between_operators(operations, os, oe):
    j = 0
    if operations[os] in supported_operations:
        j += 1
    for i in range(os, oe + 1):
        op = operations[i]

        if op in supported_operations and i + 1 == oe + 1:
            return j + 1
        elif i + 1 == len(operations):
            break

        op_next = operations[i+1]

        if op == open_bracket and op_next in supported_operations:
            j += 1
        elif op in supported_operations and op_next == closed_bracket:
            j += 1
        elif op in supported_operations and op_next in supported_operations:
            j += 1

    return j


def parse_operators(o):
    r = []
    for i in o:
        if i == ' ':
            continue
        if i in supported_operators:
            r.append(i)
        elif not i.isdigit() and i != '.':
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


def find_operation_up_to_next_add_or_sub(operations, start_index):
    # and len(operations) - start_index > 1
    i = start_index
    while i < len(operations) - start_index :
        if operations[i] == '+' or operations[i] == '-':
            return i
        if operations[i] == '(':
            i = find_index_of_closing_bracket(operations, i)
        else:
            i += 1

    return i


def find_operation_up_to_next_add_or_sub_plus(operations, start_index, end_index):
    i = start_index
    while i <= end_index:
        if operations[i] == '+' or operations[i] == '-':
            return i - 1
        if operations[i] == '(':
            i = find_index_of_closing_bracket(operations, i) + 1
        else:
            i += 1

    return i - 1
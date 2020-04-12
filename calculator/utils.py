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

        while len(o) != 0 and o[0].isdigit():
            n = n + o[0]
            o = o[1:]
        if len(o) != 0:
            o = o[1:]

        if n.isdigit():
            result.append(n)

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


def find_operation_up_to_next_add_or_sub(operations, start_index):
    # and len(operations) - start_index > 1
    i = start_index
    while i != len(operations) :
        if operations[i] == '+' or operations[i] == '-':
            return i
        if operations[i] == '(':
            i = find_index_of_closing_bracket(operations, i)
        else:
            i += 1

    return i
